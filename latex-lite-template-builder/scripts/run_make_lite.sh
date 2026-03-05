#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REPO_ROOT="${LATEX_TEMPLATE_REPO_ROOT:-$PWD}"
TOOL_PATH="$REPO_ROOT/tools/make_lite_template.sh"

if [[ ! -x "$TOOL_PATH" ]]; then
  echo "[latex-lite-skill] ERROR: cannot find executable: $TOOL_PATH" >&2
  echo "Set LATEX_TEMPLATE_REPO_ROOT to the repository root or run from that repo." >&2
  exit 3
fi

exec "$TOOL_PATH" "$@"
