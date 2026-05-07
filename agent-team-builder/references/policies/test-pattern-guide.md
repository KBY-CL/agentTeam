# Test Pattern Guide Policy

Project-Aware TDD는 테스트 도구 이름만 아는 것으로 충분하지 않습니다. agent team은 구현 전에 현재 프로젝트의 테스트 작성 관례를 별도 문서로 남기고, Red/Green 작업의 기본 근거로 사용해야 합니다.

## Canonical File

- canonical path: `.agent-team/test_pattern_guide.md`
- 생성 시점: Step 1 프로젝트 분석 중
- 사용 시점: Step 3 설계, Step 5 구현, 기능 설계, test writer, red verifier, implementation-agent, green verifier

## Analysis Rules

- 새 테스트 프레임워크나 디렉토리 구조를 제안하기 전에 기존 테스트 작성 관례를 먼저 찾습니다.
- 테스트 파일, setup 파일, fixture/factory/mock helper, CI 명령, package script를 함께 확인합니다.
- 샘플은 대표성 있게 읽되 과도하게 로드하지 않습니다. 기본 예산은 테스트 파일 최대 5개, helper/setup 파일 최대 5개, 각 150줄 이하입니다.
- 테스트가 없으면 "테스트 인프라 없음"으로 명시하고, 언어·프레임워크 기준 최소 도입안을 사용자 승인 대상으로 분리합니다.

## Required Content

`.agent-team/test_pattern_guide.md`에는 아래 항목이 있어야 합니다.

```markdown
# Test Pattern Guide

## Summary
- status: existing-tests | partial-tests | no-test-infrastructure | unknown
- primary frameworks:
- test commands:
- confidence: high | medium | low

## File Placement And Naming
- production-to-test mapping:
- naming convention:
- colocated or separate tests:

## Test Structure
- preferred style: AAA / Given-When-Then / describe-it / class-based / table-driven / other
- naming style:
- assertion style:
- async or database setup:

## Fixtures, Mocks, And Factories
- fixture sources:
- mock/stub approach:
- factory/builders:
- test data cleanup:

## Commands
- focused red command:
- related green command:
- full regression command:
- CI command or gate:

## Copyable Test Skeletons
짧은 골격만 기록합니다. 프로젝트 코드를 대량 복사하지 않습니다.

## Gaps And Approval Needs
- missing or uncertain patterns:
- dependency/config/CI changes requiring user approval:

## Evidence
- files inspected:
- commands inspected:
```

## Agent Usage Rules

- Test writer는 실패 테스트 작성 전에 이 문서를 읽고, 선택한 패턴을 handoff에 기록합니다.
- Red verifier는 실패 원인뿐 아니라 테스트가 이 문서의 패턴을 따르는지도 확인합니다.
- Implementation Agent는 승인된 tasklist와 이 문서에 명시된 테스트 명령만 기본 입력으로 사용합니다.
- Green verifier는 이 문서의 related/full regression command를 우선 실행합니다.
- 문서가 없거나 confidence가 low이면 production code 수정 전에 패턴 재조사 또는 사용자 확인이 필요합니다.

## Validation Requirements

- 설계서와 agent 파일이 `.agent-team/test_pattern_guide.md`를 참조해야 합니다.
- implementation tasklist의 Source에 test pattern guide 경로가 있어야 합니다.
- tdd-workflow 스킬은 Test Environment Profile과 Test Pattern Guide를 모두 확인해야 합니다.
- registry의 `development_methodology.test_pattern_guide`에 canonical path를 기록합니다.
