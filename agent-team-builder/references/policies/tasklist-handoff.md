# Tasklist Handoff Policy

구현 agent의 컨텍스트 오염을 줄이기 위해 검증된 설계와 TDD 흐름을 실행 가능한 tasklist로 압축해 전달합니다.

## Ownership

- 기본 생성자: `feature-architect-agent` (기능 설계 에이전트)
- 검토자: test strategy 책임자, red verifier, quality/security verifier
- 소비자: `implementation-agent`
- 큰 팀에서만 별도 `task-planner-agent` 또는 `task-breakdown-agent` 추가를 검토합니다. 기본값은 추가하지 않습니다.

## Required Flow

```text
Request Intake
→ Feature Design
→ Test Strategy
→ Implementation Tasklist 작성
→ Tasklist Verification
→ Red Test 작성/검증
→ Implementation Agent가 승인된 tasklist만 실행
→ Green Verification
→ Refactor/Quality Review
```

## Context Boundary

- Implementation Agent는 전체 설계서, 인터뷰 원문, 긴 검증 로그를 기본 입력으로 받지 않습니다.
- Implementation Agent의 기본 입력은 승인된 tasklist, 관련 handoff 요약, 수정 대상 파일 목록, 테스트 명령입니다.
- 필요할 때만 tasklist에 명시된 파일과 섹션을 선택적으로 읽습니다.
- tasklist에 없는 파일 수정, 순서 변경, 범위 확장은 verifier 또는 사용자 승인 없이는 금지합니다.

## Tasklist Template

```markdown
# Implementation Tasklist

## Source
- feature design:
- test environment profile:
- test strategy:
- red verification:

## Global Rules
- Red PASS 없는 production code 수정 금지
- task 순서 변경 금지
- task별 files 범위 밖 수정 금지
- 관련 테스트 명령과 결과 기록

## Tasks

### T1 — 실패 테스트 작성
- owner: test-writer
- files:
- command:
- done_when: 기능 미구현 사유로 실패

### T2 — 최소 구현
- owner: implementation-agent
- depends_on: T1 Red PASS
- files:
- forbidden: unrelated refactor
- done_when: 지정 테스트 Green

### T3 — 리팩터링
- owner: implementation-agent
- depends_on: T2 Green PASS
- files:
- done_when: 관련 테스트 재통과
```

## Validation Requirements

- task마다 owner, depends_on, files, done_when이 있어야 합니다.
- production code 수정 task는 Red PASS에 의존해야 합니다.
- Implementation Agent 입력은 승인된 tasklist 중심이어야 합니다.
- tasklist 승인 전 구현 시작은 FAIL입니다.
