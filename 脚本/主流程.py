from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obsidian 自动化主流程")
    parser.add_argument("--limit", type=int, default=1, help="本轮最多处理多少篇，默认 1，最大 3")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不实际写入")
    parser.add_argument("--scan-first", action="store_true", help="处理前先扫描收件箱")
    return parser


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

    args = build_parser().parse_args()

    bootstrap = None if args.dry_run else pipeline.init_environment()
    payload: dict[str, object] = {"init": bootstrap}

    if args.scan_first:
        payload["scan"] = pipeline.scan_inbox(dry_run=args.dry_run)

    payload["process"] = pipeline.process_batch(limit=args.limit, dry_run=args.dry_run)
    payload["verify"] = pipeline.verify_workspace(
        changed_only=not args.dry_run,
        smoke=args.dry_run,
        record=not args.dry_run,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))

    process_status = payload["process"]
    if isinstance(process_status, dict) and process_status.get("status") == "failed":
        return 1
    verify_status = payload["verify"]
    if isinstance(verify_status, dict) and verify_status.get("status") == "failed":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
