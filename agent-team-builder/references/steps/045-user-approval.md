# Step 4.5 — 사용자 승인 (메인 Claude 직접 수행)

references/policies/approval-and-revalidation.md도 이 단계에서 로드하세요.

## 브리핑 형식

```
## 에이전트 팀 설계 브리핑

검증이 완료되었습니다. 아래 구성을 확인하고 승인해 주세요.

### 에이전트 팀 ({N}개)
1. {에이전트명} ({alias}) — {한 줄 역할} | 왜 필요한가: {이유}
2. ...

### 적용 보안 프로필
{탐지 도메인 + Q3 수준 기반 한 줄 요약}

### 공통 구성요소
{공통 hooks / 보안 규칙 요약}
※ doc-updater는 구현 에이전트 본문에서 조건부 호출됩니다.

---
A) 승인 — 구현을 시작합니다
B) 에이전트 제거
C) 에이전트 추가
D) 역할 수정
E) 처음부터 재시작

선택:
```

## 처리 로직

수정 발생 시 approval-and-revalidation.md의 재검증 규칙에 따라 처리.
- A → Step 5 진행
- B/C/D → 수정 유형 분류 후 Step 4 재실행 또는 바로 Step 5 진행
- E → design_loop=1 초기화, Step 3 재시작
