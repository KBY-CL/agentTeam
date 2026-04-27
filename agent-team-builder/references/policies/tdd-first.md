# Project-Aware TDD-first Policy

agent team은 개발 요청을 처리할 때 현재 프로젝트의 테스트 생태계에 맞춘 TDD-first 흐름을 기본값으로 사용합니다.

## 원칙

- TDD는 프로젝트 분석 결과를 기준으로 수행합니다.
- 새 테스트 프레임워크, 디렉토리, fixture 체계를 임의로 추가하지 않습니다.
- 기존 테스트 도구, 파일 위치, naming convention, mock/factory/fixture 방식, CI 명령을 우선 따릅니다.
- production code 수정은 실패 테스트 작성과 Red 검증 이후에만 허용합니다.
- Red 실패는 기능 미구현 때문에 발생해야 합니다. import 오류, 설정 오류, fixture 오류, 문법 오류, flaky 실패는 Red 통과가 아닙니다.
- Green 검증은 프로젝트의 실제 test command 또는 CI command를 기준으로 합니다.
- 테스트 인프라가 없으면 사용자 승인 전까지 신규 프레임워크를 추가하지 않습니다. 대신 최소 도입안을 제안합니다.

## Test Environment Profile

Step 1은 아래 항목을 `.agent-team/01_project_analysis.md`에 기록해야 합니다.

- 테스트 프레임워크: pytest, jest, vitest, junit, go test 등
- 테스트 파일 위치: `tests/`, `__tests__/`, `*.spec.*`, `*.test.*` 등
- 테스트 실행 명령: package script, make target, CI command
- 테스트 레벨: unit / integration / e2e 구분 방식
- mock, fixture, factory, test database 사용 방식
- coverage 또는 CI gate 여부
- 테스트 인프라 부재 여부와 신규 도입 필요성

## Required TDD Gate

개발 요청을 처리하는 agent 흐름에는 아래 gate가 있어야 합니다.

```text
Request Intake
→ Acceptance Criteria
→ Test Strategy
→ Failing Test 작성
→ Red Verification
→ Minimal Implementation
→ Green Verification
→ Refactor
→ Regression/Security Verification
→ Documentation Update
```

소규모 팀에서는 여러 책임을 한 agent가 맡을 수 있지만, handoff와 출력 계약에는 Red/Green gate가 명확히 분리되어야 합니다.

## Agent Responsibility Rules

- Request Intake Agent는 요구사항, 영향 범위, 수용 기준, 관련 테스트 범위를 정리합니다.
- Test Strategy 또는 Test Writer 책임자는 기존 프로젝트 관례에 맞는 실패 테스트를 먼저 작성합니다.
- Red Verifier는 새 테스트가 실패하는지와 실패 이유가 올바른지 확인합니다.
- Implementation Agent는 Red Verifier의 `[PASS]` 없이는 production code를 수정하지 않습니다.
- Implementation Agent는 테스트를 통과시키는 최소 변경만 수행합니다.
- Green Verifier는 관련 테스트와 필요한 회귀 테스트를 실행합니다.
- Refactor는 Green 이후에만 수행하며, refactor 이후 관련 테스트를 다시 실행합니다.
- doc-updater는 기능 개발 완료 후에만 호출합니다.

## No Existing Test Infrastructure

테스트 인프라가 없거나 실행 명령을 식별할 수 없으면 다음 순서를 따릅니다.

1. 현재 프로젝트에 테스트 도입 흔적이 없는지 재확인합니다.
2. 언어와 프레임워크 기준의 최소 테스트 도입안을 제안합니다.
3. 사용자 승인 전에는 dependency 추가, 설정 파일 생성, CI 변경을 하지 않습니다.
4. 승인되면 최소 테스트 harness부터 추가하고 첫 failing test를 작성합니다.

## Validation Requirements

Step 4와 Step 6은 아래 항목을 검증해야 합니다.

- 설계서 또는 agent 파일에 Project-Aware TDD Gate가 있는가
- Test Environment Profile이 설계와 구현에 반영되었는가
- 기존 테스트 관례를 우선하도록 명시되어 있는가
- Red Verifier 승인 없이 implementation이 시작되지 않는가
- Red 실패 원인 검증 조건이 있는가
- Green 검증 명령이 프로젝트의 실제 명령과 연결되어 있는가
- 테스트 인프라 신규 도입이 사용자 승인 대상으로 표시되어 있는가
