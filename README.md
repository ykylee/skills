# skills

> 사용자 본인이 여러 AI 하네스(Claude Code 외 포함)에서 재사용할
> **범용 AI 워크플로우 스킬** 을 모아두고 배포하는 카탈로그.

자세한 의도 / scope / 비목표는
[ai-workflow/memory/active/PURPOSE.md](./ai-workflow/memory/active/PURPOSE.md) 참조.

## 디렉터리

```
skills/                       # 스킬 카탈로그
├── README.md                 # authoring 가이드
├── .index.json               # skill-discover 캐시 (.gitignore)
├── html-slides-builder/      # doc — 단일 1920x1080 HTML 슬라이드 빌더
├── skill-discover/           # meta — 카탈로그 검색
└── skill-lint/               # meta — frontmatter / 링크 검증

scripts/
├── skill-lint                # frontmatter / harness_compat / 링크 검증 (Python 3)
└── skill-discover            # SKILL.md 인덱싱 + 검색 (Python 3)

.github/workflows/
└── skill-lint.yml            # GitHub Actions (markdownlint-cli2 + lychee + skill-lint)

.githooks/
└── pre-push                  # 로컬 pre-push hook (선택)

.markdownlint.jsonc           # markdownlint-cli2 rule 정의

CHANGELOG.md                  # 버전별 변경 기록
```

## 빠른 시작

### 새 스킬 추가

1. `skills/<name>/SKILL.md` 를 [skills/README.md §3 포맷](./skills/README.md)에 맞춰 작성
2. 로컬에서 `python3 scripts/skill-lint --path skills` 실행 → clean
3. PR 을 올리면 GitHub Actions 가 lint / link-check 자동 실행
4. `CHANGELOG.md` 의 `[Unreleased]` 에 한 줄 추가
5. (검색 가능성 확인) `python3 scripts/skill-discover <name>` 으로 인덱스 등장 확인

### 로컬 lint

전제: Python 3.10+. (`markdownlint-cli2` / `lychee` 는 GitHub Actions 에서만 설치해도 OK.)

```bash
# 카탈로그-특유 rule (frontmatter, name/description, harness_compat, 내부 링크)
python3 scripts/skill-lint --path skills

# strict (W 코드도 에러로 처리)
python3 scripts/skill-lint --path skills --strict

# 기계 판독 가능한 JSON
python3 scripts/skill-lint --path skills --json

# 카탈로그 검색 (skill-discover)
python3 scripts/skill-discover                                   # 인덱스 출력
python3 scripts/skill-discover --index                           # .index.json 캐시 빌드
python3 scripts/skill-discover category:meta harness:claude-code # 토큰 검색
```

### pre-push hook (선택)

```bash
git config core.hooksPath .githooks
```

이후 모든 push 전 자동 검증. 우회하려면 `--no-verify`.

### CI

`.github/workflows/skill-lint.yml` 가 `push` 와 `pull_request` 두 트리거에서 다음을 순차 실행:

1. `markdownlint-cli2 "skills/**/*.md" "README.md" "CHANGELOG.md"`
2. `python3 scripts/skill-lint --path skills`
3. `lychee --offline "skills/**/*.md" "README.md" "CHANGELOG.md"`

## 범위

- **In-scope**: harness 비종속의 단일-책임 스킬, `SKILL.md` manifest + 본문, lint 절차
- **Out-of-scope**: harness 종속 스킬, 실행 가능한 애플리케이션 코드 — **다만 `scripts/`
  하위의 *운영 도구* (skill-lint 등) 는 카탈로그 운영에 필요하므로 예외로 둔다.** 자세한
  정책은 [PURPOSE.md §3](./ai-workflow/memory/active/PURPOSE.md) 참조.
- 시크릿, API 키, 개인 식별 정보는 **커밋하지 않는다**.

## 운영 정책

- 한 PR = 한 명제 (스킬 1개 또는 운영 정책 1건).
- 모든 변경은 owner (사용자 본인) 만 발행. AI 에이전트는 *제안까지만*.
- 스킬 manifest 가 깨지면 `skill-lint` 가 실패하고 harness 가 해당 스킬 호출을 거부한다는 것을 가정한다.
