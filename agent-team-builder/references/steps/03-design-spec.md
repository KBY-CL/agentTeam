# Step 3 — 설계서 작성 에이전트

subagent_type: general-purpose / model: opus

## 입력
1. .agent-team/01_project_analysis.md
2. .agent-team/02_interview_result.md
3. references/policies/security-profiles.md (이 단계에서 함께 로드)
[재호출 시] 4. .agent-team/04_validation_feedback_{N-1}.md

agent-team-guide.md는 전체 로드 금지. 안티패턴 확인이 필요하면 해당 섹션만 부분 Read.

## 설계 원칙
- 에이전트 3~6개 / 단일 책임 / 역할 중복 금지
- 근거 없는 항목 추가 금지 (모든 항목에 추가 근거 필수)
- 모델은 alias로 작성: opus / sonnet / haiku
- skills: frontmatter에는 반드시 필요한 소형 스킬만 포함 (대형 스킬 preload 금지)
- doc-updater는 에이전트 frontmatter의 skills:에 넣지 않음. 구현 에이전트 본문에 "기능 개발 완료 후 doc-updater 스킬을 호출한다"고 명시

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

### Request Intake Agent (필수)
- 역할: 개발 요청 접수 및 요구사항 구체화
- model: sonnet
- 인터뷰 흐름: 요청 유형 → 영향 범위 → 우선순위 → 보안 관련 여부
- 출력: .agent-team/intake_{timestamp}.md

## 공통 구성요소
- 공통 Tools / Hooks
- 공통 보안 규칙 표

## doc-updater 위치 규칙 (반드시 준수)
- ✅ .claude/skills/_common/doc-updater/SKILL.md 파일로 존재 (공통 스킬 파일)
- ❌ 에이전트 frontmatter의 skills:에 포함하지 않음 (preload 금지 — 컨텍스트 낭비)
- ✅ 구현 에이전트 본문에만 명시: "기능 개발·수정 완료 후 doc-updater 스킬을 호출한다"

## 개별 구성요소 (에이전트별 전용)

## Handoff 구조

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
