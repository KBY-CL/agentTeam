# 기존 파일 보호 정책

Step 5 구현 시 반드시 준수하세요.

## 수정 전 백업
기존 파일 수정 전 `.agent-team/backups/{timestamp}/`에 원본 복사.

## 수정 방식
- 전체 재작성 금지
- CLAUDE.md: `<!-- AGENT_TEAM_START -->` ~ `<!-- AGENT_TEAM_END -->` 마커 블록 내부만 수정
- 충돌 섹션 있으면 덮어쓰지 말고 사용자 승인 요청

## settings.json 병합 규칙
- 기존 hooks 배열 보존
- 동일 command가 이미 있으면 중복 추가 금지
- JSON 파싱 실패 시 수정 중단 + 오류 보고

## 수정 후 기록
diff summary를 `.agent-team/05_implementation_log.md`에 기록.

## .gitignore 보존 정책
`.agent-team/` 전체 ignore 금지. 임시 파일만 추가:
```
.claude/handoff/*.md
.agent-team/intake_*.md
.agent-team/backups/
.agent-team/tmp/
```
설계·검증·승인·로그 산출물(01~07*.md)은 보존.
