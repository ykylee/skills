<!-- standard-ai-workflow-kit: v0.13.3-beta -->

# Purpose

- 문서 목적: 프로젝트의 directional intent, scope, non-scope, 운영 원칙을 단일 출처로 정의해
  모든 작업의 in-scope 판정과 우선순위 합의의 기준으로 사용한다.
- 범위: 본 프로젝트가 지향하는 방향, 포함 영역, 제외 영역, 운영 원칙
- 대상 독자: AI 에이전트, 저장소 관리자, 기여자
- 상태: draft
- 최종 수정일: 2026-07-09
- 관련 문서: [CLAUDE.md](../../CLAUDE.md), [PROJECT_PROFILE.md](./PROJECT_PROFILE.md)

## 1. Directional Intent (1-line)

> 저장소 `skills` 는 사용자가 여러 AI 하네스(Claude Code 외 포함)에서 재사용할
> **범용 AI 워크플로우 스킬**을 모아두고 배포하기 위한 카탈로그다.

## 2. Scope (In-Scope)

- 일상 워크플로우에서 반복해서 사용하는 범용 스킬의 재사용 가능한 정의
- Claude Code 외 다른 harness 에서도 호출 가능한 *중립적 manifest + 본문* 구조의 스킬
- 각 스킬의 사용 시점, 입출력, 트레이드오프를 적은 short 문서
- 카탈로그 운영을 위한 가벼운 검증 절차 (manifest 정합성, 링크 무결성)
- harness 차이를 흡수하기 위한 얇은 어댑터 가이드 (필요 시)

## 3. Non-Scope (Excluded)

- 특정 harness 전용 syntax/API 에 *본질적으로 종속된* 스킬 (그 harness 가 아니면 호출 불가한 경우)
- 외부 서비스/API 키, 시크릿, 개인 식별 정보
- 실행 가능한 애플리케이션 코드, 빌드 결과물, 바이너리, 캐시
  - **예외**: `scripts/` 하위의 *운영 도구* (예: `scripts/skill-lint` — 카탈로그 운영에 필요한
    Python 검증 스크립트) 는 non-scope 에서 제외한다. 이는 harness 가 호출하는 *스킬* 이 아니라
    카탈로그 운영자(또는 CI)가 저장소 lint 에 사용하는 *도구* 다. 자세한 분류 기준은
    [PROJECT_PROFILE.md §3](./PROJECT_PROFILE.md) 참조.
- 프로젝트 본질과 무관한 학습 노트, 외부 글 발췌, 임시 스크랩
- 상업용 배포 / 라이선스 관리 자동화 (필요 시 별도 task 로 분리)

## 4. Operational Principle

- 스킬은 *단일 책임* 으로 작게 유지하고, 조합은 호출자(워크플로우 또는 사용자)가 담당한다.
- manifest 의 `name` / `description` 으로 *사용 시점* 을 자기-기술하고, 가능한 한 trigger phrase 를 포함한다.
- 스킬 본문은 *어떤 harness 에서도 동작 가능한 중립어* 로 작성하고, harness 고유 syntax 는 어댑터로 분리한다.
- 변경 시 본 문서(scope)와 PROFILE 의 영향 문서를 함께 갱신해드리프트(drift)를 차단한다.
- 한 세션 = 한 명제: 한 세션에서 너무 많은 결정을 동시에 확정하지 않는다.
- placeholder(TODO) 는 1세션 안에 실값 또는 명시적 N/A 로 교체한다.

## 다음에 읽을 문서
- [CLAUDE.md](../../CLAUDE.md) — 진입 규칙
- [PROJECT_PROFILE.md](./PROJECT_PROFILE.md) — 프로젝트 메타 및 명령
- [세션 인계](./session_handoff.md) — 현재 세션 상태
- [작업 백로그](./work_backlog.md) — 오늘자 작업 목록