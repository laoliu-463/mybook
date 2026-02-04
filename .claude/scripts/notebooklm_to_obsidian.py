"""
NotebookLM → Obsidian 自动化脚本
功能：从 NotebookLM 抓取笔记并保存到 Obsidian 收集箱

依赖：
pip install playwright markdownify pyyaml
playwright install chromium
"""

import os
import re
from datetime import datetime
from playwright.sync_api import sync_playwright
import yaml

# ============ 配置区 ============
OBSIDIAN_VAULT = r"D:\Docs\Notes\ObsidianVault"
OUTPUT_DIR = os.path.join(OBSIDIAN_VAULT, "00-收集箱", "临时记录")
NOTEBOOKLM_URL = "https://notebooklm.google.com"

# ============ 核心函数 ============

def extract_notebooklm_notes(page_url: str, headless: bool = False) -> dict:
    """
    从 NotebookLM 页面提取笔记内容

    Args:
        page_url: NotebookLM 笔记页面 URL
        headless: 是否无头模式（True=后台运行）

    Returns:
        {"title": str, "content": str, "url": str}
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()

        # 访问页面
        page.goto(page_url)

        # 等待内容加载（根据实际 DOM 结构调整选择器）
        page.wait_for_load_state("networkidle")

        # 提取标题（需根据 NotebookLM 实际 DOM 调整）
        title = page.title() or "NotebookLM-笔记"

        # 提取主要内容（需根据实际 DOM 结构调整选择器）
        # 这里是示例，你需要在浏览器开发者工具中找到实际的选择器
        content_element = page.query_selector("main") or page.query_selector("body")
        content = content_element.inner_text() if content_element else ""

        browser.close()

        return {
            "title": sanitize_filename(title),
            "content": content.strip(),
            "url": page_url
        }


def sanitize_filename(filename: str) -> str:
    """清理文件名中的非法字符"""
    return re.sub(r'[<>:"/\\|?*]', '-', filename)[:50]


def save_to_obsidian(note_data: dict) -> str:
    """
    保存到 Obsidian 收集箱

    Args:
        note_data: {"title": str, "content": str, "url": str}

    Returns:
        保存的文件路径
    """
    # 生成文件名
    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"{today}-{note_data['title']}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # 生成 frontmatter
    frontmatter = {
        "created": today,
        "source": note_data["url"],
        "status": "inbox",
        "tags": ["notebooklm"]
    }

    # 生成完整内容
    content = f"""---
{yaml.dump(frontmatter, allow_unicode=True, default_flow_style=False)}---

# 【NotebookLM】{note_data['title']}

## 📝 原始内容
{note_data['content']}

## 🤖 快速摘要（Capture）
- **一句话总结**：
- **价值点**：
- **下一步动作（TODO）**：
  - [ ] 执行 /sb-organize 归位
"""

    # 确保目录存在
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 写入文件
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filepath


# ============ 使用示例 ============

if __name__ == "__main__":
    # 方式 1：手动指定 URL
    notebooklm_url = input("请输入 NotebookLM 笔记页面 URL: ").strip()

    if not notebooklm_url:
        print("❌ URL 不能为空")
        exit(1)

    print("🔄 正在抓取 NotebookLM 笔记...")
    note_data = extract_notebooklm_notes(notebooklm_url, headless=False)

    print(f"📄 标题: {note_data['title']}")
    print(f"📝 内容长度: {len(note_data['content'])} 字符")

    filepath = save_to_obsidian(note_data)
    print(f"✅ 已保存到: {filepath}")
    print(f"\n💡 下一步：在终端执行")
    print(f"   /sb-organize {os.path.basename(filepath)}")
