# Registry Policy

## Purpose

registry는 다음 실행의 시작점이 되는 운영 상태 파일입니다.
산출물 전체를 다시 읽지 않고도 현재 agent team 상태를 빠르게 파악할 수 있어야 합니다.

## Canonical File

- canonical path: `.agent-team/registry.json`
- source of truth schema: `references/schemas/registry.schema.json`

## Required Top-Level Fields

- `schema_version`
- `agent_team_version`
- `mode`
- `last_updated`
- `source_design`
- `last_approved`
- `last_implementation_log`
- `security_profiles`
- `agents`
- `skills`
- `hooks`
- `files`
- `last_validation`

## Optional Top-Level Fields

- `development_methodology`: Project-Aware TDD-first 등 개발 방법론 상태

## Phase 1 Risk Level Rule

- `agents[].risk_level` 은 1차부터 필수
- `skills[].risk_level`, `hooks[].risk_level` 은 1차에서는 optional
- 2차에서 skill / hook / tool 수준까지 확장 검토

## File Hash Policy

### Hash Include
- `.claude/agents/*.md`
- `.claude/agents/_common/shared-rules.md`
- `.claude/skills/**/SKILL.md`
- `.agent-team/tools/terminal_select.py`
- `.agent-team/tools/terminal_select_windows.py`
- `.claude/settings.json`
- `CLAUDE.md`
- `AGENTS.md`
- `docs/tool-inventory.md`

### Hash Exclude
- `.claude/handoff/*.md`
- `.agent-team/backups/**`
- `.agent-team/tmp/**`
- `.agent-team/audit_report_*.md`
- `.agent-team/intake_*.md`

각 hash 대상 파일은 `files[]` 에 `path`, `type`, `sha256`, `line_count` 로 기록합니다.

## Update Rules

### Generate
- Step 7A / 7B 완료 후 Step 9에서 최초 생성

### Update
- 성공적인 구현과 검증 후 Step 9에서 갱신

### Audit
- registry를 읽을 수는 있지만 덮어쓰지 않음

## Validation Rules

- Step 7A Static Smoke에서 기존 `registry.json` 이 있으면 schema validation 수행
- Step 9에서는 새 registry를 저장하기 전에 schema validation 수행
- invalid registry는 저장 완료로 간주하지 않음

## Registry Recovery

`registry.json` 이 없거나 파싱 실패 시 아래 순서로 복구를 시도합니다.

1. 최신 `.agent-team/03_agent_design_spec_v*.md` 탐색
2. `.agent-team/05_implementation_log.md` 확인
3. 실제 `.claude/agents/*.md` 스캔
4. 필요 시 `.claude/skills/**`, `.claude/settings.json` 추가 확인
5. 복구 가능한 경우 registry 재생성 제안

복구 실패 시:
- Update Mode 자동 진입 금지
- Generate 재실행 또는 수동 검토 제안
