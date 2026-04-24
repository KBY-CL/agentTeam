# Context Budget 체크리스트

Step 4(설계 검증)와 Step 6(Reflect 검증)에서 적용하세요.

## 이번 단계 로딩 예산
□ 이번 단계에서 로드한 reference 파일 수가 3개 이하인가
□ 이번 단계에서 로드한 reference 총량이 300줄 이하인가

## 생성될 파일 크기 예산

| 대상 | 권장 | 하드 제한 | 초과 시 조치 |
|---|---:|---:|---|
| CLAUDE.md | 120줄 | 200줄 | 절차는 Skill로 이동 |
| AGENTS.md | 150~250줄 | 300줄 | 워크플로우 절차 제거 |
| .claude/agents/*.md 각 파일 | 120~180줄 | 250줄 | 체크리스트를 skill/reference로 분리 |
| shared-rules.md | 80~120줄 | 200줄 | 모든 에이전트 공통 아닌 규칙 제거 |
| 개별 SKILL.md | 200~300줄 | 500줄 | references/scripts로 분리 |
| Handoff 파일 | 40~80줄 | 200줄 | 긴 로그는 별도 파일, 요약만 handoff |

□ CLAUDE.md + AGENTS.md + shared-rules.md 합계가 300줄 이하인가 (권장) / 500줄 이하인가 (하드 제한)
□ 각 agent 정의 파일이 250줄 이하인가
□ _common에 "모든 에이전트가 매번 알아야 하는 내용"만 남았는가
□ 초과 항목이 있으면: 어떤 섹션을 skill·reference·template으로 이동할지 제안했는가

## skills: frontmatter 예산
□ agent frontmatter의 skills:에 대형 스킬(100줄+)이 포함되지 않았는가
□ preload된 skills:의 총 컨텐츠가 에이전트 시작 시 200줄을 넘지 않는가
