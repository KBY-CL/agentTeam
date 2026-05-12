# Step 2B — 위험도 기반 추가 질문 (조건부)

2A 답변과 01_project_analysis.md 기반으로 해당 조건에 해당하는 경우 **`deep-interview` 스킬을 invoke**하여 추가 인터뷰를 진행하세요.

## deep-interview 호출 방법

아래 맥락을 argument로 전달하세요:

```
Step 2A 결과: {02_interview_result.md의 Q1~Q5 요약}
프로젝트 분석: {보안/인프라/인증 관련 발견 사항}

다음 위험 영역에 대해 추가로 파악해야 합니다:
- 자동화 금지 영역 (운영 DB / 배포 / 인프라 / 결제·인증 코드)  ← Q3=C 또는 Q1에 C 포함 시
- 외부 시스템 연동 범위  ← Q1에 C 포함 또는 인프라 코드 발견 시
- TDD 검증 기준  ← Q2에 A·B·C 포함 시
- 문서화 범위  ← Q1에 D 포함 시
```

해당하는 조건의 질문만 포함하여 전달하세요. `deep-interview`가 소크라테스식으로 한 번에 하나씩 질문합니다.

## 참고: 기존 선택지 구조 (매핑 시 사용)

인터뷰 종료 후 결정사항을 아래 구조로 매핑하여 `02_interview_result.md`의 "2B 추가 답변" 섹션에 기록하세요.

```
Q6. 자동화 금지 영역 (Q3=C 또는 Q1에 C 포함 시)
A) 운영 DB 변경   B) 배포 실행   C) 인프라 apply
D) 결제·권한·인증 코드 수정   E) 없음   F) 기타

Q7. 외부 시스템 연동 범위 (Q1에 C 포함 또는 인프라 코드 발견 시)
A) GitHub·GitLab만
B) AWS·GCP·Azure 조회 필요
C) Jira·Notion·Slack 연동 필요
D) 외부 시스템 연동 불필요

Q8. TDD 검증 기준 (Q2에 A·B·C 포함 시)
A) 기존 테스트 명령과 Test Pattern Guide 기준 Red/Green 필수
B) 단위 테스트 필수
C) 통합 테스트 필수
D) 보안 리뷰 필수
E) 성능·부하 테스트 필요
F) 테스트 인프라가 없으면 최소 도입안 승인 후 진행

Q9. 문서화 범위 (Q1에 D 포함 시)
A) CLAUDE.md만   B) AGENTS.md + CLAUDE.md
C) 서비스 구조 문서까지   D) API 문서까지
```
