# Reference Manifest

이 파일은 항상 로드됩니다. 다른 reference 파일은 단계별로 필요할 때만 로드하세요.

## 파일 목록 및 로드 조건

### steps/ — 단계별 프롬프트 (해당 단계 직전에만 로드)
| 파일 | 로드 시점 |
|---|---|
| steps/00-mode-detection.md | 스킬 시작 직후 |
| steps/01-project-analysis.md | Step 1 실행 전 |
| steps/02a-bootstrap-interview.md | Step 2A 실행 전 |
| steps/02b-risk-interview.md | Step 2B 진입 조건 충족 시 |
| steps/03-design-spec.md | Step 3 실행 전 |
| steps/04-design-validation.md | Step 4 실행 전 |
| steps/045-user-approval.md | Step 4.5 실행 전 |
| steps/05-implementation.md | Step 5 실행 전 |
| steps/06-reflect-validation.md | Step 6 실행 전 |
| steps/07a-static-smoke.md | Step 7A 실행 전 |
| steps/07b-workflow-simulation.md | Step 7B 실행 전 |
| steps/08-audit.md | Audit Mode 진입 시 |
| steps/09-registry-update.md | Generate / Update 완료 후 registry 갱신 직전 |

### policies/ — 정책 문서 (관련 단계에서 함께 로드)
| 파일 | 함께 로드할 단계 |
|---|---|
| policies/operation-modes.md | Step 0 |
| policies/registry.md | Step 0, Step 8, Step 9 |
| policies/drift-detection.md | Step 8 |
| policies/update-safety.md | Step 5 (Update Mode) |
| policies/audit-mode.md | Step 8 |
| policies/security-profiles.md | Step 3 |
| policies/file-protection.md | Step 5 |
| policies/approval-and-revalidation.md | Step 4.5 |

### schemas/ — 기계 판독용 스키마
| 파일 | 함께 로드할 단계 |
|---|---|
| schemas/registry.schema.json | Step 7A, Step 9 |

### scripts/ — 실행 스크립트
| 파일 | 사용 단계 |
|---|---|
| scripts/static_smoke.py | Step 7A |

### checklists/ — 검증 체크리스트
| 파일 | 함께 로드할 단계 |
|---|---|
| checklists/context-budget.md | Step 4, Step 6, Step 8 |

### presets/ — 에이전트 팀 프리셋 (Step 3에서 참고용)
| 파일 | 적합한 상황 |
|---|---|
| presets/minimal.md | 소규모(1~5인), MVP, 단순 웹앱 |
| presets/standard.md | 중규모(2~15인), 일반 웹 서비스 |
| presets/infra-security.md | 인프라 자동화, 금융·의료 고보안 서비스 |

### 기타
| 파일 | 설명 |
|---|---|
| agent-team-guide.md | 전체 가이드 원문 — Step 3·4에서 안티패턴/구조 원칙 확인 시 필요 섹션만 부분 Read |

### legacy / 호환 문서
| 파일 | 설명 |
|---|---|
| steps/00-preflight.md | 이전 버전 preflight 문서. 기본 로드 없음 |
| steps/drift-detection.md | 이전 버전 단일 drift note. 기본 로드 없음 |

## Context Budget 요약

| 대상 | 권장 | 하드 제한 |
|---|---:|---:|
| 각 step 프롬프트 파일 | 80~150줄 | 250줄 |
| CLAUDE.md | 120줄 | 200줄 |
| AGENTS.md | 150~250줄 | 300줄 |
| .claude/agents/*.md 각 파일 | 120~180줄 | 250줄 |
| shared-rules.md | 80~120줄 | 200줄 |
| Handoff 파일 | 40~80줄 | 200줄 |
