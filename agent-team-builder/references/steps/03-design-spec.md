# Step 3 — 설계서 작성 에이전트

subagent_type: general-purpose / model: opus

## 입력
1. .agent-team/01_project_analysis.md
2. .agent-team/02_interview_result.md
3. references/policies/security-profiles.md (이 단계에서 함께 로드)
4. references/policies/tdd-first.md (이 단계에서 함께 로드)
5. references/policies/tasklist-handoff.md (이 단계에서 함께 로드)
[재호출 시] 6. .agent-team/04_validation_feedback_{N-1}.md

agent-team-guide.md는 전체 로드 금지. 안티패턴 확인이 필요하면 해당 섹션만 부분 Read.

## 설계 원칙
- 에이전트 3~6개 / 단일 책임 / 역할 중복 금지
- 근거 없는 항목 추가 금지 (모든 항목에 추가 근거 필수)
- 모델은 alias로 작성: opus / sonnet / haiku
- skills: frontmatter에는 반드시 필요한 소형 스킬만 포함 (대형 스킬 preload 금지)
- doc-updater는 에이전트 frontmatter의 skills:에 넣지 않음. 구현 에이전트 본문에 "기능 개발 완료 후 doc-updater 스킬을 호출한다"고 명시
- Project-Aware TDD-first를 기본 개발 흐름으로 설계
- production code 수정은 실패 테스트 작성과 Red 검증 `[PASS]` 이후에만 허용
- 기존 테스트 프레임워크·파일 위치·fixture/mock 방식·CI 명령을 우선 사용
- 테스트 인프라가 없으면 신규 도입을 사용자 승인 대상으로 표시
- 기능 설계 책임 agent가 있으면 이름은 `feature-architect-agent`로 고정하고, 한글 호칭은 "기능 설계 에이전트"로 명시
- 기능 설계 에이전트는 신규 기능 설계 산출 파일을 만들기 전에 파일명 선호를 사용자에게 묻거나 추천 파일명을 제시해 확정해야 함
- 기능 설계 에이전트가 implementation tasklist를 만들고, 검증 에이전트 승인 후 implementation-agent에 전달하도록 설계
- implementation-agent는 승인된 tasklist를 기본 입력으로 받고, 전체 설계서/인터뷰/긴 검증 로그를 기본 입력으로 받지 않음

## 필수 포함 에이전트
**Request Intake Agent** (.claude/agents/request-intake-agent.md)
- 역할: 선택지 방식으로 개발 요청을 구체화
- model: sonnet
- 01_project_analysis.md 참조하여 맥락 있는 선택지 생성
- 출력: .agent-team/intake_{timestamp}.md → handoff

## 산출물: `.agent-team/03_agent_design_spec_v{N}.md`

```
# 에이전트 팀 설계서 v{N}

## 설계 개요 (2~3문장)

## 인터뷰 결과 반영 사항

## 적용 보안 프로필
[Common] + [해당 도메인 목록]

## 에이전트 목록

### {에이전트명}
- 역할 / model alias / alias 선택 근거
- 트리거 조건 / 담당 워크플로우
- tools / forbidden / 출력 계약([PASS]/[FAIL])
- skills (frontmatter 포함 여부) / 본문 내 호출 조건 명시 스킬
- 보안 책임

### Feature Architect Agent (해당 시)
- 이름: `feature-architect-agent` / 한글 호칭: 기능 설계 에이전트
- 역할: 신규 기능, API, DB, 테스트 전략, 구현 계획 설계 + implementation tasklist 작성
- 금지: agent team topology, `.claude/agents`, `.claude/skills`, hooks, registry 직접 변경
- 파일명 확인 규칙: 신규 설계 산출물 작성 전 사용자에게 선호 파일명을 묻거나 추천 파일명 1~3개를 제시하고 확정 후 생성
- 추천 파일명 패턴: `.agent-team/feature_design_{slug}_{timestamp}.md`, `.claude/handoff/feature_design_{slug}_{timestamp}.md`, `docs/design/{slug}.md`
- tasklist 출력: `.agent-team/tasklist_{slug}_{timestamp}.md` 또는 `.claude/handoff/tasklist_{slug}_{timestamp}.md`
- tasklist에는 Source, Global Rules, Tasks(owner/depends_on/files/done_when), Test Commands, 승인 상태 포함
- production code 수정 task는 Red PASS에 의존해야 함

### Request Intake Agent (필수)
- 역할: 개발 요청 접수 및 요구사항 구체화
- model: sonnet
- 인터뷰 흐름: 요청 유형 → 영향 범위 → 우선순위 → 보안 관련 여부
- 출력: .agent-team/intake_{timestamp}.md

## 공통 구성요소
- 공통 Tools / Hooks
- 공통 보안 규칙 표
- Project-Aware TDD Gate: Acceptance Criteria → Test Strategy → Failing Test → Red Verification → Minimal Implementation → Green Verification → Refactor → Regression/Security Verification → Documentation Update
- Tasklist Handoff: `feature-architect-agent`가 tasklist 작성, verifier 승인, `implementation-agent`는 승인된 tasklist만 실행

## doc-updater 위치 규칙 (반드시 준수)
- ✅ .claude/skills/_common/doc-updater/SKILL.md 파일로 존재 (공통 스킬 파일)
- ❌ 에이전트 frontmatter의 skills:에 포함하지 않음 (preload 금지 — 컨텍스트 낭비)
- ✅ 구현 에이전트 본문에만 명시: "기능 개발·수정 완료 후 doc-updater 스킬을 호출한다"

## 개별 구성요소 (에이전트별 전용)

## Handoff 구조

## 설계 산출물 파일명 확인 규칙
- 기능 설계 에이전트가 신규 기능 설계 요청을 받으면 산출물 파일 생성 전에 파일명을 확정한다.
- 사용자가 파일명을 이미 지정한 경우 그 이름을 사용하되, 충돌·보안·경로 문제가 있으면 대안을 제시한다.
- 사용자가 파일명을 지정하지 않은 경우 기능명을 slug로 변환한 추천 파일명 1~3개를 제시하고 선호를 묻는다.
- 사용자가 빠른 진행을 원하거나 응답이 없으면 가장 보수적인 기본 추천안을 사용하고 handoff에 선택 근거를 기록한다.

## 사용자 인터랙션 설계
- Request Intake Agent와 질문형 agent는 채팅에서 선택지를 제시하고 사용자가 번호나 문자로 답하게 한다.
- 단일 선택은 하나의 번호/문자, 복수 선택은 쉼표로 구분한 번호/문자를 사용한다.
- 자유 입력은 "기타" 선택 후 보충 설명처럼 선택지로 표현할 수 없는 경우에만 허용한다.

## Tasklist Handoff 설계
- 기능 설계 에이전트는 기능 설계와 테스트 전략을 바탕으로 implementation tasklist를 작성한다.
- tasklist 검토자는 test strategy/red verifier/quality verifier 중 설계된 역할에 맞게 지정한다.
- tasklist 승인 전 implementation-agent는 production code를 수정하지 않는다.
- implementation-agent의 기본 입력은 승인된 tasklist, 필요한 handoff 요약, 수정 대상 파일 목록, 테스트 명령으로 제한한다.
- implementation-agent가 전체 설계서나 긴 로그를 읽어야 하면 tasklist에 그 이유와 필요한 섹션을 명시한다.
- tasklist에 없는 파일 수정, task 순서 변경, 범위 확장은 verifier 또는 사용자 승인 없이는 금지한다.

## TDD-first 설계
- Test Environment Profile 요약: 01_project_analysis.md 기반
- 개발 요청의 기본 흐름: Request Intake → 테스트 책임자 → Red Verifier → Implementation Agent → Green Verifier → Refactor/Quality Review → doc-updater
- Red gate: 실패 테스트가 기능 미구현 때문에 실패해야 하며, 설정·fixture·import 오류는 FAIL
- Green gate: 프로젝트의 실제 test/CI command 기준으로 검증
- 테스트 인프라 부재 시: 사용자 승인 전 dependency/config/CI 변경 금지

## 추가 근거 매트릭스 (필수)

### Sub-agents
| 항목 | 추가 이유 | 기존 구성으로 부족한 이유 | 비용/리스크 | 대안 |

### Skills
| 항목 | 공통/개별 | 추가 이유 | preload 여부 및 근거 | 대안 |

### Hooks
| 항목 | 이벤트 | 결정론 처리 이유 | 비용 |

### Tools
| Tool | 부여 대상 | 부여 이유 | 금지 범위 |

## 위험 수준 (Risk Level)
프로젝트 전체 위험 수준을 4단계로 평가:
- **low**: 내부 도구, 단순 CRUD, 외부 연동 없음
- **medium**: 일반 웹 서비스, 사용자 인증 포함, 외부 API 연동
- **high**: 금융·결제, 개인정보 처리, 인프라 자동화
- **critical**: 의료·법률 데이터, 멀티테넌트 SaaS, 운영 인프라 직접 제어

평가 기준: 외부 노출 범위 + 데이터 민감도 + 장애 시 영향 범위

## 보안 설계 요약
적용 프로필 / 에이전트별 보안 책임 분담 / 위험 수준: {low|medium|high|critical}
```
