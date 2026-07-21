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

### 4.1 플레이스홀더 치환 체크리스트

템플릿의 `<...>` 는 **두 종류** 다. 섞어서 다루면 인스턴스 값이 방치되거나 형식 예시가
지워진다. 아래를 먼저 훑고 §4.2 로 간다.

#### (A) 반드시 치환 — 인스턴스 값

| 위치 | 항목 | 비고 |
|---|---|---|
| 제목 | `<Wiki Name>` | `index.md` / `log.md` 제목과 **같은 이름**을 쓴다 |
| 머리말 | 최종 수정일 / 언어 / 사용자 | `YYYY-MM-DD`, 한글·영문·혼용, solo·팀·공개 |
| §1 | 도메인 / 사용자 / 핵심 사용 시나리오 | 도메인 한 줄이 이후 모든 판단의 기준 |
| §2 | `<위치>` | 실제 경로. 트리의 `<파일>` / `<pages>` 는 예시라 그대로 |
| §6 | Ingest 트리거 / Lint 트리거 / Deprecated 정책 | `<예: …>` 를 실제 운영 규칙으로 |
| §7 | stale 임계 / coverage 목표 | 기본 30일 / 0.8. 바꾸려면 여기서 |

#### (B) 그대로 둔다 — 형식 예시

| 위치 | 항목 | 이유 |
|---|---|---|
| §3 | `entity-<slug>.md`, `comparison-<topic>.md` | *파일명 규칙* 자체의 표기 |
| §4 | `<사람이 읽는 이름>`, `<파일명>`, `<이름1>` 등 | frontmatter *키 형식* 설명 |
| §5 | `[[wiki/<page>]]`, `raw/<file> §<section>` | *링크 형식* 설명 |

> 빠뜨리기 쉬운 곳은 **제목·§2·§6·§7** 이다. §1·§3·§4·§5 는 §4.2 에서 자연히 손대게 되지만
> 이 넷은 그렇지 않다.

### 4.2 도메인 적응

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
| 제목 / §2 / §6 / §7 의 플레이스홀더 방치 | `<Wiki Name>` 같은 자리표시자가 그대로 남음 | §4.1 (A) 체크리스트 |
| 형식 예시 (`<slug>` 등) 까지 치환 | 파일명 / frontmatter *규칙* 설명이 사라짐 | §4.1 (B) 는 그대로 |
| SCHEMA 를 너무 상세히 시작 | ingest 시 매번 review 필요 → 비용 ↑ | *수 회 ingest 후* 점진 좁히기 |
| frontmatter 키를 도메인별로 안 나눔 | 모델 / 개념 / 비교 페이지가 동일 schema → 검색 ↓ | §3 Page Types 에서 결정 |
| cross-link 규약을 미정함 | orphan 페이지 누적 | §5 에서 `[[wiki/<page>]]` 형식 합의 |
| raw/ 를 wiki/ 와 분리하지 않음 | LLM 이 raw 를 수정하려 함 | 디렉터리 분리 + lint 단계서 *wiki 만* writable 확인 |
| lint 를 한 번도 안 돌림 | drift 가 silent 누적 | 매 N 회 ingest 후 또는 주 1회 lint |

## 다음 단계

- SCHEMA 가 안정되면 [./ingest-procedure.md](./ingest-procedure.md) 로 첫 ingest.
- 첫 페이지 생긴 후 [./query-procedure.md](./query-procedure.md) 로 query 검증.
- ingest 5~10 회 후 [./lint-procedure.md](./lint-procedure.md) 로 첫 health check.
