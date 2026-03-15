from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def run_once() -> dict[str, object]:
    log("=" * 40)
    log("开始自动处理")

    init_result = pipeline.init_environment()
    log(f"初始化完成: feature_count={init_result.get('feature_count', 0)}")

    scan_result = pipeline.scan_inbox()
    log(f"扫描完成: 新增 {len(scan_result.get('added', []))} 篇，队列 {scan_result.get('queue_count', 0)} 篇")

    if scan_result.get("queue_count", 0) == 0:
        verify_result = pipeline.verify_workspace(changed_only=True, smoke=True)
        result = {
            "status": "skipped",
            "reason": "no pending notes",
            "init": init_result,
            "scan": scan_result,
            "verify": verify_result,
        }
        log("没有待处理笔记，跳过本轮")
        return result

    process_result = pipeline.process_batch(dry_run=False, limit=3)
    processed_count = process_result.get("processed_count", 0)
    failed_count = sum(1 for item in process_result.get("results", []) if item.get("status") == "failed")
    log(f"处理完成: success={processed_count}, failed={failed_count}")

    verify_result = pipeline.verify_workspace(changed_only=True, smoke=False)
    result = {
        "status": "ok" if verify_result.get("status") == "ok" else "failed",
        "init": init_result,
        "scan": scan_result,
        "process": process_result,
        "verify": verify_result,
    }
    log(f"自检结果: {verify_result.get('status')}")
    return result


def daemon_mode(interval_minutes: int) -> None:
    log(f"启动守护进程模式，间隔 {interval_minutes} 分钟")
    log("按 Ctrl+C 停止")

    try:
        while True:
            result = run_once()
            print(json.dumps(result, ensure_ascii=False, indent=2))
            log(f"等待 {interval_minutes} 分钟")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        log("守护进程已停止")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian Harness 自动调度器")
    parser.add_argument("--daemon", action="store_true", help="守护进程模式")
    parser.add_argument("--interval", type=int, default=30, help="守护模式检查间隔，单位分钟")
    parser.add_argument("--once", action="store_true", help="只运行一轮")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = build_parser().parse_args()

    if args.daemon:
        daemon_mode(args.interval)
        return 0

    result = run_once()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result.get("status") != "failed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
