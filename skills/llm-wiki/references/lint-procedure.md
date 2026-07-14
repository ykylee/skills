# Lint Procedure

`SKILL.md §Procedure.D` 의 상세 절차 + health 보고서 양식.

## 1. 의도

wiki 가 *시간이 지나도* 정확하게 남도록 유지. 카파시 gist 의 명시:

> "The wiki is a persistent, compounding artifact. Drift is the primary failure mode.
> Lint passes are not optional."

lint 는 *선택* 이 아니라 *정기 의무*.

## 2. 권장 주기

- 매 N 회 (default 10) ingest 후 1회
- 또는 사용자 결정으로 주 1회
- 또는 raw/ 에 큰 변화 (10+ 파일 추가) 직후

## 3. 검사 항목

### 3.1 graph 검사

- **orphan 페이지**: 들어오는 link 0. SCHEMA 의 cross-link 규약 위반 가능성 ↑.
- **dead link**: `[[wiki/<X>]]` 인데 `X` 존재 안 함.
- **누락된 역방향 link**: A→B 가 있는데 B→A 가 없음 (대칭성 위배).

검사 방법:

```bash
# 모든 페이지에서 outgoing link 수집 후 매핑 빌드
# 또는 LLM 사용: index.md + 5~10 페이지만 보고 직접 추론
```

### 3.2 stale 검사

- `updated` 메타가 임계 (default 30일) 이전인 페이지.
- 임계 사용자 조정 가능 (SCHEMA.md §7).
- 보고서에 *stale 리스트* 만. **자동 fix 안 함** (사용자가 결정).

### 3.3 contradiction 검사

1. 모든 페이지에서 `⚠ CONTRADICTION` 마커 grep.
2. `log.md` 의 `contradictions flagged` 항목과 대조.
3. *해결 안 된* contradiction = 7일 이상 마커 유지 = highlight.

해결 절차 (사용자 결정):

- 한쪽이 stale → 갱신 쪽 결정
- 두 쪽 모두 유효 → 두 page 모두에 "context-dependent" 섹션 명시
- 일방적 부정 → 마커 제거 + log 기록

### 3.4 coverage 검사

`raw/` 의 *각* 파일이 wiki 의 *어디서* 인용되는지 매핑:

- raw 파일 N 개 → wiki citation 있는 파일 M 개
- coverage = M / N (목표 ≥ 0.8)
- raw 만 있고 citation 0 → *missing entity / concept 가능성*, ingest trigger

### 3.5 schema drift

`SCHEMA.md` 의 page type / frontmatter 키 / 규약이 *실제로* wiki 페이지에서
지켜지는지 spot check.

- 규약 미준수 페이지 1~5개 sampling
- 위반 보고 (예: `entity-*.md` 인데 `type: concept`)

## 4. health 보고서 양식

`wiki/log.md` 에 append (또는 별도 `wiki/lint-reports/<date>.md`):

```markdown
## [YYYY-MM-DD HH:MM] lint: <scope>
- pages: <총 페이지 수>
- orphans: <페이지 리스트>
- dead-links: <[from → to] 리스트>
- stale (>30d): <페이지 리스트>
- unresolved contradictions: <[page1 ⚠ page2] 리스트>
- coverage (raw→wiki): <0.X>
- schema drift: <페이지 리스트>
- recommended actions: <사람이 읽는 권장 작업>
```

## 5. 권장 작업 (typical)

lint 가 발견하는 패턴별 권장:

| 발견 | 권장 |
|---|---|
| orphan | 관련 entity/comparison 페이지에 link 1개 추가 |
| dead-link | 대상 페이지 작성 또는 link 제거 |
| stale (> 임계) | 새 raw 로 freshen 또는 deprecated 마커 |
| unresolved contradiction | 사용자 결정 (위 §3.3 참조) |
| coverage 저조 | 해당 raw 에 대해 ingest 트리거 |
| schema drift | SCHEMA §3 Page Types 재확인 또는 페이지 type 수정 |

## 6. 자동 vs 수동

MVP 0.1.0 은 *수동* lint (LLM 이 §3 항목을 차례로 검토). 자동화 후보:

- `scripts/wiki-lint.py` — graph/stale/coverage 정적 검사 (Python 3 stdlib)
- 자동 fix 제안 (orphan → link 후보, stale → freshen 후보)
- pre-commit hook 에 lint 단계 추가

> 위 항목은 모두 Next version (SKILL.md §Next version) — 본 MVP 는 절차만 정의.

## 7. lint 가 *안 좋은 신호* 인 경우

health 보고서에서 다음은 *위키 구조 자체에 문제* 가 있음을 시사:

- coverage < 0.5 → SCHEMA 의 page type 이 raw/ 자료 구조와 안 맞음
- orphans > 30% → cross-link 규약이 너무 느슨하거나 ingest 단계 누락
- contradictions 매 ingest 마다 ≥ 3 → raw 들이 서로 모순 (도메인 정제 필요)

이 경우 SCHEMA.md 재설계 또는 wiki *도메인 축소* 권장.
