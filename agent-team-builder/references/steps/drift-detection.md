# Drift Detection — 설계-구현 불일치 탐지

Update Mode 또는 Audit Mode에서 실행. 설계서와 실제 구현 파일 간 불일치를 탐지합니다.

subagent_type: general-purpose / model: sonnet

## 입력 (Selective Read)
1. 최신 설계서 `.agent-team/03_agent_design_spec_v*.md` (가장 높은 버전)
2. `.agent-team/registry.json` (있는 경우)
3. `.claude/agents/*.md` — frontmatter + description만 확인 (각 30줄 이내)
4. `.claude/settings.json`

## 탐지 항목

**[모델 drift]**
□ 각 에이전트의 실제 model ID가 설계서 alias와 일치하는가
  (opus→claude-opus-4-7 / sonnet→claude-sonnet-4-6 / haiku→claude-haiku-4-5-20251001)

**[tools drift]**
□ 설계서의 tools 목록과 실제 frontmatter tools가 일치하는가
□ forbidden 목록이 실제 파일에 남아있는가

**[에이전트 존재 drift]**
□ 설계서의 모든 에이전트 파일이 실제로 존재하는가
□ 설계서에 없는 에이전트 파일이 추가되지 않았는가

**[보안 drift]**
□ shared-rules.md가 설계서의 보안 프로필을 여전히 반영하는가
□ doc-updater 호출 조건이 구현 에이전트 본문에 남아있는가

**[hooks drift]**
□ settings.json hooks가 설계서와 일치하는가

## 산출물: `.agent-team/drift_report_{timestamp}.md`

```
# Drift Detection 리포트

## 탐지 일시: {timestamp}
## 비교 대상: 설계서 v{N} ↔ 현재 구현

## 불일치 항목
| 항목 | 설계서 | 실제 구현 | 심각도 |
|---|---|---|---|
| {에이전트명}.model | opus | claude-sonnet-4-6 | high |

## 심각도 기준
- critical: 보안 책임·forbidden 누락
- high: model 불일치, tools 권한 변경
- medium: 에이전트 추가/삭제
- low: 설명 문구 변경

## 권장 조치
(항목별 수정 방법)

## 결론
[CLEAN] 불일치 없음
[DRIFT] {N}개 불일치 발견 — Update Mode로 수정 권장
```

마지막 줄: [CLEAN] 또는 [DRIFT]
