# Step 2B — 위험도 기반 추가 질문 (조건부)

2A 답변과 01_project_analysis.md 기반으로 해당 조건의 질문만 선택해 진행하세요.

```
Q6. 자동화 금지 영역 (Q3=C 또는 Q1에 C 포함 시)
A) 운영 DB 변경   B) 배포 실행   C) 인프라 apply
D) 결제·권한·인증 코드 수정   E) 없음   F) 기타

Q7. 외부 시스템 연동 범위 (Q1에 C 포함 또는 인프라 코드 발견 시)
A) GitHub·GitLab만
B) AWS·GCP·Azure 조회 필요
C) Jira·Notion·Slack 연동 필요
D) 외부 시스템 연동 불필요

Q8. 검증 기준 (Q2에 A·B·C 포함 시)
A) 린트·타입체크 중심   B) 단위 테스트 필수
C) 통합 테스트 필수     D) 보안 리뷰 필수
E) 성능·부하 테스트 필요

Q9. 문서화 범위 (Q1에 D 포함 시)
A) CLAUDE.md만   B) AGENTS.md + CLAUDE.md
C) 서비스 구조 문서까지   D) API 문서까지
```

답변을 `02_interview_result.md`의 "2B 추가 답변" 섹션에 추가하세요.
