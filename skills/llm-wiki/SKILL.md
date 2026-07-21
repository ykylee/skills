---
name: llm-wiki
description: 카파시 LLM Wiki 패턴으로 영구 markdown 위키를 부트스트랩·운영합니다. raw/wiki/schema 3계층과 Ingest/Query/Lint 3연산을 정의. "위키 만들어줘", "이 자료 wiki에 추가", "wiki에서 X 검색", "wiki lint" 요청에 사용.
metadata:
  claude_code:
    when_to_use: '"위키 부트스트랩", "위키에 추가해줘", "위키에서 검색", "wiki lint", "drift 검사"'
    harness_compat:
      - claude-code
      - generic-md
    category: meta
    version: 0.2.0
---

# llm-wiki

Karpathy의 [LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
패턴을 구현하는 **메타 스킬**. 영구 markdown 위키를 사용자 지정 위치에 부트스트랩하고,
세 가지 연산(Ingest / Query / Lint)으로 운영한다.

> **RAG 와의 차이**: 지식을 매 쿼리마다 raw 에서 재유도하지 않고, 한 번 컴파일해
> `wiki/` 에 누적·유지한다. cross-reference, 모순 플래그, synthesis 가 *pre-built* 상태로 남는다.

## When to use

- *"지식 베이스 / wiki 만들어줘"* — 신규 위키 부트스트랩 (Bootstrap 절차 A)
- *"이 자료/논문/문서 wiki 에 추가"* — 원천 ingest (Ingest 절차 B)
- *"X 가 뭐였지?", "wiki 에서 검색"* — 위키 질의 (Query 절차 C)
- *"wiki lint", "drift 검사", "위키 건강검진"* — 주기적 lint (Lint 절차 D)
- 기존 위키를 다른 위치로 옮기거나 SCHEMA.md 를 갱신할 때

> 본 스킬은 *운영자*. 위키 본체는 사용자 디렉터리에 있고, 본 카탈로그에는 영향 없음.

## Inputs

- **Bootstrap**: 사용자 지정 위치 (절대/상관 경로). wiki 도메인 (예: `AI 모델`,
  `워크플로우 규칙`, `개인 학습 노트`).
- **Ingest**: `raw/` 에 추가된 파일 또는 URL. (선택) focus — 이 주제와 관련된 페이지만 갱신.
- **Query**: 자유 텍스트 질문. (선택) scope — `index only` / 전체 wiki.
- **Lint**: (선택) `--strict` — 경고도 보고. (선택) `--scope` — 전체 / 특정 카테고리.

## Outputs

- **Bootstrap** (절차 A): 사용자 위치에 다음 생성
  - `SCHEMA.md` — 운영 계약 (사용자 + LLM 공동 진화)
  - `wiki/index.md` — 콘텐츠 카탈로그
  - `wiki/log.md` — 시간순 변경 기록 (append-only)
  - `raw/` 디렉터리 (시작점)
- **Ingest** (절차 B): 갱신된 페이지 목록 + index/log 갱신 + 모순 플래그
- **Query** (절차 C): 출처 인용 포함 답변 + (선택) 새 페이지 file-back 제안
- **Lint** (절차 D): health 보고서 (orphan / stale / contradiction / coverage)

## Procedure

> 모든 세부 절차는 `references/` 디렉터리의 walkthrough 으로 분리. 본 절에서는
> 흐름과 결정 포인트만 다룬다.

### A. Bootstrap (최초 1회)

1. **위치 확인**: 사용자에게 wiki 위치를 묻는다. 부재 시 생성.
2. **도메인 확인**: 무엇에 관한 wiki 인지 (예: `AI 모델 카탈로그`, `워크플로우 규칙`).
   → SCHEMA.md 의 도메인별 섹션과 page type 결정에 사용.
3. **template 복사**: `references/` 의 템플릿을 사용자 위치로 복사:
   - `schema-template.md` → `<위치>/SCHEMA.md`
   - `wiki-index-template.md` → `<위치>/wiki/index.md`
   - `wiki-log-template.md` → `<위치>/wiki/log.md`
4. **raw/ 시작점**: `<위치>/raw/.gitkeep` 생성.
5. **SCHEMA 적응**: 도메인에 맞춰 page type / frontmatter 키 / 모범 사례 섹션 보강.
6. **첫 ingest 안내**: 첫 원천을 `raw/` 에 추가하라고 안내하고 절차 B 로.

전체 walkthrough: [./references/bootstrap-walkthrough.md](./references/bootstrap-walkthrough.md)

### B. Ingest (원천 추가)

1. **SCHEMA 선독**: `<위치>/SCHEMA.md` 와 `<위치>/wiki/index.md` 를 *먼저* 읽어
   기존 페이지 타입 / entity 슬러그 규약 / cross-link 규약을 파악.
2. **원천 정독**: `raw/<파일>` 또는 URL 본문 전체를 chunked 로 읽는다.
3. **entity/concept 추출**: SCHEMA 의 page type 별로 후보 페이지 식별.
4. **페이지 갱신 또는 생성**:
   - 기존 페이지 갱신 시 *해당 섹션만* 갱신, 무관 부분 보존.
   - 신규 생성 시 frontmatter (`created`, `updated`, `sources`, `aliases`) 채움.
5. **cross-reference 보강**: 기존 관련 페이지 *에서* 새 페이지로 들어오는 link 를 최소
   1개 만든다 (orphan 방지). `index.md` 등재는 여기 포함되지 않으며, 기계적 대칭도
   요구하지 않는다.
6. **index 갱신**: `wiki/index.md` 에 새/갱신 페이지 1줄 추가. stale 항목 제거.
7. **log 갱신**: `wiki/log.md` 에 한 줄 형식 표준 entry append.
8. **모순 플래그**: 기존 주장과 충돌 시 페이지 본문에
   `⚠ CONTRADICTION with [[wiki/other-page]]` 마커 + log 기록.

상세 절차 + 모범 사례: [./references/ingest-procedure.md](./references/ingest-procedure.md)

### C. Query (질의 답변)

1. **index lookup 우선**: `wiki/index.md` 만 보고 관련 페이지 1~3개 식별.
   *전체 wiki 를 정독하지 않는다* — index 가 검색의 1차 인덱스.
2. **대상 페이지 정독**: 식별된 페이지만 정독. cross-link 따라 1-hop 추가 정도는 허용.
3. **합성 답변**: 각 주장마다 `(source: raw/<file> §<section>)` 또는
   `[[wiki/<page>]]` 링크로 인용.
4. **file-back 제안**: 답이 향후 재사용 가치가 있으면 *"이 답변을 새 페이지로
   만들까요?"* 라고 묻는다. 사용자 동의 시 절차 B 의 subset 으로 처리.

상세 절차 + 검색 한계: [./references/query-procedure.md](./references/query-procedure.md)

### D. Lint (건강검진)

주기적으로 (예: 매 N 회 ingest 후, 또는 일 1회) 실행. **drift 가 1순위 실패 모드**이므로
lint pass 는 선택이 아닌 정기 의무.

1. **graph 검사**: orphan 페이지 (콘텐츠 페이지 기준, `index.md` link 제외), dead link.
2. **stale 검사**: `updated` 메타가 임계 (기본 30일) 이전인 페이지.
3. **contradiction 검사**: ⚠ 마커 + log 대조.
4. **coverage 검사**: `raw/` 대비 wiki 페이지 coverage 측정.
5. **보고서**: 단일 문서로 합치고 `wiki/log.md` 에 lint 항목 기록.

상세 절차: [./references/lint-procedure.md](./references/lint-procedure.md)

## Trade-offs

- **수동 bootstrap vs 자동화**: 본 MVP 는 사용자 위치/도메인만 묻고 나머지는 *수동* 진행.
  자동화 (`scripts/bootstrap-wiki.py`) 는 향후 task 로 분리.
- **규모 한계**: 카파시 권장 — `index.md` 만으로 ~100 원천 / 수백 페이지까지.
  그 이상은 qmd 같은 hybrid 검색기 필요. 본 스킬은 그 임계 *이전* 을 가정.
- **drift 가 1순위 실패**: lint pass 없는 wiki 는 silently stale. **lint 는 정기 의무**.
- **harness 비종속 약속**: 본 SKILL.md 절차 (A~D) 는 harness 비종속.
  SCHEMA.md 는 wiki 인스턴스마다 다르며 사용자 + LLM 이 공동 진화.
- **위키 인스턴스 vs 카탈로그 격리**: 본 스킬 = 운영자. 위키 데이터는 사용자 디렉터리,
  본 카탈로그에는 영향 없음.
- **버전 0.1.0 한계**: 자동화, qmd 통합, `MEMORY.md` 양방향 링크, lint 자동 fix 는
  모두 out-of-scope (Next version § 참조).

## Next version (제안)

- [ ] `scripts/bootstrap-wiki.py` — 절차 A 의 자동화 (현재는 markdown 절차만)
- [ ] lint 결과 자동 fix 제안 (orphan → link 후보, stale → freshen 후보)
- [ ] `MEMORY.md` 와 wiki page slug 양방향 동기화 옵션
- [ ] qmd / hybrid 검색 통합 가이드
- [ ] 다국어 SCHEMA (한글 / 영문 병기) 패턴

## References

- [Karpathy LLM Wiki gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) — 원본 아이디어 출처
- [./references/bootstrap-walkthrough.md](./references/bootstrap-walkthrough.md) — 절차 A 상세 walkthrough
- [./references/ingest-procedure.md](./references/ingest-procedure.md) — 절차 B 상세 + 모범 사례
- [./references/query-procedure.md](./references/query-procedure.md) — 절차 C 상세 + 검색 한계
- [./references/lint-procedure.md](./references/lint-procedure.md) — 절차 D 상세 + health 보고서 양식
- [./references/schema-template.md](./references/schema-template.md) — `SCHEMA.md` 템플릿 (bootstrap 시 복사)
- [./references/wiki-index-template.md](./references/wiki-index-template.md) — `wiki/index.md` 템플릿
- [./references/wiki-log-template.md](./references/wiki-log-template.md) — `wiki/log.md` 템플릿
- [../README.md §3 SKILL.md 포맷](../README.md) — 본 SKILL.md 가 따른 포맷 정의
