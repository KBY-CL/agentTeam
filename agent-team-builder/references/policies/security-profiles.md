# 보안 프로필

Step 1 탐지 결과 + Step 2A Q3 수준을 기반으로 적용 프로필을 선택하세요.
모든 프로젝트에 Common을 적용하고, 탐지된 도메인 프로필을 추가합니다.

## Common Security (전체 필수)
- secrets(API 키·비밀번호·토큰) 코드 하드코딩 금지 → 환경변수 사용
- 외부 입력 반드시 검증 후 사용
- 최소 권한 원칙 적용
- 로그에 민감정보·원본 데이터 출력 금지
- 의존성 취약점 확인 (outdated·취약 패키지)

## Web App Security (auth·session·jwt·oauth 발견 시)
- OWASP Top 10 준수
  - A01 접근 제어 (IDOR, 권한 상승)
  - A02 암호화 실패 (민감정보 노출, 약한 암호화)
  - A03 인젝션 (SQLi, XSS, Command Injection)
  - A07 인증·세션 관리 실패
  - A08 소프트웨어·데이터 무결성 실패
- CSRF·XSS 방어 / CORS·CSP 설정
- 인증·인가·세션 관리 / IDOR 방지
- 입력 검증 및 출력 인코딩

## Infrastructure Security (terraform·cloudformation·cdk 발견 시)
- terraform plan 필수, apply 금지 또는 사용자 승인 필수
- IAM wildcard(*) 금지
- public ingress 반드시 검토
- 암호화·백업·태그 정책
- Q6=C(인프라 apply) → forbidden에 명시

## Data Pipeline Security (data/·pipeline/·airflow·dbt 발견 시)
- PII 마스킹
- 원본 데이터 접근 권한 최소화
- 데이터 보존 정책 준수
- 샘플링·익명화 적용
- 로그에 원본 데이터 출력 금지

## AI·RAG Security (rag/·embeddings/·vector/·llm/ 발견 시)
- 프롬프트 인젝션 방어
- retrieval source 검증
- 민감 문서 검색 제한
- tool call 승인 정책
- 사용자 입력과 시스템 지시 분리
