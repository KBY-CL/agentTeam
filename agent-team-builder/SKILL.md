---
name: agent-team-builder
description: 현재 프로젝트를 분석하여 최적화된 에이전트 팀을 자동으로 설계·검증·구현·감사합니다. 사용자가 "에이전트 팀을 만들어줘", "agent team을 구성해줘", "멀티에이전트 워크플로우를 설정해줘", "에이전트 설계해줘", "프로젝트에 맞는 에이전트들을 만들어줘", "기존 agent team을 점검해줘", "기존 agent team을 업데이트해줘"와 같이 요청하면 반드시 이 스킬을 사용하세요. Mode Detection → 프로젝트 분석 → Bootstrap Interview(2단계) → 설계(근거 매트릭스) → 설계 검증(도메인 보안) → 사용자 승인(재검증 포함) → 구현(파일 보호) → Reflect 검증 → Smoke Test(스크립트+시뮬레이션) → Registry 갱신 또는 Audit Report 작성까지 포함한 생명주기 파이프라인을 자동으로 실행합니다.
---

# Agent Team Builder

## Reference Loading Policy

**항상 로드 (스킬 시작 시):**
- `references/manifest.md` — 각 파일의 목적과 로드 조건 인덱스

**단계별 Lazy Loading (해당 단계 직전에만 로드):**

| 단계 | 로드할 파일 |
|---|---|
| Step 0 | `references/steps/00-mode-detection.md` + `references/policies/operation-modes.md` + `references/policies/registry.md` |
| Step 1 | `references/steps/01-project-analysis.md` |
| Step 2A | `references/steps/02a-bootstrap-interview.md` |
| Step 2B | `references/steps/02b-risk-interview.md` |
| Step 3 | `references/steps/03-design-spec.md` + `references/policies/security-profiles.md` |
| Step 4 | `references/steps/04-design-validation.md` + `references/checklists/context-budget.md` |
| Step 4.5 | `references/steps/045-user-approval.md` + `references/policies/approval-and-revalidation.md` |
| Step 5 | `references/steps/05-implementation.md` + `references/policies/file-protection.md` + `references/policies/update-safety.md` (Update Mode only) |
| Step 6 | `references/steps/06-reflect-validation.md` + `references/checklists/context-budget.md` |
| Step 7A | `references/steps/07a-static-smoke.md` + `references/schemas/registry.schema.json` |
| Step 7B | `references/steps/07b-workflow-simulation.md` |
| Step 8 | `references/steps/08-audit.md` + `references/policies/audit-mode.md` + `references/policies/drift-detection.md` + `references/policies/registry.md` + `references/checklists/context-budget.md` |
| Step 9 | `references/steps/09-registry-update.md` + `references/policies/registry.md` + `references/schemas/registry.schema.json` |

**금지:**
- references/ 전체 일괄 Read 금지
- 여러 Step 파일을 동시에 로드 금지
- 현재 단계에서 사용하지 않는 파일 Read 금지

---

## Execution Mode

**기본 모드: Subagent Orchestration** (이 스킬의 기본값)
- `.claude/agents/*.md` 생성
- 메인 Claude가 순차/조건부로 subagent 호출
- handoff 파일로 정보 전달

**선택 모드: Experimental Agent Teams** (사용자가 병렬 작업을 명시한 경우만)
- 사전 조건: Claude Code v2.1.32+, `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, 작업이 독립 파일 단위로 나뉨
- routine task, 같은 파일 수정, 강한 의존 작업에는 사용 금지

---

## 모델 Alias

| Alias | 실제 모델 ID | 용도 |
|---|---|---|
| `opus` | claude-opus-4-7 | 판단·추론·검증 |
| `sonnet` | claude-sonnet-4-6 | 실행·구현·코드 작성 |
| `haiku` | claude-haiku-4-5-20251001 | 반복·기계적 검사 |

설계서에는 alias로 작성. Step 5 구현 시 위 표의 실제 ID로 변환.

---

## 파이프라인 흐름

```
Step 0 (Mode Detection + Minimal Preflight)
  ├── Generate
  │     → Step 1 (프로젝트 분석)
  │       → Step 2A (Bootstrap Interview) → Step 2B (조건부)
  │         → Step 3 (설계) ⟵ Step 4 (검증, 최대 3회)
  │           → Step 4.5 (사용자 승인)
  │             → Step 5 (구현) ⟵ Step 6 (Reflect, 최대 3회)
  │               → Step 7A (Static Smoke)
  │                 → Step 7B (Workflow Simulation, 필요 시)
  │                   → Step 9 (Registry 갱신) → 최종 보고
  ├── Update
  │     → 영향 범위 분류(Minor / Moderate / Major)
  │       → Step 3 partial/full refresh (필요 시) → Step 4
  │         → Step 4.5 (Major 또는 승인 필요 시)
  │           → Step 5 (부분 구현) → Step 6 → Step 7A
  │             → Step 7B (topology/security/handoff/trigger 변경 시)
  │               → Step 9 (Registry 갱신) → 최종 보고
  └── Audit
        → Step 8 (Audit Mode) → 최종 보고
```

---

## 단계별 실행 요약

### Step 0 — Mode Detection (메인 Claude 직접)
사용자 요청과 `registry.json` 상태를 기준으로 Generate / Update / Audit 중 하나를 선택.
Update / Audit 진입 시 Minimal Preflight 수행.

### Step 1 — 프로젝트 분석 (Explore / sonnet)
탐색 예산 적용: tree depth 3, 최대 300 paths, 카테고리별 파일 수 제한.
보안 도메인 자동 탐지(웹/인프라/데이터/AI·RAG).
산출물: `.agent-team/01_project_analysis.md`

### Step 2A — Bootstrap Interview (메인 Claude 직접)
기본 선택형 Q1~Q5. 01_project_analysis.md 맥락 기반.
산출물: `.agent-team/02_interview_result.md`

### Step 2B — 위험도 기반 추가 질문 (조건부)
Q3=C, 배포 자동화, 인프라/인증/결제 코드, 팀 C/D 중 해당 시 수행.
Q6~Q9 추가 질문.

### Step 3 — 설계서 작성 (general-purpose / opus)
Request Intake Agent 필수 + 도메인 보안 프로필 + **추가 근거 매트릭스** 필수.
skills: frontmatter에는 반드시 필요한 소형 스킬만. doc-updater는 본문 호출 조건으로 명시.
루프 변수: `design_loop = 1` (최대 3)
산출물: `.agent-team/03_agent_design_spec_v{N}.md`

### Step 4 — 설계서 검증 (general-purpose / opus)
구조·안티패턴·권한·모델·보안·근거 매트릭스 + **Context Budget Gate** 검증.
[PASS] → Step 4.5 / [FAIL] → design_loop 증가 후 Step 3 재호출
산출물: `.agent-team/04_validation_approved.md` 또는 `04_validation_feedback_{N}.md`

### Step 4.5 — 사용자 승인 (메인 Claude 직접)
에이전트 팀 브리핑 후 A~E 선택. 구조/권한/보안 변경 시 Step 4 재실행.

### Step 5 — 구현 (general-purpose / sonnet)
기존 파일 백업 → 마커 블록 수정 → 전체 파일 생성.
Request Intake Agent + doc-updater 스킬 필수 생성.
skills: frontmatter 남용 금지 — 에이전트 본문에 호출 조건만 명시.
Update Mode에서는 `references/policies/update-safety.md`의 impact scope와 수정 범위 제한을 따름.
루프 변수: `reflect_loop = 1` (최대 3)
산출물: `.agent-team/05_implementation_log.md`

### Step 6 — Reflect 검증 (general-purpose / opus)
구현 파일 + **Context Budget Gate** 검증.
[PASS] → Step 7A / [FAIL] → reflect_loop 증가 후 Step 5 재호출
산출물: `.agent-team/06_reflect_approved.md` 또는 `06_reflect_feedback_{N}.md`

### Step 7A — Static Smoke Test (general-purpose / haiku)
`references/scripts/static_smoke.py`를 `.agent-team/tools/static_smoke.py`로 복사해 실행.
registry가 있으면 `registry.schema.json` 검증도 포함.
AI는 FAIL 항목의 관련 파일 일부만 읽음.
산출물: `.agent-team/07a_static_smoke_test.md`

### Step 7B — Workflow Simulation (general-purpose / opus)
3개 시나리오 에이전트 흐름 시뮬레이션.
Update Mode에서는 topology, security profile, verifier/security 책임, handoff 흐름, agent trigger condition 변경 시 재실행.
산출물: `.agent-team/07b_workflow_simulation.md`

### Step 8 — Audit Mode (메인 Claude 또는 general-purpose / opus)
source/config 파일을 수정하지 않고 registry, context budget, static smoke, drift를 종합 점검.
산출물: `.agent-team/audit_report_{timestamp}.md`

### Step 9 — Registry Update (메인 Claude 직접)
Generate / Update 완료 후 실제 상태를 바탕으로 `.agent-team/registry.json`을 생성 또는 갱신.
schema validation 후 저장.
산출물: `.agent-team/09_registry_update.md`

---

## 산출물 보존 정책

**영구 보존 (ignore 금지):**
`.agent-team/01~09*.md`, `.agent-team/audit_report_*.md`, `.agent-team/registry.json`, 설계서·검증·승인·로그 파일

**임시 (ignore 대상):**
`.agent-team/tmp/`, `.agent-team/backups/`, `.agent-team/intake_*.md`, `.claude/handoff/*.md`

기본값: 승인된 최종본을 `docs/agent-team/`에도 복사

---

## 루프 실패 시 복구

실패 유형 분류 후 자동 복구 가능 항목은 즉시 수정, 사용자 승인 필요 항목은 제안 후 대기.

**자동 수정 가능:** YAML/JSON 포맷 오류, 누락 파일 생성, hook path 오타, forbidden 누락, line count 초과 시 reference 분리

**승인 필수:** 에이전트 추가/삭제, Write·Edit·Bash·MCP 권한 추가, 보안 책임 변경, 마커 외부 수정
