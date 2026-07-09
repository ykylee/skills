---
name: skill-discover
description: 카탈로그의 스킬을 카테고리·키워드·harness_compat 로 검색하고 추천합니다. 새 작업 시작 전 "이런 일에 쓸 스킬이 있나?" 검색할 때 사용.
when_to_use: 새 작업을 시작하기 전 사용 가능한 스킬을 빠르게 훑어볼 때, 또는 "어떤 스킬이 있는지" 인덱스가 필요할 때
metadata:
  harness_compat:
    - claude-code
    - generic-md
  category: meta
  version: 0.1.0
---

# skill-discover

`skills/` 카탈로그의 모든 `SKILL.md` 를 인덱싱하고, 사용자 질의에 대해 적합한 스킬을 추천한다.
*harness 비종속* — 어떤 환경에서도 markdown 으로 해석 가능. 자동 인덱싱이 필요하면
[skill-lint](../skill-lint/SKILL.md) 의 검증 절차에 인덱스 빌드 단계를 추가해 활용 가능.

## When to use

- 새 작업을 시작하기 전 *"이런 일에 쓸 스킬이 있나?"* 검색할 때
- 카탈로그에 어떤 스킬이 있는지 빠르게 훑어볼 때
- harness 별로 사용 가능한 스킬 목록이 필요할 때
- 카테고리별 분류를 빠르게 보고 싶을 때

## Inputs

- `skills/` 디렉터리 (또는 `--path` 로 지정한 하위 경로)
- (선택) 사용자 질의 — 자유 텍스트 또는 구조화된 토큰:
  - 카테고리: `category:meta` / `category:doc` / `category:code` …
  - harness: `harness:claude-code` / `harness:generic-md` …
  - 키워드: 임의의 단어 (description / name 매칭)
- (선택) `--top N` — 출력할 추천 수 (default 3)
- (선택) `--category <cat>` / `--harness <h>` — 단일 필터

## Outputs

- 사람이 읽는 표: `name` / `category` / `harness_compat` / `description` / `score`
- JSON 옵션: `{"results": [{"name": ..., "score": ..., "matches": [...]}]}`
- 종료 코드: 0 (found) / 1 (no match) / 2 (사용 오류)

## Procedure

1. **인덱스 빌드**: `skills/*/SKILL.md` 를 glob 으로 순회.
   각 파일에서 *indexable* 필드만 추출:
   - `name`, `description`, `metadata.category`, `metadata.harness_compat`
2. **질의 토큰화**: 사용자 입력을 다음 토큰으로 분리:
   - `category:<value>` → 카테고리 필터
   - `harness:<value>` → harness 필터
   - 그 외 단어들 → 키워드 풀
3. **scoring** (각 스킬에 대해):
   - 카테고리 정확 일치: +3
   - 키워드가 `name` 의 단어와 일치: +2
   - 키워드가 `description` 의 단어와 일치: +2
   - `harness_compat` 가 질의 harness 와 겹침: +1
   - `harness_compat` 가 `generic-md` 를 포함: +0.5 (범용 보너스)
4. **필터 적용**: `category:` / `harness:` 토큰이 있으면 *score 0 인 후보 제외*.
5. **정렬**: score 내림차순. 동점이면 `name` 알파벳순.
6. **출력**: 상위 N (default 3) 을 표로 출력. 각 행 끝에 *호출 예시 1줄* 부록:
   ```
   예: Claude Code → 슬래시 자동완성 트리거
       generic-md  → SKILL.md 의 Procedure 단락을 그대로 따름
   ```
7. **없음 처리**: score > 0 후보가 0 이면 *가장 가까운 카테고리* 1개 추천 + "no exact match" 표시.

## Trade-offs

- **순수 정적**: 본 절차는 *런타임 인덱싱* 없이 매번 `SKILL.md` 를 다시 읽는다. 카탈로그가
  수십 개 이상으로 커지면 *사전 빌드된 인덱스 파일* (예: `skills/.index.json`) 을 두고
  `skill-lint` 가 빌드 책임, `skill-discover` 가 조회 책임으로 분리하는 것을 권장.
- **키워드 일치의 한계**: `description` 의 단어 매칭은 *어근 처리* 가 없다. 한국어/영어 혼합
  검색의 정확도보다 *재현 가능성* 을 우선.
- **점수 가중치**: 위 가중치(3/2/2/1/0.5)는 *기본값*. 본 카탈로그에서 직접 수치 변경이
  필요하면 §Score tuning 섹션에 한 줄 명시.
- **harness 비종속 약속**: 본 스킬은 `generic-md` 로 해석 가능. 즉 어떤 harness 라도
  markdown 으로 본 SKILL.md 를 읽고 §Procedure 를 그대로 따라 검색 가능.

## Score tuning

기본 가중치(상수) 외에 *프로젝트별 override* 가 필요하면 SKILL.md 의 frontmatter 에
`metadata.score_overrides: {category: 5}` 같은 형태로 둔다. 본 카탈로그 기본값 사용 시
이 필드 생략 가능.

## Error codes

- `E001` — `skills/` 경로 부재
- `E010` — `SKILL.md` 0건 (카탈로그 비어있음)
- `E020` — 사용자 질의 파싱 실패 (잘못된 `category:` / `harness:` 형식)

## References

- [../README.md §3 SKILL.md 포맷](../README.md) — 인덱싱 대상 포맷 정의
- [../skill-lint/SKILL.md](../skill-lint/SKILL.md) — 인덱스 빌드 자동화 후보
- [../skill-lint/SKILL.md §Recommended tooling](../skill-lint/SKILL.md) — 도구 분리 원칙
