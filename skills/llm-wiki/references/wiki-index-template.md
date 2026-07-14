# `<Wiki Name>` — Index

> 콘텐츠 카탈로그. 모든 ingest 후 갱신. LLM 이 유지.
>
> - **읽는 법**: 카테고리 섹션 → 1줄 요약 → 페이지 링크. 본문은 각 페이지.
> - **갱신 주기**: 매 ingest 직후 (그리고 lint 시).
> - **커버리지**: `raw/` 대비 wiki citation 비율로 측정 (lint 단계).

- **마지막 갱신**: YYYY-MM-DD
- **총 페이지 수**: `<N>`
- **총 raw 원천**: `<N>`
- **coverage**: <0.X>

## Entities

> 고유 명사 (모델, 시스템, 사람). 한 줄 = *링크 + 한 줄 정의*.

- entity-`<slug>` (page: ./wiki/entity-`<slug>`.md) — <한 줄 정의>
- entity-`<slug>` (page: ./wiki/entity-`<slug>`.md) — <한 줄 정의>

## Concepts

> 정의 가능한 개념, 용어.

- concept-`<slug>` (page: ./wiki/concept-`<slug>`.md) — <한 줄 정의>

## Comparisons

> 다중 entity 비교.

- comparison-`<topic>` (page: ./wiki/comparison-`<topic>`.md) — <비교 주제 한 줄>

## Syntheses

> 다중 raw 종합, 의사결정 가이드.

- synthesis-`<topic>` (page: ./wiki/synthesis-`<topic>`.md) — <가이드 주제 한 줄>

## Recent Ingest

> 최근 5건만 표시 (전체는 wiki/log.md).

- YYYY-MM-DD: raw/`<file>` → `<N>` new pages, `<N>` updated, `<N>` contradictions
- YYYY-MM-DD: raw/`<file>` → `<N>` new pages, `<N>` updated
- YYYY-MM-DD: raw/`<file>` → `<N>` updated only

## Open Contradictions

> ⚠ 마커가 7일 이상 미해결된 contradiction 만 표시. lint 결과에서 가져옴.

- ⚠ entity-A (page: ./wiki/entity-A.md) vs entity-B (page: ./wiki/entity-B.md) — ingested YYYY-MM-DD

## Tags Index

> 자주 쓰이는 tag 별 페이지 모음 (선택).

- `#frontier`: entity-A (page: ./wiki/entity-A.md), entity-B (page: ./wiki/entity-B.md)
- `#deprecated`: entity-C (page: ./wiki/entity-C.md)
