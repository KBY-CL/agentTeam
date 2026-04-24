# Step 4 — 설계서 검증 에이전트

subagent_type: general-purpose / model: opus
**설계서 자체**가 올바른지 검증. 구현 검증 아님.
context-budget.md 체크리스트도 이 단계에서 함께 적용.

## 입력
1. .agent-team/03_agent_design_spec_v{N}.md
2. .agent-team/02_interview_result.md
3. references/checklists/context-budget.md (이 단계에서 함께 로드)

## 체크리스트

**[구조]**
□ 에이전트 수 3~6개 / 단일 책임 / 역할 중복 없음
□ Request Intake Agent 포함, 파일명 request-intake-agent.md, 선택지 기반 구조

**[안티패턴]** (agent-team-guide.md §안티패턴 섹션 기준)
□ 만능 에이전트 없음 / _common 비대화 없음 / 근거 없는 추가 없음
□ 메인이 직접 다 하는 패턴 없음 / Handoff 없는 구두 전달 없음
□ AGENTS.md에 워크플로우 절차 없음 / Hook으로 AI 판단 대체 없음

**[권한]**
□ tools가 역할에 적합 / 과도한 권한 없음 / 공통·개별 분리 적절
□ skills: frontmatter에 소형·필수 스킬만, 대형 스킬은 본문 호출 조건으로 명시

**[모델]**
□ alias(opus/sonnet/haiku)가 역할에 맞게 배정

**[인터뷰 반영]**
□ Q1·Q3·Q5 반영 / Q6(자동화 금지) → forbidden 반영

**[근거 매트릭스]**
□ 추가 근거 매트릭스 섹션 존재
□ Sub-agent·Skill·Hook·Tool 각각 이유·대안 있음
□ skills preload 여부 및 근거 명시

**[보안 — Common]**
□ secrets 하드코딩 금지 / 외부 입력 검증 / 최소 권한 / 로그 민감정보 금지 / 의존성 취약점

**[보안 — Web (해당 시)]**
□ OWASP Top 10 / CSRF·XSS·CORS·CSP / 인증·세션·IDOR / 입력 검증·출력 인코딩

**[보안 — Infrastructure (해당 시)]**
□ apply 금지·승인 / IAM wildcard 금지 / public ingress 검토

**[보안 — DataPipeline (해당 시)]**
□ PII 마스킹 / 원본 접근 제한 / 로그에 원본 금지

**[보안 — AI·RAG (해당 시)]**
□ 프롬프트 인젝션 방어 / retrieval source 검증 / 민감 문서 검색 제한

**[Context Budget]**
→ references/checklists/context-budget.md 항목 적용

## 결과 저장
통과 → `.agent-team/04_validation_approved.md`
실패 → `.agent-team/04_validation_feedback_{loop}.md`
  (문제점: 위치·문제·권장 수정 / 보안 미비사항 / 수정 우선순위)

마지막 줄: [PASS] 또는 [FAIL]
