#!/usr/bin/env python3
"""
Obsidian Harness 自动调度器

用法:
    python 自动调度器.py --daemon      # 守护进程模式（每30分钟检查一次）
    python 自动调度器.py --interval 60 # 每60分钟运行一次
    python 自动调度器.py --once        # 运行一次就退出
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# 动态导入 pipeline
script_dir = Path(__file__).resolve().parent
pipeline_spec = importlib.util.spec_from_file_location("pipeline", script_dir / "pipeline.py")
pipeline = importlib.util.module_from_spec(pipeline_spec)
pipeline_spec.loader.exec_module(pipeline)


def log(msg: str) -> None:
    """带时间戳的日志输出"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")


def run_once() -> dict:
    """运行一次完整流程"""
    log("=" * 40)
    log("开始自动处理...")

    # 1. 扫描收件箱
    scan_result = pipeline.scan_inbox()
    log(f"扫描收件箱: 添加 {len(scan_result.get('added', []))} 篇")

    if scan_result.get("queue_count", 0) == 0:
        log("队列为空，跳过处理")
        return {"status": "skipped", "reason": "no new notes"}

    # 2. 处理笔记（默认最多3篇）
    process_result = pipeline.process_batch(dry_run=False, limit=3)

    log(f"处理完成: {process_result.get('processed_count', 0)} 篇")
    log(f"失败: {process_result.get('failed_count', 0)} 篇")

    return {
        "status": "ok",
        "scan": scan_result,
        "process": process_result,
    }


def daemon_mode(interval_minutes: int = 30) -> None:
    """守护进程模式：定期运行"""
    log(f"启动守护进程模式，间隔 {interval_minutes} 分钟")
    log("按 Ctrl+C 停止")

    try:
        while True:
            run_once()
            log(f"等待 {interval_minutes} 分钟...")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        log("守护进程已停止")


def main() -> int:
    parser = argparse.ArgumentParser(description="Obsidian Harness 自动调度器")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--interval", type=int, default=30, help="运行间隔（分钟，默认30）")
    parser.add_argument("--once", action="store_true", help="运行一次就退出")

    args = parser.parse_args()

    if args.daemon:
        daemon_mode(args.interval)
    elif args.once:
        result = run_once()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 默认运行一次
        result = run_once()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
