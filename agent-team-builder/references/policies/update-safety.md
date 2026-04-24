# Update Mode Safety Policy

Update Mode는 유용하지만 가장 위험한 모드이기도 합니다.
기존 팀 전체를 다시 생성하지 않고, 필요한 범위만 안전하게 수정해야 합니다.

## Non-negotiables

- 전체 재생성 기본 금지
- 변경 대상 파일 목록을 먼저 제시
- 기존 파일은 백업 후 수정
- 마커 블록 또는 관련 섹션만 수정
- 성공적인 Update 후 `registry.json` 갱신 필수

## Update Impact Scope

### Minor
- 설명 문구 수정
- agent description 개선
- 문서 호출 조건 보완

실행 규칙:
- Step 4 quick validation
- Step 5는 관련 문서 / 본문 일부만 수정

### Moderate
- agent tools 변경 없음
- agent 책임 일부 조정
- skill 호출 조건 추가

실행 규칙:
- Step 3 partial design
- Step 4 validation
- Step 5 부분 구현

### Major
- agent 추가 / 삭제
- tools 권한 변경
- 보안 프로필 변경
- verifier / security 책임 변경

실행 규칙:
- Step 3 full design refresh
- Step 4
- Step 4.5
- Step 5
- Step 7B 조건부 재실행

## Escalation

아래 중 하나라도 참이면 사용자 승인 후 Generate 재실행 제안을 우선 검토합니다.
- 변경 범위가 3개 agent 이상
- agent topology 재구성 필요
- 보안 프로필 전면 재설계 필요
- handoff / trigger 구조가 크게 변경됨
