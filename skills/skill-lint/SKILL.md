---
name: skill-lint
description: 스킬 카탈로그의 SKILL.md frontmatter 정합성, name/description 규칙, harness_compat, references 링크를 검증합니다. 새 스킬 추가 또는 PR 전 사용.
when_to_use: 새 스킬을 skills/ 에 추가한 직후, PR 올리기 전, 또는 저장소 lint 실패가 의심될 때
metadata:
  harness_compat:
    - claude-code
    - generic-md
  category: meta
  version: 0.2.0
---

# skill-lint

`skills/` 디렉터리의 모든 `SKILL.md` 를 순회해 manifest 정합성과 링크 무결성을 검증한다.
*harness 비종속* — 어떤 환경에서도 markdown 으로 해석 가능. **실제 실행은 권장 도구(`markdownlint-cli2`,
`lychee`)와 본 SKILL 의 절차 매핑**으로 수행한다.

## When to use

- 새 스킬을 `skills/` 에 추가한 직후
- 기존 스킬의 frontmatter / 본문을 변경한 뒤
- 저장소 전체 lint 가 실패했다는 신호가 있을 때
- PR 올리기 전 로컬 사전 점검

## Inputs

- `skills/` 디렉터리 (또는 `--path` 로 지정한 하위 경로)
- (선택) `--strict` — 경고(W 코드)도 에러로 처리
- (선택) `--json` — 기계 판독 가능한 출력
- (선택) `--tool markdownlint-cli2|lychee|both` — 외부 lint 도구 선택

## Outputs

- 사람이 읽는 보고서: 위반 파일 / 줄 / rule code / 사유
- 종료 코드: 0 (clean) / 1 (violations) / 2 (사용 오류)
- `--json` 모드: `{"violations": [{"file": ..., "line": ..., "rule": ..., "message": ...}]}`

## Recommended tooling

| 단계 | 도구 | 설치 (개념) | 호출 |
|---|---|---|---|
| Markdown lint | [`markdownlint-cli2`](https://github.com/DavidAnson/markdownlint-cli2) | `npm i -g markdownlint-cli2` 또는 `npx` | `markdownlint-cli2 "skills/**/*.md"` |
| 링크 무결성 | [`lychee`](https://github.com/lycheeverse/lychee) | `brew install lychee` 등 | `lychee --offline "skills/**/*.md"` |
| Frontmatter 검증 | `skill-lint` 절차 자체 | — | 본 SKILL §Procedure |

> 도구 자체는 본 카탈로그 범위 **밖** 이다. 위 표는 *권장* 일 뿐, 강제하지 않는다.
> harness 비종속 약속을 위해 본 카탈로그는 *도구 호출 절차* 만 정의한다.

## Procedure

1. **경로 수집**: `skills/**/SKILL.md` 를 glob 으로 수집한다.
2. **markdownlint 실행**: `markdownlint-cli2 "skills/**/*.md"` 를 호출하고 결과를 *rule code* 단위로 받는다.
   - 일반 markdown 규칙(MD001~MD058) 은 그대로 사용.
   - 본 카탈로그 특유의 추가 규칙은 `.markdownlint.jsonc` 에 정의(아래 §Custom rules 참조).
3. **frontmatter parse**: 각 `SKILL.md` 의 YAML frontmatter 를 파싱한다. 파싱 실패는 `E001`.
4. **required keys 검사**: `name`, `description` 이 존재하는지 확인. 누락 시 `E010`.
5. **name 형식 검사**: `^[a-z0-9]+(-[a-z0-9]+)*$` 매치 + *디렉터리명과 일치*. 위반 시 `E020`.
6. **description 검사**: 1-line, ≤ 200자. 위반 시 `E030`.
7. **harness_compat 검사**: `metadata.harness_compat` 가 배열이고 ≥ 1 요소. 위반 시 `E040`.
8. **본문 구조 검사**: `## When to use` / `## Procedure` 단락 존재. 누락 시 `W100` (strict 시 에러).
9. **references 링크 검사**:
   - 본문이 `references/`, `assets/`, `scripts/` 의 *존재하지 않는* 파일을 참조하면 `E200`.
   - 본문이 *한 번도 참조하지 않는* `references/`, `assets/`, `scripts/` 가 있으면 `W110` (strict 시 에러).
10. **lychee 실행**: `lychee --offline "skills/**/*.md"` 로 외부 링크의 정적 무결성 확인. 깨지면 `E210`.
11. **집계**: violations 배열을 만들고 종료 코드 결정.

### Custom rules (`.markdownlint.jsonc` 예시)

```jsonc
{
  "MD013": false,                    // 한 줄 길이 제한 비활성
  "MD041": false,                    // 파일 첫 줄이 H1 이어야 하는 규칙 비활성
  "MD033": { "allowed_elements": ["br", "kbd", "details", "summary"] },
  "no-inline-html": false,
  "frontmatter-name-matches-dir": true   // 본 카탈로그 특유 — name == dir
}
```

## Trade-offs

- **정적 검증 vs dynamic 실행**: 본 버전은 *정적* 검증만 한다. dynamic 실행(스킬을 실제로 harness 에서
  호출)은 본 카탈로그 범위 **밖**. lint 가 깨지면 *harness 가 호출을 거부* 한다는 가정.
- **외부 도구 의존**: `markdownlint-cli2` / `lychee` 가 없으면 *lint* 부분만 동작. frontmatter 검증
  (3~9 단계) 은 도구 없이도 *수동 체크리스트* 로 수행 가능.
- **`--strict` 기본값**: 기본은 permissive (경고는 통과). CI / pre-push 에서만 `--strict` 권장.
- **rule 충돌**: markdownlint 의 일반 rule 이 본 카탈로그의 frontmatter / 디렉터리 규칙과 의미가 겹칠
  수 있어, `.markdownlint.jsonc` 로 *카탈로그 특유 custom rule* 을 둔다.

## Workflow integration

선택적 통합 옵션 (마크다운 절차로만 명세 — 실제 구현은 harness 또는 저장소 운영자의 책임):

- **GitHub Actions**: 저장소 `.github/workflows/skill-lint.yml` 에 `markdownlint-cli2` + `lychee` 단계를 추가.
- **pre-push hook**: `git config core.hooksPath .githooks` 후 `pre-push` 에 lint 명령 삽입.
- **Claude Code 사용자**: 본 스킬을 slash 로 호출해 *수동 검증 보고* 만 받는 경로.
- **다른 markdown-aware harness**: `metadata.harness_compat` 가 `generic-md` 인 경우, harness 가
  본 SKILL 을 읽고 자체적으로 §Procedure 를 실행.

## Error codes

- `E001` — frontmatter YAML 파싱 실패
- `E010` — required key 누락 (`name` / `description`)
- `E020` — `name` 형식 위반 또는 디렉터리명 불일치
- `E030` — `description` 1-line 또는 길이 위반
- `E040` — `harness_compat` 누락 또는 비어있음
- `E200` — 깨진 내부 링크
- `E210` — 깨진 외부 링크 (lychee)
- `W100` — 본문 단락(`When to use` / `Procedure`) 누락
- `W110` — 미사용 `references/` / `assets/` / `scripts/`

## References

- [../README.md §3 SKILL.md 포맷](../README.md) — 검증 대상 포맷 정의
- [../README.md §6 검증 / Lint](../README.md) — 본 스킬의 1차 수동 체크리스트 출처
- [.markdownlint.jsonc 예시](../README.md#custom-rules-markdownlintjsonc-예시) — 카탈로그 특유 custom rule
