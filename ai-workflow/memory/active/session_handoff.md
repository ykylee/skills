<!-- standard-ai-workflow-kit: v0.13.3-beta -->

# Session Handoff

- Purpose: Compact restore context for the next AI agent session.
- Scope: current focus, task status, key changes, next actions, risks
- Audience: AI agents, maintainers
- Status: draft
- Updated: 2026-07-10 (TASK-F done + wiki 신규 진행)
- Related docs: [Purpose](./PURPOSE.md), [Project Profile](./PROJECT_PROFILE.md), [Work Backlog](./work_backlog.md)

## Current Focus

- **TASK-D + TASK-E + TASK-PI + TASK-F 완료, wiki 신규 + 세션 마무리**: TASK-001 (a~e) +
  TASK-002-B (운영 자동화) + TASK-003-A (skill-discover SKILL.md) + TASK-002-B-verify (1차 CI) +
  TASK-A-2 (Node 20 deprecation 해소) + TASK-C (skill-discover 실제 구현, .index.json 캐시) +
  TASK-D (html-deck 위치 이동 + frontmatter 보정 + 인덱스 갱신) +
  TASK-E (이름 변경 `html-deck` → `html-slides-builder` + 운영 문서 동기화 + lint 검증) +
  TASK-PI (외부 레퍼런스 deep-research, 1순위 = Marpit) +
  TASK-F (Marpit 통합 — `references/marpit-directives.md` 신설, astryx-component-map.md §2 확장,
  SKILL.md §Procedure Phase 1 step 6 보강, verify_deck.py `--strict` 옵션, 기존 MD024 + MD029
  즉시 해소) 모두 done.
  본 세션의 추가 산출물: `ai-workflow/wiki/index.md` 신규 (R4 anchor 기반 인덱스, 운영 도구 +
  레퍼런스 link).
  두 commit (① TASK-F, ② wiki) 진행.

## Work Status

- TASK-001 표준 AI 워크플로우 초기 도입: **done** (TASK-001a~e)
- TASK-002-B 운영 자동화 (B-2): **done**
  - .markdownlint.jsonc, .github/workflows/skill-lint.yml, .githooks/pre-push, scripts/skill-lint, README.md
- TASK-003-A 두 번째 메타 스킬 (skill-discover): **done**
  - skills/skill-discover/SKILL.md v0.1.0
  - skill-lint 통과 (2 SKILL.md clean)
  - CHANGELOG.md v0.3.0
- TASK-D html-deck 카탈로그 진입: **done**
  - 저장소 루트 `html-deck/` → `skills/html-slides-builder/` 이동 (CLAUDE.md 메모리
    `[[workflow-skills-not-managed]]` 정책과 무관 — html-deck 은 workflow-* 아님)
  - frontmatter 보정 (lint E030/E040 해소), 본문 lint W100/W110 보정
- TASK-E 이름 변경 html-deck → html-slides-builder: **done**
  - 디렉터리 mv, SKILL.md / references / scripts 잔재 0건
  - .index.json + CHANGELOG + handoff + README 동기화
- TASK-PI 외부 레퍼런스 deep-research: **done**
  - 5 phase 자동, 106 agents, 15 confirmed / 10 refuted
  - 1순위 = Marpit (Marp-first markdown + section auto-scoping + build-step-free)
  - Axes 2/3 (디자인 시스템 + AI agent skills) 는 uninvestigated
- TASK-F Marpit 통합: **done (본 세션)**
  - `references/marpit-directives.md` 신설 (~160줄, 3-scope directive 규약 + metadata comment 규약)
  - `references/astryx-component-map.md` §2 분할 (2.1 layer / 2.2 metadata / 2.3 section scoping) + §6 끝 1줄
  - `SKILL.md` §Procedure Phase 1 step 6 metadata comment 1 paragraph + §References 항목 추가
  - `scripts/verify_deck.py` `--strict` 옵션 (gate 1 `/* @theme: */` + `/* mood: */` 부재 시 WARN)
  - 기존 MD024 + MD029 즉시 해소 (CHANGELOG `### Infra` 분리 + SKILL.md Phase 2/3/4 step 1~N renumber)
  - lint 사전 검증 clean (markdownlint-cli2 0 error, skill-lint 3 SKILL.md clean)
- N/A: blocked
- N/A: blocked

## Key Changes

- TASK-001 산출물 (이전 세션): PURPOSE.md, PROJECT_PROFILE.md, state.json, session_handoff.md,
  work_backlog.md, backlog/2026-07-09.md, skills/README.md, skills/skill-lint/SKILL.md, CHANGELOG.md v0.1.0
- TASK-002-B 운영 자동화 (이전 세션): .markdownlint.jsonc, .github/workflows/skill-lint.yml,
  .githooks/pre-push, scripts/skill-lint (YAML mini-parser 버그 수정), README.md, PURPOSE §3 예외,
  PROJECT_PROFILE §3 runtime_checks, CHANGELOG v0.2.0
- TASK-003-A 두 번째 메타 스킬 (이전 세션): skills/skill-discover/SKILL.md v0.1.0, CHANGELOG v0.3.0
- TASK-002-B-verify 1차 CI 검증 (이전 세션): 4-cycle (6cd8d17 → 42a36fc → d39993c → 3937de2)
  후 run 29022844646 통과. 5차 CI (29023288041) 재현성 확인.
- TASK-A-2 Node 20 deprecation 해소 (이전 세션): actions v-line 업그레이드
  (checkout @v5, setup-node @v5 + 'lts/*', setup-python @v6). 6차 CI (29023548610) 통과.
- TASK-C 운영 도구 보강 (이전 세션):
  - `scripts/skill-discover` Python 3 stdlib-only 구현. skill-discover/SKILL.md §Procedure 1~7 의
    *실제 동작*. `--index` 캐시 빌드 (skills/.index.json), `category:X` / `harness:X` 토큰, `--json`,
    `--top N`. dry-run 정상 (인덱스 2 entries, 검색 / JSON 정상).
  - `skills/README.md` §6 — 검색 절차 + scoring 가중치 추가.
  - `skill-discover/SKILL.md` — Trade-offs 에 *구현 도구* 1줄, References 에 `scripts/skill-discover`.
  - `README.md` (저장소 루트) — 디렉터리 트리 / 빠른 시작 / 로컬 lint 갱신.
  - `.gitignore` — `skills/.index.json` 캐시 제외.
  - `CHANGELOG.md` [Unreleased] — TASK-C 항목 추가, TASK-A-2 해소 표시.
- TASK-D html-deck 카탈로그 진입 (본 세션):
  - 위치 이동: 저장소 루트 `html-deck/` → `skills/html-deck/` (CLAUDE.md 메모리
    `[[workflow-skills-not-managed]]` 정책과 무관 — html-deck 은 workflow-* 아님).
  - frontmatter 보정: description 200자 이내로 단축, `metadata.harness_compat:[claude-code, generic-md]`
    추가, `metadata.category:doc` 추가, `when_to_use` 필드 추가, 기존 `version`/`author`/`license`/
    `platforms`/`metadata.hermes` 보존. lint E030/E040 해소.
  - `skills/.index.json` — html-deck 항목 prepend (3 entries).
  - `CHANGELOG.md` [Unreleased] — TASK-D 항목 1줄 추가.
  - `README.md` (저장소 루트) — 디렉터리 트리 갱신.
  - `python3 scripts/skill-lint --path skills` 사전 검증 — 깨짐 0 확인 (3 SKILL.md 모두 clean).
- TASK-E 이름 변경 html-deck → html-slides-builder (본 세션):
  - 사용자 결정: `html-slides-builder` 채택 (builder suffix 로 도구 역할 명시, category 는 `doc` 유지).
  - `skills/html-deck/` → `skills/html-slides-builder/` mv.
  - SKILL.md frontmatter `name: html-deck` → `name: html-slides-builder`, 본문
    `localStorage` key 예시 `html-deck-<basename>-index` → `html-slides-builder-<basename>-index`.
  - `skills/.index.json` — `name` + `path` 갱신.
  - `CHANGELOG.md` [Unreleased] — Added 의 TASK-D 항목을 현재 이름으로 갱신, Changed 에 TASK-E
    1줄 추가.
  - `README.md` (저장소 루트) — 트리의 `html-deck/` → `html-slides-builder/`.
  - 잔재 0건 (`references/astryx-component-map.md` 8 라인 + `scripts/verify_deck.py` docstring 1건 모두 갱신).
  - `python3 scripts/skill-lint --path skills --strict` — 깨짐 0 재확인.
- TASK-PI 외부 레퍼런스 deep-research (본 세션):
  - 5 phase 자동: Scope → Search → Fetch → Verify → Synthesize.
  - 5개 검색 축: HTML 슬라이드 빌더 / 디자인 시스템 / AI agent skill 생태계 / Self-contained 패턴
    / 테마·레이아웃·프런트매터 코드셰이프.
  - 23 source fetch, 105 claim 추출, 25 verify → 15 confirmed / 10 refuted.
  - **1순위 = Marpit** (Marp-first markdown + section auto-scoping + build-step-free). 4가지 핵심
    패턴: dual metadata carrier (YAML/HTML-comment), three-scope directives (global/local/spot),
    `/* @theme name */` metadata + section auto-scoping, two-tier config discipline.
  - **Axes 2/3 는 uninvestigated**: 디자인 시스템 / AI agent skills 의 verify 단계에서 kill 됨
    (1차 통합은 Marpit 패턴만으로 가능). 4 open question 식별.
  - 결과 보관: `/private/tmp/.../wxo7ehm8l.output` (2588 lines, 5 phase 로그 + 23 source 목록 +
    7 confirmed findings + 10 refuted + 4 open questions).
- TASK-F Marpit 통합 (본 세션, done) — 4건 신규 + 2건 lint 정합:
  - 1순위 액션: `references/marpit-directives.md` 신설 — 3-scope directive (global / local / spot)
    와의 매핑 표 + canonical metadata comment 규약 + 사용 예시 + anti-patterns. ~160줄, 본문 lint clean.
  - `references/astryx-component-map.md` §2 → §2.1 layer structure + §2.2 metadata convention
    (NEW) + §2.3 section scoping (NEW, hand-written 재현 명시). §6 끝에 marpit-directives.md
    참조 1줄.
  - `SKILL.md` §Procedure Phase 1 step 6 끝에 metadata comment 규약 1 paragraph, §References 에
    marpit-directives.md 항목 추가, verify_deck.py 의 `--strict` 옵션도 §References 에 노출.
  - `scripts/verify_deck.py` 에 `--strict` 옵션 추가 (gate 1 에서 metadata comment 부재 시 WARN,
    FAIL 아님 — marpit-directives.md §4 의 canonical list 와 연동).
  - lint 정합: CHANGELOG 두 번째 `### Changed` → `### Infra` 분리 (MD024 해소), SKILL.md §Procedure
    Phase 2/3/4 의 step 번호 7~13 → 각 Phase 별 1~N 으로 renumber (MD029 해소).
- wiki/index.md 신규 (본 세션, done) — CLAUDE.md 의 "다음에 읽을 문서" 에 명시되어 있으나
  부재하던 R4 anchor 기반 wiki. §1~§6 (overview / state / active-ops / catalog / slash / how-to).
  운영 도구 + 레퍼런스 link 통합.
- Axes 2/3 후속 deep-research (본 세션, done) — 13 confirmed → 8 findings 으로 합성. 디자인 시스템:
  Open Props (deck 보강 후보, 4.0 kB core) + Panda CSS `@layer tokens` (cascade 통합) 추천,
  W3C DTCG preview (do-not-implement 경고, 2026-07-10) → Style Dictionary bridge 필요.
  USWDS rule out. AI agent skills: agentskills.io = canonical cross-vendor (40+ 제품);
  우리 SKILL.md catalog 표준 정합이나 확장 필드는 Claude-Code-flavored → portable 제한.
  1차 4 open question 중 3개 해소, 1개는 *정책 결정* (standard-strict vs. Claude-flavored).

## Next Actions

- [x] TASK-F commit (`abf0fcf`) + wiki/index.md 신규 작성 + wiki commit (`4b98c38`) + Axes 2/3 후속 deep-research + 운영 문서 동기화
- [ ] push — 사용자 confirm 대기 (GitHub 원격 추가 / `git push -u origin main`)
- [ ] 다음 세션 (선택 항목):
  - **A. Open Props / Panda CSS @layer tokens 의 deck 보강** (2차 deep-research 의 1순위 디자인 시스템 후보) — verify_deck.py 의 gate 확장 / ASTRYX layer 와의 통합 검토
  - **B. agentskills.io strict vs. Claude-Code extension 정책 결정** (2차 deep-research 의 잔여 정책) — SKILL.md 의 확장 필드 표준화 vs. harness 친화 유지
  - **C. Marpit §3 hand-written 발현 검증** — `/* @theme: */` + `data-spot` 패턴 실제 deck 빌더 테스트
  - **D. 신규 task** — 도메인 스킬 1~2개 / harness 어댑터 / 운영 도구 추가 보강

## Risks & Blockers

- **운영 자동화 1차 실전 검증 통과 (해소)**: GitHub Actions run `29022844646` (3 step clean) +
  `29023288041` (재현성 확인) + `29023548610` (Node 20 deprecation 해소 후).
- **Python 3.10+ 의존**: `scripts/skill-lint` / `scripts/skill-discover` 는 GitHub Actions `3.12`,
  로컬 사용자에게 Python 3.10+ 요구. README 에 명시.
- **YAML mini-parser 중복**: skill-lint 와 skill-discover 가 *동일한 1-depth mini-parser* 를
  inline 으로 가짐. 향후 `scripts/_frontmatter.py` 모듈로 추출 리팩터링 별도 task.
- **`.markdownlint.jsonc` 의 globs 미사용**: 호출 globs 는 GitHub Actions / pre-push 에서 명시.
- **harness 어댑터 정책**: Claude Code 외 harness 호환은 별도 task 분리 권장.
- **deep-research 의 Axes 2/3 uninvestigated**: 디자인 시스템 + AI agent skills 의 verify 단계에서
  kill 됨. Marpit 1순위 권고는 Axis 1 의 15 confirmed claims 기반. Axes 2/3 별도 후속 가능.
- **Marpit section-ancestor scoping 의 hand-written 재현은 inference**: Marpit *output* 에서는
  확인됐지만, hand-written single .html 에서 `:where([data-slide-root])` prefix 로 재현하는 것은
  TASK-F 에서 *테스트 필요*.
- **W3C DTCG preview (2026-07-10 do-not-implement)**: 2차 deep-research 의 디자인 시스템 보강
  후보 중 DTCG 직접 도입은 *미루고* Style Dictionary bridge 를 통해 간접 활용. DTCG 가 stable
  되면 native import 검토.
- **agentskills.io strict vs. Claude-Code extension 정책 결정 미완료**: 2차 deep-research 의
  잔여 정책. 1차 4 open question 중 1개. 다음 세션 결정 사항 (handoff Next Actions §B 참조).
- **Marpit scope label 의 hand-written 활용성**: `<!-- @scope: ... -->` 라벨은 *문서화* 목적.
  실제 build-step 없는 deck 에서는 metadata-comment grep 외 활용 없음. 향후 도구 추가 시
  활용 가능.
