# Step 8 — Audit Mode

메인 Claude 또는 general-purpose / opus가 수행합니다.
Audit Mode에서는 source/config 파일을 수정하지 않습니다.

## 로드 대상

- `references/policies/audit-mode.md`
- `references/policies/drift-detection.md`
- `references/policies/registry.md`
- `references/checklists/context-budget.md`

## 실행 절차

1. Minimal Preflight 결과 확인
2. registry load 또는 recovery
3. checked files selective read
4. context budget 검사
5. Step 7A Static Smoke 실행
6. Drift Detection 수행
7. `.agent-team/audit_report_{timestamp}.md` 작성

## 필수 포함 사항

Audit Report에는 반드시 아래 섹션이 있어야 합니다.
- `Summary`
- `Findings`
- `Checked Files`
- `No-write Guarantee`

## 금지 사항

- `.claude/agents/*.md` 수정 금지
- `.claude/skills/**` 수정 금지
- `.claude/settings.json`, `CLAUDE.md`, `AGENTS.md` 수정 금지
