<!-- standard-ai-workflow-kit: v0.13.3-beta -->

# Project Workflow Profile

- 문서 목적: 프로젝트 특화 규칙과 운영/검증 기준을 정의한다.
- 범위: 프로젝트 개요, 문서 구조, 카탈로그 운영 명령, 검증 포인트, 예외 규칙
- 대상 독자: 저장소 관리자, AI agent, 온보딩 담당자
- 상태: draft
- 최종 수정일: 2026-07-09
- 관련 문서: [PURPOSE.md](./PURPOSE.md), [공통 표준](../../core/global_workflow_standard.md)

## 1. 프로젝트 개요
- 프로젝트명: `skills` (저장소명 = 디렉터리명)
- 한 줄 정의: 사용자가 여러 AI 하네스(Claude Code 외 포함)에서 재사용할
  *범용 AI 워크플로우 스킬* 을 모아두고 배포하는 카탈로그. ([PURPOSE.md §1](./PURPOSE.md))
- 프로젝트 목적:
  - 일상적으로 반복되는 AI 워크플로우를 *재사용 가능한 단위* 로 묶어 자산화
  - harness 종속을 최소화해 동일 스킬을 여러 도구에서 호출 가능하게 함
  - 스킬 단위로 *short 문서 + manifest* 를 유지해 검색·조합·드리프트 감지를 쉽게 함
- 주요 이해관계자:
  - Owner: 사용자 본인 (single-owner)
  - 1차 사용자: 사용자 본인
  - AI 에이전트: 본 저장소를 *읽고* 스킬을 호출/실행함 (편집 권한은 owner 만)

## 2. 문서 구조 (Path)
- 문서 위키 홈: `README.md`
- 운영 문서 홈: `ai-workflow/memory/active/`
  - `state.json` — 빠른 상태 요약
  - `session_handoff.md` — 세션 인계
  - `work_backlog.md` — 백로그 인덱스
  - `backlog/YYYY-MM-DD.md` — 날짜별 백로그
  - `PROJECT_PROFILE.md` — 본 문서
  - `PURPOSE.md` — directional intent + scope
- 스킬 카탈로그 위치: `skills/` (TASK-001e 에서 골격 확정)
- 환경 기록 위치: `ai-workflow/memory/active/project_status_assessment.md`

## 3. 기본 명령 (Commands)
이 저장소는 *실행 가능한 애플리케이션 코드를 포함하지 않으므로* install / run / quick test /
isolated test / smoke check 모두 **N/A** 다. 대신 카탈로그 운영을 위한 보조 명령을 정의한다.

- **markdown lint**: 저장소 내 모든 `.md` 의 lint. 권장 도구: [`markdownlint-cli2`](https://github.com/DavidAnson/markdownlint-cli2).
  카탈로그 특유 규칙은 `.markdownlint.jsonc` 에 정의. 호출:
  ```bash
  markdownlint-cli2 "skills/**/*.md" "README.md" "CHANGELOG.md"
  ```
- **skill manifest validate**: `skills/**/SKILL.md` 의 frontmatter(name / description / metadata) +
  내부 링크 정합성 검사. 도구: `scripts/skill-lint` (Python 3 stdlib-only). 호출:
  ```bash
  python3 scripts/skill-lint --path skills          # 일반
  python3 scripts/skill-lint --path skills --strict  # W 코드도 에러
  python3 scripts/skill-lint --path skills --json    # 기계 판독
  ```
  절차 원형은 `skills/skill-lint/SKILL.md` §Procedure (3~9 단계). 자동화: GitHub Actions
  (`.github/workflows/skill-lint.yml`) + pre-push hook (`.githooks/pre-push`).
- **link check**: 문서 간 상대/절대 링크 무결성 검사. 권장 도구: [`lychee`](https://github.com/lycheeverse/lychee) (`--offline`).
  호출: `lychee --offline "skills/**/*.md" "README.md" "CHANGELOG.md"`.
- **changelog 갱신**: 새 스킬 추가/변경 시 `CHANGELOG.md` 의 `## [Unreleased]` 섹션에 항목 추가.
- **release tag**: 범용 카탈로그 버전을 의미 있을 때 부여. 버전은 semver.

> 권장 도구(`markdownlint-cli2`, `lychee`) 자체는 *본 카탈로그 범위 밖*. 운영자가
> 저장소 운영 시 별도 설치. 본 카탈로그는 *도구 호출 절차* 만 정의한다.

## 4. 검증 포인트 (Validation)
- 문서 변경:
  - frontmatter 의 `description` 은 1-line 으로 유지하고, 가능하면 trigger phrase 포함
  - 모든 상대 링크는 commit 전 `link check` 로 무결성 확인
  - PURPOSE.md 의 scope 변경이 아닌 이상, 본문/예시 추가는 *free-form* (lint 만 통과하면 OK)
- 스킬 변경:
  - `SKILL.md` frontmatter의 `name` / `description` 변경 시 manifest validate 필수
  - 새 harness 추가 시 `metadata.harness_compat` 갱신
- 카탈로그 운영:
  - 추가/삭제/이름변경은 `CHANGELOG.md` 와 `backlog/<date>.md` 에 동시 기록
  - 한 PR = 한 명제 (스킬 1개 또는 운영 정책 1건)
- 배포/릴리즈:
  - owner 만이 tag/release 를 발행할 수 있음 (single-owner 정책)
  - breaking change(manifest schema, scope 변경) 는 `CHANGELOG.md` 의 `### Breaking` 섹션에 명시

## 5. 예외 규칙 (Policy)
- 병합: 상태 문서(state.json / handoff / backlog) 충돌 시 *최신 갱신 일시* 가 우선.
  단, `generated_at` 이 동일하면 *PURPOSE.md 의 directional intent* 가 모든 판단의 최종 근거.
- 승인: 모든 변경은 *owner 승인* 이 필요하다 (single-owner). AI agent 는 *제안까지만*.
- 제약:
  - 본 저장소에 *시크릿, API 키, 개인 식별 정보* 를 커밋하지 않는다.
  - 외부 라이브러리/툴 도입 시 PURPOSE 의 non-scope 와의 정합을 먼저 확인한다.
- 컨벤션:
  - 한 세션 = 한 명제. 한 세션에서 *3개 이상의 신규 결정을 동시에 확정* 하지 않는다.
  - placeholder(TODO) 는 1세션 안에 실값 또는 명시적 N/A 로 교체한다.

## 다음에 읽을 문서
- [PURPOSE.md](./PURPOSE.md) — directional intent / scope / non-scope
- [세션 인계 문서](./session_handoff.md)
- [작업 백로그](./work_backlog.md)
- [CLAUDE.md](../../CLAUDE.md) — 진입 규칙
