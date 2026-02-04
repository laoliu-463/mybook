#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
NotebookLM 本地导入桥接脚本：
- 从 70-NotebookLM导入/ 读取最新或指定文件
- 套用 80-模板/Capture-模板.md
- 在 00-收集箱/ 创建 YYYY-MM-DD-关键词.md
- 打印新文件相对路径，供 Claude 后续 /sb-organize /sb-distill 使用
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from datetime import datetime

VAULT_ROOT = Path(".").resolve()

IN_DIR = VAULT_ROOT / "70-NotebookLM导入"
INBOX_DIR = VAULT_ROOT / "00-收集箱"
TEMPLATE_PATH = VAULT_ROOT / "80-模板" / "Capture-模板.md"


def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}")
    sys.exit(code)


def parse_args(argv: list[str]) -> tuple[str | None, str]:
    """
    returns: (filename_or_none, mode)
    mode in {"latest", "file"}
    """
    if not argv:
        return None, "latest"

    # accept: --latest OR filename (possibly with flags after)
    if argv[0] == "--latest":
        return None, "latest"

    # first non-flag token treated as filename
    if argv[0].startswith("--"):
        # e.g. "--then all" without filename -> still latest
        return None, "latest"

    return argv[0], "file"


def newest_file(folder: Path) -> Path:
    if not folder.exists():
        die(f"导入目录不存在：{folder}")
    files = [p for p in folder.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".txt"}]
    if not files:
        die(f"导入目录下没有 .md/.txt 文件：{folder}")
    return max(files, key=lambda p: p.stat().st_mtime)


def read_text(p: Path) -> str:
    # try utf-8, fallback to gbk (common on Windows)
    for enc in ("utf-8", "utf-8-sig", "gbk"):
        try:
            return p.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    die(f"无法解码文件（请保存为 UTF-8）：{p}")
    return ""


def slug_keywords(text: str, max_len: int = 16) -> str:
    # 取前若干中文/英文/数字词作为关键词，避免太长
    cleaned = re.sub(r"\s+", " ", text).strip()
    if not cleaned:
        return "未命名"

    # 优先抓中文词块，否则抓英文/数字
    zh = re.findall(r"[\u4e00-\u9fff]{2,6}", cleaned)
    if zh:
        kw = "".join(zh[:3])
    else:
        en = re.findall(r"[A-Za-z0-9]{2,10}", cleaned)
        kw = "-".join(en[:3]) if en else "未命名"

    kw = re.sub(r"[^\u4e00-\u9fffA-Za-z0-9\-]", "", kw)
    return kw[:max_len] or "未命名"


def extract_source_hint(text: str) -> str:
    """
    从内容中尝试提取来源链接；没有就返回 '未提供'
    """
    m = re.search(r"https?://\S+", text)
    return m.group(0).strip() if m else "未提供"


def fill_template(template: str, title: str, content: str, source: str, date_str: str) -> str:
    out = template
    out = out.replace("{{date}}", date_str)
    out = out.replace("{{url}}", source)
    out = out.replace("{{title}}", title)
    out = out.replace("{{content}}", content.strip())

    # 如果来源缺失，追加提示
    if source == "未提供":
        out += "\n\n> [!WARNING] 待确认：来源缺失（建议在 NotebookLM 中保留/补充来源链接或引用片段）\n"
    return out


def main(argv: list[str]) -> None:
    filename, mode = parse_args(argv)

    src_path = newest_file(IN_DIR) if mode == "latest" else (IN_DIR / filename)
    if not src_path.exists():
        # 允许用户传相对 Vault 的路径
        alt = VAULT_ROOT / filename
        if alt.exists():
            src_path = alt
        else:
            die(f"找不到要导入的文件：{filename}（已尝试 {IN_DIR/filename} 与 {alt}）")

    if not TEMPLATE_PATH.exists():
        die(f"缺少模板文件：{TEMPLATE_PATH}")

    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    raw = read_text(src_path)
    date_str = datetime.now().strftime("%Y-%m-%d")

    title_kw = slug_keywords(raw)
    title = f"NotebookLM导入-{title_kw}"

    source = extract_source_hint(raw)

    template = read_text(TEMPLATE_PATH)
    rendered = fill_template(template, title=title, content=raw, source=source, date_str=date_str)

    out_name = f"{date_str}-{title_kw}.md"
    out_path = INBOX_DIR / out_name

    # 避免覆盖：重名则加序号
    if out_path.exists():
        i = 2
        while True:
            candidate = INBOX_DIR / f"{date_str}-{title_kw}-{i}.md"
            if not candidate.exists():
                out_path = candidate
                break
            i += 1

    out_path.write_text(rendered, encoding="utf-8")

    # 打印相对路径，方便 skill 后续引用
    rel = out_path.relative_to(VAULT_ROOT)
    print(str(rel))


if __name__ == "__main__":
    main(sys.argv[1:])
