<!-- standard-ai-workflow-kit: v0.13.3-beta -->

# 작업 백로그 인덱스

- 문서 목적: 프로젝트의 모든 작업 항목과 날짜별 백로그 링크를 관리한다.
- 범위: 전체 태스크 목록, 우선순위, 진행 상태, 날짜별 기록 연결
- 대상 독자: 개발자, AI 에이전트, 프로젝트 매니저
- 상태: stable
- 최종 수정일: 2026-07-10
- 관련 문서: [세션 인계](./session_handoff.md), [프로젝트 프로파일](../../docs/PROJECT_PROFILE.md)

## 1. 운영 원칙
1. 세션 시작 시 인덱스와 최신 백로그 확인
2. **세션 종료 직전(commit 직전) 인덱스 및 Handoff 갱신** — [`../core/global_workflow_standard.md` §8](../core/global_workflow_standard.md) 정합 — `memory 갱신 → commit → push` 순서
3. 모든 작업 상태는 날짜별 백로그에 기록

## 2. 날짜별 백로그
- [2026-07-09](./backlog/2026-07-09.md)
- [2026-07-10](./backlog/2026-07-10.md)

## 3. 전체 작업 상태 요약
- [x] TASK-001: 표준 AI 워크플로우 초기 도입 (a~e 세션 1·2 전부 done, 2026-07-09)
- [x] TASK-002-B: 운영 자동화 (B-2, markdownlint-cli2 + lychee + skill-lint + GitHub Actions + pre-push hook + 저장소 README, 2026-07-09)
- [x] TASK-003-A: 두 번째 메타 스킬 — skill-discover (skills/skill-discover/SKILL.md v0.1.0, CHANGELOG v0.3.0, 2026-07-09)
- [x] TASK-002-B-verify: 1차 CI 검증 통과 (run 29022844646, 23s) + 재현성 (29023288041, 20s) + Node 20 해소 (29023548610, 18s)
- [x] TASK-A-2: Node 20 deprecation 해소 — actions v-line 업그레이드 (checkout @v5, setup-node @v5 + 'lts/*', setup-python @v6)
- [x] TASK-C: 운영 도구 보강 — scripts/skill-discover Python 3 구현 + .index.json 캐시 (.gitignore 추가)
- [x] TASK-D: html-slides-builder 카탈로그 진입 — 저장소 루트 `html-deck/` → `skills/html-slides-builder/`, frontmatter 보정 (E030/E040/W100/W110 해소), lint 사전 검증 (2026-07-09)
- [x] TASK-E: 이름 변경 `html-deck` → `html-slides-builder` — 디렉터리 mv, SKILL.md / references / scripts 잔재 정리, .index.json + CHANGELOG + handoff + README 동기화 (2026-07-09)
- [x] TASK-PI: 외부 레퍼런스 deep-research — 15 confirmed / 10 refuted, 1순위 = Marpit. Axes 2/3 (디자인 시스템 + AI agent skills) 는 uninvestigated (2026-07-09 → 2026-07-10)
- [x] TASK-F: Marpit 통합 — `references/marpit-directives.md` 신설 (~160줄, 3-scope directive 규약), astryx-component-map.md §2 분할 (2.1/2.2/2.3) + §6 끝 참조, SKILL.md §Procedure Phase 1 step 6 보강 + §References 추가, verify_deck.py `--strict` 옵션, 기존 MD024 + MD029 즉시 해소 (CHANGELOG `### Infra` 분리 + SKILL.md Phase 2/3/4 step 1~N renumber). lint 사전 검증 clean (2026-07-10)
- [x] wiki/index.md 신규 (R4 anchor 기반 단일 페이지 인덱스, 운영 도구 + 레퍼런스 link 통합, ~75줄) — CLAUDE.md 의 "다음에 읽을 문서" 에 wiki 명시되어 있었으나 부재하던 wiki 를 본 세션에서 보강 (2026-07-10)
- [x] Axes 2/3 후속 deep-research (2026-07-10): 13 confirmed → 8 findings. 디자인 시스템 (Open Props / Panda CSS / W3C DTCG preview / Style Dictionary bridge / USWDS rule out) + AI agent skills (agentskills.io canonical 40+ 제품 / 우리 SKILL.md catalog 표준 정합이나 Claude-Code-flavored 확장 / progressive disclosure). 1차 4 open question 중 3개 해소, 1개는 정책 결정.
- [x] Open Props + tokens layer 통합 (TASK-PI-Followup §A, 2026-07-10): astryx-component-map.md §2 cascade 3-layer → 4-layer (`reset / **tokens** / astryx-base / astryx-theme`). §2.4 tokens layer slot 정의 + §6.4 Open Props preset (CDN link + npm PostCSS JIT recipe). §6.3 Forest → §6.5 renumber, §6.3 reserved. SKILL.md §ASTRYX-Inspired Design System 절에 "Optional tokens layer" 1 paragraph + "When to skip" 1줄. **Backward compatible**: tokens layer 가 비어있어도 3-layer 정상.
- [x] frontmatter 정책 결정 (TASK-PI-Followup §A 잔여, 2026-07-10): agentskills.io canonical 40+ 제품 정합 + Claude-Code-flavored extension 허용 = **현재 상태 유지**. hybrid migration (depth-2 nested, `metadata.claude_code.*`) 은 YAML mini-parser recursive depth-n 확장 시 *동시에* (별도 task). 본 세션은 정책 문서만, **코드 변경 0건**. PROJECT_PROFILE.md §5 정책 결정 추가, CHANGELOG.md Added 1줄.
- [x] YAML mini-parser recursive depth-n + 3 SKILL.md depth-2 nested 재구성 (2026-07-10): `scripts/_frontmatter.py` 모듈 추출 (recursive depth-n nested object + nested list 지원). 두 parser 의 중복 단일화. 3 SKILL.md (`html-slides-builder`, `skill-lint`, `skill-discover`) 의 frontmatter 를 `metadata.claude_code.*` depth-2 nested 구조로 재구성. hermes namespace 폐기. skill-lint E040 path 갱신. 검증: skill-lint 3 SKILL.md clean, skill-discover 3 entries 정상, markdownlint 0 error. 3 commit (parser 단일화 / SKILL.md 재구성 / 운영 문서 동기화).
- [x] Marpit §3 hand-written 발현 검증 (2026-07-10): 3-slide test deck (`/tmp/_test_warm_deck.html`, ephemeral) — 4-layer cascade + `/* @theme: warm */` + `/* mood: WARM */` + `<!-- slide N: ... -->` + `<!-- @scope: ... -->` + `data-spot="hint"` + `data-theme` toggle. verify_deck.py --gate 1 (--strict) / --gate 2 / --gate 3 / --gate 4 / --mood-check 모두 통과. 부수적 보강: verify_deck.py 의 `--mood-check` 가 `--bg-dark` 만 찾던 것을 `--bg` fallback 으로 보강 (문서-코드 정합). handoff Risks 의 "Marpit section-ancestor scoping 의 hand-written 재현은 inference" 해소.
- [x] `.gitignore` 의 `__pycache__/` 패턴 추가 (2026-07-10, 가장자리 변경): `**/__pycache__/` + `*.py[cod]` + `*$py.class`. Python 3 가 `scripts/_frontmatter.py` / `scripts/skill-lint` / `scripts/skill-discover` 의 .pyc 캐시를 git 추적 차단. 기존 untracked `scripts/__pycache__/` 정리.
- [x] Ant Design (antd) 적용 가능성 검토 (2026-07-10): **antd 도입 보류**. (a) deep-research 5 axes (CSS-in-JS architecture / vanilla HTML 부재 / cssVar runtime-hash / static-extract SSR-only / 1920x1080 정합) + (b) minimal sample build (Vite 5 + React 18 + antd 5.21, dist 552 kB, JS 555 kB / gzip 178 kB / CSS 48 bytes, build step 필수, node_modules 161 MB). 우리 html-slides-builder deck (~20-50 kB) 대비 **~10x**, **no-build 원칙 위배**. 권고: UnoCSS CDN runtime 또는 ASTRYX 정합 hand-authored layer. 다음 세션: UnoCSS 도입 가능성 검토 후보.
- [x] UnoCSS 적용 가능성 검토 (2026-07-10, antd 후속): minimal sample HTML + CDN runtime 정량 측정 — `https://cdn.jsdelivr.net/npm/@unocss/runtime/uno.global.js`, raw 175 kB / **gzip 48 kB** / single script tag / no build step / npm 불필요. antd sample (gzip 178 kB, build step 필수) 대비 **~3.7x 작음** + no-build 정합. 단 FOUC caveat (`un-cloak` attribute 로 mitigation) + atomic CSS runtime generation overhead + `@media print` dynamic injection 미검증. **결론 — ASTRYX hand-authored 가 1순위, UnoCSS CDN runtime 이 옵션**. 권고: 기본 deck 작성은 ASTRYX 정합 layer + Open Props absorption (§A hybrid 정책) 유지, *선택적* UnoCSS CDN runtime 가능 (작성자 Tailwind-syntax 선호 시).
- [x] §A.5 선택적 UnoCSS CDN runtime 안내 (2026-07-10, antd/UnoCSS 후속): `references/astryx-component-map.md` 에 §10 (선택적 UnoCSS CDN runtime) 절 신규 — adoption 기준 / 안 할 경우 / `un-cloak` + script 1줄 recipe / trade-off 표 (ASTRYX default vs UnoCSS optional vs antd not-viable) / verification. SKILL.md §ASTRYX-Inspired Design System 절에 "Optional UnoCSS CDN runtime" cross-reference 단락 추가. *기본* 작성법은 ASTRYX hand-authored + Open Props (이미 §A hybrid 정책), UnoCSS 는 *opt-in* 작성법 대안 안내.
