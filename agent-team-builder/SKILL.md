---
name: agent-team-builder
description: 현재 프로젝트를 분석하여 최적화된 Claude agent team을 자동으로 설계, 검증, 구현, 갱신합니다. 사용자가 "에이전트 팀 만들어줘", "agent team 구성해줘", "멀티에이전트 워크플로우를 설정해줘", "프로젝트에 맞는 에이전트들을 만들어줘", "기존 agent team에 추가/수정해줘", "기존 agent team을 점검만 해줘"처럼 요청하면 사용하세요. Mode Detection, 프로젝트 분석, Bootstrap Interview, 설계, 설계 검증, 사용자 승인, 구현, Reflect 검증, Smoke Test, Workflow Simulation, Registry 갱신 또는 Audit Report 작성을 포함합니다. 프로젝트 구성에 맞는 TDD-first 개발 흐름을 기본 원칙으로 적용하며, Red 검증 이후에만 구현이 진행되도록 agent team을 설계합니다. 선택형 인터뷰와 agent 질문은 터미널 방향키 선택 UI를 우선 사용하도록 설계합니다.
---

# Agent Team Builder

## Reference Loading Policy

항상 먼저 `references/manifest.md`를 로드하여 파일 목적과 로드 조건을 확인하세요.

단계별 reference는 해당 단계 직전에만 lazy loading 하세요.

| 단계 | 로드할 파일 |
|---|---|
| Step 0 | `references/steps/00-mode-detection.md` + `references/policies/operation-modes.md` + `references/policies/registry.md` |
| Step 1 | `references/steps/01-project-analysis.md` + `references/policies/tdd-first.md` |
| Step 2A | `references/steps/02a-bootstrap-interview.md` + `references/policies/terminal-interaction.md` |
| Step 2B | `references/steps/02b-risk-interview.md` + `references/policies/terminal-interaction.md` |
| Step 3 | `references/steps/03-design-spec.md` + `references/policies/security-profiles.md` + `references/policies/tdd-first.md` + `references/policies/terminal-interaction.md` + `references/policies/tasklist-handoff.md` |
| Step 4 | `references/steps/04-design-validation.md` + `references/checklists/context-budget.md` + `references/policies/tdd-first.md` + `references/policies/terminal-interaction.md` + `references/policies/tasklist-handoff.md` |
| Step 4.5 | `references/steps/045-user-approval.md` + `references/policies/approval-and-revalidation.md` |
| Step 5 | `references/steps/05-implementation.md` + `references/policies/file-protection.md` + `references/policies/tdd-first.md` + `references/policies/terminal-interaction.md` + `references/policies/tasklist-handoff.md` + `references/policies/update-safety.md` (Update Mode only) |
| Step 6 | `references/steps/06-reflect-validation.md` + `references/checklists/context-budget.md` + `references/policies/tdd-first.md` + `references/policies/terminal-interaction.md` + `references/policies/tasklist-handoff.md` |
| Step 7A | `references/steps/07a-static-smoke.md` + `references/schemas/registry.schema.json` |
| Step 7B | `references/steps/07b-workflow-simulation.md` |
| Step 8 | `references/steps/08-audit.md` + `references/policies/audit-mode.md` + `references/policies/drift-detection.md` + `references/policies/registry.md` + `references/checklists/context-budget.md` |
| Step 9 | `references/steps/09-registry-update.md` + `references/policies/registry.md` + `references/schemas/registry.schema.json` |

금지:
- `references/` 전체를 한 번에 읽지 마세요.
- 여러 Step 파일을 동시에 미리 로드하지 마세요.
- 현재 단계에서 사용하지 않는 reference를 읽지 마세요.

## Execution Mode

기본 모드는 **Subagent Orchestration**입니다.

- `.claude/agents/*.md`를 생성합니다.
- 메인 Claude가 절차와 조건 분기를 제어하고 subagent를 호출합니다.
- handoff 파일로 agent 간 정보를 전달합니다.

선택 모드인 **Experimental Agent Teams**는 사용자가 병렬 agent team 실행을 명시하고 사전 조건이 충족되는 경우에만 사용합니다.

- 사전 조건: Claude Code v2.1.32+, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, 작업이 독립 파일 단위로 분할 가능
- routine task, 같은 파일 수정, 강한 순서 의존 작업에는 사용하지 마세요.

## Model Alias

| Alias | 실제 모델 ID | 용도 |
|---|---|---|
| `opus` | claude-opus-4-7 | 판단, 추론, 검증 |
| `sonnet` | claude-sonnet-4-6 | 실행, 구현, 코드 작성 |
| `haiku` | claude-haiku-4-5-20251001 | 반복, 기계적 검사 |

설계서에는 alias로 작성하고, Step 5 구현 시 실제 ID로 변환하세요.

## Core Development Policy

agent team은 기본적으로 **Project-Aware TDD-first**를 지향합니다.

- Step 1에서 현재 프로젝트의 테스트 환경을 먼저 식별합니다.
- 새 테스트 프레임워크나 디렉토리 구조를 임의로 도입하지 않습니다.
- 기존 테스트 도구, 파일 배치, fixture/mock 방식, CI 명령을 우선 사용합니다.
- production code 수정은 실패 테스트 작성과 Red 검증 이후에만 허용합니다.
- Red 실패 원인은 기능 미구현이어야 하며 import/config/fixture 오류는 Red 통과로 보지 않습니다.
- 테스트 인프라가 없으면 사용자 승인 전까지 테스트 프레임워크를 추가하지 않고 최소 도입안을 제안합니다.

## Agent Naming Policy

- agent team 자체를 설계하는 책임은 `team-architect-agent` 또는 Step 3 설계서 작성 에이전트로 구분합니다.
- 구성된 team 안에서 기능, API, DB, 테스트 전략, 구현 계획을 설계하는 agent는 `feature-architect-agent`로 부르고, 한글 호칭은 "기능 설계 에이전트"로 고정합니다.
- `design-agent`, `architect-agent`처럼 설계 대상이 불분명한 이름은 사용하지 않습니다.
- 기능 설계 에이전트는 신규 기능 설계 산출 파일을 만들기 전에 사용자에게 선호 파일명을 묻거나 추천 파일명을 제시해 확정합니다.

## Interaction Policy

- 선택형 인터뷰와 agent 질문은 터미널 방향키 선택 UI를 우선 사용합니다.
- 단일 선택은 방향키 + Enter, 복수 선택은 방향키 + Space + Enter로 받습니다.
- 사용자가 선택지를 직접 타이핑하게 만드는 A/B/C 방식은 fallback일 때만 허용합니다.
- 생성된 agent team에는 `.claude/skills/_common/terminal-choice/SKILL.md`와 `.agent-team/tools/terminal_select.py` 사용 규칙을 포함합니다.

## Tasklist Handoff Policy

- 기능 설계 에이전트가 검증 가능한 implementation tasklist를 작성합니다.
- test strategy/red/quality verifier가 tasklist를 검토합니다.
- 구현 에이전트는 승인된 tasklist를 기본 입력으로 받고, 전체 설계서나 긴 검증 로그를 기본 입력으로 받지 않습니다.
- tasklist에 없는 파일 수정, 순서 변경, 범위 확장은 verifier 또는 사용자 승인 없이는 금지합니다.

## Pipeline

```text
Step 0 (Mode Detection + Minimal Preflight)
  Generate
    Step 1 (프로젝트 분석 + Test Environment Profile)
      Step 2A (Bootstrap Interview) / Step 2B (조건부)
        Step 3 (설계 + Project-Aware TDD Gate)
          Step 4 (설계 검증, 최대 3회)
            Step 4.5 (사용자 승인)
            Step 5 (구현 + Terminal Choice/TDD/Tasklist Skill 생성)
                Step 6 (Reflect 검증, 최대 3회)
                  Step 7A (Static Smoke)
                    Step 7B (Workflow Simulation, 필요 시)
                      Step 9 (Registry 갱신)

  Update
    영향 범위 분류(Minor / Moderate / Major)
      Step 3 partial/full refresh (필요 시)
        Step 4
          Step 4.5 (Major 또는 승인 필요 시)
            Step 5 (부분 구현)
              Step 6
                Step 7A
                  Step 7B (topology/security/handoff/trigger/TDD gate 변경 시)
                    Step 9 (Registry 갱신)

  Audit
    Step 8 (Audit Mode)
```

## Step Summary

### Step 0 — Mode Detection
사용자 요청과 `.agent-team/registry.json` 상태를 기준으로 Generate / Update / Audit 중 하나를 선택합니다. Update / Audit 진입 전 Minimal Preflight를 수행합니다.

### Step 1 — 프로젝트 분석
tree depth 3, 최대 300 paths 예산으로 프로젝트를 분석합니다. 보안 도메인과 함께 Test Environment Profile을 반드시 산출합니다.

산출물: `.agent-team/01_project_analysis.md`

### Step 2A — Bootstrap Interview
기본 선택지 Q1~Q5를 terminal-choice 방식으로 묻고, `01_project_analysis.md` 맥락을 반영합니다.

산출물: `.agent-team/02_interview_result.md`

### Step 2B — 위험 기반 추가 질문
고보안, 배포 자동화, 인프라, 인증, 결제, PII, 큰 팀 규모 등이 있으면 Q6~Q9를 terminal-choice 방식으로 추가 질문합니다.

### Step 3 — 설계서 작성
Request Intake Agent는 필수입니다. 보안 프로필, 추가 근거 매트릭스, Project-Aware TDD Gate를 반드시 포함합니다.

산출물: `.agent-team/03_agent_design_spec_v{N}.md`

### Step 4 — 설계서 검증
구조, 안티패턴, 권한, 모델, 보안, 근거 매트릭스, Context Budget, TDD Gate를 검증합니다. 실패하면 최대 3회까지 Step 3으로 돌아갑니다.

산출물: `.agent-team/04_validation_approved.md` 또는 `.agent-team/04_validation_feedback_{N}.md`

### Step 4.5 — 사용자 승인
agent team 브리프를 제시하고 사용자 승인을 받습니다. 구조, 권한, 보안, TDD Gate가 바뀌면 Step 4를 다시 수행합니다.

### Step 5 — 구현
기존 파일은 보호 정책에 따라 백업하고, 마커 블록 또는 전체 파일 생성 규칙을 지킵니다. Request Intake Agent, terminal-choice, tasklist-handoff, doc-updater, tdd-workflow 공통 스킬을 생성합니다.

산출물: `.agent-team/05_implementation_log.md`

### Step 6 — Reflect 검증
구현 파일이 설계와 일치하는지 확인합니다. TDD-first 흐름이 실제 agent 파일에 반영되었는지도 검증합니다. 실패하면 최대 3회까지 Step 5로 돌아갑니다.

산출물: `.agent-team/06_reflect_approved.md` 또는 `.agent-team/06_reflect_feedback_{N}.md`

### Step 7A — Static Smoke Test
`references/scripts/static_smoke.py`를 `.agent-team/tools/static_smoke.py`로 복사해 실행합니다. registry가 있으면 schema validation도 수행합니다.

산출물: `.agent-team/07a_static_smoke_test.md`

### Step 7B — Workflow Simulation
3개 시나리오로 agent 흐름을 시뮬레이션합니다. development request는 TDD gate를 통과해야 합니다.

산출물: `.agent-team/07b_workflow_simulation.md`

### Step 8 — Audit Mode
source/config 파일을 수정하지 않고 registry, context budget, static smoke, drift를 종합 점검합니다.

산출물: `.agent-team/audit_report_{timestamp}.md`

### Step 9 — Registry Update
Generate / Update 완료 후 실제 파일 상태를 기준으로 `.agent-team/registry.json`을 생성 또는 갱신합니다. schema validation 후 저장합니다.

산출물: `.agent-team/09_registry_update.md`

## Output Preservation

영구 보존:
- `.agent-team/01~09*.md`
- `.agent-team/audit_report_*.md`
- `.agent-team/registry.json`
- 설계서, 검증 로그, 구현 로그

임시 또는 ignore 대상:
- `.agent-team/tmp/`
- `.agent-team/backups/`
- `.agent-team/intake_*.md`
- `.claude/handoff/*.md`

기본값: 승인된 최종본은 필요 시 `docs/agent-team/`에도 복사합니다.

## Loop Failure Recovery

실패 유형을 분류한 뒤 자동 복구 가능한 항목은 즉시 수정하고, 사용자 승인이 필요한 항목은 제안 후 대기합니다.

자동 수정 가능:
- YAML/JSON 포맷 오류
- 누락 파일 생성
- hook path 오류
- forbidden 누락
- line count 초과로 reference 분리
- TDD handoff 누락 또는 Red/Green verifier 조건 누락

사용자 승인 필수:
- agent 추가/삭제
- Write, Edit, Bash, MCP 권한 추가
- 보안 책임 변경
- 테스트 프레임워크 신규 도입
- 기존 테스트/CI 구조 변경
