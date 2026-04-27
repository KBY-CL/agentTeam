# Terminal Interaction Policy

선택형 질문은 사용자가 값을 직접 타이핑하게 만들지 말고 터미널 선택 UI를 우선 사용합니다.

## Required Behavior

- 단일 선택: 방향키로 이동하고 Enter로 확정합니다.
- 복수 선택: 방향키로 이동하고 Space로 토글한 뒤 Enter로 확정합니다.
- 선택지는 프로젝트명, 모듈명, 감지된 테스트 명령처럼 현재 맥락을 반영해 작성합니다.
- "기타"를 고른 경우에만 짧은 자유 입력을 요청할 수 있습니다.
- 터미널 선택 UI를 실행할 수 없는 환경에서만 문자/번호 입력 fallback을 사용합니다.

## Tooling

Step 2A/2B와 생성된 agent team의 인터뷰형 agent는 `terminal_select.py` 또는 생성된 `terminal-choice` skill을 사용합니다.

권장 runtime 위치:

- `.agent-team/tools/terminal_select.py`
- `.claude/skills/_common/terminal-choice/SKILL.md`

## UX Contract

- 질문 하나당 선택 UI 하나를 띄웁니다.
- 기본 추천값이 있으면 첫 번째 항목 또는 명시된 default로 커서를 둡니다.
- 사용자가 선택한 label과 value를 모두 handoff 또는 interview result에 기록합니다.
- UI 실패 시 fallback을 사용했다는 사실을 산출물에 기록합니다.

## Forbidden

- 선택형 질문에서 "A/B/C를 타이핑하세요"를 기본 방식으로 쓰지 않습니다.
- 여러 질문을 한 번에 던지고 사용자가 쉼표로 직접 입력하게 만들지 않습니다.
- agent가 임의로 선택지를 확정하지 않습니다. 빠른 진행 요청 또는 응답 불가 상황에서만 기본 추천안을 사용하고 근거를 기록합니다.
