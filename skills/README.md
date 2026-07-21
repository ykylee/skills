# Skills Catalog

- 문서 목적: 본 저장소 `skills` 의 카탈로그 authoring 규약과 디렉터리 구조를 정의한다.
- 범위: 디렉터리 레이아웃, `SKILL.md` 포맷, frontmatter 키, 작성 절차, harness 호환 가이드
- 대상 독자: 스킬 작성자, AI 에이전트, 카탈로그 기여자
- 상태: draft
- 최종 수정일: 2026-07-21
- 관련 문서: [../ai-workflow/memory/active/PURPOSE.md](../ai-workflow/memory/active/PURPOSE.md), [../ai-workflow/memory/active/PROJECT_PROFILE.md](../ai-workflow/memory/active/PROJECT_PROFILE.md)

## 1. 카탈로그 정의

본 디렉터리는 *사용자가 여러 AI 하네스(Claude Code 외 포함)에서 재사용할 범용 AI 워크플로우
스킬* 의 카탈로그다. 자세한 의도는 [PURPOSE.md](../ai-workflow/memory/active/PURPOSE.md) §1 참조.

원칙 요약:
- **단일 책임**: 한 스킬 = 한 명제. 조합은 호출자(워크플로우)가 담당한다.
- **harness 비종속 지향**: 스킬 본문은 중립적으로 작성하고, harness 고유 syntax 는 어댑터로 분리한다.
- **자기-기술**: `name` / `description` 만으로 호출 시점을 알 수 있어야 한다.

### 1.1 현재 카탈로그 목록

본 문서는 *authoring 가이드* 이므로 스킬 목록을 손으로 복사해두지 않는다. 정본은 항상
`SKILL.md` frontmatter 이고, 다음으로 생성한다:

```bash
python3 scripts/skill-discover            # 전체 목록
python3 scripts/skill-discover --json     # 기계 판독
```

사람이 읽는 요약 트리는 [저장소 README](../README.md) 에 있다. 손으로 관리하는 목록이
늘어날수록 드리프트가 생기므로 (실제로 `react-premium-design` 이 여러 문서에서 누락된 적이
있다), 새 스킬 추가 시 목록을 늘리기보다 위 명령으로 확인하는 쪽을 권한다.

## 2. 디렉터리 구조

```
skills/
├── README.md                    # 본 문서 (authoring 가이드)
└── <skill-name>/
    ├── SKILL.md                 # 필수: manifest + 본문
    ├── references/              # 선택: 본문이 인용하는 추가 자료
    ├── assets/                  # 선택: 스킬이 사용하는 정적 파일
    └── scripts/                 # 선택: 스킬이 호출하는 보조 스크립트
```

규칙:
- 스킬 디렉터리명은 **kebab-case**, 전부 소문자 + 숫자 + 하이픈.
- 한 디렉터리에 `SKILL.md` 는 **정확히 1개**.
- `references/`, `assets/`, `scripts/` 는 **스킬 본문이 실제로 참조할 때만** 둔다 (placeholder 금지).
- 카테고리 분류는 `metadata.category` 필드로 표현하며, 디렉터리 구조에는 반영하지 않는다
  (검색성과 1-depth 단순성 우선).

## 3. SKILL.md 포맷

`SKILL.md` 는 **YAML frontmatter + Markdown 본문** 두 부분으로 구성된다.

### 3.1 Frontmatter (필수 + 권장)

```yaml
---
name: <kebab-case>                    # 필수, 디렉터리명과 일치
description: <1-line>                 # 필수, 호출 시점 + 트리거 표현 포함
metadata:
  claude_code:                        # depth-2 nested (PROJECT_PROFILE §5 정책)
    when_to_use: <문장>                # 권장, 본문 시작에 트리거 단계가 있으면 생략 가능
    harness_compat:                   # 권장, 호환 harness 목록
      - claude-code
      - generic-md
    category: <meta|workflow|doc|code|research|data>  # 권장
    version: 0.1.0                    # 권장, semver
    author: <표기>                     # 선택
    license: MIT                      # 선택
    tags: [a, b]                      # 선택
    related_skills: [x, y]            # 선택
---
```

Claude-Code-flavored 확장 필드는 **`metadata.claude_code.*` 아래 depth-2 로 중첩**한다
(top-level 이나 `metadata.*` 직하가 아니다). 근거와 이력은
[PROJECT_PROFILE.md §5](../ai-workflow/memory/active/PROJECT_PROFILE.md) 참조.

#### 3.1.0 YAML 인용 규칙 (필수)

frontmatter 는 **표준 YAML 파서로 파싱 가능해야** 한다. 자체 mini-parser
(`scripts/_frontmatter.py`) 는 의도적으로 관대해서 아래 오류를 그냥 통과시킨다. 두 가지가
실제로 발생했다 (2026-07-21 수정):

- **평문 스칼라 안의 콜론+공백** — `description: ... Triggers: 'a', 'b'` 는 `Triggers:` 를
  두 번째 key 로 해석해 파싱 실패. → 값 전체를 `"` 로 감쌀 것.
- **닫는 따옴표 뒤의 쉼표** — `when_to_use: "A", "B"` 는 `"A"` 에서 스칼라가 끝나므로 뒤의
  `, "B"` 가 문법 오류. → 값 전체를 `'` 로 감쌀 것 (내부 `"` 는 그대로 유지).

이 두 유형과 미닫힘 따옴표는 **`skill-lint` 가 `E002` 로 자동 검출**한다 (2026-07-21 추가).
별도 명령 없이 평소대로 실행하면 된다:

```bash
python3 scripts/skill-lint --path skills
```

`E002` 는 전체 YAML 스펙 검증이 *아니라* 위 3종만 본다. 복잡한 frontmatter (multi-line
scalar, anchor, flow mapping 등) 를 쓴다면 표준 파서로 직접 확인한다:

```bash
sed -n '2,/^---$/p' skills/<name>/SKILL.md | sed '$d' > /tmp/fm.yaml
npx --yes js-yaml /tmp/fm.yaml    # 파싱 실패 시 non-zero + 위치 표시
```

`js-yaml` 은 **첫 오류에서 멈추므로**, 한 건을 고친 뒤에는 전체를 다시 돌려 뒤에 가려져 있던
오류가 없는지 확인한다.

#### 3.1.1 `name`
- 형식: `^[a-z0-9]+(-[a-z0-9]+)*$`
- 디렉터리명과 **정확히 일치**해야 한다 (skill-lint 가 검증).

#### 3.1.2 `description`
- 1-line, **공백 포함 200자 이내** 권장.
- 다음을 포함하면 좋다:
  - 무엇을 하는지 (동사)
  - 호출해야 하는 시점 (트리거 phrase)
- 예: `"스킬 카탈로그의 manifest 정합성과 frontmatter, 링크를 검증합니다. 새 스킬 추가/PR 전 사용."`

#### 3.1.3 `metadata.claude_code.harness_compat`
- 호환 가능한 harness 목록. 가능한 값:
  - `claude-code` — Claude Code native
  - `generic-md` — 어떤 harness 라도 markdown 으로 해석 가능
  - `claude-api`, `langchain`, `llamaindex` 등 (필요 시 확장)
- 한 스킬이 **반드시 1개 이상** 의 harness 와 호환되어야 한다.
- `generic-md` 만 단독으로 두면 가장 범용성이 높다.

#### 3.1.4 `metadata.claude_code.category`
- 권장 값 (필요 시 확장):
  - `meta` — 카탈로그 운영 / lint / validate
  - `workflow` — 워크플로우 단계 (session-start, doc-sync 등)
  - `doc` — 문서 작성/검토
  - `code` — 코드 보조 (테스트, 리팩터, 리뷰)
  - `research` — 리서치/리뷰
  - `data` — 데이터 처리

### 3.2 본문 (Markdown)

권장 골격:

```markdown
# <사람이 읽는 이름>

<한 단락 개요>

## When to use
- <트리거 1>
- <트리거 2>

## Inputs
- <필요 입력>

## Outputs
- <결과물 형식>

## Procedure
1. <단계 1>
2. <단계 2>
...

## Trade-offs
- <대안/제약/주의>

## References
- <references/ 안 파일 또는 외부 URL>
```

- 단계는 **번호 목록** 으로 작성. 워크플로우처럼 호출 가능한 형태로.
- `references/` 의 파일은 **상대 경로** 로 인용.
- harness 고유 syntax (예: `<command-name>` 태그) 는 사용하지 않는다.

## 4. 작성 절차

1. **의도 정의**: PURPOSE 의 scope 안인지 확인 (`meta`, `workflow`, `doc`, `code`, `research`, `data`).
2. **이름 확정**: kebab-case, 디렉터리명과 일치. 기존 스킬과 충돌 없는지 `skills/` 를 grep.
3. **골격 작성**: `skills/<name>/SKILL.md` 를 §3 포맷에 맞춰 작성.
4. **검증**: `skill-lint` 스킬(또는 수동 체크리스트)로 frontmatter / 링크 / 정합성 확인.
5. **CHANGELOG 갱신**: `### Added` 또는 `### Changed` 항목 1줄 추가.
6. **handoff 갱신**: 현재 세션의 `session_handoff.md` Key Changes + Next Actions 반영.

## 5. Harness 호환 가이드

- **Claude Code**: `SKILL.md` 가 자동으로 인식됨. `description` 의 trigger phrase 가 slash 자동완성에 사용.
- **다른 markdown-aware harness**: `name` + `description` + 본문의 *Procedure* 단락을 따라 직접 호출 가능.
- **API 기반 harness (LangChain 등)**: `metadata.harness_compat` 가 해당 라이브러리 키를 포함하면
  어댑터가 그 입력을 해석. (어댑터 자체는 본 카탈로그 범위 밖.)

## 6. 검증 / Lint

기본 검증은 [`skill-lint`](./skill-lint/SKILL.md) 가 담당한다. 1차 수동 체크리스트:

- [ ] 디렉터리명 = `name` (kebab-case)
- [ ] `description` ≤ 200자, 1-line
- [ ] `metadata.claude_code.harness_compat` ≥ 1 (depth-2 nested 위치 확인)
- [ ] frontmatter 가 표준 YAML 파서로 파싱됨 — `skill-lint` `E002` 가 자동 검사 (§3.1.0)
- [ ] 본문에 `## When to use` / `## Procedure` 가 존재
- [ ] `references/`, `assets/`, `scripts/` 가 실제로 사용됨 (placeholder 금지)
- [ ] `CHANGELOG.md` 에 본 변경 1줄 기록
- [ ] `session_handoff.md` 의 Recent Done / Next Actions 반영

검색 / 인덱싱은 [`skill-discover`](./skill-discover/SKILL.md) 가 담당한다. 로컬 / CI 에서
다음 절차로 호출:

```bash
python3 scripts/skill-discover                                  # 인덱스 출력
python3 scripts/skill-discover --index                          # .index.json 빌드
python3 scripts/skill-discover meta                             # 자유 텍스트 검색
python3 scripts/skill-discover category:meta harness:claude-code   # 토큰 필터
python3 scripts/skill-discover --top 5 --json 메타                # JSON
```

검색 scoring (skill-discover §Procedure 3):
- 카테고리 정확 일치: +3
- 키워드 ∈ `name`: +2
- 키워드 ∈ `description`: +2
- `harness_compat` 매치: +1
- `generic-md` 보너스: +0.5

## 다음에 읽을 문서
- [PURPOSE.md](../ai-workflow/memory/active/PURPOSE.md) — scope / non-scope
- [PROJECT_PROFILE.md](../ai-workflow/memory/active/PROJECT_PROFILE.md) — 운영 명령 / 정책
- [skill-lint/SKILL.md](./skill-lint/SKILL.md) — 첫 스킬 (manifest validate)
