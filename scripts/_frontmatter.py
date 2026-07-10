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

Usage:
    from _frontmatter import parse_frontmatter
    fm, errors = parse_frontmatter(text)
"""
from __future__ import annotations

import re
from typing import Any

# list item 의 시작 (`- ...` 형태; 들여쓰기 무관).
_LIST_ITEM_RE = re.compile(r"^\s+-\s+")
# nested key 의 시작 (들여쓰기 + `key:` 형태).
# 들여쓰기 깊이는 호출자가 *prefix* 로 검사한다.

# list item 의 text 부분에서 quote strip
def _strip_quotes(s: str) -> str:
    return s.strip().strip('"').strip("'")


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
