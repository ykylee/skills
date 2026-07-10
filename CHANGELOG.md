# Changelog

- 문서 목적: 카탈로그의 모든 notable 변경을 시간순으로 기록한다.
- 범위: 추가/변경/제거된 스킬, 운영 정책, lint 절차 변경
- 대상 독자: 카탈로그 사용자, AI 에이전트, 기여자
- 상태: active
- 최종 수정일: 2026-07-10
- 관련 문서: [README.md](./skills/README.md), [./ai-workflow/memory/active/PROJECT_PROFILE.md](./ai-workflow/memory/active/PROJECT_PROFILE.md)

본 문서는 [Keep a Changelog](https://keepachangelog.com/ko/) 의 정신을 따른다.
버전은 [Semantic Versioning](https://semver.org/lang/ko/) 을 지향한다.

## [Unreleased]

### Added
- `html-slides-builder` 스킬 (v1.1.0, doc): 단일 1920x1080 HTML 슬라이드 빌더 (키보드 네비,
  PDF 인쇄, 6종 content-type spine, ASTRYX 테마 레이어). 위치: `skills/html-slides-builder/`.
  `references/` 2건 (astryx-component-map.md, presentation-patterns.md), `scripts/verify_deck.py` 1건.
- 운영 자동화 1차 실전 검증 통과 (GitHub Actions run `29022844646`): markdownlint-cli2 →
  `python3 scripts/skill-lint` → `lychee --offline` 3-step CI 검증 성공 (23s).
- 운영 자동화 정책 결정: markdownlint 스타일 rule (`MD022` / `MD031` / `MD032` / `MD060`) 비활성화
  — 카탈로그는 *의미 검증* (frontmatter / harness_compat / 링크) 이 핵심.
- 운영 도구 보강: `scripts/skill-discover` Python 3 stdlib-only 구현. `skill-discover/SKILL.md`
  §Procedure 1~7 의 실제 동작. `--index` 캐시 빌드, `category:X` / `harness:X` 토큰, `--json`,
  `--top N`. dry-run 결과: 인덱스 빌드 2 entries, 검색 (meta / category:meta / harness:generic-md) 정상.
- `references/marpit-directives.md` (html-slides-builder, v0.1.0): Marpit 3-scope directive 규약을
  우리 hand-written no-build deck 에 매핑 (global / local / spot + metadata comment 규약 +
  anti-patterns). TASK-PI deep-research 의 1순위 후속.
- frontmatter 정책 결정 (TASK-PI-Followup §A 잔여, 2026-07-10): agentskills.io canonical 40+
  제품 (Claude Code / Cursor / Cline / VS Code / OpenAI Codex / GitHub Copilot / Gemini CLI /
  Roo Code / Spring AI) 의 base shape 정합 + Claude-Code-flavored extension 허용 — *현재 상태
  유지* 결정. 향후 migration 방향 = hybrid (depth-2 nested, `metadata.claude_code.*`); 이
  migration 은 scripts/skill-lint · scripts/skill-discover 의 YAML mini-parser recursive
  depth-n 확장 시 *동시에* (별도 task). 코드 변경 없음, PROJECT_PROFILE.md §5 정책으로만
  기록. 2차 deep-research (TASK-PI-Followup, 2026-07-10) 의 1차 4 open question 중 마지막 1개
  해소.
- YAML mini-parser recursive depth-n + 3 SKILL.md depth-2 nested 재구성 (2026-07-10): hybrid
  정책 *구현*. `scripts/_frontmatter.py` 모듈 추출 (두 parser 의 중복 단일화 + recursive
  depth-n nested object / nested list 지원). 3 SKILL.md (`html-slides-builder`, `skill-lint`,
  `skill-discover`) 의 frontmatter 를 `metadata.claude_code.{when_to_use, version, author,
  license, platforms, harness_compat, category, tags, related_skills}` 의 depth-2 nested
  구조로 재구성. hermes namespace 폐기. skill-lint E040 path 갱신 (`metadata.claude_code.
  harness_compat`). lint 검증: skill-lint 3 SKILL.md clean, skill-discover 3 entries 정상,
  markdownlint 0 error.
- Marpit §3 hand-written 발현 검증 (2026-07-10): 3-slide test deck (`/tmp/_test_warm_deck.html`,
  ephemeral) — 4-layer cascade (`reset / tokens / astryx-base / astryx-theme`) + `/* @theme:
  warm */` + `/* mood: WARM */` + `<!-- slide N: ROLE — title -->` + `<!-- @scope: ... -->` +
  `data-spot="hint"` + `data-theme` toggle. 검증 결과: gate 1 (--strict metadata check) +
  gate 2 (scaffold) + gate 3 (3 slides) + gate 4 (3 notes) + `--mood-check` (warm hue family,
  dark #1C1917 + light #FAF7F2) 모두 통과. 부수적 보강: `verify_deck.py` 의 `--mood-check` 가
  `--bg-dark` 만 찾던 것을 `--bg` fallback 으로 보강 (SKILL.md / astryx-component-map.md §6
  theme preset 예시 코드와 정합). handoff Risks 항목 ("Marpit section-ancestor scoping 의
  hand-written 재현은 inference") 해소.
- `.gitignore` 의 `__pycache__/` 패턴 추가 (2026-07-10, 가장자리 변경): `**/__pycache__/`
  / `*.py[cod]` / `*$py.class` 패턴 추가. Python 3 가 `scripts/_frontmatter.py`,
  `scripts/skill-lint`, `scripts/skill-discover` 의 .pyc 바이트코드 캐시를 누적하던 것을
  git 추적 차단. 기존 untracked `scripts/__pycache__/` 정리.
- Ant Design (antd) 적용 가능성 검토 (2026-07-10): deep-research + minimal sample build
  (`/tmp/antd-sample/`, ephemeral) 결과 **antd 도입 보류**. sample build: Vite 5 + React 18
  / antd 5.21 minimal scaffold → dist 552 kB (JS 555 kB / gzip 178 kB / CSS 48 bytes),
  build step 필수, React runtime 필수, node_modules 161 MB. 우리 html-slides-builder
  deck (~20-50 kB) 대비 **~10x**, **no-build 원칙 위배**. deep-research 5 axes 결과:
  antd v5/v6 CSS-in-JS runtime architecture, vanilla HTML 진입점 없음 (유일한
  static-extraction 도구는 SSR-time 전용), cssVar theming 의 runtime-hash-knowledge
  제약. 권고: antd 직접 도입 보류, design-system fidelity 필요 시 **UnoCSS CDN runtime**
  (`<script src="https://cdn.jsdelivr.net/npm/@unocss/runtime"></script>`) 또는 **ASTRYX
  정합 hand-authored layer** (이미 §A hybrid 정책으로 구현됨).
- UnoCSS 적용 가능성 검토 (2026-07-10, antd 후속): minimal sample HTML (`/tmp/unocss-test.html`,
  ephemeral, ~5 kB) + CDN runtime 정량 측정 (`https://cdn.jsdelivr.net/npm/@unocss/runtime/
  uno.global.js`, raw 175 kB / gzip 48 kB / single script tag / no build step / npm
  불필요). antd sample (gzip 178 kB, build step 필수) 대비 **~3.7x 작음** + no-build
  정합. 단 FOUC caveat (첫 paint unstyled, `un-cloak` attribute 로 mitigation) +
  atomic CSS runtime generation overhead + `@media print` 의 dynamic injection 정합
  미검증. **결론 — ASTRYX hand-authored 가 1순위, UnoCSS CDN runtime 이 옵션**.
  권고: 기본 deck 작성은 ASTRYX 정합 layer + Open Props absorption (§A hybrid 정책)
  유지. *선택적* 도구로 UnoCSS CDN runtime 한 줄 추가 가능 — 작성자가
  Tailwind-syntax (utility-class) 선호 시. SKILL.md 또는 astryx-component-map.md 에
  §A.5 (선택적) 섹션으로 추가 가능.
- §A.5 선택적 UnoCSS CDN runtime 안내 (2026-07-10, antd/UnoCSS 후속):
  `references/astryx-component-map.md` 에 §10 (선택적 UnoCSS CDN runtime) 절 신규
  — adoption 기준 / adoption 하지 말아야 할 경우 / `un-cloak` + script 1줄 recipe /
  trade-off 표 (ASTRYX default vs UnoCSS optional vs antd not-viable) /
  verification. SKILL.md §ASTRYX-Inspired Design System 절에 "Optional UnoCSS
  CDN runtime (utility-class authoring, opt-in)" cross-reference 단락 추가. *기본*
  작성법은 ASTRYX hand-authored + Open Props (이미 §A hybrid 정책으로 구현),
  UnoCSS 는 *opt-in* 작성법 대안으로 안내.
- §A.5 UnoCSS CDN runtime sample deck (2026-07-10, §A.5 실증):
  `skills/html-slides-builder/references/examples/uno-cdn-deck.html` 신규 (~9 KB).
  3-slide deck (Title / Section / Content + `data-spot="hint"` callout) — ASTRYX
  4-layer cascade (`reset / tokens / astryx-base / astryx-theme`) + UnoCSS CDN runtime
  utility classes + Marpit metadata comments + `data-theme` toggle + `localStorage`
  persistence + keydown nav + `@media print` 16:9. Open in browser to verify keyboard
  nav + print + theme toggle. `verify_deck.py --gate 1|2|3|4 --mood-check --strict` ALL
  GATES PASSED. verify_deck.py gate 4 allowlist 확장 (cdn.jsdelivr.net / unpkg.com,
  web fonts 와 같은 카테고리) + regex 매치 trailing host 포함 보강 (group(0) 이
  `<script src="https://` 까지만 매치하던 버그 → `https?://[^"\']+` 로 host 까지 매치).
- ASTRYX 4-layer cascade + Open Props preset (html-slides-builder, astryx-component-map.md):
  §2.4 tokens layer slot (Panda CSS `@layer tokens` *개념만* 차용 — framework 도입 X) +
  §6.4 Open Props sub-atomic absorption recipe. §6.3 Forest 가 §6.5 로 renumber, §6.3 은
  *reserved*. 2차 deep-research (Axes 2 디자인 시스템) 의 1순위 후보 = Open Props 후속.

### Changed
- 스킬 이름 변경 (TASK-E): `html-deck` → `html-slides-builder`. builder suffix 로 *도구 역할*
  명시. 카테고리는 `doc` 유지 (산출물이 단일 HTML 문서). 영향: `skills/<name>/` 디렉터리명,
  SKILL.md frontmatter `name`, 본문 `localStorage` key 예시, `skills/.index.json`, CHANGELOG,
  session_handoff, README(루트) 트리 동기화.
- Marpit 통합 (TASK-F): `references/astryx-component-map.md` §2 를 §2.1 / §2.2 / §2.3 으로 분할
  (§2.2 metadata convention 신규, §2.3 section scoping 신규), §6 끝에 `marpit-directives.md`
  참조 1줄 추가. `SKILL.md` §Procedure Phase 1 step 6 끝에 metadata comment 규약 1 paragraph,
  §References 에 marpit-directives.md 항목 + `--strict` 옵션 추가. `scripts/verify_deck.py` 에
  `--strict` 옵션 신규 (gate 1 에서 `/* @theme: */` / `/* mood: */` 부재 시 WARN, FAIL 아님).
- ASTRYX cascade 3-layer → 4-layer (TASK-PI-Followup §A): `astryx-component-map.md` §2 의
  cascade order 가 `reset / astryx-base / astryx-theme` → `reset / **tokens** / astryx-base /
  astryx-theme`. `§5` 의 pasted CSS block 도 tokens slot 추가. SKILL.md §ASTRYX-Inspired
  Design System 절에 "Optional tokens layer" 1 paragraph + "When to skip" 1줄 추가. **Backward
  compatible**: tokens layer 가 비어있어도 3-layer cascade 정상.

### Infra
- `.markdownlint.jsonc` — 의미 검증은 `scripts/skill-lint` 가 담당, markdownlint-cli2 는 *문법*
  만 잡는다 (스타일 rule 비활성화).
- `.github/workflows/skill-lint.yml` — lychee 설치를 `taiki-e/install-action@v2` (tool: lychee) 로
  교체. `curl | bash + PATH` 의 불안정성 제거.
- `.github/workflows/skill-lint.yml` — 액션 v-line 업그레이드 (Node 20 deprecation 해소):
  `actions/checkout@v4` → `@v5`, `actions/setup-node@v4` → `@v5` + `node-version: '20'` → `'lts/*'`,
  `actions/setup-python@v5` → `@v6`. 각 major 1 step (A-2 점진).
- `skills/README.md` §6 — 검색 절차 + scoring 가중치 추가.
- `skill-discover/SKILL.md` — Trade-offs 에 *구현 도구* 1줄 추가, References 에 `scripts/skill-discover`.
- `README.md` (저장소 루트) — 디렉터리 트리에 `scripts/skill-discover` 추가, 빠른 시작 / 로컬 lint
  절차에 검색 / 인덱스 빌드 명령 추가.
- `CHANGELOG.md` — 저장소 루트이므로 `./ai-workflow/...` 링크로 수정 (이전 `../ai-workflow/...`).
- `PROJECT_PROFILE.md` — `../../core/global_workflow_standard.md` 로 수정 (이전 `../core/...`,
  한 단계 위로 부족).

### Fixed
- 1차 CI 실패 (`29022405829`) — markdownlint 스타일 48 errors 비활성화로 해결.
- 2차 CI 실패 (`29022615698`) — lychee `command not found` (PATH 미적용) → install-action 으로 해결.
- 3차 CI 실패 (`29022734640`) — `CHANGELOG.md` / `PROJECT_PROFILE.md` 깨진 링크 2건 수정.
- Node.js 20 deprecation annotation — 액션 v-line 업그레이드로 해소 (6차 CI 검증 통과, run `29023548610`).
- markdownlint 기존 lint error 해소: `CHANGELOG.md` 의 두 번째 `### Changed` (TASK-002-B 운영
  자동화 항목) → `### Infra` 로 분리 (MD024 siblings_only 해소). `SKILL.md` §Procedure Phase 2/3/4
  의 step 번호 7~13 → 각 Phase 별 1~N 으로 renumber (MD029 ol-prefix 해소).

## [0.3.0] - 2026-07-09

### Changed
- `.github/workflows/skill-lint.yml` — lychee 설치를 `taiki-e/install-action@v2` (tool: lychee) 로
  교체. `curl | bash + PATH` 의 불안정성 제거.
- `.github/workflows/skill-lint.yml` — 액션 v-line 업그레이드 (Node 20 deprecation 해소):
  `actions/checkout@v4` → `@v5`, `actions/setup-node@v4` → `@v5` + `node-version: '20'` → `'lts/*'`,
  `actions/setup-python@v5` → `@v6`. 각 major 1 step (A-2 점진).
- `CHANGELOG.md` — 저장소 루트이므로 `./ai-workflow/...` 링크로 수정 (이전 `../ai-workflow/...`).
- `PROJECT_PROFILE.md` — `../../core/global_workflow_standard.md` 로 수정 (이전 `../core/...`,
  한 단계 위로 부족).

### Fixed
- 1차 CI 실패 (`29022405829`) — markdownlint 스타일 48 errors 비활성화로 해결.
- 2차 CI 실패 (`29022615698`) — lychee `command not found` (PATH 미적용) → install-action 으로 해결.
- 3차 CI 실패 (`29022734640`) — `CHANGELOG.md` / `PROJECT_PROFILE.md` 깨진 링크 2건 수정.

## [0.2.0] - 2026-07-09

### Added
- 운영 자동화: `.markdownlint.jsonc` (markdownlint-cli2 rule 정의 — MD013/041 비활성 등)
- 운영 자동화: `.github/workflows/skill-lint.yml` (GitHub Actions, push / pull_request 트리거)
  — `markdownlint-cli2` → `python3 scripts/skill-lint` → `lychee --offline` 순차 실행
- 운영 자동화: `.githooks/pre-push` (로컬 pre-push hook, `git config core.hooksPath .githooks`)
- 운영 자동화: `scripts/skill-lint` (Python 3 stdlib-only, frontmatter / harness_compat / 내부 링크 검증)
- 저장소 루트 `README.md` — 사용자 진입점, 빠른 시작, 로컬 lint 절차, 운영 정책
- `skills/skill-lint/SKILL.md` v0.2.0 — Recommended tooling, Workflow integration, Custom rules,
  error code 확장(E210 외부 링크, W110 미사용 디렉터리)

### Changed
- `PURPOSE.md` §3 — `scripts/` 하위 *운영 도구* (skill-lint 등 Python 스크립트) 는
  non-scope 예외로 명시
- `PROJECT_PROFILE.md` §3 — `runtime_checks` TBD → 합의값 (markdownlint-cli2 + lychee + skill-lint 절차)
- `state.json.commands.runtime_checks` — 합의값으로 승격

### Breaking
- `skill-lint` SKILL.md frontmatter 의 `description` 이 1-line / ≤ 200자 규칙을 강제 (E030).
  기존 `skill-lint/SKILL.md` 의 description 길이 검증으로 회귀 확인 완료.

## [0.1.0] - 2026-07-09

### Added
- 카탈로그 bootstrap: `skills/` 디렉터리 및 authoring 가이드 (`skills/README.md`)
- 첫 메타 스킬: `skill-lint` (`skills/skill-lint/SKILL.md`) — SKILL.md frontmatter 정합성,
  name/description/harness_compat/references 검증 절차
- 표준 AI 워크플로우 문서 실값화: `PURPOSE.md`, `PROJECT_PROFILE.md`, `state.json`,
  `session_handoff.md`, `backlog/2026-07-09.md`
- 카탈로그 운영 명령 합의: `markdownlint-cli2` (markdown lint), `lychee` (link check),
  `skill-lint` 절차 (frontmatter / 디렉터리 / harness_compat)

### Changed
- (없음 — bootstrap 직후 첫 릴리즈)

### Deprecated
- (없음)

### Removed
- placeholder 프로젝트명 `Export Sample` → `skills` 로 확정
- placeholder PURPOSE / PROFILE / state / handoff 의 TODO 항목 전부 실값화 또는 명시적 N/A

### Fixed
- (없음)

### Security
- (해당 없음 — 코드 부재 저장소)

### Breaking
- (bootstrap 이므로 해당 없음)
