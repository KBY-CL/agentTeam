# Operation Modes Policy

이 스킬은 실행 시작 시 반드시 하나의 operation mode를 선택합니다.

## Detection Inputs

- 사용자 요청 문구
- `.agent-team/registry.json` 존재 / 파싱 여부
- 기존 `.agent-team/03_agent_design_spec_v*.md` 등 산출물 존재 여부
- "수정하지 말고", "점검만" 같은 명시적 no-write 요청

## Mode Detection

### Generate Mode
- "에이전트 팀 만들어줘"
- "프로젝트에 맞는 agent team 구성해줘"
- 기존 `registry.json` 이 없음

### Update Mode
- "기존 agent team에 ___ 추가해줘"
- "verifier 강화해줘"
- "보안 에이전트 추가해줘"
- `registry.json` 이 유효하고 변경 요청이 있음

### Audit Mode
- "점검만 해줘"
- "문제 있는지 봐줘"
- "수정하지 말고 검토해줘"
- "drift 있는지 확인해줘"

## Detection Priority

1. 사용자가 명시적으로 no-write를 요구하면 Audit Mode
2. 변경 요청이 있고 `registry.json` 이 유효하면 Update Mode
3. 신규 생성 요청이거나 `registry.json` 이 없으면 Generate Mode
4. 변경 요청이 있지만 `registry.json` 이 손상되었으면 Registry Recovery 후 Update 여부 판단

## Minimal Preflight

Update / Audit 진입 전 아래를 확인합니다.
- `.agent-team/registry.json` 존재 / 파싱 여부
- `.claude/agents` 디렉토리 존재 여부
- `.claude/settings.json` JSON 파싱 가능 여부

결과 해석:
- `PASS`: 계속 진행
- `WARN`: Registry Recovery 또는 사용자 확인 후 진행
- `FAIL`: Update / Audit 중단, 복구 또는 Generate 제안

## Execution Paths

### Generate
`Step 1 → Step 2A/B → Step 3 → Step 4 → Step 4.5 → Step 5 → Step 6 → Step 7A → Step 7B(필요 시) → Step 9`

### Update
영향 범위를 Minor / Moderate / Major로 분류 후 부분 Step 3 재설계 여부를 결정합니다.

### Audit
`Step 8`만 수행하며 source/config 파일은 수정하지 않습니다.

## Step 7B Re-run Triggers

아래 변경이 있으면 Update Mode에서도 Step 7B를 재실행합니다.
- agent topology 변경
- 보안 프로필 변경
- verifier / security 책임 변경
- handoff 흐름 변경
- agent trigger condition 변경
