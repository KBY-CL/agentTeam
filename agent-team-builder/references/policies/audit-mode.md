# Audit Mode Policy

## No-write Guarantee

Audit Mode는 source/config 파일에 대한 no-write를 보장합니다.
허용되는 write는 audit 결과 산출물 1개뿐입니다.

- allowed: `.agent-team/audit_report_{timestamp}.md`
- forbidden: `.claude/agents/*.md`, `.claude/skills/**`, `.claude/settings.json`, `CLAUDE.md`, `AGENTS.md`

## Minimal Preflight Flow

- `PASS`: 그대로 Audit 진행
- `WARN`: Registry Recovery 또는 사용자 확인 후 진행
- `FAIL`: Audit 중단, 복구 또는 Generate 제안

## Execution Order

1. Minimal Preflight
2. registry load / recovery
3. checked files selective read
4. context budget 검사
5. Step 7A Static Smoke
6. Drift Detection
7. Audit Report 작성

## Default Checked Files

- `.agent-team/registry.json`
- `.claude/agents/*.md`
- `.claude/settings.json`
- `CLAUDE.md`
- `AGENTS.md`

필요 시 `docs/tool-inventory.md`, `.claude/skills/**`, `_common/shared-rules.md` 를 추가로 포함합니다.

## Audit Report Format

```markdown
# Agent Team Audit Report

## Summary
- Overall: PASS / WARN / FAIL / CRITICAL
- Drift count:
- Context budget:
- Static smoke:

## Findings
| Severity | Area | File | Finding | Recommended Action |
|---|---|---|---|---|

## Checked Files
- .agent-team/registry.json
- .claude/agents/*.md
- .claude/settings.json
- CLAUDE.md
- AGENTS.md

## No-write Guarantee
This audit did not modify project files.
```
