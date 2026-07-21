#!/usr/bin/env python3
"""_frontmatter: 카탈로그 SKILL.md frontmatter 의 mini-parser.

정밀한 YAML 파서(PyYAML 등) 를 의도적으로 사용하지 않는다 — 카탈로그 frontmatter 가
단순한 구조(top-level key:value + 1-depth/2-depth nested + nested list) 라는 가정.
본 모듈은 scripts/skill-lint 와 scripts/skill-discover 의 중복 parser 를 단일화한다.

핵심 동작:
- top-level scalar/list/inline-list 지원
- 들여쓰기 *prefix* 기반의 nested object 파싱 (depth 무제한)
  → `metadata.claude_code.harness_compat: [list]` 같은 2-depth nested 의 *list 값* 도 지원
- 들여쓰기 prefix 가 정확히 *한 단계 더 깊거나 얕음* 일 때만 진입/탈출

본 모듈의 관대함이 *값을 조용히 망가뜨리는* 경우를 잡기 위해 `check_yaml_strict` 를 함께
제공한다 (표준 YAML 파서가 거부하는 구조 검출; skill-lint 의 E002).

Usage:
    from _frontmatter import parse_frontmatter, check_yaml_strict
    fm, errors = parse_frontmatter(text)
    yaml_errors = check_yaml_strict(text)
"""
from __future__ import annotations

import re
from typing import Any

# list item 의 시작 (`- ...` 형태; 들여쓰기 무관).
_LIST_ITEM_RE = re.compile(r"^\s+-\s+")
# nested key 의 시작 (들여쓰기 + `key:` 형태).
# 들여쓰기 깊이는 호출자가 *prefix* 로 검사한다.

# list item 의 text 부분에서 quote strip.
# *짝이 맞는 한 쌍* 만 제거한다. 이전 구현 (`.strip('"').strip("'")`) 은 따옴표 문자를
# 개수 제한 없이 양쪽에서 벗겨내서, `say 'hi'` 같은 값의 끝 따옴표를 잘라먹었다.
def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ('"', "'"):
        return s[1:-1]
    return s


def _scan_quoted(value: str) -> int:
    """따옴표로 시작하는 scalar 에서 *닫는 따옴표* 의 인덱스를 찾는다.

    double-quoted 는 `\\` escape 를, single-quoted 는 `''` (따옴표 2개 = 리터럴 1개) 를
    고려한다. 닫히지 않으면 -1.
    """
    q = value[0]
    i = 1
    while i < len(value):
        c = value[i]
        if q == '"':
            if c == "\\":
                i += 2
                continue
            if c == '"':
                return i
        else:
            if c == "'":
                if i + 1 < len(value) and value[i + 1] == "'":
                    i += 2
                    continue
                return i
        i += 1
    return -1


def _check_scalar(value: str) -> str:
    """scalar 값 하나가 표준 YAML 에서 파싱 가능한지 검사. 문제 없으면 빈 문자열."""
    value = value.strip()
    if not value:
        return ""
    # flow collection (`[a, b]`, `{a: b}`) 은 본 검사 범위 밖
    if value[0] in "[{":
        return ""
    if value[0] in ('"', "'"):
        end = _scan_quoted(value)
        if end == -1:
            return f"따옴표가 닫히지 않음: {value[:40]}"
        rest = value[end + 1:].strip()
        if rest and not rest.startswith("#"):
            return (
                f"닫는 따옴표 뒤에 내용이 있음 (표준 YAML 문법 오류): "
                f"...{value[max(0, end - 8):end + 1]} >>> {rest[:30]}"
            )
        return ""
    # 평문(plain) 스칼라: 콜론+공백은 두 번째 mapping key 로 해석된다
    if ": " in value or value.endswith(":"):
        return (
            f"평문 스칼라에 콜론+공백이 있음 (두 번째 key 로 해석됨). "
            f"값 전체를 따옴표로 감쌀 것: {value[:50]}"
        )
    return ""


def check_yaml_strict(text: str) -> list:
    """frontmatter 가 *표준 YAML 파서* 에서도 파싱 가능한지 검사.

    본 모듈의 mini-parser 는 의도적으로 관대하므로, 관대함이 *값을 조용히 망가뜨리는*
    구조만 골라 잡아낸다. 전체 YAML 스펙 검증이 아니다 — 실제로 카탈로그에서 발생한
    두 유형 (평문 스칼라의 콜론+공백, 닫는 따옴표 뒤 쉼표) 과 미닫힘 따옴표를 본다.

    Returns:
        [(code, line, message), ...]. line 은 *파일 기준* 1-based 줄 번호.
    """
    if not text.startswith("---"):
        return []
    end = text.find("\n---", 3)
    if end == -1:
        return []

    errors: list = []
    lines = text[3:end].strip("\n").split("\n")
    # `strip("\n")` 이 시작 마커 뒤 개행을 제거하므로 lines[0] = 파일의 2번째 줄
    # (1번째 줄은 `---`). 따라서 idx 0 → line 2.
    offset = 2
    for idx, line in enumerate(lines):
        content = line.strip()
        if not content or content.startswith("#"):
            continue
        if content.startswith("- "):
            value = content[2:]
        elif ":" in content:
            value = content.partition(":")[2]
        else:
            continue
        msg = _check_scalar(value)
        if msg:
            errors.append(("E002", idx + offset, msg))
    return errors


def _parse_block(lines: list[str], start_idx: int, prefix: str) -> tuple[dict, int]:
    """`start_idx` 부터 `prefix` 와 *정확히* 같은 들여쓰기로 시작하는 key:value 줄들을
    nested dict 로 파싱. 자식이 또 nested object / list 일 때 recursive.

    Args:
        lines: frontmatter body 의 줄 리스트 (frontmatter 마커 제외).
        start_idx: 파싱 시작 위치.
        prefix: 매칭해야 할 *들여쓰기 prefix* (예: `"  "` = 2 spaces).

    Returns:
        (block_dict, end_idx). end_idx 는 block 의 *다음 줄* 위치.
    """
    block: dict[str, Any] = {}
    i = start_idx
    while i < len(lines):
        line = lines[i]
        if not line.startswith(prefix):
            # 다른 들여쓰기 → outer block 의 끝
            break
        if ":" not in line:
            i += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()

        if not rest:
            # 값이 비어있음 — 자식이 list 또는 nested object 인지 확인
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                deeper_prefix = prefix + "  "
                # 자식이 list 형태 (`- ...`) 인 경우
                if next_line.startswith(deeper_prefix) and _LIST_ITEM_RE.match(next_line):
                    items: list = []
                    j = i + 1
                    while j < len(lines) and lines[j].startswith(deeper_prefix) and _LIST_ITEM_RE.match(lines[j]):
                        items.append(_strip_quotes(lines[j].strip()[2:]))
                        j += 1
                    block[key] = items
                    i = j
                    continue
                # 자식이 또 nested object 형태 (`key: ...`) 인 경우 — recursive
                if next_line.startswith(deeper_prefix) and ":" in next_line:
                    sub, end_idx = _parse_block(lines, i + 1, deeper_prefix)
                    block[key] = sub
                    i = end_idx
                    continue
            block[key] = ""
            i += 1
            continue

        # inline list `[a, b, c]`
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            block[key] = [
                _strip_quotes(x.strip()) for x in inner.split(",") if x.strip()
            ] if inner else []
            i += 1
            continue

        # 그 외: scalar
        block[key] = _strip_quotes(rest)
        i += 1

    return block, i


def parse_frontmatter(text: str) -> tuple[dict | None, list]:
    """SKILL.md 본문에서 frontmatter 마커 사이의 YAML 을 dict 로 파싱.

    Returns:
        (fm, errors). fm 이 None 이면 errors 에 fatal 파싱 실패가 담긴다.
        errors 는 [(code, line, message), ...] 형태의 list.
    """
    if not text.startswith("---"):
        return None, [("E001", 0, "frontmatter 시작 마커 (---) 없음")]
    end = text.find("\n---", 3)
    if end == -1:
        return None, [("E001", 0, "frontmatter 종료 마커 (---) 없음")]

    raw = text[3:end].strip("\n")
    fm: dict[str, Any] = {}
    errors: list = []
    lines = raw.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()
        if not s or s.startswith("#"):
            i += 1
            continue
        if ":" not in line:
            errors.append(("E001", 0, f"YAML 파싱 실패: `{s}`"))
            i += 1
            continue
        key, _, rest = line.partition(":")
        key = key.strip()
        rest = rest.strip()

        if not rest:
            # top-level key 의 값이 비어있음
            if i + 1 < len(lines):
                next_line = lines[i + 1]
                # 자식이 list 형태
                if _LIST_ITEM_RE.match(next_line):
                    items: list = []
                    j = i + 1
                    while j < len(lines) and _LIST_ITEM_RE.match(lines[j]):
                        items.append(_strip_quotes(lines[j].strip()[2:]))
                        j += 1
                    fm[key] = items
                    i = j
                    continue
                # 자식이 nested object 형태 — `  key:` (2-space 들여쓰기)
                if next_line.startswith("  ") and ":" in next_line:
                    sub, end_idx = _parse_block(lines, i + 1, "  ")
                    fm[key] = sub
                    i = end_idx
                    continue
            fm[key] = ""
            i += 1
            continue

        # inline list
        if rest.startswith("[") and rest.endswith("]"):
            inner = rest[1:-1].strip()
            fm[key] = [
                _strip_quotes(x.strip()) for x in inner.split(",") if x.strip()
            ] if inner else []
            i += 1
            continue

        # scalar
        fm[key] = _strip_quotes(rest)
        i += 1

    return fm, errors
