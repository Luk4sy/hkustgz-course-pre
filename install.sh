#!/usr/bin/env bash
# Install the hkustgz-course-pre skill for Claude, Codex and DeepSeek Harness (macOS / Linux).
# Usage:  bash install.sh            # all three
#         bash install.sh claude     # only Claude Code
#         bash install.sh agents     # only Codex + DeepSeek Harness (shared ~/.agents/skills)
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/skills/hkustgz-course-pre"
target="${1:-all}"
copy() {
  mkdir -p "$1"
  rm -rf "$1/hkustgz-course-pre.new" && cp -R "$SRC" "$1/hkustgz-course-pre.new"
  rm -rf "$1/hkustgz-course-pre" && mv "$1/hkustgz-course-pre.new" "$1/hkustgz-course-pre"
  echo "installed -> $1/hkustgz-course-pre"
}
case "$target" in
  claude) copy "$HOME/.claude/skills" ;;
  agents) copy "$HOME/.agents/skills" ;;
  all)    copy "$HOME/.claude/skills"; copy "$HOME/.agents/skills" ;;
  *) echo "unknown target: $target (use claude, agents or all)"; exit 1 ;;
esac
echo "Next: python3 \"$SRC/scripts/check_env.py\" to see if any tools are missing."
