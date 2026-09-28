#!/bin/sh
set -eu
CONFIG_REPO=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec uv run --offline --no-project "$CONFIG_REPO/scripts/launch.py" codex "$@"
