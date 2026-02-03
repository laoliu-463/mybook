#!/usr/bin/env python3
"""
白名单扫描器：拦截非 github.com / youtube.com / huggingface.co 的链接
"""
import json, sys, os, re
from pathlib import Path

# 白名单域名（含子域名）
ALLOWED_HOSTS = {
    "github.com", "www.github.com", "raw.githubusercontent.com", "api.github.com",
    "youtube.com", "www.youtube.com", "youtu.be", "youtube-nocookie.com",
    "huggingface.co", "www.huggingface.co"
}

URL_PATTERN = re.compile(r"https?://([a-zA-Z0-9\.\-]+)(/[^\s\)\]]*)?")

def load_event():
    try:
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}
    except:
        return {}

def scan_file(path: Path):
    """扫描文件中的URL，返回违规链接"""
    violations = []
    try:
        text = path.read_text(encoding="utf-8")
    except:
        return violations

    for match in URL_PATTERN.finditer(text):
        host = match.group(1).lower()
        url = match.group(0)

        if host not in ALLOWED_HOSTS:
            violations.append({
                "host": host,
                "url": url,
                "file": path.name
            })

    return violations

def main():
    event = load_event()
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())

    # 扫描关键目录
    scan_dirs = [
        project_dir / "02-学习记录" / "01-日报",
        project_dir / "00-收集箱" / "News-Knowledge-Drafts",
        project_dir / "00-收集箱" / "News-Inbox",
    ]

    all_violations = []

    for scan_dir in scan_dirs:
        if not scan_dir.exists():
            continue

        # 递归扫描所有 .md 文件
        for md_file in scan_dir.rglob("*.md"):
            violations = scan_file(md_file)
            all_violations.extend(violations)

    if all_violations:
        # 去重并格式化
        unique_violations = {}
        for v in all_violations:
            key = v["url"]
            if key not in unique_violations:
                unique_violations[key] = v

        violation_list = "\n".join(
            f"- {v['file']}: {v['host']} → {v['url']}"
            for v in list(unique_violations.values())[:30]
        )

        print(json.dumps({
            "decision": "block",
            "reason": f"""❌ 白名单检查失败：发现非授权来源

【检测结果】
发现 {len(unique_violations)} 个非白名单链接

【违规清单】
{violation_list}

【白名单域名】
仅允许以下域名：
- github.com (及子域名)
- youtube.com / youtu.be
- huggingface.co

【修复建议】
1. 删除所有非白名单链接
2. 如果需要引用外部资料，必须：
   - 找到对应的 GitHub issue/discussion
   - 或找到 YouTube 官方频道视频
   - 或在 Hugging Face 找到对应模型/数据集
3. 禁止使用博客/新闻/Medium/StackOverflow等第三方来源

【反幻觉约束】
如果白名单来源中没有该信息，说明：
1. 该信息不符合"资讯"标准（可能是营销/炒作）
2. 或者需要等待官方发布到 GitHub/YouTube
3. 不要为了凑数而引用低质量来源
"""
        }, ensure_ascii=False))
        sys.exit(2)

    # 白名单检查通过
    sys.exit(0)

if __name__ == "__main__":
    main()
