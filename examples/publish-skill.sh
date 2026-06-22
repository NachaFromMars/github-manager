#!/usr/bin/env bash
set -euo pipefail

S="${S:-scripts/gh_manager.py}"
SKILL_PATH="${1:?usage: examples/publish-skill.sh /path/to/skill OWNER/repo}"
REPO="${2:?usage: examples/publish-skill.sh /path/to/skill OWNER/repo}"

python3 "$S" push \
  --path "$SKILL_PATH" \
  --repo "$REPO" \
  --create \
  --message "Publish OpenClaw skill" \
  --desc "OpenClaw skill published by github-manager"
