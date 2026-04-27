# Terminal Interaction Policy

선택형 질문은 사용자가 값을 직접 타이핑하게 만들지 말고 터미널 선택 UI를 우선 사용합니다.

## Required Behavior

- 단일 선택: 방향키로 이동하고 Enter로 확정합니다.
- 복수 선택: 방향키로 이동하고 Space로 토글한 뒤 Enter로 확정합니다.
- 선택지는 프로젝트명, 모듈명, 감지된 테스트 명령처럼 현재 맥락을 반영해 작성합니다.
- "기타"를 고른 경우에만 짧은 자유 입력을 요청할 수 있습니다.
- 터미널 선택 UI를 실행할 수 없는 비대화형 환경에서는 입력을 기다리지 말고 `INTERACTIVE_REQUIRED`를 반환합니다.
- 문자/번호 입력 fallback은 사용자가 명시적으로 허용했거나 실제 stdin 입력이 가능한 환경에서만 사용합니다.
- Windows 비대화형 셸에서는 `terminal_select_windows.py`를 사용해 별도 cmd 창을 띄우고 선택 결과를 JSON 파일로 회수할 수 있습니다.

## Tooling

Step 2A/2B와 생성된 agent team의 인터뷰형 agent는 `terminal_select.py` 또는 생성된 `terminal-choice` skill을 사용합니다.

권장 runtime 위치:

- `.agent-team/tools/terminal_select.py`
- `.agent-team/tools/terminal_select_windows.py`
- `.claude/skills/_common/terminal-choice/SKILL.md`

## UX Contract

- 질문 하나당 선택 UI 하나를 띄웁니다.
- 기본 추천값이 있으면 첫 번째 항목 또는 명시된 default로 커서를 둡니다.
- 사용자가 선택한 label과 value를 모두 handoff 또는 interview result에 기록합니다.
- UI 실패 시 agent는 fallback 입력을 강제하지 말고 사용자에게 채팅으로 선택을 요청하거나 진짜 TTY에서 재실행하도록 안내합니다.
- `terminal_select.py`가 `INTERACTIVE_REQUIRED`를 반환하면 그 JSON의 options를 그대로 사용자에게 보여줍니다.
- Windows에서 별도 cmd 창 사용이 가능하면 `terminal_select_windows.py`를 먼저 시도합니다. 성공하면 stdout의 JSON을 선택 결과로 사용합니다.

## Forbidden

- 선택형 질문에서 "A/B/C를 타이핑하세요"를 기본 방식으로 쓰지 않습니다.
- 여러 질문을 한 번에 던지고 사용자가 쉼표로 직접 입력하게 만들지 않습니다.
- agent가 임의로 선택지를 확정하지 않습니다. 빠른 진행 요청 또는 응답 불가 상황에서만 기본 추천안을 사용하고 근거를 기록합니다.
- 비대화형 `Bash(...)`에서 `input()`을 기다리는 fallback을 기본으로 실행하지 않습니다.
