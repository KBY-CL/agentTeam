# Step 6 — Reflect 검증 에이전트

subagent_type: general-purpose / model: opus

## 입력 (Selective Read)

전체 일괄 Read 금지. 아래 순서로 필요한 파일만 읽으세요.

1. .agent-team/05_implementation_log.md — 생성된 파일 목록 파악
2. 최신 승인 설계서 — 설계 의도 파악
3. references/checklists/context-budget.md
4. references/policies/tdd-first.md
5. CLAUDE.md, AGENTS.md, .claude/settings.json
6. .claude/agents/_common/shared-rules.md
7. .claude/skills/_common/tdd-workflow/SKILL.md
8. .claude/agents/request-intake-agent.md
9. 나머지 agent 파일: implementation_log에 기재된 파일만, 각 50줄 이하로 frontmatter + description 위주 확인
   - 전체 내용이 필요한 경우에만 해당 파일 전체 Read

## 체크리스트

**[완전성]**
□ 설계서의 모든 에이전트 파일 생성
□ request-intake-agent.md 존재
□ tdd-workflow/SKILL.md 존재
□ doc-updater/SKILL.md 존재
□ 공통·개별 스킬·hook 모두 생성
□ .agent-team/backups/ 존재 (기존 파일 수정 시)

**[형식]**
□ frontmatter: name / description / model(실제 ID) / tools
□ alias가 실제 ID로 변환되었는가
□ description에 트리거 조건 명확히 포함

**[내용]**
□ tools 목록이 설계서와 일치
□ CLAUDE.md에 AGENT_TEAM_START·END 마커 블록 존재
□ CLAUDE.md가 @AGENTS.md import
□ settings.json hooks 중복 없음
□ request-intake-agent가 선택지 기반 인터뷰·handoff 구조 보유
□ Q6(자동화 금지) 항목이 forbidden에 반영

**[skills: frontmatter]**
□ agent frontmatter의 skills:에 대형 스킬이 preload되지 않았는가
□ doc-updater가 에이전트 본문 호출 조건으로 명시되었는가
□ tdd-workflow가 본문 호출 조건 또는 소형 preload로 명시되었는가

**[Project-Aware TDD 구현]**
□ shared-rules.md에 Red 검증 전 production code 수정 금지 규칙이 있음
□ 개발 담당 agent가 기존 테스트 관례와 Test Environment Profile을 먼저 확인하도록 되어 있음
□ Red Verifier `[PASS]` 없이는 implementation이 시작되지 않는 handoff 구조인가
□ Red 실패 원인이 기능 미구현인지 확인하는 조건이 있음
□ Green 검증이 프로젝트의 실제 test/CI command 기준으로 명시됨
□ 테스트 인프라 부재 시 사용자 승인 전 dependency/config/CI 변경 금지가 명시됨

**[보안 구현]**
□ shared-rules.md에 Common 보안 규칙 + 해당 도메인 규칙 포함
□ Q3 보안 수준에 맞는 강도 반영
□ 구현 에이전트에 보안 검토 책임 명시

**[Context Budget]**
→ references/checklists/context-budget.md 항목 적용

**[가이드 준수]**
□ 에이전트별 출력 계약([PASS]/[FAIL]) 명시
□ Forbidden 항목 각 에이전트에 명시

통과 → .agent-team/06_reflect_approved.md
실패 → .agent-team/06_reflect_feedback_{loop}.md (구체적 수정 지시)
마지막 줄: [PASS] 또는 [FAIL]
