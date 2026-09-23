#!/bin/sh
set -eu
CONFIG_REPO=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec codex --add-dir "$CONFIG_REPO" "$@"
