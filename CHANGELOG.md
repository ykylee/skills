# Changelog

- 문서 목적: 카탈로그의 모든 notable 변경을 시간순으로 기록한다.
- 범위: 추가/변경/제거된 스킬, 운영 정책, lint 절차 변경
- 대상 독자: 카탈로그 사용자, AI 에이전트, 기여자
- 상태: active
- 최종 수정일: 2026-07-09
- 관련 문서: [README.md](./skills/README.md), [./ai-workflow/memory/active/PROJECT_PROFILE.md](./ai-workflow/memory/active/PROJECT_PROFILE.md)

본 문서는 [Keep a Changelog](https://keepachangelog.com/ko/) 의 정신을 따른다.
버전은 [Semantic Versioning](https://semver.org/lang/ko/) 을 지향한다.

## [Unreleased]

### Added
- 운영 자동화 1차 실전 검증 통과 (GitHub Actions run `29022844646`): markdownlint-cli2 →
  `python3 scripts/skill-lint` → `lychee --offline` 3-step CI 검증 성공 (23s).
- 운영 자동화 정책 결정: markdownlint 스타일 rule (`MD022` / `MD031` / `MD032` / `MD060`) 비활성화
  — 카탈로그는 *의미 검증* (frontmatter / harness_compat / 링크) 이 핵심.
- 운영 도구 보강: `scripts/skill-discover` Python 3 stdlib-only 구현. `skill-discover/SKILL.md`
  §Procedure 1~7 의 실제 동작. `--index` 캐시 빌드, `category:X` / `harness:X` 토큰, `--json`,
  `--top N`. dry-run 결과: 인덱스 빌드 2 entries, 검색 (meta / category:meta / harness:generic-md) 정상.

### Changed
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
