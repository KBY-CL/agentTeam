# agent-team-builder

Claude Code 프로젝트에 최적화된 에이전트 팀을 자동으로 설계·검증·구현하는 스킬입니다.

## 설치 방법

### 1. Claude Code 설치 확인

```bash
claude --version
```

### 2. 스킬 설치

```bash
git clone --depth 1 https://github.com/KBY-CL/agentTeam && bash agentTeam/install.sh
```

### 3. Claude Code 재시작

이미 실행 중이면 새 세션을 열어야 스킬이 로드됩니다.

### 4. 사용

아무 프로젝트 디렉토리에서 Claude Code 실행 후 아래와 같이 입력합니다.

```
에이전트 팀을 만들어줘
```

## 업데이트

`install.sh`를 재실행하면 됩니다. 기존 버전은 자동으로 `.bak`으로 백업됩니다.

```bash
bash agentTeam/install.sh
```

## 주요 기능

- 프로젝트 자동 분석 및 에이전트 팀 설계
- Generate / Update / Audit 모드 지원
- 도메인별 보안 프로필 자동 적용 (Web, Infra, Data Pipeline, AI·RAG)
- Static Smoke Test로 구현 품질 자동 검증
- Drift Detection으로 설계-구현 불일치 탐지
- Preset 제공 (Minimal / Standard / Infra-Security)
