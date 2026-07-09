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
- [ ] TASK-F: Marpit 통합 — `references/marpit-directives.md` 신설, verify_deck.py gate 2/3 directive 검출, 3-layer cascade 의 `/* @theme */` metadata 명문화 (다음 세션, pending)
