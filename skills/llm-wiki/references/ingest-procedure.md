# Ingest Procedure

`SKILL.md §Procedure.B` 의 상세 절차 + 모범 사례.

## 1. 선독 (Read-First)

원천 정독 *전에* 다음을 먼저 읽어 컨텍스트를 잡는다:

| 파일 | 읽기 범위 | 목적 |
|---|---|---|
| `SCHEMA.md` | 전체 | page type, frontmatter 규약, cross-link 형식 |
| `wiki/index.md` | 1줄 단위 빠르게 | 기존 entity 슬러그, 카테고리 분류 파악 |
| `wiki/log.md` | `grep "^## \[" log.md \| tail -5` | 최근 5건 ingest 흐름 — 모순 맥락 |

> 전체 wiki 를 정독하지 않는다. index 가 검색의 1차 인덱스.

## 2. 원천 식별

사용자가 추가한 원천을 식별한다:

- `raw/<파일명>` — 디렉터리 스캔으로 발견
- URL — `WebFetch` 로 본문 확보 후 `raw/<slug>.md` 로 저장
- 다중 파일 (논문 + 슬라이드) — 각각 ingest 단위로 취급

**권장**: 외부 자료는 ingest 직전 `raw/` 에 *한 번 저장*해 *재현 가능성* 확보.

## 3. chunked 읽기

LLM 컨텍스트 한도 내에서 chunked 로 읽는다:

1. **전체 구조**: headings / TOC 파악
2. **핵심 청크**: entity 정의, 비교표, 수치, 인용
3. **context 청크**: 필요한 부분만 추가 정독

> 카파시 권장 — 이미지 / 표는 텍스트로 환원 가능하면 마크다운으로, 아니면
> 별도 ingest 노트.

## 4. entity/concept 추출

원천에서 candidate 를 식별:

| page type | 추출 기준 |
|---|---|
| `entity-*` | 고유 명사 (모델, 사람, 시스템, 제품) |
| `concept-*` | 정의 가능한 개념 (용어, 방법론, 패턴) |
| `comparison-*` | 다중 entity 비교 (프론티어 모델 비교, provider 비교) |
| `synthesis-*` | 다중 원천 종합 (전략, 의사결정 가이드) |

> SCHEMA.md §3 의 page type 정의가 우선. 거기서 정의 안 한 type 은 만들지 않음.

## 5. 페이지 갱신 / 생성

### 기존 페이지 갱신

- 해당 섹션만 *in-place* 갱신, 무관 부분 보존
- `updated` 메타를 오늘 날짜로
- 새 정보 출처를 본문 끝 또는 frontmatter `sources` 에 추가
- 변경 범위가 큰 경우 (50%+) 사용자 확인 권장

### 신규 페이지 생성

frontmatter 필수:

```yaml
---
title: <사람이 읽는 이름>
type: entity | concept | comparison | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/<file>
aliases: [<이름1>, <이름2>]
tags: [<tag1>, <tag2>]   # 선택
---
```

본문:
- 첫 단락 = 1-line 정의
- 단락 구분 = SCHEMA 의 page type 별 표준 구조 따르기
- 끝 = `## 출처` 또는 `## Sources` 섹션에 raw/ 파일 인용

## 6. cross-reference 보강

- 새 entity 페이지 → 기존 비교/개념 페이지에서 *역방향 링크* 추가
- `[[wiki/<page>]]` 형식 (vault tool 인지) + 상대 경로 (`../entity-x/`) 둘 다 허용
- orphan 페이지 (들어오는 link 0) 만들지 말 것 — 최소 1개 outgoing link 보장

## 7. index 갱신

`wiki/index.md` 갱신:

- 새 페이지 = 페이지 type 섹션에 1줄 (링크 + 한 줄 요약)
- 갱신 페이지 = 요약 1줄에서 *변경* 표시 예: `~~이전 요약~~` + 새 요약
- 삭제 페이지 = 단순 제거 (log 에는 유지)

> index 는 매 ingest 후 갱신. *stale index = silent failure*.

## 8. log 갱신

`wiki/log.md` 에 append (한 줄 형식 표준):

```markdown
## [YYYY-MM-DD HH:MM] ingest: <파일명 또는 URL>
- source: raw/<파일명> 또는 <URL>
- new pages: [<page1>, <page2>]
- updated pages: [<page3>, ...]
- contradictions flagged: [<page4> ⚠ with <page5>]
- duration: <분>
- ingest scope: <domain> | focus: <tag>
```

append-only. *수정/삭제 금지*.

## 9. 모순 플래그

기존 페이지 주장과 충돌 시:

1. 신규 정보 페이지 (또는 신규 모순 섹션)에 마커:
   ```
   ⚠ CONTRADICTION with [[wiki/<other-page>]] — ingested from raw/<file>, <brief reason>
   ```
2. 반대쪽 페이지에도 같은 마커 (또는 종결 결정) 추가.
3. log 에 `contradictions flagged` 항목으로 기록.
4. **해결은 사용자가 결정** — LLM 은 *flag 까지만*, 자동 해결 금지.

## 10. 자주 하는 실수

| 실수 | 결과 | 회피 |
|---|---|---|
| 원천 전체를 한 entity 페이지에 복사 | entity 페이지 > 원천 → 음가치 | *요약 + 인용*, 복사 X |
| index 갱신 누락 | 다음 query 시 stale 페이지 참조 | 매 ingest 후 즉시 |
| log 형식 표준 안 지킴 | grep `^## \[` 실패 | 표준 형식 강제 |
| 모순을 자동 해결 | 사용자 의도 무시 | flag 만, 결정은 사용자 |
| cross-link를 무시 | orphan / 고립 페이지 | entity 페이지마다 outgoing link ≥ 1 |
| `updated` 메타 미갱신 | lint 가 false-positive stale 경고 | 매 ingest 후 즉시 |
