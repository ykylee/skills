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

## [0.3.0] - 2026-07-09

### Added
- 두 번째 메타 스킬: `skill-discover` (`skills/skill-discover/SKILL.md`) — 카테고리·키워드·harness_compat
  기반 검색 절차 (인덱스 빌드 → 토큰화 → scoring → 정렬 → top-N → 호출 예시 7단계).
  `metadata.harness_compat: [claude-code, generic-md]`, `category: meta`, `version: 0.1.0`.

### Changed
- (없음)

### Breaking
- (없음)

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
