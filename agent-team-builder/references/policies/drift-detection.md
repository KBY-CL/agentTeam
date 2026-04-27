# Drift Detection Policy

## Purpose

Drift Detection은 설계서, registry, 실제 구현 파일 사이의 정합성을 점검합니다.
생성 직후 검증이 아니라 운영 중 변화가 설계를 무너뜨렸는지 확인하는 절차입니다.

## Comparison Inputs

- `.agent-team/registry.json`
- 최신 설계서 `.agent-team/03_agent_design_spec_v*.md`
- 최신 승인 / 구현 로그
- 실제 `.claude/agents/*.md`
- 실제 `.claude/skills/**`
- 실제 `.claude/settings.json`
- 필요 시 `CLAUDE.md`, `AGENTS.md`, `docs/tool-inventory.md`

## Drift Checks

- model alias / 실제 model ID 불일치
- tools 목록 변경
- forbidden 누락
- 설계서에 없는 agent 추가 또는 기존 agent 삭제
- `shared-rules.md` 와 보안 프로필 불일치
- doc-updater 호출 조건 약화 / 삭제
- tdd-workflow 누락 또는 Red/Green gate 약화 / 삭제
- terminal-choice 누락 또는 선택형 질문의 직접 타이핑 방식 회귀
- tasklist-handoff 누락 또는 implementation-agent의 전체 설계서 기본 입력 회귀
- Implementation Agent의 Red Verifier 승인 조건 삭제
- settings hooks 변경
- registry hash / line_count 와 실제 파일 불일치

## Severity

### INFO
- 설명 문구 변경
- comment 변경

### WARN
- line count 증가
- description trigger 변경
- doc-updater 호출 조건 약화
- tdd-workflow 호출 조건 약화
- terminal-choice fallback 조건 불명확
- tasklist template 필드 일부 누락

### FAIL
- 설계서에 없는 agent 추가
- 설계서에 있는 agent 삭제
- tools 권한 변경
- forbidden 누락
- model 변경
- Red 검증 전 production code 수정 금지 규칙 삭제
- 선택형 인터뷰가 기본적으로 A/B/C 직접 타이핑 방식으로 변경됨
- 승인된 tasklist 없이 implementation-agent가 production code를 수정할 수 있음

### CRITICAL
- Bash / Write / Edit 권한 무단 추가
- 외부 MCP write / delete 권한 추가
- security hook 삭제
- apply / deploy / DB 변경 가능성 추가
- 테스트 인프라 또는 CI 변경을 사용자 승인 없이 허용하는 흐름 추가
- 사용자 확인 없이 질문형 agent가 선택지를 임의 확정하는 흐름 추가
- tasklist 밖 파일 수정/순서 변경/범위 확장을 승인 없이 허용하는 흐름 추가

## Audit Overall Mapping

- 하나라도 `CRITICAL` 이 있으면 Overall = `CRITICAL`
- `CRITICAL` 이 없고 `FAIL` 이 있으면 Overall = `FAIL`
- `FAIL` 이 없고 `WARN` 이 있으면 Overall = `WARN`
- 그 외는 `PASS`

## Output Usage

Drift findings는 Audit Report의 Findings 표에 들어갑니다.
Update Mode에서는 drift severity가 높을수록 Major scope 또는 Generate 재실행 제안 근거로 사용합니다.
