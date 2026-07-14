# `<Wiki Name>` — Log

> 시간순 변경 기록. **append-only**.
>
> - 형식: `## [YYYY-MM-DD HH:MM] <operation>: <scope>`
> - 최근 5건 조회: `grep "^## \[" log.md | tail -5`
> - ingest/contradiction 1건당 *반드시* 1 entry.
> - 수정/삭제 금지. 실수 시 *새 entry 로 mark* (예: `[CORRECTION]`).

<!-- 첫 entry 예시 — 실제 사용 시 지우고 시작 -->

<!--
## [2026-07-14 00:00] bootstrap
- source: skills/llm-wiki SKILL.md §Procedure.A
- created: SCHEMA.md, wiki/index.md, wiki/log.md, raw/.gitkeep
- domain: <예: AI 모델 카탈로그>
-->
