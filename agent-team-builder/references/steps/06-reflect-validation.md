# Step 6 — Reflect 검증 에이전트

subagent_type: general-purpose / model: opus

## 입력 (Selective Read)

전체 일괄 Read 금지. 아래 순서로 필요한 파일만 읽으세요.

1. .agent-team/05_implementation_log.md — 생성된 파일 목록 파악
2. 최신 승인 설계서 — 설계 의도 파악
3. references/checklists/context-budget.md
4. references/policies/tdd-first.md
5. references/policies/terminal-interaction.md
6. references/policies/tasklist-handoff.md
7. CLAUDE.md, AGENTS.md, .claude/settings.json
8. .claude/agents/_common/shared-rules.md
9. .claude/skills/_common/terminal-choice/SKILL.md
10. .claude/skills/_common/tasklist-handoff/SKILL.md
11. .claude/skills/_common/tdd-workflow/SKILL.md
12. .claude/agents/request-intake-agent.md
13. 나머지 agent 파일: implementation_log에 기재된 파일만, 각 50줄 이하로 frontmatter + description 위주 확인
   - 전체 내용이 필요한 경우에만 해당 파일 전체 Read

## 체크리스트

**[완전성]**
□ 설계서의 모든 에이전트 파일 생성
□ request-intake-agent.md 존재
□ terminal-choice/SKILL.md 존재
□ .agent-team/tools/terminal_select.py 존재
□ tasklist-handoff/SKILL.md 존재
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
□ request-intake-agent가 terminal-choice 기반 인터뷰·handoff 구조 보유
□ Q6(자동화 금지) 항목이 forbidden에 반영
□ feature-architect-agent가 있으면 기능 설계 산출물 파일명 확인 규칙을 보유
□ feature-architect-agent가 agent team topology/config 직접 변경 금지를 명시
□ feature-architect-agent가 implementation tasklist 생성 책임을 명시
□ implementation-agent가 있으면 승인된 tasklist를 기본 입력으로 사용하도록 명시
□ implementation-agent가 전체 설계서/인터뷰/긴 검증 로그를 기본 입력으로 받지 않도록 명시

**[skills: frontmatter]**
□ agent frontmatter의 skills:에 대형 스킬이 preload되지 않았는가
□ terminal-choice가 질문형 agent 본문 호출 조건 또는 소형 preload로 명시되었는가
□ tasklist-handoff가 관련 agent 본문 호출 조건으로 명시되었는가
□ doc-updater가 에이전트 본문 호출 조건으로 명시되었는가
□ tdd-workflow가 본문 호출 조건 또는 소형 preload로 명시되었는가

**[터미널 인터랙션 구현]**
□ 선택형 질문이 방향키 + Enter 방식으로 안내됨
□ 복수 선택 질문이 Space 토글 + Enter 방식으로 안내됨
□ A/B/C 직접 타이핑 또는 쉼표 입력이 기본 방식으로 남아 있지 않음
□ 비대화형 셸에서 `INTERACTIVE_REQUIRED`를 반환하고 입력 대기하지 않도록 명시됨
□ 번호 입력 fallback은 사용자 명시 허용 시에만 사용하도록 명시됨
□ fallback 사용 조건과 fallback 기록 위치가 명시됨

**[Tasklist Handoff 구현]**
□ tasklist 생성자(feature-architect-agent), 검토자, 소비자(implementation-agent)가 구분됨
□ tasklist template에 Source / Global Rules / Tasks / Test Commands / Approval이 있음
□ 각 task에 owner, depends_on, files, done_when이 요구됨
□ tasklist 승인 전 production code 수정 금지가 명시됨
□ tasklist 밖 파일 수정, 순서 변경, 범위 확장이 승인 대상으로 명시됨

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
