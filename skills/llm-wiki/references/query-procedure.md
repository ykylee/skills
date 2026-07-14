# Query Procedure

`SKILL.md §Procedure.C` 의 상세 절차 + 검색 한계.

## 1. 의도

wiki 사용의 *절반* 이상은 query. RAG 와 달리 wiki 는 *이미 인덱싱된*
cross-reference 그래프를 사용하므로 query 비용이 낮다.

핵심: **index lookup → targeted read → 인용 포함 답변**.

## 2. 절차

### 2.1 index lookup (필수)

질문을 받으면 *가장 먼저* `wiki/index.md` 만 본다 (전체 wiki 정독 ❌).

1. 질문을 wiki 도메인 vocabulary 로 매핑:
   - 키워드 = entity 슬러그, capability 이름, provider 이름 등
2. `index.md` 의 해당 섹션 (e.g. `### Entities`) 에서 매칭 페이지 1~3개 선별
3. 만약 안 보이면:
   - spelling 차이 → `aliases` 메타 또는 SCHEMA 의 별칭 규칙 확인
   - 정말 없으면 → "wiki 에 정보 없음" 명시 후 ingest 권장

### 2.2 targeted read

식별된 페이지만 정독한다. cross-link 따라가는 1-hop 정도는 허용.

- 3개 페이지 넘어 정독 ❌ — 그 시점에서 사용자에게 *focus 재설정* 요청
- 페이지당 *필요 섹션만* — 전체 entity 정독 ❌

### 2.3 합성 답변

답은 다음 형식을 따른다:

```markdown
<1-line 결론>

(상세 답변)

출처:
- [[wiki/<page1>]] §<section> — <인용>
- [[wiki/<page2>]] §<section> — <인용>
- raw/<file> §<line> — <인용>  # raw 직접 인용 시
```

규칙:

- 모든 주장에 *출처* 표기. source-less 주장 ❌
- 모순 발견 시 (lint 가 못 잡은 것) 인용과 함께 명시
- 답변 끝에 "이 정보를 wiki 에 정식 페이지로 만들까요?" 1줄 (file-back 제안)

### 2.4 file-back

사용자가 동의하면 *ingest 의 subset* 으로 처리:

1. 답변을 `wiki/answer-<topic>.md` 임시 페이지로 저장
2. 사용자 검토 후:
   - 영구 가치 있음 → SCHEMA page type 으로 승격, entities/concepts/synthesis 링크
   - 일회성 → 그대로 두거나 삭제

> file-back 은 *옵션*. 일회성 질문은 file-back 없이 답변만으로도 충분.

## 3. 검색 한계와 fallback

| 한계 | 증상 | fallback |
|---|---|---|
| index 가 stale | 관련 페이지를 못 찾음 | `lint` 트리거 권장 |
| cross-link 부족 | 페이지가 고립 | ingest 단계에서 보강 |
| raw/ 만 있고 wiki/ 없음 | "wiki 에 정보 없음" | ingest 권장 |
| 위키 규모 > 임계 (~100 raw, 수백 wiki 페이지) | index lookup 부족 | qmd 같은 hybrid 검색 (별도 task) |
| 다국어 혼용 | 슬러그 검색 실패 | aliases 메타에 다국어 별칭 |

## 4. 모범 사례

- 사용자 질문 ambiguous → *추측 전에* "어떤 측면인지" 1줄 확인
- 인용 형식 위계: `[[wiki/<page>]]` 1순위 → `raw/<file> §<line>` 2순위 → 없음 ❌
- 답변 길이: 짧고 정확하게. detail 은 link 로 escape
- 모순 발견 시 *자동 해결 ❌*, flag + 사용자 결정

## 5. 메트릭

query 비용을 점진 측정:

- 평균 read 페이지 수/질문 (목표 ≤ 3)
- 답변 1건당 평균 인용 수 (목표 ≥ 1)
- "wiki 에 정보 없음" 비율 (목표 ≤ 10%)

위 메트릭이 *안 좋아지면* 보통 index 가 stale 이거나 cross-link 부족 — lint 트리거.
