# Step 2A — Bootstrap Interview (메인 Claude 직접 수행)

01_project_analysis.md를 읽은 후 프로젝트명·모듈명을 실제로 채워 질문을 제시하세요.
`references/policies/terminal-interaction.md`를 적용하세요.
사용자는 타이핑하지 않고 방향키로 선택합니다. 복수 선택은 Space로 토글하고 Enter로 확정합니다.

실행 예:

```bash
python references/scripts/terminal_select.py --multi --json \
  --question "Q1. 에이전트 팀의 주요 목적" \
  --option "A=신규 기능 개발 지원" \
  --option "B=코드 품질 관리" \
  --option "C=배포 및 CI/CD 자동화" \
  --option "D=문서화·CLAUDE.md 유지" \
  --option "E=보안 취약점 탐지·수정" \
  --option "F=기타"
```

비대화형 셸에서 `INTERACTIVE_REQUIRED`가 반환되면 `input()` fallback을 실행하지 말고, 반환된 options를 사용자에게 보여주고 채팅 응답 또는 실제 TTY 재실행을 요청하세요.
Windows 환경에서는 먼저 `python references/scripts/terminal_select_windows.py ...`로 별도 cmd 창 선택을 시도하세요.

```
Q1. 에이전트 팀의 주요 목적 (복수 선택 가능)
A) 신규 기능 개발 지원   B) 코드 품질 관리
C) 배포 및 CI/CD 자동화  D) 문서화·CLAUDE.md 유지
E) 보안 취약점 탐지·수정  F) 기타

Q2. 가장 자주 발생하는 반복 작업
A) API 엔드포인트 추가   B) 컴포넌트·모듈 신규 생성
C) 테스트 작성·업데이트  D) 버그 수정·디버깅
E) 코드 리뷰 준비        F) 기타

Q3. 보안 요구사항 수준
A) 기본 (Common 보안만)
B) 중간 (Common + 도메인 보안)
C) 높음 (전 단계 보안 검토, 보안 전담 에이전트 포함)
D) 모르겠음

Q4. 팀 규모
A) 1인   B) 2~5명   C) 6~15명   D) 16명 이상

Q5. 초기 에이전트 수
A) 최소 (3개)   B) 표준 (4~5개, 권장)   C) 풀 (6개)
```

## Step 2B 진입 조건 확인

아래 중 하나라도 해당하면 Step 2B 진행:
- Q3 = C
- Q1에 C(배포 자동화) 포함
- 01_project_analysis.md에서 인프라 코드 발견
- 01_project_analysis.md에서 인증·결제·PII 코드 발견
- Q4 = C 또는 D

## 산출물: `.agent-team/02_interview_result.md`

```
---
# 요구사항 인터뷰 결과

## 선택 항목
Q1: {선택 value + label}  Q2: {선택 value + label}  Q3: {선택 value + label}  Q4: {선택 value + label}  Q5: {선택 value + label}

## 인터랙션 방식
- terminal_select.py 사용 여부: yes/no
- status: OK / INTERACTIVE_REQUIRED / FALLBACK_PROMPT / DEFAULTED
- fallback 또는 default 사용 시 사유:

## 2B 추가 답변 (해당 시)
Q6: {값}  Q7: {값}  Q8: {값}  Q9: {값}

## 적용 보안 프로필
[Common] [Web] [Infrastructure] [DataPipeline] [AI·RAG]

## 설계서 반영 지침
(선택 결과 → 설계에 반영할 사항 정리)

## TDD 정책
- 기본값: Project-Aware TDD-first
- 01_project_analysis.md의 Test Environment Profile 기준으로 적용
- 테스트 인프라 신규 도입이 필요하면 사용자 승인 대상으로 표시
---
```
