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
- `llm-wiki` 스킬 (v0.1.0, meta): Karpathy의 [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 패턴을 구현하는 메타 스킬. 사용자 지정 위치에 `raw/` + `wiki/` + `SCHEMA.md` 3계층 영구 markdown 위키를 부트스트랩하고 Ingest/Query/Lint 3연산으로 운영. 위치: `skills/llm-wiki/`, `references/` 7건 (bootstrap-walkthrough / ingest-procedure / query-procedure / lint-procedure / schema-template / wiki-index-template / wiki-log-template). MVP 0.1.0 — 절차만 정의, `scripts/bootstrap-wiki.py` 자동화는 Next version.
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
- Browser 시각 검증 (2026-07-10, headless): 두 sample 의 visual rendering 검증.
  Google Chrome 148.0.7778.96 /chromium 150.0.7871.46 (snap confinement 의
  AppArmor `/tmp/` 차단 확인 — google-chrome 으로 우회) + `--no-sandbox
  --disable-gpu --disable-dev-shm-usage --virtual-time-budget=10000-15000`.
  검증 결과: ① warm-deck (test/4-layer + data-spot) — espresso dark `#1C1917` 배경 +
  amber 제목 `Marpit §3 hand-written test` + 회색 caption + slide counter `1/3` 모두
  시각 정상 (ASTRYX 4-layer cascade 검증). ② uno-cdn-deck — 검정 배경 + amber `UnoCSS
  opt-in` 제목 (large) + 본문 + counter 정상 (ASTRYX cascade 검증), 다만 상단에
  HTML comment 가 raw text 로 노출되는 **FOUC 발견** — UnoCSS CDN runtime 의 CSS
  injection 이 본 sandbox 환경에서 timeout (15초) 내에 미완료, 또는 network
  interception 으로 script load 실패 추정. **운영 노트**: 사용자의 일반 browser 환경
  에서는 정상 동작 예상 (sandbox/network 한계 외). FOUC 가 *실제 사용자 환경에서도*
  발생할 경우 `<body un-cloak>` 만으로 mitigation 부족 — CSS pre-injection 또는
  critical CSS inline 고려 필요 (다음 세션 task 후보).
- FOUC mitigation (2026-07-10, A1+A3 결합): §A 잔여. `references/astryx-component-map.md`
  §10 에 **FOUC caveat** 단락 추가 — `<body un-cloak>` 의 한계 명시 + 3가지 mitigation
  pattern (pre-paint critical CSS inline / `visibility: hidden` + JS toggle / pre-rendered
  build) + priority ordering (ASTRYX §5 가 1순위, UnoCSS 옵션). `references/examples/
  uno-cdn-deck.html` 의 `<head>` 에 *pre-paint critical CSS inline* 추가 — slide 1 의
  실제 utility classes (~30 rules + body visibility toggle) inline 으로 pre-inject,
  UnoCSS runtime 이 *이후* 추가 utilities 채움. verify_deck.py ALL GATES PASSED (file 9 →
  11.6 KB).
- UnoCSS 대안 preset 안내 (2026-07-10, B, §11+§12 신규): `references/astryx-component-map.md`
  끝에 §11 (Alternative UnoCSS presets) + §12 (When UNO CSS adoption is the wrong call)
  추가. `preset-mini` (~30 kB, utility subset), `preset-attributify` (attribute-based,
  no-FOUC, ~50 kB), `preset-icons` (~10 kB), `preset-web-fonts` (~5 kB), `preset-uno`
  palette (build step 필요). Swap pattern + recommended decision flow + verify_deck.py
  contract. ASTRYX 가 *여전히 1순위* 인 *decision tree* 명시. 코드 변경 없음 (sample
  변경 X, runtime 변경 X).
- UnoCSS deep-research (2026-07-10, §B 검증·근거 강화): `astryx-component-map.md` §11+§12
  갱신. 5 axes workflow `wc3la5p3f` 결과 (15 surviving claims, 4 load-bearing facts):
  ① §11 표에서 stale `preset-uno` row *제거* (officially deprecated, renamed to
  `preset-wind3`) + deprecated 노트. ② `preset-attributify` 보강 — *additive mode, NOT a
  standalone engine*; JSX/TSX 는 `transformerAttributifyJsx()` 필수 (valueless attribute 의
  JSX rewrite 문제). ③ CDN runtime caveats 추가 — *preflights 안 ship* (reset CSS link
  전, `<un-cloak>` rule inline 필수), default bundled = Wind3 (mini 사용 시
  `mini.global.js` 명시). ④ `preset-mini` 보강 — strict subset (container/animation/
  gradient 제외). ⑤ §12 보강 — 6 가지 *operational* yes-branch 표 (preflights/JSX/
  preset-mini load/FOUC/JSX authoring/preflights by default). 권고 synthesis 통합. 코드
  변경 없음 (sample 변경 X, runtime 변경 X).
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
- **`skill-lint` E002 — 표준 YAML 교차검증 (2026-07-21)**: mini-parser 가 관대해서 표준 YAML
  파서가 거부하는 값을 통과시키던 사각지대를 닫았다. 앞선 frontmatter 3건이 CI green 상태로
  깨져 있던 원인.
  - `scripts/_frontmatter.py` 에 `check_yaml_strict()` 추가 — **stdlib-only 유지** (PyYAML
    도입 없음, PROJECT_PROFILE §3 정합). 검출 3종: 평문 스칼라의 콜론+공백 / 닫는 따옴표 뒤
    잔여 내용 / 미닫힘 따옴표. 위반 시 파일 기준 줄 번호와 함께 `E002`.
  - `_strip_quotes()` 버그 수정 — `.strip('"').strip("'")` 이 따옴표를 개수 제한 없이
    벗겨내어 `say 'hi'` 의 끝 따옴표를 잘라먹던 것을 *짝이 맞는 한 쌍* 만 제거하도록 변경.
  - 검증: js-yaml 과의 차등 테스트 16 케이스 (정상 8 / 깨짐 8) **전부 일치, false positive 0**.
    URL 값 (`https://…`), 평문 아포스트로피, `''` / `\"` escape, inline list, comment 는
    정상 통과. 실제 5 SKILL.md 는 전체 키 재귀 비교로 js-yaml 과 **불일치 0**.
  - 한계: 전체 YAML 스펙 검증이 아니다. multi-line scalar / anchor / flow mapping 은 대상
    밖이며, `skills/README.md` §3.1.0 에 표준 파서 직접 확인 절차를 함께 안내한다.
- `skills/skill-lint/SKILL.md` — §Procedure 에 E002 단계 추가 (이후 단계 renumber),
  rule code 목록에 `E002` 추가, `E040` 경로를 `metadata.claude_code.harness_compat` 로 보정
  (§3.1 예시와 같은 stale 경로였음).

### Fixed
- **`llm-wiki` graph 검사 규칙 정정 (2026-07-21, v0.1.1 → v0.2.0)**: TASK-M 실전 검증의
  결함 ④. 조사해 보니 한 건이 아니라 세 갈래였다.
  - **역방향 link 대칭성 검사 폐기** (`lint-procedure.md` §3.1). "A→B 면 B→A 도" 규칙이
    `ingest` §6 (새 entity → 비교/개념 페이지, 한 경우) 보다 훨씬 넓게 적용돼 있었다.
    실측에서 지적 4건이 **전부 오탐** — `synthesis → concept` 같은 상하위 인용은 비대칭이
    옳다. 대칭성은 도달 가능성의 대리 지표일 뿐이라 orphan 검사로 대체.
  - **orphan 처방의 논리 오류 수정** (`ingest-procedure.md` §6·§10, `SKILL.md` §B.5):
    orphan 을 *들어오는* link 0 으로 정의하면서 처방은 "최소 1개 **outgoing** link 보장"
    이었다. 나가는 link 는 자신의 orphan 상태를 바꾸지 못한다. "기존 관련 페이지 *에서*
    새 페이지로 들어오는 link 최소 1개" 로 정정.
  - **orphan 의 index link 취급 정의** (`lint-procedure.md` §3.1, `SKILL.md` §D.1):
    `index.md` link 를 incoming 으로 셀지가 미정의였고 결과가 뒤집혔다. `ingest` §7 이
    모든 페이지의 index 등재를 요구하므로 index 를 세면 orphan 이 원리적으로 발생 불가
    — **index 제외** 로 확정.
  - 부수: `ingest` §6 의 상대 경로 예시 `../entity-x/` → `./entity-x.md` (페이지는 `wiki/`
    안 형제).
  - 검증: 검증 위키에 새 규칙 적용 시 **오탐 4건 → 진짜 orphan 1건** (`entity-llm-wiki`,
    콘텐츠 페이지 중 이를 가리키는 것이 실제로 없음). 지적 수는 줄고 신호는 늘었다.
  - **미수정**: ⑤ bootstrap 의 SCHEMA 플레이스홀더 치환 체크리스트 누락.
- **`llm-wiki` 템플릿 결함 4건 (2026-07-21, v0.1.0 → v0.1.1)**: 실전 검증 (bootstrap →
  ingest 6회 → query → lint) 중 발견. 절차 자체가 아니라 *복사되는 템플릿* 의 문제.
  - `wiki-index-template.md` 경로 오류 — 예시가 `./wiki/entity-<slug>.md` 인데 `index.md`
    자체가 `wiki/` 안에 있어 `wiki/wiki/` 를 가리켰다 (8개 항목 전부). `./entity-foo.md` 로 보정.
  - `wiki-index-template.md` 에 markdown 링크가 **0개** 였던 것을 복원. `e21e755` (lychee
    CI green) 이 링크를 `(page: …)` 서술형으로 바꿨는데, index 는 Query 절차 §C.1 의 1차
    검색 인덱스라 페이지 이동이 끊겼다. 예시 행을 **fenced code block** 안에 두어 링크
    문법을 보존하면서 lychee 의 링크 추출 대상에서 제외 — `wiki-log-template.md` 가 이미
    쓰던 "예시는 지우고 시작" 관례와 같은 방향. 부수 효과로 `a881deb` 의 백틱 wrap 이
    불필요해져 `<slug>` → `foo` 로 단순화.
  - `schema-template.md` 의 `[llm-wiki SKILL.md](../SKILL.md)` — `references/` 안에서만
    유효하고 사용자 위치로 복사하면 깨졌다 (lychee 는 원본 위치만 보므로 통과). 서술형
    경로로 교체하고 복사 후 기준임을 명시.
  - 오타 2건 — `mucic/index/log` (bootstrap-walkthrough), `AI 모델 wikil는` (schema-template).
  - 검증: 수정한 템플릿으로 재-bootstrap → 펜스를 벗긴 실제 링크가 destination 에서
    해석됨 (수정 전이면 `wiki/wiki/…`). 코드 펜스·코드 스팬 제외 상대 링크 15건 전부 해석.
    markdownlint 18 files 0 issues, skill-lint --strict clean.
  - **미수정 (별도 task)**: lint 의 역방향 link 대칭성 규칙이 ingest 절차와 불일치 (동급
    관계가 아닌 `synthesis → concept` 까지 대칭 요구), bootstrap 의 SCHEMA 플레이스홀더
    치환 체크리스트 누락.
- 1차 CI 실패 (`29022405829`) — markdownlint 스타일 48 errors 비활성화로 해결.
- 2차 CI 실패 (`29022615698`) — lychee `command not found` (PATH 미적용) → install-action 으로 해결.
- 3차 CI 실패 (`29022734640`) — `CHANGELOG.md` / `PROJECT_PROFILE.md` 깨진 링크 2건 수정.
- Node.js 20 deprecation annotation — 액션 v-line 업그레이드로 해소 (6차 CI 검증 통과, run `29023548610`).
- markdownlint 기존 lint error 해소: `CHANGELOG.md` 의 두 번째 `### Changed` (TASK-002-B 운영
  자동화 항목) → `### Infra` 로 분리 (MD024 siblings_only 해소). `SKILL.md` §Procedure Phase 2/3/4
  의 step 번호 7~13 → 각 Phase 별 1~N 으로 renumber (MD029 ol-prefix 해소).
- **표준 YAML 파서 비호환 frontmatter 3건 (2026-07-21)**: 5 SKILL.md 중 3건이 표준 YAML
  파서에서 파싱 실패하던 것을 수정. 값은 그대로 두고 따옴표만 보정 — 의미 변경 없음.
  - `html-slides-builder` `description` — 평문(unquoted) 스칼라 안의 `Triggers:` + 공백이 두 번째
    mapping key 로 해석됨. 값 전체를 `"` 로 감쌈.
  - `llm-wiki` / `react-premium-design` `when_to_use` — `"A", "B", "C"` 형태로 닫는 따옴표 뒤에
    쉼표가 이어져 문법 오류. 값 전체를 `'` 로 감쌈 (내부 `"` 보존).
  - 배경: 자체 mini-parser (`scripts/_frontmatter.py`) 가 관대해 `skill-lint` 는 clean 을
    보고했고 CI 도 green 이었으나, agentskills.io canonical 제품군이 사용하는 표준 YAML
    파서에서는 3건 모두 파싱 불가 상태였다 ([PURPOSE.md §1](./ai-workflow/memory/active/PURPOSE.md)
    의 cross-harness 재사용 목적과 충돌).
  - 검증: `npx js-yaml` 로 5건 모두 파싱 성공 + mini-parser 와 값 10건 전부 일치 확인.
  - 재발 방지 (미착수): `skill-lint` 에 표준 YAML 교차검증을 넣지 않는 한 동일 유형이 다시
    통과함 — 별도 task.
- **카탈로그 문서 드리프트 (2026-07-21)**:
  - `react-premium-design` 미등재 해소 — 저장소 `README.md` 트리와
    `ai-workflow/wiki/index.md` §4 에 누락되어 있던 것을 추가. 5개 스킬 전부 두 문서에 등재됨.
  - `skills/README.md` §3.1 frontmatter 예시가 **stale** 하던 것을 수정 — top-level
    `when_to_use` + `metadata.harness_compat` 를 보여주고 있었으나, 2026-07-10 정책 이후
    실제 구조는 `metadata.claude_code.*` depth-2 nested 다. 가이드대로 새 스킬을 쓰면
    `skill-lint` E040 에 걸리는 상태였다. §3.1.3 / §3.1.4 제목과 §6 체크리스트도 동일하게 보정.
  - `skills/README.md` §3.1.0 (YAML 인용 규칙) 신설 — 위 3건의 실제 실패 유형 2종과
    `js-yaml` 확인 절차 (동작 검증 완료: 정상 SKILL.md exit 0, 고장 케이스 non-zero).
  - `skills/README.md` §1.1 — 스킬 목록을 손으로 복사하는 대신 `scripts/skill-discover`
    로 생성하도록 안내. 손 관리 목록이 늘수록 본 드리프트가 반복되므로 목록을 추가하지 않음.

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
