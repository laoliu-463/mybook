from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian Harness 自检入口")
    parser.add_argument("--changed-only", action="store_true", help="缩小为当前改动范围")
    parser.add_argument("--smoke", action="store_true", help="只执行基础检查")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = build_parser().parse_args()
    result = pipeline.verify_workspace(changed_only=args.changed_only, smoke=args.smoke)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
