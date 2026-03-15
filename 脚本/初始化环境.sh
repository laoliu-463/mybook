#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "== 初始化 Obsidian Harness =="
python 脚本/cli.py init
echo
echo "== 当前状态 =="
python 脚本/cli.py status
