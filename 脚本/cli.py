from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import sys

# 动态导入 pipeline 模块
script_dir = Path(__file__).resolve().parent
pipeline_spec = importlib.util.spec_from_file_location("pipeline", script_dir / "pipeline.py")
pipeline = importlib.util.module_from_spec(pipeline_spec)
pipeline_spec.loader.exec_module(pipeline)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian 自动化系统 Harness CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="初始化 harness 环境和状态文件")
    subparsers.add_parser("scan", help="扫描收件箱并写入处理队列")

    process_parser = subparsers.add_parser("process", help="处理队列中的下一条笔记")
    process_parser.add_argument("--dry-run", action="store_true", help="仅预览处理结果，不落盘")
    process_parser.add_argument("--limit", type=int, default=1, help="本轮最多处理多少篇，默认 1，最大 3")

    subparsers.add_parser("status", help="查看当前处理状态")
    verify_parser = subparsers.add_parser("verify", help="执行 smoke/full 自检")
    verify_parser.add_argument("--changed-only", action="store_true", help="缩小为当前改动范围自检")
    verify_parser.add_argument("--smoke", action="store_true", help="只做基础 smoke 检查")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "init":
        result = pipeline.init_environment()
    elif args.command == "scan":
        result = pipeline.scan_inbox()
    elif args.command == "process":
        result = pipeline.process_batch(dry_run=args.dry_run, limit=args.limit)
    elif args.command == "status":
        result = pipeline.get_status()
    elif args.command == "verify":
        result = pipeline.verify_workspace(changed_only=args.changed_only, smoke=args.smoke)
    else:
        parser.error(f"不支持的命令: {args.command}")
        return 2

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") not in {"failed"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
