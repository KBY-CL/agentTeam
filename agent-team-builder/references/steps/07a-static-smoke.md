# Step 7A — Static Smoke Test

subagent_type: general-purpose / model: haiku

## 실행 준비

아래 자산을 runtime 위치로 복사한 뒤 실행하세요.

- `references/scripts/static_smoke.py` → `.agent-team/tools/static_smoke.py`
- `references/schemas/registry.schema.json` → `.agent-team/schemas/registry.schema.json`

필요 디렉토리가 없으면 먼저 생성합니다.

## 실행 명령

```bash
python .agent-team/tools/static_smoke.py
```

Python이 없으면:
- Step 0 / Minimal Preflight 결과를 참고해 WARN 처리
- AI가 직접 같은 체크 항목을 수동 점검

## 스크립트 책임 범위

스크립트는 최소한 아래를 검사해야 합니다.

- agent frontmatter 필수 필드
- required files 존재 여부
  - request-intake-agent.md
  - terminal-choice/SKILL.md
  - tasklist-handoff/SKILL.md
  - tdd-workflow/SKILL.md
  - doc-updater/SKILL.md
  - handoff-writer/SKILL.md
  - .agent-team/tools/terminal_select.py
  - .agent-team/tools/terminal_select_windows.py
- CLAUDE.md / AGENTS.md / shared-rules line budget
- settings.json 유효성 및 duplicate hooks
- tools / forbidden overlap
- global forbidden MCP tool patterns
- dangerous command patterns
  - `.claude/settings.json` hook command
  - `.claude/hooks/**/*.sh`
  - `.agent-team/tools/*.py` 내 `subprocess` / `os.system` 호출
- `registry.json` 존재 시 `registry.schema.json` validation

## AI 후처리

스크립트 실행 후:
1. FAIL 항목의 관련 파일만 부분 Read하여 원인 파악
2. 자동 수정 가능 항목(포맷 오류, 누락 파일, 경로 오타, line count 초과)은 즉시 수정
3. 승인 필요 항목은 목록 작성 후 사용자에게 제시

## 산출물: `.agent-team/07a_static_smoke_test.md`

```markdown
# Static Smoke Test 리포트

## 결과 요약
PASS X / FAIL Y

## FAIL 항목 상세 + 조치
| 항목 | 원인 | 자동수정가능 | 조치 내용 |

## 전체 결과
(스크립트 출력)
```
