# `<Wiki Name>` — Index

> 콘텐츠 카탈로그. 모든 ingest 후 갱신. LLM 이 유지.
>
> - **읽는 법**: 카테고리 섹션 → 1줄 요약 → 페이지 링크. 본문은 각 페이지.
> - **갱신 주기**: 매 ingest 직후 (그리고 lint 시).
> - **커버리지**: `raw/` 대비 wiki citation 비율로 측정 (lint 단계).

- **마지막 갱신**: YYYY-MM-DD
- **총 페이지 수**: N
- **총 raw 원천**: N
- **coverage**: 0.X

> **본 템플릿 사용법**: 아래 각 절의 코드 블록은 *행 형식 예시* 다. 실제 index 를 쓸 때는
> 코드 블록 fence 를 지우고 그 안의 형식대로 실제 항목을 채운다. 링크는 **반드시 실제
> markdown 링크**여야 한다 — index 는 Query 절차 (`SKILL.md §Procedure.C` 1단계) 의
> 1차 검색 인덱스이므로, 서술형 텍스트로 두면 페이지 이동이 끊긴다.
>
> 경로 주의: `index.md` 는 `wiki/` **안에** 있으므로 형제 페이지는 `./entity-foo.md` 로
> 참조한다 (`./wiki/entity-foo.md` 아님).

## Entities

> 고유 명사 (모델, 시스템, 사람). 한 줄 = *링크 + 한 줄 정의*.

```markdown
- [entity-foo](./entity-foo.md) — 한 줄 정의
- [entity-bar](./entity-bar.md) — 한 줄 정의
```

## Concepts

> 정의 가능한 개념, 용어.

```markdown
- [concept-foo](./concept-foo.md) — 한 줄 정의
```

## Comparisons

> 다중 entity 비교. (사용하지 않는 page type 의 절은 지워도 된다.)

```markdown
- [comparison-foo](./comparison-foo.md) — 비교 주제 한 줄
```

## Syntheses

> 다중 raw 종합, 의사결정 가이드.

```markdown
- [synthesis-foo](./synthesis-foo.md) — 가이드 주제 한 줄
```

> `SCHEMA.md` §3 에서 page type 을 추가했다면 (예: `policy-*`) 그에 대응하는 절을
> 여기에 같은 형식으로 추가한다.

## Recent Ingest

> 최근 5건만 표시 (전체는 `./log.md`).

```markdown
- YYYY-MM-DD: raw/foo.md → N new pages, N updated, N contradictions
- YYYY-MM-DD: raw/bar.md → N new pages, N updated
- YYYY-MM-DD: raw/baz.md → N updated only
```

## Open Contradictions

> ⚠ 마커가 7일 이상 미해결된 contradiction 만 표시. lint 결과에서 가져옴.

```markdown
- ⚠ [entity-foo](./entity-foo.md) vs [entity-bar](./entity-bar.md) — ingested YYYY-MM-DD
```

## Tags Index

> 자주 쓰이는 tag 별 페이지 모음 (선택). `tags` 키를 안 쓰는 wiki 는 이 절을 지운다.

```markdown
- `#frontier`: [entity-foo](./entity-foo.md), [entity-bar](./entity-bar.md)
- `#deprecated`: [entity-baz](./entity-baz.md)
```
