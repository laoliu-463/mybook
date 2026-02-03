#!/usr/bin/env python3
"""
Gate1 守门员：发布前必须完成人工Review
"""
import json, sys, os, re, datetime
from pathlib import Path

def read_stdin():
    try:
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}
    except:
        return {}

def find_today_candidate(project_dir: str):
    today = datetime.date.today().isoformat()
    # 候选包路径：00-收集箱/News-Inbox/YYYY-MM-DD/00-candidate-pack.md
    path = Path(project_dir) / "00-收集箱" / "News-Inbox" / today / "00-candidate-pack.md"
    return path if path.exists() else None

def frontmatter_get(text: str, key: str):
    """极简frontmatter解析"""
    m = re.search(r"^---\s*\n(.*?)\n---\s*\n", text, re.S)
    if not m:
        return None
    fm = m.group(1)
    km = re.search(rf"^{re.escape(key)}\s*:\s*(.*)$", fm, re.M)
    return km.group(1).strip() if km else None

def main():
    event = read_stdin()
    project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()

    tool_name = event.get("tool_name", "")
    tool_input = event.get("tool_input", {})

    # 检测发布命令
    cmd = tool_input.get("command", "") if tool_name == "Bash" else ""
    skill = tool_input.get("skill", "") if tool_name == "Skill" else ""

    # 发布触发条件：1) 调用skill发布 2) Bash命令包含"publish"
    is_publish = (
        "publish" in skill.lower() or
        "publish" in cmd.lower() or
        "我已 review" in str(event).lower() or
        "news-publish" in cmd.lower()
    )

    if not is_publish:
        sys.exit(0)  # 非发布命令，放行

    # 查找今日候选包
    cand = find_today_candidate(project_dir)
    if not cand:
        print(json.dumps({
            "decision": "block",
            "reason": f"❌ 发布失败：未找到今日候选包\n预期路径：00-收集箱/News-Inbox/{datetime.date.today()}/00-candidate-pack.md"
        }, ensure_ascii=False))
        sys.exit(2)

    # 检查frontmatter中的gate状态
    text = cand.read_text(encoding="utf-8")
    gate = frontmatter_get(text, "gate")

    if gate != "gate1_reviewed":
        print(json.dumps({
            "decision": "block",
            "reason": f"❌ 发布失败：候选包未完成人工Review\n\n当前状态：gate={gate}\n要求状态：gate=gate1_reviewed\n\n请先在候选包中完成Review并更新frontmatter：\ngate: gate1_reviewed\nreviewed_at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\nreview_summary: \"approve=X, skip=Y, needs-verify=Z\""
        }, ensure_ascii=False))
        sys.exit(2)

    # Review完成，放行发布
    sys.exit(0)

if __name__ == "__main__":
    main()
