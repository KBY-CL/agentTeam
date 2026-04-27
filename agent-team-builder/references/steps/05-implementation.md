# Step 5 — 구현 에이전트

subagent_type: general-purpose / model: sonnet
file-protection.md도 이 단계에서 로드하세요.

## 입력
1. .agent-team/04_validation_approved.md + 최신 설계서
2. references/policies/file-protection.md (이 단계에서 함께 로드)
3. references/policies/tdd-first.md (이 단계에서 함께 로드)
4. references/policies/terminal-interaction.md (이 단계에서 함께 로드)
5. references/policies/tasklist-handoff.md (이 단계에서 함께 로드)
[재호출 시] 6. .agent-team/06_reflect_feedback_{N}.md (지적 파일만 수정)

## 생성할 파일

**AGENTS.md** — 가이드 §3 형식, 도구 비종속 사실만

**CLAUDE.md** — 기존 있으면 마커 블록에 "## Agent Team" 섹션 추가, 없으면 신규
```
<!-- AGENT_TEAM_START -->
## Agent Team
...
<!-- AGENT_TEAM_END -->
```

**.claude/agents/*.md** — frontmatter 필수: name, description(트리거 포함), model(실제 ID), tools
alias → 실제 ID 변환: opus→claude-opus-4-7 / sonnet→claude-sonnet-4-6 / haiku→claude-haiku-4-5-20251001

**.claude/agents/request-intake-agent.md** (필수)
- 01_project_analysis.md 참조 경로 명시
- terminal-choice 기반 인터뷰 흐름: 요청 유형 → 영향 범위 → 우선순위 → 보안 관련 여부
- 선택형 질문은 방향키 + Enter로 받고, 복수 선택은 Space 토글 + Enter로 받음
- 결과: .agent-team/intake_{timestamp}.md + handoff 규칙

**.claude/agents/feature-architect-agent.md** (설계서에 포함된 경우)
- 한글 호칭: 기능 설계 에이전트
- 신규 기능, API, DB, 테스트 전략, 구현 계획 설계 및 implementation tasklist 작성 담당
- agent team topology, `.claude/agents`, `.claude/skills`, hooks, registry 직접 변경 금지
- 신규 기능 설계 산출물 생성 전 파일명 확인 규칙 명시:
  - 사용자가 파일명을 지정했으면 충돌·경로 문제만 확인 후 사용
  - 지정하지 않았으면 추천 파일명 1~3개를 terminal-choice로 제시하고 선호를 질문
  - 추천 패턴: `.agent-team/feature_design_{slug}_{timestamp}.md`, `.claude/handoff/feature_design_{slug}_{timestamp}.md`, `docs/design/{slug}.md`
  - 빠른 진행 요청 또는 응답 부재 시 기본 추천안을 사용하고 handoff에 근거 기록
- tasklist 생성 규칙 명시:
  - 출력: `.agent-team/tasklist_{slug}_{timestamp}.md` 또는 `.claude/handoff/tasklist_{slug}_{timestamp}.md`
  - 각 task에 owner, depends_on, files, done_when, test command 포함
  - production code 수정 task는 Red PASS에 의존
  - tasklist 검토자와 승인 상태 기록

**.claude/agents/implementation-agent.md** (설계서에 포함된 경우)
- 승인된 implementation tasklist를 기본 입력으로 사용
- 전체 설계서, 인터뷰 원문, 긴 검증 로그를 기본 입력으로 받지 않음
- tasklist에 명시된 파일과 섹션만 선택적으로 읽음
- tasklist 승인 전 production code 수정 금지
- tasklist 밖 파일 수정, task 순서 변경, 범위 확장은 verifier 또는 사용자 승인 필요

**.claude/agents/_common/shared-rules.md** — 250줄 이하 유지
Common 보안 규칙 포함: 하드코딩 금지, 입력 검증, 파라미터화 쿼리, XSS 방지, 로그 민감정보 금지
도메인 보안 규칙(Web/Infra/DataPipeline/AI·RAG)은 해당 시만 추가
Project-Aware TDD 공통 규칙 포함: Red 검증 전 production code 수정 금지, 기존 테스트 관례 우선, 신규 테스트 인프라 도입은 사용자 승인 필요
Terminal Interaction 공통 규칙 포함: 선택형 질문은 terminal-choice 우선, 직접 타이핑은 fallback 또는 "기타" 보충 입력에만 허용
Tasklist Handoff 공통 규칙 포함: 구현은 승인된 tasklist 중심으로 수행, tasklist 밖 범위 확장 금지

**.claude/skills/_common/handoff-writer/SKILL.md**

**.claude/skills/_common/terminal-choice/SKILL.md** (필수)
- 선택형 질문은 `.agent-team/tools/terminal_select.py`로 실행
- 단일 선택: 방향키 이동 + Enter 확정
- 복수 선택: 방향키 이동 + Space 토글 + Enter 확정
- 실행 불가 환경에서만 번호 입력 fallback 허용
- 선택 결과 value + label + fallback 여부를 handoff에 기록

**.claude/skills/_common/tdd-workflow/SKILL.md** (필수)
- 현재 프로젝트의 Test Environment Profile을 먼저 확인
- Acceptance Criteria → Failing Test → Red Verification → Minimal Implementation → Green Verification → Refactor 순서 강제
- 기존 테스트 프레임워크·테스트 위치·fixture/mock·CI 명령 우선
- Red 실패 원인 검증: 기능 미구현 외 실패는 FAIL
- Green 검증: 실제 test/CI command 기준
- 테스트 인프라가 없으면 사용자 승인 전 dependency/config/CI 변경 금지

**.claude/skills/_common/tasklist-handoff/SKILL.md** (필수)
- feature-architect-agent가 tasklist를 작성
- verifier가 tasklist를 승인
- implementation-agent는 승인된 tasklist만 기본 입력으로 사용
- tasklist template: Source / Global Rules / Tasks(owner, depends_on, files, done_when) / Test Commands / Approval
- tasklist 밖 파일 수정, 순서 변경, 범위 확장은 승인 필요

**.claude/skills/_common/doc-updater/SKILL.md** (필수)
- 신규 기능·모듈 개발 후 CLAUDE.md, docs/service-structure.md 업데이트
- 변경 파일 확인 → 해당 섹션만 수정(전체 재작성 금지) → changelog 한 줄 추가

**.claude/hooks/_common/** / **.claude/hooks/per-agent/**

**.agent-team/tools/terminal_select.py** — `references/scripts/terminal_select.py`를 복사

**.claude/settings.json** — hooks 배열 append만, 중복 command 방지, JSON 파싱 실패 시 수정 중단

**docs/tool-inventory.md** — 공통/개별/Forbidden 도구 목록

**.gitignore 추가** (없는 경우만):
```
.claude/handoff/*.md
.agent-team/intake_*.md
.agent-team/backups/
.agent-team/tmp/
```

**`.agent-team/registry.json`** — 팀 생성 메타데이터 (Update/Audit Mode에서 기준값으로 활용)
```json
{
  "schema_version": "1",
  "agent_team_version": "1.0.0",
  "mode": "subagent-orchestration",
  "last_updated": "{ISO8601 timestamp}",
  "source_design": ".agent-team/03_agent_design_spec_v{N}.md",
  "last_approved": ".agent-team/04_validation_approved.md",
  "last_implementation_log": ".agent-team/05_implementation_log.md",
  "security_profiles": ["Common", "..."],
  "development_methodology": {
    "name": "project-aware-tdd",
    "tdd_gate": "required",
    "test_environment_profile": ".agent-team/01_project_analysis.md#Test Environment Profile"
  },
  "agents": [
    {"name": "{agent-name}", "model": "{실제 model ID}", "file": ".claude/agents/{file}.md", "tools": ["Read"], "risk_level": "medium", "status": "active"}
  ],
  "skills": [
    {"name": "terminal-choice", "file": ".claude/skills/_common/terminal-choice/SKILL.md", "preload": false, "risk_level": "low"},
    {"name": "tasklist-handoff", "file": ".claude/skills/_common/tasklist-handoff/SKILL.md", "preload": false, "risk_level": "medium"},
    {"name": "tdd-workflow", "file": ".claude/skills/_common/tdd-workflow/SKILL.md", "preload": false, "risk_level": "medium"}
  ],
  "hooks": [],
  "files": [],
  "last_validation": {
    "status": "PASS",
    "static_smoke": "PASS",
    "workflow_simulation": "PASS"
  }
}
```

**`.agent-team/decision-log.md`** — 설계 결정 및 변경 이력 추적
```markdown
# Decision Log

## {YYYY-MM-DD} — 초기 생성
- 프리셋: {preset명}
- 에이전트 수: {N}개
- 보안 프로필: {목록}
- 주요 결정: {인터뷰에서 도출된 핵심 선택과 근거}
```

## skills: frontmatter 주의사항
- agent frontmatter의 skills:에는 반드시 시작 시 필요한 소형 스킬만 포함
- doc-updater 같은 대형 스킬은 frontmatter 제외, 에이전트 본문에 호출 조건만 명시
- terminal-choice는 질문형 agent 본문에 호출 조건을 명시하고, preload가 꼭 필요한 소형 구성으로 유지할 때만 frontmatter 포함
- tasklist-handoff는 feature-architect-agent와 implementation-agent 본문에 호출 조건을 명시하고, preload는 최소화
- tdd-workflow는 에이전트 본문에 호출 조건을 명시하고, preload가 꼭 필요한 소형 구성으로 유지할 때만 frontmatter 포함
- 큰 스킬을 preload하면 모든 에이전트 시작 컨텍스트가 증가함

## 완료 후
`.agent-team/05_implementation_log.md`에 생성/수정 파일 목록 + diff summary 기록
