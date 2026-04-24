# Step 0 — Mode Detection

메인 Claude가 항상 가장 먼저 수행합니다.

## 로드 대상

- `references/policies/operation-modes.md`
- `references/policies/registry.md`

## 실행 절차

1. 사용자 요청에서 Generate / Update / Audit 신호를 찾습니다.
2. `.agent-team/registry.json` 존재 / 파싱 여부를 확인합니다.
3. Update / Audit 후보라면 Minimal Preflight를 실행합니다.
4. PASS / WARN / FAIL 결과에 따라 계속 진행 여부를 결정합니다.
5. 최종 mode를 명시적으로 선언한 뒤 해당 파이프라인으로 이동합니다.

## PASS / WARN / FAIL 처리

- `PASS`: 선택된 mode로 계속 진행
- `WARN`: Registry Recovery 또는 사용자 확인 후 진행
- `FAIL`: Update / Audit 중단, 복구 또는 Generate 제안

## 추가 규칙

- no-write 요청이 있으면 Audit Mode 우선
- 변경 요청이 있고 valid registry가 있으면 Update Mode 우선
- registry가 없고 신규 생성 요청이면 Generate Mode
- 변경 요청이지만 registry가 손상되었으면 Recovery 후 Update 가능 여부 판단
