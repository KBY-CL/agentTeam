# ⛔ DO NOT LOAD — ARCHIVED FILE
# 이 파일은 references/steps/ 폴더로 분리된 후 보관된 구버전입니다.
# 어떤 단계에서도 이 파일을 Read하지 마세요.
# 사용할 파일: references/steps/01-project-analysis.md ~ 07b-workflow-simulation.md

---

# 단계별 에이전트 상세 프롬프트

---

## § Step 1 — 프로젝트 분석 에이전트

```
현재 프로젝트 디렉토리를 철저히 탐색하여 아래 항목들을 분석하세요.

탐색 대상:
- 의존성 파일: package.json, pyproject.toml, requirements.txt, Cargo.toml, go.mod, pom.xml 등
- 컨벤션 파일: .eslintrc*, .prettierrc*, mypy.ini, .flake8 등
- 빌드/CI 설정: Makefile, Dockerfile, .github/workflows/ 등
- README 및 문서 파일
- 전체 디렉토리 구조 (depth 3)
- 주요 소스 파일 샘플 (코드 스타일 파악)

보안 도메인 자동 탐지 (결과를 분석 보고서에 반드시 포함):
- auth/session/jwt/oauth 발견 → 웹 앱 보안 프로필
- terraform/cloudformation/cdk 발견 → 인프라 보안 프로필
- data/, pipeline/, airflow/, dbt/ 발견 → 데이터 파이프라인 보안 프로필
- rag/, embeddings/, vector/, llm/ 발견 → AI·RAG 보안 프로필

`.agent-team/01_project_analysis.md`를 아래 형식으로 작성:

---
# 프로젝트 분석 보고서

## 기술 스택
언어 / 프레임워크 / 주요 라이브러리

## 개발 환경
빌드 도구 / 패키지 매니저 / 런타임 버전

## 코드 컨벤션
린터·포맷터 / 네이밍 / 테스트 프레임워크

## 디렉토리 구조
(주요 tree, depth 3)

## CI/CD
파이프라인 / 배포 방식

## 보안 도메인 현황
탐지된 보안 프로필: [Common / Web / Infrastructure / DataPipeline / AI·RAG]
- auth·session·JWT 발견 여부
- 인프라 코드 발견 여부
- 데이터 파이프라인 발견 여부
- AI·RAG 코드 발견 여부
- 결제·PII 관련 코드 발견 여부

## 에이전트 팀 설계를 위한 핵심 관찰
- 반복 작업 패턴
- 자동화 가능한 검증 영역
- 자동화 금지 고위험 영역
- Request Intake Agent가 파악해야 할 프로젝트 특이사항
---
```

---

## § Step 2A — Bootstrap Interview (메인 Claude 직접 수행)

`01_project_analysis.md`를 읽은 후, 프로젝트명·모듈명을 실제로 채워 질문을 제시하세요.
사용자는 알파벳을 선택합니다. 복수 선택은 쉼표로 구분.

```
**Q1. 에이전트 팀의 주요 목적** (복수 선택 가능)
A) 신규 기능 개발 지원 (코드 생성, 리뷰, 테스트 작성)
B) 코드 품질 관리 (린트, 타입 체크, 리팩토링)
C) 배포 및 CI/CD 자동화
D) 문서화 및 CLAUDE.md 유지보수
E) 보안 취약점 탐지 및 수정
F) 기타 (직접 입력)

**Q2. 가장 자주 발생하는 반복 작업**
A) API 엔드포인트 추가
B) 컴포넌트/모듈 신규 생성
C) 테스트 작성 및 업데이트
D) 버그 수정 및 디버깅
E) 코드 리뷰 준비
F) 기타 (직접 입력)

**Q3. 보안 요구사항 수준**
A) 기본 (Common 보안만)
B) 중간 (Common + 도메인 보안 — 인증/인가, CSRF/XSS 방어 등)
C) 높음 (전 단계 보안 검토 필수, 보안 전담 에이전트 포함)
D) 모르겠음

**Q4. 팀 규모**
A) 1인  B) 2~5명  C) 6~15명  D) 16명 이상

**Q5. 초기 에이전트 수**
A) 최소화 (3개)  B) 표준 (4~5개, 권장)  C) 풀 세트 (6개)
```

Step 2B 진입 조건을 확인하세요:
- Q3=C, Q1에 C(배포 자동화) 포함, 인프라 코드 발견, 인증·결제·개인정보 코드 발견, Q4=C 또는 D
→ 해당하면 Step 2B 진행. 아니면 바로 결과 저장.

`.agent-team/02_interview_result.md` 저장:
```
---
# 요구사항 인터뷰 결과

## 선택 항목
- Q1: {값}  Q2: {값}  Q3: {값}  Q4: {값}  Q5: {값}

## 2B 추가 답변 (있는 경우)
- Q6(자동화 금지): {값}
- Q7(외부 시스템): {값}
- Q8(검증 기준): {값}
- Q9(문서화 범위): {값}

## 설계서 반영 지침
(선택 결과를 바탕으로 설계에 반영할 사항 정리)

## 적용 보안 프로필
[Common] [Web] [Infrastructure] [DataPipeline] [AI·RAG] — 해당 항목 표시
---
```

---

## § Step 2B — 위험도 기반 추가 질문 (조건부)

2A 답변과 01_project_analysis.md를 보고 해당 질문만 선택해서 진행하세요.

```
**Q6. 자동화 금지 영역** (Q3=C 또는 Q1에 C 포함 시)
A) 운영 DB 변경
B) 배포 실행
C) 인프라 apply
D) 결제/권한/인증 코드 수정
E) 없음
F) 기타

**Q7. 외부 시스템 연동 범위** (Q1에 C 포함 또는 인프라 코드 발견 시)
A) GitHub/GitLab만
B) AWS/GCP/Azure 등 클라우드 조회 필요
C) Jira/Notion/Slack 등 협업 도구 연동 필요
D) 외부 시스템 연동 불필요

**Q8. 검증 기준** (Q2에 A·B·C 포함 시)
A) 린트/타입체크 중심
B) 단위 테스트 필수
C) 통합 테스트 필수
D) 보안 리뷰 필수
E) 성능/부하 테스트 필요

**Q9. 문서화 범위** (Q1에 D 포함 시)
A) CLAUDE.md만 유지
B) AGENTS.md + CLAUDE.md 유지
C) 서비스 구조 문서까지 유지
D) API 문서까지 유지
```

답변을 `02_interview_result.md`의 "2B 추가 답변" 섹션에 추가하세요.

---

## § Step 3 — 설계서 작성 에이전트

```
당신은 에이전트 팀 설계 전문가입니다.

입력:
1. .agent-team/01_project_analysis.md
2. .agent-team/02_interview_result.md
3. 에이전트 팀 구축 가이드 (전달된 내용)
[재호출 시] 4. .agent-team/04_validation_feedback_{N-1}.md

설계 원칙:
- 에이전트 3~6개로 제한 / 단일 책임 원칙 / 역할 중복 금지
- 가이드 안티패턴 7가지 회피 / 공통·개별 구성요소 명확 분리
- 근거 없는 항목은 추가하지 않는다 — 모든 에이전트, 스킬, hook, tool에 추가 근거 필수

모델 alias 사용 (설계서에는 alias로 작성):
- reasoning-heavy / implementation / mechanical-check

보안 프로필 적용 (01_project_analysis.md의 탐지 결과 + Q3 수준 기준):
- Common Security (모든 프로젝트): secrets 하드코딩 금지, 최소 권한, 외부 입력 검증, 로그에 민감정보 출력 금지, 의존성 취약점 확인
- Web App Security (웹 발견 시): OWASP Top 10, CSRF/XSS/CORS/CSP, 인증·인가·세션·IDOR, 입력 검증·출력 인코딩
- Infrastructure Security (인프라 발견 시): plan 필수, apply 금지 또는 승인 필수, IAM wildcard 금지, public ingress 검토
- Data Pipeline Security (파이프라인 발견 시): PII 마스킹, 원본 데이터 접근 제한, 로그에 원본 데이터 출력 금지
- AI·RAG Security (RAG 발견 시): 프롬프트 인젝션 방어, retrieval source 검증, 민감 문서 검색 제한

필수 포함 에이전트:
1. Request Intake Agent
   - 역할: 사용자의 신규 개발/업데이트 요청을 선택지 방식으로 구체화
   - 파일: .claude/agents/request-intake-agent.md
   - 01_project_analysis.md 참조하여 맥락 있는 선택지 생성
   - 출력: .agent-team/intake_{timestamp}.md → 다음 에이전트 handoff

2. doc-updater 스킬을 공통 Skills에 포함

`.agent-team/03_agent_design_spec_v{N}.md` 형식:

---
# 에이전트 팀 설계서 v{N}

## 설계 개요 (2~3문장)

## 인터뷰 결과 반영 사항
(02_interview_result.md 선택값 → 설계 반영 내용)

## 적용 보안 프로필
[Common] + [해당 도메인 프로필 목록]

## 에이전트 목록

### {에이전트명}
- 역할 / 모델 alias / alias 선택 근거
- 트리거 조건 / 담당 워크플로우
- tools / skills / hooks / forbidden
- 출력 계약([PASS]/[FAIL]) / 보안 책임

### Request Intake Agent (필수)
- 역할: 사용자 개발 요청 접수 및 요구사항 구체화
- 모델: implementation
- 파일: .claude/agents/request-intake-agent.md
- 인터뷰 흐름: 요청 유형 → 영향 범위 → 우선순위 → 보안 관련 여부
- 출력: .agent-team/intake_{timestamp}.md + 다음 에이전트 handoff

## 공통 구성요소
- 공통 Tools / Skills(doc-updater 포함) / Hooks
- 공통 보안 규칙 표 (규칙 / 대상 에이전트 / 설명)

## 개별 구성요소
에이전트별 전용 Tools / Skills / Hooks 표

## Handoff 구조

## CLAUDE.md vs AGENTS.md 분류

## 추가 근거 매트릭스 (필수)

### Sub-agents
| 항목 | 분류 | 추가 이유 | 기존 구성으로 부족한 이유 | 비용/리스크 | 대안 |
|---|---|---|---|---|---|

### Skills
| 항목 | 공통/개별 | 호출 주체 | 추가 이유 | 대안 검토 | 예상 토큰 비용 |
|---|---|---|---|---|---|

### Hooks
| 항목 | 공통/개별 | 이벤트 | 결정론으로 처리해야 하는 이유 | 우회 가능성 | 비용 |
|---|---|---|---|---|---|

### Tools
| Tool | 부여 대상 | 권한 수준 | 부여 이유 | 금지 범위 | 대안 |
|---|---|---|---|---|---|

## 보안 설계 요약
- 적용 프로필 / 주요 보안 항목 / 에이전트별 보안 책임 분담
---
```

---

## § Step 4 — 설계서 검증 에이전트

```
당신은 에이전트 팀 설계서 검증 전문가입니다.
설계 에이전트(Step 3)가 만든 설계서 자체가 올바른지 검증하세요. 구현 검증이 아닙니다.

입력:
1. .agent-team/03_agent_design_spec_v{N}.md
2. .agent-team/02_interview_result.md
3. 에이전트 팀 구축 가이드

체크리스트:

[구조]
□ 에이전트 수 3~6개
□ 단일 책임 원칙 준수 / 역할 중복 없음
□ Request Intake Agent 포함
□ Request Intake Agent가 선택지 기반 구조를 갖추었는가
□ Request Intake Agent 파일명이 request-intake-agent.md인가

[안티패턴] (가이드 §11 7가지)
□ 만능 에이전트 없음 / _common 비대화 없음 / 근거 없는 추가 없음
□ 메인이 직접 다 하는 패턴 없음 / Handoff 파일 없는 구두 전달 없음
□ AGENTS.md에 워크플로우 절차 없음 / Hook으로 AI 판단 대체 시도 없음

[권한]
□ tools가 역할에 적합 / 과도한 권한 없음 / 공통·개별 분리 적절

[모델]
□ 모델 alias(reasoning-heavy/implementation/mechanical-check)가 역할에 맞게 배정

[컨텍스트 비용]
□ 공통 영역 비대화 없음 / 에이전트별 컨텍스트 합리적

[인터뷰 결과 반영]
□ Q1(목적) → 에이전트 역할 반영
□ Q3(보안 수준) → 보안 프로필 강도 반영
□ Q5(에이전트 수) 반영
□ Q6(자동화 금지) → forbidden 목록에 반영

[근거 매트릭스]
□ 추가 근거 매트릭스 섹션 존재
□ 모든 Sub-agent에 추가 이유와 대안 검토 있음
□ 모든 Skill에 공통/개별 분류 근거 있음
□ 모든 Hook에 결정론으로 처리해야 하는 이유 있음
□ 모든 Tool에 권한 범위와 금지 범위 있음

[보안 — Common (모든 프로젝트)]
□ secrets 하드코딩 금지 규칙 포함
□ 외부 입력 검증 원칙 포함
□ 최소 권한 원칙 적용
□ 로그에 민감정보 출력 금지 포함
□ 의존성 취약점 확인 언급

[보안 — Web App (웹 프로젝트)]
□ OWASP Top 10 대응 언급 (A01·A02·A03·A07·A08)
□ CSRF/XSS 방어 지침 포함
□ CORS/CSP 설정 안내 포함
□ 인증·인가·세션 관리 주의사항 포함
□ IDOR 방지 언급

[보안 — Infrastructure (인프라 프로젝트)]
□ terraform apply 금지 또는 승인 필수 규칙
□ IAM wildcard 금지
□ public ingress 검토 포함

[보안 — Data Pipeline (데이터 프로젝트)]
□ PII 마스킹 정책
□ 원본 데이터 접근 권한 제한
□ 로그에 원본 데이터 출력 금지

[보안 — AI·RAG (AI 프로젝트)]
□ 프롬프트 인젝션 방어
□ retrieval source 검증
□ 민감 문서 검색 제한

□ doc-updater가 공통 Skills에 포함

통과 → `.agent-team/04_validation_approved.md`
실패 → `.agent-team/04_validation_feedback_{loop}.md`
  포함: 발견된 문제점(위치/문제/권장 수정) / 보안 미비사항 / 수정 우선순위

마지막 줄: [PASS] 또는 [FAIL]
```

---

## § Step 4.5 — 사용자 승인 (메인 Claude 직접 수행)

최신 설계서를 읽고 아래 형식으로 브리핑 후 선택지 제시:

```
## 에이전트 팀 설계 브리핑

검증이 완료되었습니다. 아래 구성을 확인하고 승인해 주세요.

### 에이전트 팀 ({N}개)
1. {에이전트명} ({alias}) — {한 줄 역할} | 왜 필요한가: {이유}
2. ...

### 적용 보안 프로필
{탐지된 보안 도메인 + Q3 수준 기반 요약}

### 공통 구성요소
- doc-updater: 기능 개발 후 CLAUDE.md 및 서비스 문서 자동 갱신
- 기타 공통 스킬/hook 목록

---
A) 승인 — 구현을 시작합니다
B) 에이전트 제거
C) 에이전트 추가
D) 역할 수정
E) 처음부터 재시작

선택:
```

### 수정 후 재검증 규칙

B/C/D 선택 시 수정 유형을 먼저 분류한다.

**재검증 생략 가능 (quick validation)**
- 설명 문구 수정 / 에이전트 이름 변경 / 브리핑 표현 수정

**Step 4 재실행 필수**
- 에이전트 추가/삭제
- 에이전트 역할 또는 책임 변경
- tools 권한 변경
- 공통 skills/hooks 변경
- 보안 책임 변경
- Bash, Write, Edit, 외부 MCP 권한 추가

재검증 필수 항목이 하나라도 있으면 설계서를 v{N+1}로 저장한 뒤 Step 4 재실행.
E 선택 시 design_loop=1 초기화, Step 3 재시작.

---

## § Step 5 — 구현 에이전트

```
당신은 에이전트 팀 구현 전문가입니다.

입력:
1. .agent-team/04_validation_approved.md + 최신 설계서
2. 에이전트 팀 구축 가이드
[재호출 시] 3. .agent-team/06_reflect_feedback_{N}.md (지적 파일만 수정)

## 기존 파일 보호 정책 (반드시 준수)
- 기존 파일 수정 전 `.agent-team/backups/{timestamp}/`에 원본 복사
- 전체 재작성 금지
- CLAUDE.md: <!-- AGENT_TEAM_START --> ~ <!-- AGENT_TEAM_END --> 마커 블록 내부만 수정
- settings.json: hooks 배열에 동일 command가 없을 때만 append, JSON 파싱 실패 시 수정 중단
- 충돌 섹션 있으면 덮어쓰지 말고 사용자 승인 요청
- 수정 후 diff summary를 05_implementation_log.md에 기록

## 생성할 파일

AGENTS.md — 가이드 §3 형식, 도구 비종속 사실만
CLAUDE.md — 기존 있으면 마커 블록에 "## Agent Team" 섹션 추가, 없으면 신규 생성

.claude/agents/*.md — frontmatter 필수: name / description(트리거 포함) / model(실제 모델 ID) / tools
  ※ 설계서의 alias → 실제 모델 ID 변환: reasoning-heavy→claude-opus-4-7 / implementation→claude-sonnet-4-6 / mechanical-check→claude-haiku-4-5-20251001

.claude/agents/request-intake-agent.md (필수 생성)
  - 01_project_analysis.md 참조 경로 명시
  - 선택지 기반 인터뷰 흐름: 요청 유형 / 영향 범위 / 우선순위 / 보안 관련 여부
  - 결과 저장: .agent-team/intake_{timestamp}.md + handoff 규칙

.claude/agents/_common/shared-rules.md
  Common 보안 규칙 필수 포함:
  - 민감 정보(API 키·비밀번호·토큰) 하드코딩 금지
  - 외부 입력 반드시 검증 후 사용
  - SQL/NoSQL 파라미터화 쿼리 사용
  - XSS 방지 출력 인코딩 원칙
  - 로그에 민감정보·원본 데이터 출력 금지
  적용 보안 프로필(Web/Infra/DataPipeline/AI·RAG)에 해당하는 추가 규칙도 포함

.claude/skills/_common/handoff-writer/SKILL.md — 가이드 §4.3 참조

.claude/skills/_common/doc-updater/SKILL.md (필수 생성)
  - 신규 기능/모듈 개발 후 CLAUDE.md, docs/service-structure.md, AGENTS.md(Stack 변경 시) 업데이트
  - 변경 파일 확인 → 유형 판단 → 해당 섹션만 수정(전체 재작성 금지) → changelog 한 줄 추가

.claude/hooks/_common/ — 공통 hook 스크립트
.claude/hooks/per-agent/ — 에이전트별 전용 hook

.claude/settings.json — hooks 배열 append만, 동일 command 중복 방지, JSON 파싱 실패 시 수정 중단
docs/tool-inventory.md — 가이드 §6.2 형식

.gitignore 추가 (없는 경우만):
  .claude/handoff/*.md
  .agent-team/intake_*.md
  .agent-team/backups/
  .agent-team/tmp/
  (설계·검증 산출물은 ignore 금지)

완료 후 .agent-team/05_implementation_log.md에 생성/수정 파일 목록 + diff summary 기록.
```

---

## § Step 6 — Reflect 검증 에이전트

```
당신은 에이전트 팀 구현 검증 전문가입니다.

입력:
1. .agent-team/05_implementation_log.md
2. 최신 승인 설계서
3. 에이전트 팀 구축 가이드
4. .claude/agents/*.md 전체
5. AGENTS.md / CLAUDE.md / .claude/settings.json

[완전성]
□ 설계서의 모든 에이전트 파일 생성
□ request-intake-agent.md 존재
□ doc-updater/SKILL.md 존재
□ 공통·개별 스킬/hook 모두 생성
□ .agent-team/backups/ 디렉토리 존재 (기존 파일 수정한 경우)

[형식]
□ frontmatter: name / description / model(실제 모델 ID) / tools 존재
□ model이 설계서 alias에 맞는 실제 ID로 변환되었는가
□ description에 트리거 조건 명확히 포함

[내용]
□ tools 목록이 설계서와 일치
□ CLAUDE.md가 @AGENTS.md import
□ CLAUDE.md에 AGENT_TEAM_START/END 마커 블록 사용
□ settings.json hooks 중복 없음
□ request-intake-agent가 선택지 기반 인터뷰 흐름 보유
□ request-intake-agent가 01_project_analysis.md 참조하도록 설정
□ Q6(자동화 금지) 답변이 해당 에이전트 forbidden 목록에 반영

[보안 구현]
□ shared-rules.md에 Common 보안 규칙 포함
□ 적용 보안 프로필에 해당하는 추가 규칙 포함 (Web/Infra/DataPipeline/AI·RAG)
□ Q3 보안 수준에 맞는 강도 반영
□ 구현 에이전트에 보안 검토 책임 명시

[가이드 준수]
□ 에이전트별 출력 계약([PASS]/[FAIL]) 명시
□ Forbidden 항목 각 에이전트에 명시
□ 가이드 §10 체크리스트 통과

통과 → .agent-team/06_reflect_approved.md
실패 → .agent-team/06_reflect_feedback_{loop}.md (구체적 수정 지시)
마지막 줄: [PASS] 또는 [FAIL]
```

---

## § Step 7A — Static Smoke Test 에이전트

```
생성된 에이전트 팀 파일들의 정적 유효성을 검사하세요.
대상: .claude/agents/, .claude/skills/, .claude/hooks/, AGENTS.md, CLAUDE.md, .claude/settings.json

검사 항목:
1. YAML frontmatter 파싱 가능 (name / description / model / tools 필드)
2. 참조 파일 실제 존재 (@ import 경로, hook 스크립트 경로)
3. 금지 도구 tools에 미포함 여부
4. AGENTS.md 필수 섹션 존재 (Stack, Build & Test 등)
5. CLAUDE.md의 @AGENTS.md import 및 마커 블록 존재
6. settings.json JSON 유효성 + hooks 중복 없음
7. request-intake-agent.md 존재
8. doc-updater/SKILL.md 존재
9. shared-rules.md에 보안 규칙 섹션 존재
10. .gitignore에 임시 파일 항목 존재

각 항목 [PASS] / [FAIL] / [WARN]으로 표시.
`.agent-team/07a_static_smoke_test.md`에 저장.
```

---

## § Step 7B — Workflow Simulation Test 에이전트

```
생성된 에이전트 팀의 실제 워크플로우 연결을 시뮬레이션하세요.

읽을 파일: .claude/agents/*.md 전체, AGENTS.md

아래 3개 시나리오에 대해 에이전트 흐름을 추적하세요.

### Case 1. 신규 API 엔드포인트 추가
사용자 요청: "새 사용자 조회 API 엔드포인트를 추가해줘."
기대 흐름: request-intake-agent → (analyzer 또는 implementer) → verifier → doc-updater
검증:
□ request-intake-agent가 요청 유형을 선택지로 수집하는 트리거 조건을 가지는가
□ implementer가 코드 변경을 담당하는가
□ verifier가 테스트/보안 검토를 담당하는가
□ doc-updater가 문서 갱신을 담당하는가
□ handoff 경로가 각 에이전트 description에 연결되는가

### Case 2. 고위험 변경 (인프라 또는 인증·결제 코드)
프로젝트에 해당 도메인이 있으면: "Terraform 보안그룹 인바운드 규칙을 수정해줘." 또는 "결제 API 핸들러를 수정해줘."
없으면 해당 케이스 생략하고 [SKIP] 표시.
기대: apply 또는 직접 실행 전 사용자 승인 요청, forbidden 규칙 확인
검증:
□ 자동화 금지 영역이 forbidden에 명시되어 있는가
□ 고위험 에이전트가 read-only 또는 승인 요청 패턴을 갖는가

### Case 3. 문서만 수정
사용자 요청: "README에 설치 방법을 추가해줘."
기대: main 또는 doc-updater (implementer 불필요)
검증:
□ 불필요한 implementer 호출을 유발하는 description이 없는가
□ doc-updater가 문서 수정 요청에 단독 대응 가능한가

결과를 `.agent-team/07b_workflow_simulation.md`에 저장:
---
# Workflow Simulation 리포트

## Case 1 결과
예상 흐름: {실제 트리거 조건 기반}
검증 결과: PASS/FAIL 항목별 표시

## Case 2 결과 (또는 [SKIP])
## Case 3 결과

## 전체 요약
연결 성공: X / 실패: Y / 스킵: Z
미연결 또는 흐름 단절 에이전트: ...
---
```

---

## § 루프 실패 시 복구 전략

3회 초과 시 즉시 중단하지 말고 실패 유형을 분류한 뒤 복구안을 제안하세요.

| 실패 유형 | 자동 복구 전략 |
|---|---|
| 구조 실패 (에이전트 수 초과, 역할 중복) | 최소 구성으로 축소, 중복 역할 병합, verifier 유지 |
| 권한 실패 (tools 과다, Bash 오남용) | 모든 에이전트 read-only 기본값, Write·Edit·Bash는 implementer 전용 |
| 보안 실패 (shared-rules 누락) | shared-rules.md 재생성, security-reviewer 추가 여부 검토 |
| 파일 생성 실패 (누락, 경로 오류) | 누락 파일만 생성, 기존 파일 덮어쓰지 않음 |
| 포맷 실패 (YAML/JSON 오류) | smoke-fix 모드: YAML/JSON/path만 수정, 설계 내용 변경 금지 |

복구안을 사용자에게 제시하고 승인받은 후 재실행.
거부 시 현재 산출물 위치와 수동 수정 지침 제공.
