#!/usr/bin/env python3
"""
Obsidian 自动化处理 CLI
用法:
    python cli.py scan      # 扫描收件箱
    python cli.py process  # 处理下一条
    python cli.py status   # 查看状态
    python cli.py process --dry-run  # 预览模式
"""
import argparse
import sys
from pathlib import Path

# 添加脚本目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from pipeline import Pipeline


def main():
    parser = argparse.ArgumentParser(description="Obsidian 自动化处理工具")
    parser.add_argument("command", choices=["scan", "process", "status"],
                        help="命令: scan(扫描) / process(处理) / status(状态)")
    parser.add_argument("--dry-run", action="store_true",
                        help="预览模式，不实际执行")

    args = parser.parse_args()

    pipeline = Pipeline(dry_run=args.dry_run)

    if args.command == "scan":
        print("🔍 扫描收件箱...")
        notes = pipeline.scan()
        if notes:
            print(f"📥 发现 {len(notes)} 条新笔记:")
            for note in notes:
                print(f"   - {note['file']}")
        else:
            print("📭 没有新笔记")
        print(f"\n队列状态: {pipeline.status()['pending']} 条待处理")

    elif args.command == "process":
        print("⚙️  处理笔记...")
        result = pipeline.process_next()
        if result is None:
            print("📭 队列为空")
        elif result.get("status") == "error":
            print(f"❌ 处理失败: {result.get('message')}")
        elif result.get("status") == "dry_run":
            # Dry run 已在 process_next 中输出
            pass
        else:
            print(f"✅ 处理完成")

    elif args.command == "status":
        status = pipeline.status()
        print("📊 队列状态:")
        print(f"   待处理: {status['pending']}")
        print(f"   已处理: {status['processed']}")
        print(f"   失败:   {status['failed']}")
        print(f"   上次扫描: {status['last_scan'] or '从未'}")

        if status["pending"] > 0:
            print(f"\n📋 待处理列表:")
            for item in status["queue"]:
                print(f"   - {item['file']}")


if __name__ == "__main__":
    main()
