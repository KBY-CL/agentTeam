# Step 9 — Registry Update

Generate / Update가 성공적으로 끝난 뒤 메인 Claude가 수행합니다.

## 로드 대상

- `references/policies/registry.md`
- `references/schemas/registry.schema.json`

## 실행 절차

1. 실제 `.claude/agents/*.md`, `.claude/skills/**`, `.claude/settings.json`, `CLAUDE.md`, `AGENTS.md`, `docs/tool-inventory.md` 상태 수집
2. hash policy 대상 파일에 대해 `sha256` 과 `line_count` 계산
3. `registry.json` top-level fields 채우기
4. `last_validation` 에 Step 7A / Step 7B 결과 반영
5. schema validation 수행
6. 유효한 경우 `.agent-team/registry.json` 저장
7. `.agent-team/09_registry_update.md` 에 갱신 요약 기록

## 규칙

- invalid registry는 저장 완료로 간주하지 않음
- Audit Mode에서는 Step 9를 실행하지 않음
- Step 7B를 실행하지 않았다면 `workflow_simulation` 은 `SKIP` 또는 `NOT_RUN` 으로 기록
