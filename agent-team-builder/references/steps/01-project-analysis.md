# Step 1 — 프로젝트 분석 에이전트

subagent_type: Explore / model: sonnet

## Exploration Budget (반드시 준수)

1. 먼저 파일 목록만 수집 (tree depth 3, 최대 300 paths)
   - 제외: node_modules, dist, build, target, .git, .next, coverage, vendor, __pycache__

2. 파일 본문 Read는 카테고리별 최대치 적용:
   - 의존성/설정 파일: 최대 20개
   - README/docs: 최대 10개, 각 200줄 이하
   - 주요 소스 샘플: 언어·레이어별 최대 3개, 각 150줄 이하
   - CI/CD 파일: 최대 10개

3. 긴 파일은 전문 금지 — 헤더, import/dependency 영역, 주요 함수 시그니처, 보안 키워드 주변 30줄만 읽음

4. 분석 결과에 "읽은 파일 목록"과 "읽지 않은 고위험 후보"를 분리 기록

## 보안 도메인 자동 탐지

- auth/session/jwt/oauth 발견 → 웹 앱 보안 프로필
- terraform/cloudformation/cdk 발견 → 인프라 보안 프로필
- data/, pipeline/, airflow/, dbt/ 발견 → 데이터 파이프라인 보안 프로필
- rag/, embeddings/, vector/, llm/ 발견 → AI·RAG 보안 프로필

## 테스트 패턴 분석

`references/policies/test-pattern-guide.md`를 함께 적용하여 `.agent-team/test_pattern_guide.md`를 생성하세요.

- 기존 테스트 파일, setup 파일, fixture/factory/mock helper, package script, CI command를 우선 확인합니다.
- 대표 테스트 파일은 최대 5개, helper/setup 파일은 최대 5개, 각 150줄 이하만 읽습니다.
- production 파일과 test 파일의 매핑, naming, assertion, mock/fixture/factory, database/async setup, cleanup 방식을 기록합니다.
- 테스트가 없으면 "테스트 인프라 없음"으로 명시하고, dependency/config/CI 변경이 필요한 최소 도입안을 사용자 승인 대상으로 분리합니다.
- 불확실한 부분은 추정하지 말고 confidence와 gaps에 기록합니다.

## 산출물: `.agent-team/01_project_analysis.md`

```
# 프로젝트 분석 보고서

## 기술 스택
언어 / 프레임워크 / 주요 라이브러리

## 개발 환경
빌드 도구 / 패키지 매니저 / 런타임 버전

## 코드 컨벤션
린터·포맷터 / 네이밍 / 테스트 프레임워크

## Test Environment Profile
- 테스트 프레임워크: pytest / jest / vitest / junit / go test / 기타 / 없음
- 테스트 파일 위치: tests/ / __tests__/ / *.spec.* / *.test.* / 기타
- 테스트 실행 명령: package script / make target / CI command / 미확인
- 테스트 레벨: unit / integration / e2e 구분 방식
- mock·fixture·factory·test database 사용 방식
- coverage 또는 CI gate 여부
- 테스트 인프라 부재 시: 신규 도입 필요성과 사용자 승인 필요 여부
- Test Pattern Guide: .agent-team/test_pattern_guide.md

## 디렉토리 구조 (depth 3, 핵심만)

## CI/CD
파이프라인 / 배포 방식

## 보안 도메인 현황
탐지된 보안 프로필: [Common / Web / Infrastructure / DataPipeline / AI·RAG]
- auth·JWT 발견 여부
- 인프라 코드 발견 여부
- 결제·PII 코드 발견 여부

## 탐색 메타
- 읽은 파일 수: N개
- 읽지 않은 고위험 후보: (있으면 목록)

## 에이전트 팀 설계를 위한 핵심 관찰
- 반복 작업 패턴
- 자동화 가능 영역
- 자동화 금지 고위험 영역
- Request Intake Agent가 파악해야 할 특이사항
```

## 산출물: `.agent-team/test_pattern_guide.md`

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
- preferred style:
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
짧은 골격만 기록합니다.

## Gaps And Approval Needs
- missing or uncertain patterns:
- dependency/config/CI changes requiring user approval:

## Evidence
- files inspected:
- commands inspected:
```
