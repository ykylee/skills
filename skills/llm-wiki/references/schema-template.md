# `<Wiki Name>` — Schema

> 운영 계약. 사용자 + LLM 이 공동으로 진화시키는 단일 진실 출처 (source of truth).
> 본 문서 자체가 wiki 의 일부이며 lint 대상.

- 최종 수정일: YYYY-MM-DD
- 언어: <한글 | 영문 | 혼용>
- 사용자: <solo | 팀 | 공개>

## 1. Purpose

- **도메인**: <이 wiki 가 다루는 주제. 예: "AI 모델(provider, capability, 가격) 추적">
- **사용자**: <solo / 팀 / 공개>
- **핵심 사용 시나리오**: <예: "신모델 출시 시 빠른 카드 추가 + capability 비교">

## 2. 디렉터리 구조

```
<위치>/
├── raw/                  # 불변 원천 (사용자 추가, LLM read-only)
│   └── <파일>.md
├── wiki/
│   ├── index.md          # 콘텐츠 카탈로그 (페이지 + 링크 + 1줄 요약)
│   ├── log.md            # 시간순 변경 기록 (append-only)
│   └── <pages>.md        # LLM 유지 페이지
└── SCHEMA.md             # 본 문서 — 운영 계약
```

규칙:

- `raw/` 안의 파일은 *불변*. LLM 이 수정하지 않는다.
- `wiki/` 안의 파일은 *LLM 전담*. 사용자도 직접 수정 가능하나 그 경우 log 에 기록.
- `SCHEMA.md` 는 사용자 + LLM *공동* 진화. 변경 시 lint 가 §5 변경 사항 검증.

## 3. Page Types

| 타입 | 파일명 규칙 | 용도 | 예시 |
|---|---|---|---|
| `entity-*` | `entity-<slug>.md` | 고유 명사 (모델, 시스템, 사람) | `entity-claude-opus-4-8.md` |
| `concept-*` | `concept-<slug>.md` | 정의 가능한 개념, 용어 | `concept-foundation-models.md` |
| `comparison-*` | `comparison-<topic>.md` | 다중 entity 비교 | `comparison-frontier-2026.md` |
| `synthesis-*` | `synthesis-<topic>.md` | 다중 raw 종합, 의사결정 가이드 | `synthesis-model-selection.md` |

> 도메인에 따라 page type 추가 가능. 예: AI 모델 wiki 는 `release-note-*` 추가.
> page type 을 추가하면 `wiki/index.md` 에도 대응하는 절을 추가한다.

## 4. Frontmatter 규약

```yaml
---
title: <사람이 읽는 이름>
type: entity | concept | comparison | synthesis
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - raw/<파일명>
  - <URL>
aliases: [<이름1>, <이름2>]
tags: [<tag1>, <tag2>]   # 선택
---
```

도메인별 추가 키 (예: AI 모델 wiki):

```yaml
provider: anthropic | openai | google | meta | mistral | ...
context_window: <tokens>
modalities: [text, vision, audio, ...]
deprecated: <YYYY-MM-DD | null>
replaced_by: <entity-<slug>> | null
```

## 5. Cross-reference 규약

- **다른 wiki 페이지 참조**: `[[wiki/<page>]]` 형식. 마크다운 link 도 허용 `[name](../<page>)`.
- **원천 인용**: `> source: raw/<file> §<section>` 형식 blockquote 또는 본문 끝 출처 섹션.
- **모순 표시**: 본문에 마커 후 log 기록:
  ```
  ⚠ CONTRADICTION with [[wiki/<other-page>]] — ingested from raw/<file>
  ```
- **양방향 link**: 새 entity 페이지는 관련 페이지에 *역방향* link 추가 (orphan 방지).

## 6. Operations (운영 절차)

본 wiki 의 Ingest / Query / Lint 절차는 *상위* `llm-wiki` 스킬의 SKILL.md 가
source of truth. 본 문서는 wiki-인스턴스-특유의 *추가 규칙만* 다룬다.

wiki-인스턴스 추가 규칙:

- **Ingest 트리거**: <예: "raw/ 에 파일 떨어뜨린 직후 + '이 자료 wiki 에 추가' 명령">
- **Lint 트리거**: <예: "주 1회 일요일, 또는 매 10회 ingest 후">
- **Deprecated 정책**: <예: "모델이 deprecated 로 발표되면 7일 내 entity 페이지에 마킹">

## 7. Lint 규칙 (wiki-인스턴스 튜닝)

`llm-wiki` 스킬의 lint 절차를 *추가로* wiki-인스턴스-특유 규칙으로 좁힌다:

- **stale 임계**: <30일 | 사용자 조정값>
- **coverage 목표**: <0.8 | 사용자 조정값>
- **허용 page type**: §3 의 type 만. 신규 type 은 SCHEMA 변경 후 도입.

## 다음에 읽을 문서

> 아래 경로는 *복사된 위치 기준* 이다. 본 템플릿 파일 위치에서는 존재하지 않으므로
> markdown 링크로 쓰지 않는다 (복사 후 링크가 깨지는 것을 막기 위함).

- `./wiki/index.md` — 전체 페이지 카탈로그
- `./wiki/log.md` — 최근 ingest / lint 흐름
- 상위 메타 스킬 `llm-wiki` 의 `SKILL.md` — 절차의 source of truth.
  카탈로그 내 경로는 `skills/llm-wiki/SKILL.md`
