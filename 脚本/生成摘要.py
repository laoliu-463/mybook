"""
Obsidian 笔记摘要生成脚本

功能：
- 读取笔记内容
- 提取标题（第一行 # 开头）
- 提取前 2-3 段作为摘要（跳过 frontmatter）
- 生成 TL;DR 格式：不超过 5 行
- 返回结构化结果 {title, summary, original_title}
"""

import re
from pathlib import Path
from typing import Optional


def read_note(file_path: str) -> str:
    """读取笔记文件内容"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def extract_title(content: str) -> Optional[str]:
    """
    提取标题
    规则：第一行以 # 开头的内容
    """
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # 去掉 # 和多余空格
            return line.lstrip('#').strip()
    return None


def skip_frontmatter(content: str) -> str:
    """
    跳过 frontmatter
    frontmatter 格式：以 --- 包围的 YAML
    """
    # 检查是否包含 frontmatter
    if content.startswith('---'):
        # 找到第二个 --- 的位置
        parts = content.split('---', 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return content


def extract_paragraphs(content: str, max_paragraphs: int = 3) -> list[str]:
    """
    提取前 N 段
    段落定义：以空行分隔的非空行组
    """
    content = skip_frontmatter(content)

    # 按空行分割段落
    paragraphs = []
    current_para = []

    for line in content.split('\n'):
        line = line.strip()
        # 跳过 frontmatter 分隔线和 wikilink 等
        if not line or line == '---':
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
            continue

        # 跳过仅包含 [[]] 或图片的行
        if re.match(r'^\[\[.*\]\]$', line) or line.startswith('!'):
            continue

        current_para.append(line)

    # 处理最后一段
    if current_para:
        paragraphs.append(' '.join(current_para))

    return paragraphs[:max_paragraphs]


def generate_summary(paragraphs: list[str]) -> str:
    """
    生成 TL;DR 摘要
    规则：不超过 5 行
    """
    if not paragraphs:
        return ""

    # 取前 3 段，每段作为一行
    summary_lines = []
    for para in paragraphs[:3]:
        # 截断过长的段落
        if len(para) > 200:
            para = para[:197] + "..."
        summary_lines.append(para)

    return '\n'.join(summary_lines[:5])


def generate_summary_for_note(file_path: str) -> dict:
    """
    为指定笔记生成摘要

    返回结构化结果：
    {
        "title": str,        # 提取的标题
        "summary": str,      # TL;DR 摘要
        "original_title": str  # 原始标题（含 #）
    }
    """
    content = read_note(file_path)

    # 提取原始标题（含 #）
    lines = content.strip().split('\n')
    original_title = None
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            original_title = line
            break

    # 提取标题（不含 #）
    title = extract_title(content)

    # 提取段落
    paragraphs = extract_paragraphs(content)

    # 生成摘要
    summary = generate_summary(paragraphs)

    return {
        "title": title,
        "summary": summary,
        "original_title": original_title
    }


if __name__ == "__main__":
    import sys
    import json

    if len(sys.argv) < 2:
        print("用法: python 生成摘要.py <笔记文件路径>")
        sys.exit(1)

    file_path = sys.argv[1]
    result = generate_summary_for_note(file_path)

    # 输出 JSON 格式，避免编码问题
    print(json.dumps(result, ensure_ascii=False, indent=2))
