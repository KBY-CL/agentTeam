# Preset: Standard (5 Agents)

중규모 팀(2~15인), 일반 웹 서비스에 권장하는 표준 구성입니다.

## 에이전트 구성

### 1. Request Intake Agent
- model: sonnet
- 역할: 개발 요청 접수, 요구사항 선택지 기반 구체화
- tools: Read, Glob
- forbidden: Write, Edit, Bash

### 2. Analyzer
- model: opus
- 역할: 영향 범위 분석, 기술 검토, 설계 제안
- tools: Read, Grep, Glob
- forbidden: Write, Edit, Bash

### 3. Implementer
- model: sonnet
- 역할: 코드 구현, 파일 생성·수정
- tools: Read, Write, Edit, Grep, Glob, Bash
- forbidden: git push, 운영 DB 직접 접근, 인프라 변경

### 4. Verifier
- model: opus
- 역할: 코드 리뷰, 보안 검토 (Web 보안 프로필), 테스트 실행
- tools: Read, Grep, Glob, Bash(읽기 전용)
- forbidden: Write, Edit

### 5. Doc Updater Agent
- model: haiku
- 역할: CLAUDE.md, AGENTS.md, service-structure.md 업데이트
- tools: Read, Write, Edit
- forbidden: Bash, 코드 파일 수정

## 공통 구성
- shared-rules.md: Common + Web 보안 규칙
- doc-updater 스킬: Doc Updater Agent에 할당 + Verifier 본문 조건부 호출
- handoff-writer 스킬: 공통

## 적합한 프로젝트
- 일반 웹 서비스 (REST API, SPA)
- 중규모 팀
- 보안 수준 B
