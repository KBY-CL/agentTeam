# Step 7B — Workflow Simulation Test

subagent_type: general-purpose / model: opus
.claude/agents/*.md 전체와 AGENTS.md를 읽고 시뮬레이션하세요.

다음 변경이 있으면 Update Mode에서도 Step 7B를 재실행하세요.
- agent topology 변경
- 보안 프로필 변경
- verifier / security 책임 변경
- handoff 흐름 변경
- agent trigger condition 변경
- tasklist handoff 방식 변경

## 3개 시나리오

### Case 1. 신규 API 엔드포인트 추가
요청: "새 사용자 조회 API 엔드포인트를 추가해줘."
기대 흐름: request-intake-agent → feature-architect-agent(tasklist 생성) → 테스트 책임자 → tasklist verification/red verifier → implementer(tasklist 실행) → green verifier → refactor/quality review → doc-updater

검증:
□ request-intake-agent의 트리거 조건이 이 요청에 맞는가
□ feature-architect-agent가 포함된 설계라면 기능 설계 산출물 파일명 선호를 묻거나 추천 파일명을 제시하는가
□ feature-architect-agent가 implementation tasklist를 생성하는가
□ tasklist에 owner, depends_on, files, done_when, test command가 포함되는가
□ implementation-agent가 승인된 tasklist 없이 production code를 수정하지 않는가
□ implementation-agent가 전체 설계서/긴 로그 대신 tasklist 중심 입력을 받는가
□ Acceptance Criteria와 테스트 범위가 handoff에 기록되는가
□ 기존 프로젝트 테스트 관례를 먼저 확인하는가
□ 실패 테스트 작성 후 Red Verification이 구현보다 먼저 실행되는가
□ Red 실패 원인이 기능 미구현인지 확인하는가
□ implementer가 Red Verifier `[PASS]` 이후 코드 변경을 담당하는가
□ Green Verification이 실제 test/CI command 기준으로 실행되는가
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
