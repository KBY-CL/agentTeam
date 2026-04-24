# Step 7B — Workflow Simulation Test

subagent_type: general-purpose / model: opus
.claude/agents/*.md 전체와 AGENTS.md를 읽고 시뮬레이션하세요.

다음 변경이 있으면 Update Mode에서도 Step 7B를 재실행하세요.
- agent topology 변경
- 보안 프로필 변경
- verifier / security 책임 변경
- handoff 흐름 변경
- agent trigger condition 변경

## 3개 시나리오

### Case 1. 신규 API 엔드포인트 추가
요청: "새 사용자 조회 API 엔드포인트를 추가해줘."
기대 흐름: request-intake-agent → implementer → verifier → doc-updater

검증:
□ request-intake-agent의 트리거 조건이 이 요청에 맞는가
□ implementer가 코드 변경을 담당하는가
□ verifier가 테스트·보안 검토를 담당하는가
□ doc-updater 호출 조건이 구현 에이전트 본문에 명시되어 있는가
□ handoff 경로가 각 에이전트 description에 연결되는가

### Case 2. 고위험 변경
프로젝트에 인프라 또는 인증·결제 코드가 있으면:
  인프라: "Terraform 보안그룹 인바운드 규칙을 수정해줘."
  결제·인증: "결제 API 핸들러를 수정해줘."
없으면 [SKIP].

검증:
□ Q6(자동화 금지) 항목이 forbidden에 명시되어 있는가
□ 해당 에이전트가 apply·직접 실행 전 사용자 승인을 요청하는 구조인가
□ 고위험 에이전트가 read-only 또는 승인 요청 패턴을 갖는가

### Case 3. 문서만 수정
요청: "README에 설치 방법을 추가해줘."
기대: main 또는 doc-updater (implementer 불필요)

검증:
□ 불필요한 implementer를 유발하는 트리거 조건이 없는가
□ doc-updater가 문서 수정 요청에 단독 대응 가능한가

## 산출물: `.agent-team/07b_workflow_simulation.md`

```
# Workflow Simulation 리포트

## Case 1 — 신규 API
예상 흐름: {트리거 조건 기반}
검증 결과: 항목별 PASS/FAIL

## Case 2 — 고위험 변경 (또는 SKIP)
## Case 3 — 문서 수정

## 전체 요약
연결 성공 X / 실패 Y / 스킵 Z
미연결·흐름 단절 에이전트: (있으면 목록)
```
