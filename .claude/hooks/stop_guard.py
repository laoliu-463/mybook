#!/usr/bin/env python3
"""
Stop hook: 强制"极限输出"模式
只有当目标文件足够大时才允许 Claude 停止（用于分块续写）
"""
import json
import sys
from pathlib import Path

def check_output_file():
    """检查是否已写入足够内容"""
    # Stop hook 输入从 stdin 来
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except:
        payload = {}

    # 防止无限循环：如果已经触发过 stop hook，直接放行
    if payload.get("stop_hook_active") is True:
        return {"allow": True}

    # 极限输出目标文件（Claude 应该持续往这里分块写入）
    output_file = Path(".claude/logs/news-educator/big_output.md")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # 检查文件大小（小于 5KB 视为未完成）
    if not output_file.exists():
        return {
            "allow": False,
            "reason": f"Output file {output_file.as_posix()} not found. Please keep writing in chunks."
        }

    size_kb = output_file.stat().st_size / 1024
    if size_kb < 5:
        return {
            "allow": False,
            "reason": f"Output file only {size_kb:.1f}KB (need >5KB). Continue writing in chunks."
        }

    # 文件足够大，允许停止
    return {"allow": True}

if __name__ == "__main__":
    result = check_output_file()

    if not result["allow"]:
        # Stop hook 需要返回 decision: "block" 来阻止停止
        decision = {
            "decision": "block",
            "reason": result["reason"]
        }
        print(json.dumps(decision, ensure_ascii=False))
        sys.exit(0)

    # 允许停止：不输出 decision
    sys.exit(0)
