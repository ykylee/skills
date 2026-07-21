# Bootstrap Walkthrough

`SKILL.md §Procedure.A` 의 상세 walkthrough. wiki 인스턴스를 사용자 지정 위치에
최초 생성할 때 단계별로 따르기 위한 가이드.

## 0. 사전 확인

Bootstrap 시작 전 다음을 사용자(또는 환경)에서 확인:

- [ ] **위치**: wiki 를 만들 디렉터리 (절대/상관 경로). 디렉터리가 없어도 됨.
- [ ] **도메인**: 이 wiki 가 다룰 주제 (예: `AI 모델 카탈로그`, `워크플로우 규칙`,
      `개인 학습 노트`). SCHEMA.md 의 page type 결정에 사용.
- [ ] **사용자**: solo / 팀 / 공개. 공개일 경우 publish 정책 별도 task.
- [ ] **언어 기본값**: SCHEMA.md / index.md 의 본문 언어 (한글, 영문, 혼용).

## 1. 디렉터리 생성

```bash
# 경로 예시
mkdir -p /path/to/my-wiki/raw
mkdir -p /path/to/my-wiki/wiki
```

> 위치가 git repo 안이면 자동으로 versioned. 아니라면 `git init` 권장
> (wiki = git repo 면 cross-machine 동기화 무료).

## 2. template 복사

본 스킬의 `references/` 에서 다음 3개 템플릿을 사용자 위치로 복사:

```bash
# 스킬 위치에서 실행 (또는 절대 경로 사용)
cp skills/llm-wiki/references/schema-template.md      /path/to/my-wiki/SCHEMA.md
cp skills/llm-wiki/references/wiki-index-template.md  /path/to/my-wiki/wiki/index.md
cp skills/llm-wiki/references/wiki-log-template.md    /path/to/my-wiki/wiki/log.md
```

또는 LLM 에이전트 사용 시:

```
읽기: skills/llm-wiki/references/schema-template.md
쓰기: /path/to/my-wiki/SCHEMA.md
(index / log 템플릿도 동일)
```

## 3. raw/ 시작점

```bash
touch /path/to/my-wiki/raw/.gitkeep
```

## 4. SCHEMA 적응 (사용자 + LLM 공동)

`SCHEMA.md` 의 다음 섹션을 도메인에 맞춰 보강한다:

- **§1 Purpose**: 도메인 한 줄 명시 (예: "AI 모델(provider, capability, 가격 추적)")
- **§3 Page Types**: 위키가 추적할 entity type 결정. 예:
  - AI 모델 위키 → `entity-model`, `concept-capability`, `comparison-frontier`, `synthesis-selection`
  - 워크플로우 위키 → `entity-step`, `concept-principle`, `synthesis-pattern`
- **§4 Frontmatter 키**: 도메인별 추가 키 결정 (예: `model_id`, `provider`,
      `context_window`).
- **§5 Cross-reference 규약**: 도메인별 별칭 규칙 (예: 모델 ID canonical 표기).

> SCHEMA.md 는 lint 대상이다. 너무 엄격하면 ingest 비용 ↑, 너무 느슨하면
> cross-link 깨짐. 사용자 + LLM 이 *수 회* ingest 를 거치며 점진 좁히는 것을 권장.

## 5. 첫 ingest 안내

사용자에게 다음을 안내:

1. 관심 있는 자료 (PDF, web article, tweet, paper 등) 를 `raw/` 에 떨어뜨려라.
2. 떨어뜨린 후 *"이 자료 wiki 에 추가해줘"* 라고 본 스킬을 트리거.
3. 절차 B (`SKILL.md §Procedure.B`) 가 첫 페이지를 만든다.
4. 결과 (갱신 페이지, 모순 플래그, log entry) 을 보고 SCHEMA 의 page type 을 조정하라.

## 6. 자주 하는 실수

| 실수 | 결과 | 회피 |
|---|---|---|
| SCHEMA 를 너무 상세히 시작 | ingest 시 매번 review 필요 → 비용 ↑ | *수 회 ingest 후* 점진 좁히기 |
| frontmatter 키를 도메인별로 안 나눔 | 모델 / 개념 / 비교 페이지가 동일 schema → 검색 ↓ | §3 Page Types 에서 결정 |
| cross-link 규약을 미정함 | orphan 페이지 누적 | §5 에서 `[[wiki/<page>]]` 형식 합의 |
| raw/ 를 wiki/ 와 분리하지 않음 | LLM 이 raw 를 수정하려 함 | 디렉터리 분리 + lint 단계서 *wiki 만* writable 확인 |
| lint 를 한 번도 안 돌림 | drift 가 silent 누적 | 매 N 회 ingest 후 또는 주 1회 lint |

## 다음 단계

- SCHEMA 가 안정되면 [./ingest-procedure.md](./ingest-procedure.md) 로 첫 ingest.
- 첫 페이지 생긴 후 [./query-procedure.md](./query-procedure.md) 로 query 검증.
- ingest 5~10 회 후 [./lint-procedure.md](./lint-procedure.md) 로 첫 health check.
