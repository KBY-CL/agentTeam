# Agent Team 구축 가이드

> **이 문서의 목적**
> 이 가이드는 Claude Code(및 Codex/Cursor 혼용 환경)에서 **에이전트 팀을 설계·생성·운영**하기 위한 표준 절차를 정의합니다. 이 문서를 참조한 메인 Claude는 사용자와 **인터뷰 기반**으로 에이전트 팀을 구성하고, 각 구성요소(Skill / Hook / Tool)를 **공통 vs 개별로 분리**해 관리하며, **모든 추가 요소에 대해 반드시 근거(rationale)를 명시**해야 합니다.

> **사용 방법**
> 사용자는 "이 가이드 기반으로 agent team을 만들어줘"라고 요청합니다. 메인 Claude는 본 문서 §6의 인터뷰 프로토콜을 그대로 실행하며, §7의 산출물 체크리스트로 결과를 검증합니다.

---

## 1. 설계 철학

### 1.1 세 가지 절대 원칙

1. **컨텍스트 보존 (Context Preservation)**
   메인 에이전트의 컨텍스트 윈도우는 모든 의사결정의 허브이므로 노이즈를 최소화한다. 무거운 탐색·분석은 서브에이전트의 격리된 컨텍스트로 위임한다.

2. **근거 기반 추가 (Justified Addition)**
   Skill, Hook, Tool, Sub-agent를 추가할 때마다 "왜 필요한가, 무엇을 해결하는가, 왜 기존 구성으로는 부족한가"를 답할 수 있어야 한다. 답할 수 없으면 추가하지 않는다. (YAGNI 원칙 적용)

3. **공통과 개별의 명시적 분리 (Explicit Scope)**
   모든 구성요소는 "공통(common)" 또는 "개별(per-agent)"로 명시적으로 분류한다. 모호한 위치에 두지 않는다.

### 1.2 왜 이 원칙들인가

**컨텍스트 보존이 왜 1순위인가** — 200K 토큰 컨텍스트 윈도우라도 실제 코드베이스 작업에서는 2/3 용량 도달 시점부터 신호 대 잡음비 붕괴로 인한 응답 품질 저하가 관찰된다. 모델을 더 좋은 것으로 바꾸기보다 컨텍스트를 깨끗하게 유지하는 것이 비용 대비 효과가 훨씬 크다.

**근거 기반 추가가 왜 필요한가** — 2026년 ETH Zurich 연구에서 LLM이 자동 생성한 컨텍스트 파일은 작업 성공률을 ~3% 떨어뜨렸고, 컨텍스트 파일 포함 자체가 추론 비용을 20%+ 증가시켰다. "있으면 좋겠지"로 추가된 모든 구성요소는 비용·노이즈·유지보수 부담을 생산한다.

**공통/개별 분리가 왜 중요한가** — 공통 영역에 들어간 모든 것은 모든 에이전트가 매번 받는다. 개별 영역에 들어간 것은 해당 에이전트만 받는다. 이 경계가 흐려지면 컨텍스트 비대화와 권한 누수가 동시에 발생한다.

---

## 2. 시스템 아키텍처

### 2.1 4계층 모델

```
┌──────────────────────────────────────────────────────┐
│  Layer 1: Project Context (정책 - 항상 로드)          │
│  AGENTS.md (크로스 툴) + CLAUDE.md (Claude 전용)      │
└──────────────────────────────────────────────────────┘
                         ↓ 자동 주입
┌──────────────────────────────────────────────────────┐
│  Layer 2: Main Claude (오케스트레이터)                │
│  - 사용자 요청 분석                                    │
│  - 서브에이전트 위임 결정                              │
│  - Handoff 파일 관리                                  │
│  - 최종 검증 및 응답                                   │
└──────────────────────────────────────────────────────┘
                         ↓ 위임
┌──────────────────────────────────────────────────────┐
│  Layer 3: Sub-agents (격리된 워커)                    │
│  각자 독립된 컨텍스트 윈도우 + 자체 system prompt      │
│  + 제한된 tool 접근 + 모델 선택 가능                   │
└──────────────────────────────────────────────────────┘
                         ↓ 호출
┌──────────────────────────────────────────────────────┐
│  Layer 4: Resources (도구·스킬·훅)                    │
│  공통(common) / 개별(per-agent) 명시적 분리            │
└──────────────────────────────────────────────────────┘
```

### 2.2 디렉터리 구조 (Claude Code + AGENTS.md 호환)

```
프로젝트 루트/
├── AGENTS.md                       # 크로스 툴 공통 규칙 (Codex/Cursor도 읽음)
├── CLAUDE.md                       # Claude 전용 + @AGENTS.md import
│
├── .claude/
│   ├── agents/                     # 서브에이전트 정의
│   │   ├── _common/
│   │   │   └── shared-rules.md     # 모든 에이전트가 @ 참조하는 공통 규칙
│   │   ├── analyzer.md
│   │   ├── implementer.md
│   │   ├── verifier.md
│   │   └── infra-reviewer.md
│   │
│   ├── skills/                     # Skill 정의 (Skills 2.0)
│   │   ├── _common/                # 모든 에이전트가 호출 가능
│   │   │   ├── code-search/
│   │   │   │   └── SKILL.md
│   │   │   └── handoff-writer/
│   │   │       └── SKILL.md
│   │   ├── pr-review/              # 특정 에이전트 전용
│   │   │   └── SKILL.md
│   │   └── deploy-check/
│   │       └── SKILL.md
│   │
│   ├── hooks/                      # Hook 스크립트
│   │   ├── _common/                # 전역 적용
│   │   │   ├── block-secrets.sh
│   │   │   └── log-tool-use.sh
│   │   └── per-agent/              # 특정 에이전트만 적용
│   │       ├── implementer-lint.sh
│   │       └── infra-tflint.sh
│   │
│   ├── handoff/                    # 에이전트 간 작업 전달 파일
│   │   └── .gitkeep
│   │
│   └── settings.json               # Hook 매칭 규칙 등
│
└── docs/
    ├── conventions.md              # @ 참조 대상 (코딩 컨벤션)
    ├── architecture.md             # @ 참조 대상 (아키텍처)
    └── tool-inventory.md           # 공통/개별 도구 인벤토리
```

### 2.3 왜 이 구조인가

**AGENTS.md를 별도로 두는 이유** — Codex, Cursor, GitHub Copilot 등이 AGENTS.md를 표준으로 채택하고 있고, Linux Foundation 산하 Agentic AI Foundation이 표준을 관리한다. Claude Code는 2026년 4월 기준 AGENTS.md를 네이티브로 지원하지는 않지만, CLAUDE.md에서 `@AGENTS.md`로 import하면 동일하게 활용 가능하다. 팀에 다른 에이전트 도구 사용자가 있다면 필수.

**`_common/` 접두사를 쓰는 이유** — 디렉터리 이름만으로 "공통"임이 즉시 식별되어, 새 에이전트를 추가하는 사람이 실수로 공통 영역을 오염시킬 가능성을 줄인다. 코드 리뷰 시에도 `_common/` 변경은 영향 범위가 크다는 신호가 된다.

**`handoff/` 디렉터리를 별도로 두는 이유** — 에이전트는 자체 컨텍스트를 유지하지 않는다. 서브에이전트 종료 후 메인이 받는 것은 요약뿐이므로, 다음 에이전트에게 전달할 상세 정보는 파일로 보존해야 한다. 디렉터리를 명시적으로 분리하면 .gitignore 정책(보통 ignore)도 일관되게 적용 가능하다.

---

## 3. CLAUDE.md와 AGENTS.md 역할 분담

### 3.1 역할표

| 항목 | AGENTS.md | CLAUDE.md |
|---|---|---|
| **읽는 도구** | Codex, Cursor, Copilot, Gemini CLI 등 | Claude Code |
| **로드 시점** | 세션 시작 시 (해당 도구가 지원하면) | 매 세션 시작 시 자동 |
| **표현력** | 단순 Markdown | @import, 경로 스코프, 사용자 레벨 오버라이드 |
| **권장 내용** | 프로젝트 아키텍처, 컨벤션, 빌드 명령 등 **공통 사실** | Claude 전용 워크플로우, @AGENTS.md import, 스킬/에이전트 위치 안내 |

### 3.2 작성 원칙

**AGENTS.md는 "사실"만 담는다.** 코드를 보면 알 수 있는 것(예: "TypeScript를 사용함" — `tsconfig.json`만 봐도 자명)은 적지 않는다. 린터가 강제하는 규칙도 적지 않는다. 추론으로는 알 수 없는 **선택과 의도**만 적는다.

**CLAUDE.md는 가볍게 유지한다.** 모든 에이전트와 모든 세션에 매번 주입되므로, "거의 모든 작업에 적용되는 규칙"만 둔다. 가끔만 적용되는 절차는 Skill로 분리한다.

### 3.3 예시

**AGENTS.md 예시:**
```markdown
# Project: 사내 대시보드

## Stack
- Frontend: Vue 3 + TypeScript + Vite
- Backend: FastAPI (Python 3.12)
- Infra: AWS (ECS Fargate, RDS PostgreSQL, CloudFront)
- IaC: Terraform 1.7+

## Hard Constraints
- API 응답 스키마는 backend/schemas/ 의 Pydantic 모델을 단일 진실 공급원(SSOT)으로 한다
- Terraform 변경은 반드시 `terraform plan` 결과를 PR에 첨부한다
- secrets는 AWS Secrets Manager만 사용 (.env 커밋 금지)

## Build & Test
- 프론트: `pnpm dev`, `pnpm test`, `pnpm build`
- 백엔드: `uv run pytest`, `uv run uvicorn main:app --reload`
- 인프라: `terraform fmt && terraform validate && terraform plan`
```

**CLAUDE.md 예시:**
```markdown
# Claude Code Configuration

@AGENTS.md

## Agent Team
이 프로젝트는 .claude/agents/ 의 서브에이전트를 사용합니다.
각 에이전트의 트리거 조건은 해당 .md 파일의 description 필드를 따릅니다.

## Handoff Protocol
- 모든 에이전트 작업 결과는 .claude/handoff/{에이전트명}-{타임스탬프}.md 로 저장
- 다음 에이전트 호출 시 메인이 직전 handoff 파일을 명시적으로 전달
- handoff 파일은 PR 머지 후 정리 (별도 cleanup 스킬)

## Skill Discovery
- 공통 스킬: .claude/skills/_common/
- 에이전트 전용 스킬: 각 에이전트 정의 파일의 frontmatter에 명시
```

---

## 4. Skill 설계 (Skills 2.0 기준)

### 4.1 Skills 2.0의 핵심 변화

2026년 업데이트로 Skill은 다음 기능을 갖는다:

- **Commands와 통합**: 모든 Skill은 자동으로 슬래시 커맨드(`/skill-name`)가 된다
- **서브에이전트에서 사용 가능**: `context: fork` 설정 시 격리된 컨텍스트에서 실행
- **조건부 로딩**: 일반 세션에서는 description만 로드, 호출 시 전체 내용 주입
- **권한 제어**: `disable-model-invocation`, `allowed-tools` 등으로 세밀한 제어
- **Lifecycle hooks**: 스킬 자체에 훅을 결합 가능

### 4.2 공통 스킬 vs 개별 스킬 분류 기준

**공통 스킬에 들어가야 하는 것:**
- 두 개 이상의 에이전트가 호출할 가능성이 있는 워크플로우
- 프로젝트 표준 절차(예: handoff 파일 작성 형식)
- 코드 탐색·검색 같은 범용 동작

**개별 스킬에 들어가야 하는 것:**
- 특정 에이전트의 전문 도메인 절차(예: PR 리뷰 체크리스트는 verifier 전용)
- 다른 에이전트가 실행하면 권한 또는 책임 경계가 모호해지는 작업
- 해당 에이전트의 도메인 지식이 필요한 절차

### 4.3 Skill 정의 템플릿

```markdown
---
name: handoff-writer
description: 에이전트 작업 결과를 표준 형식으로 .claude/handoff/ 에 저장. 모든 서브에이전트가 작업 종료 시 호출.
allowed-tools: [Write, Read]
disable-model-invocation: false
context: inline   # 또는 fork (서브에이전트로 격리 실행)
---

# Handoff Writer Skill

## When to invoke
서브에이전트가 작업을 완료하고 [PASS] 또는 [FAIL]을 결정한 직후.

## Output format
파일명: `.claude/handoff/{agent-name}-{ISO8601-timestamp}.md`

내용 구조:
1. ## Status — [PASS] / [FAIL]
2. ## Summary — 1~3문장 요약
3. ## Key Findings — bullet 형식 핵심 발견
4. ## Files Touched — 변경/생성/조회한 파일 경로
5. ## Next Recommended Agent — (선택) 다음에 호출되어야 할 에이전트
6. ## Open Questions — 해결되지 않은 문제

## Why this exists
서브에이전트는 메인에 요약만 반환하므로, 후속 에이전트가 전체 맥락을 복원하려면 영구 기록이 필요하다.
```

### 4.4 Skill 추가 시 필수 근거 양식

새 Skill을 만들 때 메인 Claude는 사용자에게 다음을 명시해야 한다:

```
[Skill 추가 제안] handoff-writer
- 분류: 공통 (_common/)
- 근거:
  1. 어떤 문제를 해결하는가: 에이전트 간 컨텍스트 전달이 비표준 형식이면 후속 에이전트가 파싱 실패할 수 있음
  2. 기존 구성으로 안 되는 이유: CLAUDE.md에 형식만 명시하면 서브에이전트가 매번 다르게 작성할 위험
  3. 공통으로 두는 이유: 모든 에이전트가 종료 시 호출해야 하므로
- 비용: 약 300토큰 (description만 로드, 호출 시 전체 ~1500토큰)
- 대안 검토: CLAUDE.md에 형식만 명시 → 강제력 없음, 채택 안 함
```

---

## 5. Hook 설계

### 5.1 Hook의 본질

Hook은 AI 추론이 아닌 **결정론적 제어**다. Lifecycle 이벤트(PreToolUse, PostToolUse, SessionStart 등)에서 셸 명령을 실행한다. 품질 게이트, 보안 차단, 자동 포맷팅 등에 사용한다.

### 5.2 공통 Hook vs 개별 Hook 분류 기준

**공통 Hook에 들어가야 하는 것:**
- 보안 차단(secrets 커밋 방지, `rm -rf` 차단 등)
- 감사 로그(모든 Bash 실행 기록)
- 프로젝트 전역 정책(예: 모든 파일 저장 후 trailing whitespace 제거)

**개별 Hook에 들어가야 하는 것:**
- 특정 에이전트가 작성한 코드만 검사(예: implementer가 쓴 .ts 파일만 ESLint)
- 특정 도메인 전용 검증(예: infra-reviewer가 .tf 파일 변경 시 tflint)
- 해당 에이전트가 책임지는 산출물에만 적용되는 후처리

### 5.3 settings.json 매칭 패턴

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/_common/block-secrets.sh" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/_common/log-tool-use.sh" }
        ]
      },
      {
        "matcher": "Write",
        "agent": "implementer",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/per-agent/implementer-lint.sh" }
        ]
      },
      {
        "matcher": "Write",
        "agent": "infra-reviewer",
        "hooks": [
          { "type": "command", "command": ".claude/hooks/per-agent/infra-tflint.sh" }
        ]
      }
    ]
  }
}
```

### 5.4 Hook 추가 시 필수 근거 양식

```
[Hook 추가 제안] block-secrets
- 분류: 공통 (_common/, PreToolUse + Bash matcher)
- 근거:
  1. 어떤 문제를 해결하는가: AWS 키, GitHub 토큰 등이 git commit에 포함되는 사고 방지
  2. AI 판단으로 처리하지 않는 이유: 100% 차단이 필요한 보안 사항이므로 결정론이 필수
  3. 공통으로 두는 이유: 모든 에이전트의 모든 Bash 호출에 적용되어야 함
- 검사 비용: 매 Bash 호출당 ~50ms
- 우회 가능성: 현재 정규식은 일반적인 패턴만 잡음. 추후 truffleHog 같은 도구로 강화 가능
```

---

## 6. Tool (MCP) 설계

### 6.1 도구 분류 원칙

**공통 도구(모든 에이전트가 사용 가능)에 들어가야 하는 것:**
- Read, Grep, Glob — 코드베이스 탐색에 보편적으로 필요
- Write, Edit — 단, 일부 에이전트(read-only verifier 등)는 제외
- 표준 MCP(예: 사내 위키 검색)

**개별 도구(특정 에이전트만)에 들어가야 하는 것:**
- Bash — 실행 권한이 큰 에이전트만(implementer, infra-reviewer 등)
- 외부 시스템 변경 MCP(예: AWS API, Jira 생성/수정 등)
- 검증·읽기 전용 MCP(예: Datadog 조회 → verifier 전용)

### 6.2 도구 인벤토리 문서

`docs/tool-inventory.md`에 다음 형식으로 관리:

```markdown
# Tool Inventory

## Common (모든 에이전트 기본 부여)
| Tool | 목적 | 위험도 |
|---|---|---|
| Read | 파일 읽기 | 낮음 |
| Grep | 패턴 검색 | 낮음 |
| Glob | 파일 경로 패턴 매칭 | 낮음 |

## Per-Agent
| Tool | 부여 대상 | 근거 |
|---|---|---|
| Write | analyzer, implementer | analyzer는 분석 보고서 작성, implementer는 코드 수정 |
| Edit | implementer | 코드 수정의 핵심 도구 |
| Bash | implementer, infra-reviewer | implementer는 빌드/테스트, infra-reviewer는 terraform plan |
| mcp__aws__describe_* | infra-reviewer | AWS 리소스 조회. 변경 권한은 부여하지 않음 |
| mcp__datadog__query | verifier | 메트릭/로그 조회로 배포 검증 |

## Forbidden (어떤 에이전트에도 부여하지 않음)
| Tool | 이유 |
|---|---|
| mcp__aws__delete_* | 인프라 삭제는 사람만 |
| mcp__github__delete_repo | 동일 |
```

### 6.3 도구 추가 시 필수 근거 양식

```
[Tool 추가 제안] mcp__datadog__query
- 분류: 개별 (verifier 전용)
- 근거:
  1. 어떤 문제를 해결하는가: 배포 후 에러율·레이턴시 검증을 위해 Datadog 메트릭 조회 필요
  2. 다른 에이전트에 부여하지 않는 이유: 검증은 verifier의 단일 책임. 다른 에이전트가 메트릭에 의존하면 책임 경계 모호
  3. 공통이 아닌 이유: implementer/analyzer는 메트릭이 필요 없음. 공통화 시 컨텍스트 노이즈만 증가
- 권한 범위: 읽기 전용 (query만, 알람/대시보드 생성 권한 없음)
- 비용: 호출당 약 100토큰 (응답 크기에 따라 가변)
```

---

## 7. 에이전트 정의 작성

### 7.1 에이전트 정의 템플릿

```markdown
---
name: infra-reviewer
description: Terraform/CloudFormation 변경 사항을 검토하고 보안·비용·운영성 관점에서 [PASS]/[FAIL] 판정. 인프라 코드(.tf, .yaml in infra/) 변경이 감지되면 호출.
model: sonnet
tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__aws__describe_instances
  - mcp__aws__describe_security_groups
---

@_common/shared-rules.md
@docs/architecture.md

# Role
인프라 변경의 안전성·비용·운영성을 독립적으로 검증한다.

# Workflow
1. 변경된 .tf / .yaml 파일을 Read
2. `terraform plan` 결과 확인 (Bash)
3. 영향받는 리소스를 mcp__aws 도구로 현재 상태 조회
4. 다음 항목 체크:
   - 보안 그룹 0.0.0.0/0 노출 여부
   - 암호화 미적용 리소스
   - 명시적 태그 누락
   - 예상 월간 비용 증가 (수동 추정)
5. handoff-writer 스킬 호출하여 결과 저장
6. 메인에 [PASS] 또는 [FAIL] + 1~3문장 요약 반환

# Output Contract
- [PASS]: 모든 체크 통과
- [FAIL]: 하나라도 실패 시. 반드시 실패 항목과 권장 조치 명시

# Skills Available
- handoff-writer (공통)
- terraform-cost-estimate (개별, .claude/skills/terraform-cost-estimate/)

# Forbidden
- 인프라 변경 직접 적용 금지 (apply 명령 실행 금지)
- IAM 정책 수정 제안 금지 (별도 보안 리뷰 필요)
```

### 7.2 에이전트 추가 시 필수 근거 양식

```
[Sub-agent 추가 제안] infra-reviewer
- 모델: sonnet (이유: 보안 판단이 필요해 haiku로는 위험, opus는 과한 비용)
- 컨텍스트 격리 이유: terraform plan 출력이 수천 줄이라 메인 컨텍스트 오염 방지
- 부여 도구: Read, Grep, Glob, Bash, mcp__aws__describe_* (조회만)
  - 변경 권한 미부여 근거: 검토자가 직접 변경하면 검토-실행 분리 원칙 위반
- 부여 스킬: handoff-writer(공통), terraform-cost-estimate(개별)
- 적용 훅: infra-tflint.sh (PostToolUse + Write)
- 다른 에이전트와의 책임 경계:
  - implementer: 인프라 코드 작성 ↔ infra-reviewer: 검토만
  - verifier: 배포 후 런타임 검증 ↔ infra-reviewer: 배포 전 정적 검증
```

---

## 8. Handoff 설계

### 8.1 Handoff 파일이 필요한 이유

서브에이전트는 작업 종료 시 메인에 **요약만** 반환한다. 모든 중간 산출물(파일 목록, 분석 세부사항, 테스트 출력 등)은 격리된 컨텍스트와 함께 사라진다. 다음 에이전트가 이 정보가 필요하면 파일로 보존된 형태에서만 복원할 수 있다.

### 8.2 Handoff 파일 표준 형식

```markdown
# Handoff: {agent-name}
- Timestamp: 2026-04-23T14:32:00+09:00
- Status: [PASS] | [FAIL]
- Triggered by: {user request 한 줄 요약}

## Summary
1~3문장으로 작업 결과 요약.

## Key Findings
- 발견 1
- 발견 2
- 발견 3

## Files Touched
- read: src/api/users.py
- modified: src/api/users.py:L45-L78
- created: tests/test_users.py

## Decisions Made
- 결정 1과 그 근거
- 결정 2와 그 근거

## Next Recommended Agent
verifier — 변경된 API에 대한 통합 테스트 검증 필요

## Open Questions
- DB 마이그레이션 시점이 명확하지 않음. 사용자 확인 필요.
```

### 8.3 Handoff 흐름 패턴

**순차 흐름 (가장 일반적):**
```
사용자 요청
  → 메인이 analyzer 호출 → analyzer 작업 → handoff 파일 작성 → 메인에 요약 반환
  → 메인이 handoff 파일 경로를 implementer에 전달 → implementer 작업 → handoff 작성 → 요약 반환
  → 메인이 verifier 호출 (이전 두 handoff 모두 전달) → verifier 검증 → 최종 [PASS]/[FAIL]
  → 메인이 사용자에 최종 응답
```

**병렬 흐름 (Agent Teams 또는 다중 Task):**
```
사용자 요청
  → 메인이 analyzer + infra-reviewer + security-reviewer 동시 호출
  → 각자 handoff 파일 작성
  → 메인이 세 handoff를 종합해 implementer에 전달
  → implementer 작업 → 메인에 결과 반환
```

### 8.4 Handoff 관리 정책

- **저장 위치**: `.claude/handoff/{agent-name}-{ISO8601-timestamp}.md`
- **버전 관리**: 기본적으로 .gitignore (작업 산출물이지 영구 자산이 아님)
- **보관 기간**: PR 머지 후 cleanup 스킬로 정리 (또는 7일 후 자동 삭제)
- **참조 방식**: 메인이 다음 에이전트 호출 시 프롬프트에 파일 경로를 명시적으로 포함

---

## 9. 인터뷰 프로토콜 (메인 Claude의 실행 절차)

이 가이드 기반으로 "agent team을 만들어줘" 요청을 받은 메인 Claude는 다음 순서로 사용자와 인터뷰를 진행한다.

### Phase 1: 도메인 파악
사용자에게 다음을 질문(이때 가능하면 ask_user_input_v0 같은 선택형 도구 사용):
1. 프로젝트 도메인은? (예: 웹 앱, 데이터 파이프라인, 인프라 자동화)
2. 주요 기술 스택은?
3. 다른 AI 에이전트 도구(Codex, Cursor 등) 사용 여부?
4. 팀 규모와 협업 패턴?

### Phase 2: 워크플로우 도출
사용자가 자주 수행하는 작업 유형을 3~5개 도출:
- "어떤 종류의 작업이 가장 반복적으로 발생하나요?"
- "검증·리뷰가 별도로 필요한 작업이 있나요?"
- "절대 자동화하면 안 되는 작업은?"

### Phase 3: 에이전트 후보 제안
도출된 워크플로우를 기반으로 에이전트 3~6개를 후보로 제시. 각 후보마다:
- 이름과 역할
- 왜 별도 에이전트로 분리해야 하는지 근거
- 메인에서 직접 처리하지 않는 이유

사용자 승인 후 다음 단계 진행.

### Phase 4: 구성요소 분류
승인된 각 에이전트에 대해:

1. **공통 vs 개별 분류**
   각 에이전트가 필요로 하는 Skill/Hook/Tool 목록을 작성.
   같은 항목이 2개 이상 에이전트에 등장하면 → 공통 후보.
   1개 에이전트에만 등장하면 → 개별.
   사용자에게 분류안 제시 후 승인.

2. **각 항목의 추가 근거 명시**
   §4.4, §5.4, §6.3, §7.2의 양식을 따라 각 추가 항목의 근거를 정리.
   사용자가 "이건 빼자"라고 하면 즉시 제거.

### Phase 5: 파일 생성
사용자 최종 승인 후:
1. AGENTS.md 작성/업데이트
2. CLAUDE.md 작성/업데이트
3. .claude/agents/*.md 생성
4. .claude/skills/_common/, .claude/skills/{개별}/ 생성
5. .claude/hooks/_common/, .claude/hooks/per-agent/ 생성
6. .claude/settings.json 작성
7. docs/tool-inventory.md 작성

### Phase 6: 검증
§10의 체크리스트를 실행하고 결과를 사용자에게 보고.

---

## 10. 산출물 검증 체크리스트

에이전트 팀 생성 완료 후 메인 Claude는 다음을 모두 확인하고 사용자에게 보고한다.

### 구조 검증
- [ ] AGENTS.md가 프로젝트 루트에 존재하고, 도구 비종속적인 사실만 포함
- [ ] CLAUDE.md가 `@AGENTS.md`를 import
- [ ] CLAUDE.md가 200줄 이하 (가벼움 유지)
- [ ] .claude/agents/, .claude/skills/, .claude/hooks/, .claude/handoff/ 디렉터리 존재
- [ ] _common/ 접두사로 공통 영역이 명시적으로 구분됨

### 에이전트 검증
- [ ] 각 에이전트가 단일 책임 원칙을 따름 (한 에이전트가 분석+구현+검증을 동시에 하지 않음)
- [ ] 각 에이전트의 description이 트리거 조건을 명확히 명시
- [ ] 각 에이전트의 tools 목록이 docs/tool-inventory.md와 일치
- [ ] 검증자(verifier) 역할의 에이전트가 별도로 존재 (또는 의도적 제외 근거 문서화)
- [ ] 각 에이전트의 출력 계약([PASS]/[FAIL] 형식 등)이 명시됨

### 근거 검증
- [ ] 모든 추가된 Skill에 대해 §4.4 양식의 근거가 문서화됨
- [ ] 모든 추가된 Hook에 대해 §5.4 양식의 근거가 문서화됨
- [ ] 모든 추가된 Tool에 대해 §6.3 양식의 근거가 문서화됨
- [ ] 모든 추가된 Sub-agent에 대해 §7.2 양식의 근거가 문서화됨

### 운영 검증
- [ ] handoff-writer 스킬이 공통 영역에 존재
- [ ] settings.json의 hook 매칭 패턴이 공통/개별로 명확히 구분됨
- [ ] tool-inventory.md에 Forbidden 도구 목록이 존재
- [ ] .gitignore에 `.claude/handoff/*.md` 추가됨 (영구 자산이 아닌 경우)

### 컨텍스트 비용 추정
- [ ] CLAUDE.md + AGENTS.md + 모든 _common 참조의 총 토큰 수 추정 (목표: 5,000 토큰 이하)
- [ ] 에이전트별 평균 시작 컨텍스트 추정 (목표: 10,000 토큰 이하)

---

## 11. 안티패턴 (피해야 할 것)

### 11.1 "만능 에이전트"
한 에이전트가 분석·구현·검증·배포를 모두 처리하도록 설계하는 것. **금지.**
이유: 단일 책임 원칙 위반, 검증 독립성 상실, 컨텍스트 비대화.

### 11.2 "공통이 비대해지는 _common"
의심스러우면 일단 공통에 넣는 습관. **금지.**
이유: 공통은 모든 에이전트가 매번 받는다. 새 항목을 공통에 넣을 때는 "정말로 모든 에이전트가 필요로 하는가"를 두 번 묻는다.

### 11.3 "근거 없는 추가"
"있으면 좋겠지" "나중에 쓸 수도" "AI 트렌드라" 같은 사유로 추가. **금지.**
이유: ETH Zurich 연구 결과 — 근거 없는 컨텍스트 추가는 성공률을 오히려 낮추고 비용은 20%+ 증가시킨다.

### 11.4 "메인이 직접 다 하기"
서브에이전트를 만들지 않고 메인이 모든 무거운 작업을 직접 처리. **상황에 따라 금지.**
이유: 메인 컨텍스트가 빠르게 오염되어 후속 응답 품질 저하.
예외: 작업이 단발성이고 200~500토큰 이내로 끝나는 경우.

### 11.5 "Handoff 파일 없이 구두 전달"
서브에이전트의 결과를 메인이 자기 컨텍스트에만 보관하고 다음 에이전트에 구두로 요약 전달. **금지.**
이유: 메인 컨텍스트가 압축되거나 세션이 종료되면 모두 손실. handoff 파일은 영속성을 위한 안전장치.

### 11.6 "AGENTS.md에 워크플로우 절차 작성"
"PR 만드는 법", "배포 절차" 같은 가끔 쓰는 절차를 AGENTS.md에 작성. **금지.**
이유: AGENTS.md는 모든 세션에 항상 로드되는 정책 영역. 가끔 쓰는 절차는 Skill로 분리해 on-demand 로딩.

### 11.7 "Hook으로 AI 판단을 대체하려는 시도"
복잡한 코드 품질 판단을 Hook의 셸 스크립트로 처리하려는 시도. **금지.**
이유: Hook은 결정론적 제어용. AI 판단이 필요한 영역은 verifier 같은 에이전트로 처리.

---

## 12. 요청 양식 (사용자가 메인 Claude에게 전달하는 트리거 문구)

사용자는 다음 양식 중 하나로 메인 Claude에게 요청:

**짧은 양식:**
```
@docs/agent-team-guide.md 기반으로 agent team을 만들어줘.
```

**상세 양식:**
```
@docs/agent-team-guide.md 기반으로 agent team을 만들어줘.

프로젝트 정보:
- 도메인: {도메인}
- 주요 기술: {스택}
- 사용 도구: Claude Code + {추가 도구}

특별 요구사항:
- {예: 인프라 변경은 반드시 별도 검토 에이전트 필요}
- {예: 성능 메트릭 검증 자동화}
```

메인 Claude는 트리거 받은 즉시 §9 인터뷰 프로토콜의 Phase 1부터 시작한다.

---

## 부록 A: 빠른 참조 카드

### "공통 vs 개별" 판단 플로우차트
```
이 항목이 필요한 에이전트가 몇 개인가?
├── 1개 → 개별
├── 2개 이상 → 공통 후보
└── 모든 에이전트 → 공통 (확정)

공통 후보일 경우 추가 질문:
├── 모든 에이전트가 매번 필요로 하는가?
│   ├── 예 → 공통
│   └── 아니오 → 사용하는 에이전트들에 개별 부여
```

### "Skill로 만들 것인가, CLAUDE.md에 적을 것인가" 판단
```
이 절차가 적용되는 빈도는?
├── 거의 모든 작업 → CLAUDE.md
├── 가끔 (특정 조건 충족 시) → Skill
└── 한 번뿐 → 그냥 사용자 메시지로 전달
```

### "Hook으로 처리할 것인가, 에이전트로 처리할 것인가" 판단
```
이 검사/처리가 결정론적인가?
├── 예 (정규식, 명령 실행 결과 등) → Hook
└── 아니오 (판단·해석 필요) → 에이전트
```

---

## 부록 B: 참고 자료

- Claude Code 공식 문서: https://code.claude.com/docs
- AGENTS.md 표준: https://agents.md
- Skills 2.0 발표 (2026년 3월)
- ETH Zurich, "Evaluating AGENTS.md" (2026년 2월)
