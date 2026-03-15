from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian 自动化系统 MVP CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("scan", help="扫描收件箱并写入处理队列")

    process_parser = subparsers.add_parser("process", help="处理队列中的下一条笔记")
    process_parser.add_argument("--dry-run", action="store_true", help="仅预览处理结果，不落盘")

    subparsers.add_parser("status", help="查看当前处理状态")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        result = pipeline.scan_inbox()
    elif args.command == "process":
        result = pipeline.process_next(dry_run=args.dry_run)
    elif args.command == "status":
        result = pipeline.get_status()
    else:
        parser.error(f"不支持的命令: {args.command}")
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") not in {"failed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
