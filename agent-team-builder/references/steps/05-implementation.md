# Step 5 — 구현 에이전트

subagent_type: general-purpose / model: sonnet
file-protection.md도 이 단계에서 로드하세요.

## 입력
1. .agent-team/04_validation_approved.md + 최신 설계서
2. references/policies/file-protection.md (이 단계에서 함께 로드)
3. references/policies/tdd-first.md (이 단계에서 함께 로드)
[재호출 시] 4. .agent-team/06_reflect_feedback_{N}.md (지적 파일만 수정)

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
- 선택지 기반 인터뷰 흐름: 요청 유형 → 영향 범위 → 우선순위 → 보안 관련 여부
- 결과: .agent-team/intake_{timestamp}.md + handoff 규칙

**.claude/agents/_common/shared-rules.md** — 250줄 이하 유지
Common 보안 규칙 포함: 하드코딩 금지, 입력 검증, 파라미터화 쿼리, XSS 방지, 로그 민감정보 금지
도메인 보안 규칙(Web/Infra/DataPipeline/AI·RAG)은 해당 시만 추가
Project-Aware TDD 공통 규칙 포함: Red 검증 전 production code 수정 금지, 기존 테스트 관례 우선, 신규 테스트 인프라 도입은 사용자 승인 필요

**.claude/skills/_common/handoff-writer/SKILL.md**

**.claude/skills/_common/tdd-workflow/SKILL.md** (필수)
- 현재 프로젝트의 Test Environment Profile을 먼저 확인
- Acceptance Criteria → Failing Test → Red Verification → Minimal Implementation → Green Verification → Refactor 순서 강제
- 기존 테스트 프레임워크·테스트 위치·fixture/mock·CI 명령 우선
- Red 실패 원인 검증: 기능 미구현 외 실패는 FAIL
- Green 검증: 실제 test/CI command 기준
- 테스트 인프라가 없으면 사용자 승인 전 dependency/config/CI 변경 금지

**.claude/skills/_common/doc-updater/SKILL.md** (필수)
- 신규 기능·모듈 개발 후 CLAUDE.md, docs/service-structure.md 업데이트
- 변경 파일 확인 → 해당 섹션만 수정(전체 재작성 금지) → changelog 한 줄 추가

**.claude/hooks/_common/** / **.claude/hooks/per-agent/**

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
- tdd-workflow는 에이전트 본문에 호출 조건을 명시하고, preload가 꼭 필요한 소형 구성으로 유지할 때만 frontmatter 포함
- 큰 스킬을 preload하면 모든 에이전트 시작 컨텍스트가 증가함

## 완료 후
`.agent-team/05_implementation_log.md`에 생성/수정 파일 목록 + diff summary 기록
