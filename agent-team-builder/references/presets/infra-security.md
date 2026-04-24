# Preset: Infra / Security Heavy (6 Agents)

인프라 자동화 또는 높은 보안 요구사항 프로젝트에 적합한 풀 구성입니다.

## 에이전트 구성

### 1. Request Intake Agent
- model: sonnet
- 역할: 개발 요청 접수, 위험도 사전 분류 포함
- tools: Read, Glob
- forbidden: Write, Edit, Bash

### 2. Analyzer
- model: opus
- 역할: 영향 범위 분석, 인프라 변경 사전 검토
- tools: Read, Grep, Glob
- forbidden: Write, Edit, Bash, 인프라 apply

### 3. Implementer
- model: sonnet
- 역할: 코드 구현 (인프라 코드 제외)
- tools: Read, Write, Edit, Grep, Glob, Bash
- forbidden: terraform apply, kubectl apply, 운영 DB 접근

### 4. Infra Reviewer
- model: opus
- 역할: 인프라 변경 검토 전용 (plan 결과 분석, apply 금지)
- tools: Read, Grep, Glob, Bash(plan/diff 전용)
- forbidden: terraform apply, cloudformation deploy, kubectl apply

### 5. Security Reviewer
- model: opus
- 역할: 전 단계 보안 검토 (Web + Infra 보안 프로필)
- tools: Read, Grep, Glob
- forbidden: Write, Edit, Bash

### 6. Doc Updater Agent
- model: haiku
- 역할: 문서 업데이트 전담
- tools: Read, Write, Edit
- forbidden: Bash, 코드 파일 수정

## 공통 구성
- shared-rules.md: Common + Web + Infrastructure 보안 규칙
- 공통 hook: 인프라 변경 시 Infra Reviewer 자동 트리거
- doc-updater 스킬: Doc Updater Agent 전담

## 적합한 프로젝트
- 인프라 자동화 (Terraform, k8s)
- 금융·의료 등 고보안 요구 서비스
- 보안 수준 C
