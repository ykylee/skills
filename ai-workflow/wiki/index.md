<!-- standard-ai-workflow-kit: v0.13.3-beta -->

# Project Wiki Index

- 문서 목적: AI 에이전트가 *세션 복원 시점에 가장 먼저 로드* 하는 warp-point.
  저장소의 모든 운영 문서 / 카탈로그 / 메타 스킬 / 외부 레퍼런스를 단일 페이지에서
  안내한다.
- 범위: 링크 인덱스. 본문은 각 문서가 가진다.
- 대상 독자: Claude Code, 신규 AI 에이전트, 저장소 온보딩 담당자.
- 상태: active
- 최종 수정일: 2026-07-10
- 관련 문서: [CLAUDE.md](../../CLAUDE.md), [state.json](../memory/active/state.json)

## §1 Project Overview

<a id="anchor-overview"></a>

- [Purpose](../memory/active/PURPOSE.md) — directional intent 1-line + scope / non-scope
- [Project Profile](../memory/active/PROJECT_PROFILE.md) — 운영 규칙 / 검증 포인트 / 예외 규칙
- [README.md](../../README.md) — 저장소 루트 안내 (디렉터리 트리 / 빠른 시작 / lint)

## §2 State (현재 세션 상태)

<a id="anchor-state"></a>

- [state.json](../memory/active/state.json) — 머신 판독 가능한 상태 요약 (schema_version 1)
- [Session Handoff](../memory/active/session_handoff.md) — 다음 세션을 위한 인계
- [Work Backlog](../memory/active/work_backlog.md) — 백로그 인덱스 (날짜별 백로그 link)

## §3 Active Operations

<a id="anchor-active-ops"></a>

- [Latest Backlog (2026-07-10)](../memory/active/backlog/2026-07-10.md) — 당일 작업 상세
- [Project Status Assessment](../memory/active/project_status_assessment.md) — 환경 점검 결과

### 운영 도구

<a id="anchor-tools"></a>

- [scripts/skill-lint](../../scripts/skill-lint) — frontmatter / harness_compat / 내부 링크 검증 (Python 3 stdlib-only)
- [scripts/skill-discover](../../scripts/skill-discover) — SKILL.md 인덱싱 + 검색 (Python 3 stdlib-only)
- [.markdownlint.jsonc](../../.markdownlint.jsonc) — markdownlint-cli2 rule 정의
- [.github/workflows/skill-lint.yml](../../.github/workflows/skill-lint.yml) — GitHub Actions CI
- [.githooks/pre-push](../../.githooks/pre-push) — 로컬 pre-push hook (선택)

### 표준 문서

<a id="anchor-core"></a>

- [core/global_workflow_standard.md](../core/global_workflow_standard.md) — 표준 AI 워크플로우 8개 원칙
- [core/workflow_adoption_entrypoints.md](../core/workflow_adoption_entrypoints.md) — 세션 진입 옵션
- [core/workflow_skill_catalog.md](../core/workflow_skill_catalog.md) — 카탈로그 표준

## §4 Skill Catalog

<a id="anchor-skill-catalog"></a>

- [skills/README.md](../../skills/README.md) — 카탈로그 authoring 가이드

### 도메인 스킬

<a id="anchor-domain-skills"></a>

- [html-slides-builder/SKILL.md](../../skills/html-slides-builder/SKILL.md) — 단일 1920x1080 HTML 슬라이드 빌더
- [html-slides-builder/references/presentation-patterns.md](../../skills/html-slides-builder/references/presentation-patterns.md) — 6종 content-type spine + SCQA / Pyramid / Chart Chooser
- [html-slides-builder/references/astryx-component-map.md](../../skills/html-slides-builder/references/astryx-component-map.md) — ASTRYX 디자인 시스템 3-layer CSS cascade
- [html-slides-builder/references/marpit-directives.md](../../skills/html-slides-builder/references/marpit-directives.md) — Marpit 3-scope directive + metadata comment 규약
- [html-slides-builder/scripts/verify_deck.py](../../skills/html-slides-builder/scripts/verify_deck.py) — Phase gate headless verifier

### 메타 스킬

<a id="anchor-meta-skills"></a>

- [skill-lint/SKILL.md](../../skills/skill-lint/SKILL.md) — manifest 검증 스킬 절차 원형
- [skill-discover/SKILL.md](../../skills/skill-discover/SKILL.md) — 카탈로그 검색 스킬 절차 원형

## §5 In-Session Slash Commands

<a id="anchor-slash-commands"></a>

본 카탈로그에 등록된 진입 slash command 들:

- `/workflow-session-start` — baseline 복원 (state.json + handoff + backlog)
- `/workflow-backlog-update` — task 등록/갱신 + scope creep 경고
- `/workflow-doc-sync` — 영향 문서 동기화 (advisory)

## §6 How to read this wiki

<a id="anchor-how-to-read"></a>

1. AI 에이전트는 세션 시작 시 *반드시* §2 (state + handoff + backlog) + §3 (active operations) 를
   먼저 읽어 *현재 컨텍스트* 를 복원한다.
2. §1 (overview) 는 신규 에이전트 온보딩용 1회 read; 매 세션 반복 read 는 불필요.
3. §4 (catalog) 는 사용자가 *카탈로그 추가/변경* 시에만 참조.
4. §5 (slash commands) 는 진입점 검색용; 자세한 절차는 각 스킬 SKILL.md 가 source of truth.
