# Step 0 — Preflight Compatibility Check (메인 Claude 직접 수행)

파이프라인 시작 전 환경 호환성을 확인합니다. 문제 발견 시 사용자에게 알리고 계속 진행할지 확인합니다.

## 확인 항목

### Operation Mode 선택
기존 .agent-team/ 폴더 존재 여부를 확인하세요.

**존재하지 않으면** → Generate Mode (신규 생성) 자동 선택

**존재하면** 사용자에게 모드를 선택받으세요:
```
기존 에이전트 팀이 감지되었습니다. 어떤 작업을 할까요?

A) Generate Mode — 기존 내용을 무시하고 새로 생성
B) Update Mode  — 기존 에이전트 팀의 일부를 수정
C) Audit Mode   — 현재 구조만 검증 (파일 생성 없음)

선택:
```

- **A (Generate)**: 전체 파이프라인 실행 (Step 1~7)
- **B (Update)**: Step 2A 대신 변경 범위 인터뷰 → 영향받는 Step만 실행
- **C (Audit)**: Step 4(설계 검증) + Step 6(Reflect) + Step 7A(Smoke) 만 실행

### 환경 호환성 확인
아래 항목을 순서대로 확인하세요:

```
□ .claude/ 디렉토리 존재 여부 (Claude Code 환경)
□ .claude/settings.json 구조: JSON 유효성, hooks 필드 형식
□ Python 사용 가능 여부 (Step 7A 스크립트 실행용)
  - `python3 --version` 또는 `python --version`
□ .agent-team/registry.json 존재 시: 마지막 실행 정보 로드
```

### Preflight 결과 처리
- 모든 항목 통과 → 선택된 모드로 파이프라인 시작
- 경고 항목 있음 → 사용자에게 알리고 계속 진행 여부 확인
- Python 없음 → "Step 7A 스크립트 실행 불가. AI가 직접 정적 검사를 수행합니다." 안내

## Update Mode 실행 흐름

Update Mode 선택 시:
```
어떤 부분을 수정할까요? (복수 선택 가능)

A) 에이전트 추가/삭제/역할 변경
B) 보안 프로필 변경
C) tools/hooks/skills 변경
D) 문서(CLAUDE.md/AGENTS.md)만 업데이트
E) 전체 재검증 (코드 변경 없이 Audit)

선택:
```

- A/B/C 선택: registry.json 로드 → 변경 범위 파악 → Step 3(설계) ~ Step 6(Reflect) 실행
- D 선택: doc-updater 스킬 직접 실행
- E 선택: Audit Mode와 동일

## Audit Mode 실행 흐름

기존 파일을 수정하지 않고 검증만 수행:
1. Step 4 체크리스트로 현재 설계서 검증
2. Step 6 체크리스트로 현재 구현 파일 검증
3. Step 7A Static Smoke Test 실행
4. 결과를 `.agent-team/audit_{timestamp}.md`에 저장
