# Step 2A — Bootstrap Interview

01_project_analysis.md를 읽은 후 **`deep-interview` 스킬을 invoke**하여 인터뷰를 진행하세요.

## deep-interview 호출 방법

아래 맥락을 argument로 전달하세요:

```
프로젝트: {01_project_analysis.md에서 추출한 프로젝트명 및 기술 스택 요약}

다음 결정 사항을 파악해야 합니다:
- 에이전트 팀의 주요 목적 (기능 개발 / 품질 / 배포자동화 / 문서화 / 보안)
- 가장 자주 발생하는 반복 작업
- 보안 요구사항 수준 (기본 / 중간 / 높음)
- 팀 규모
- 초기 에이전트 수 (최소 3개 / 표준 4~5개 / 풀 6개)
```

`deep-interview`가 소크라테스식으로 한 번에 하나씩 질문하여 위 결정 사항을 파악합니다.

## 참고: 기존 선택지 구조 (매핑 시 사용)

인터뷰 종료 후 결정사항을 아래 구조로 매핑하여 `02_interview_result.md`에 기록하세요.

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
Q1: {값}  Q2: {값}  Q3: {값}  Q4: {값}  Q5: {값}

## 2B 추가 답변 (해당 시)
Q6: {값}  Q7: {값}  Q8: {값}  Q9: {값}

## 적용 보안 프로필
[Common] [Web] [Infrastructure] [DataPipeline] [AI·RAG]

## 설계서 반영 지침
(선택 결과 → 설계에 반영할 사항 정리)

## TDD 정책
- 기본값: Project-Aware TDD-first
- 01_project_analysis.md의 Test Environment Profile 기준으로 적용
- `.agent-team/test_pattern_guide.md`의 테스트 작성 패턴 기준으로 실패 테스트 작성
- 테스트 인프라 신규 도입이 필요하면 사용자 승인 대상으로 표시
---
```
