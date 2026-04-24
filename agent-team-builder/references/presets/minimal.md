# Preset: Minimal (3 Agents)

소규모 팀(1~5인) 또는 단순 프로젝트에 적합한 최소 구성입니다.

## 에이전트 구성

### 1. Request Intake Agent
- model: sonnet
- 역할: 개발 요청 접수 및 요구사항 구체화 (선택지 기반)
- tools: Read, Glob
- forbidden: Write, Edit, Bash

### 2. Implementer
- model: sonnet
- 역할: 코드 구현, 파일 생성·수정
- tools: Read, Write, Edit, Grep, Glob, Bash
- forbidden: git push, 운영 DB 직접 접근

### 3. Verifier
- model: opus
- 역할: 코드 리뷰, 보안 검토, 테스트 검증, doc-updater 호출
- tools: Read, Grep, Glob, Bash(읽기 전용)
- forbidden: Write, Edit

## 공통 구성
- shared-rules.md: Common 보안 규칙
- doc-updater 스킬: Verifier 본문에서 조건부 호출
- handoff-writer 스킬: 공통

## 적합한 프로젝트
- 단일 개발자 프로젝트
- MVP / 프로토타입
- 단순 웹앱 (보안 수준 A/B)
