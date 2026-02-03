#!/usr/bin/env python3
"""
Gate0/1 候选包校验器：白名单 + Review 复选框 + 版本流水账拦截
PostToolUse hook - 每次 Edit/Write 后自动运行
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

# 白名单域名（严格）
ALLOWED_DOMAINS = {
    "github.com",
    "www.youtube.com",
    "youtube.com",
    "huggingface.co"
}

# 版本流水账特征词（命中过多则告警）
RELEASE_KEYWORDS = [
    "Release Notes", "releases/tag", "changelog",
    "v3.", "v2.", "版本", "发布", "更新日志"
]

def validate_candidate_pack():
    """校验最新的候选包文件"""
    inbox = Path("00-收集箱/News-Inbox")
    if not inbox.exists():
        return True  # 目录不存在不算错误

    packs = sorted(inbox.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not packs:
        return True  # 没有候选包也不算错误

    latest = packs[0]
    text = latest.read_text(encoding="utf-8", errors="ignore")

    # 1) URL 白名单检查
    urls = re.findall(r"https?://[^\s\)\]]+", text)
    violations = []
    for url in urls:
        try:
            host = urlparse(url).netloc.lower()
            if host and host not in ALLOWED_DOMAINS:
                violations.append((url, host))
        except:
            pass

    if violations:
        print(f"❌ [news_validate] FAIL: Non-whitelist domains found:", file=sys.stderr)
        for url, host in violations[:5]:  # 只显示前5个
            print(f"   - {host} in {url[:60]}...", file=sys.stderr)
        return False

    # 2) Review 复选框检查（Gate0 必备）
    has_approve = "[ ] approve" in text or "- [ ] approve" in text
    has_reject = any(x in text for x in ["[ ] skip", "[ ] reject", "[ ] needs-verify"])

    if not (has_approve and has_reject):
        print("❌ [news_validate] FAIL: Review checkboxes missing.", file=sys.stderr)
        print("   Expected: [ ] approve + ([ ] skip / [ ] reject / [ ] needs-verify)", file=sys.stderr)
        return False

    # 3) 版本流水账告警（不直接 fail，但会提醒）
    hit_count = sum(1 for kw in RELEASE_KEYWORDS if kw.lower() in text.lower())
    if hit_count >= 5:
        print(f"⚠️  [news_validate] WARN: Detected {hit_count} release-related keywords.", file=sys.stderr)
        print("   This looks like changelog/version updates, not news. Consider filtering.", file=sys.stderr)
        # 不阻止，只警告

    print(f"✅ [news_validate] OK: {latest.name}", file=sys.stderr)
    return True

if __name__ == "__main__":
    success = validate_candidate_pack()
    sys.exit(0 if success else 1)
