#!/usr/bin/env bash
# agent-team-builder installer
# Usage: bash install.sh

set -e

SKILL_NAME="agent-team-builder"
REPO_URL="https://github.com/KBY-CL/agentTeam"
SKILLS_DIR="${HOME}/.claude/skills"
TARGET="${SKILLS_DIR}/${SKILL_NAME}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== agent-team-builder installer ==="

# --- 설치 소스 결정 ---
if [ -f "${SCRIPT_DIR}/${SKILL_NAME}/SKILL.md" ]; then
  # 로컬 리포에서 실행 중
  SOURCE="${SCRIPT_DIR}/${SKILL_NAME}"
  echo "소스: 로컬 (${SOURCE})"
else
  # 원격에서 클론
  TMP_DIR="$(mktemp -d)"
  trap 'rm -rf "$TMP_DIR"' EXIT
  echo "소스: GitHub (${REPO_URL})"
  git clone --depth 1 "$REPO_URL" "$TMP_DIR" 2>/dev/null
  SOURCE="${TMP_DIR}/${SKILL_NAME}"
fi

# --- 기존 설치 백업 ---
if [ -d "$TARGET" ]; then
  BACKUP="${TARGET}.bak.$(date +%Y%m%d%H%M%S)"
  echo "기존 설치 백업 → ${BACKUP}"
  mv "$TARGET" "$BACKUP"
fi

# --- 설치 ---
mkdir -p "$SKILLS_DIR"
cp -r "$SOURCE" "$TARGET"

echo ""
echo "✓ 설치 완료: ${TARGET}"
echo ""
echo "사용법: Claude Code에서 '에이전트 팀을 만들어줘' 라고 입력하세요."
