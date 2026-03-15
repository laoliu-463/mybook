"""
Obsidian 笔记 Frontmatter 读写工具

功能：
1. 读取 Markdown 文件的 frontmatter
2. 写入/更新 frontmatter
3. 路径安全校验（确保在 vault 内）
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional

# Vault 根目录
VAULT_PATH = Path(r"D:\Docs\Notes\ObsidianVault")

# 支持的 frontmatter 字段
FRONTMATTER_FIELDS = {
    "title": str,
    "type": str,  # concept | overview | interview | project | resource
    "domain": list,
    "tags": list,
    "source": str,  # notebooklm | web | book | voice
    "created": str,  # YYYY-MM-DD
    "status": str,  # draft | review | done
    "next_review": str,  # YYYY-MM-DD
    "interval": int,
    "ease": float,
    "reps": int,
}

# type 字段的有效值
VALID_TYPES = {"concept", "overview", "interview", "project", "resource"}

# source 字段的有效值
VALID_SOURCES = {"notebooklm", "web", "book", "voice"}

# status 字段的有效值
VALID_STATUSES = {"draft", "review", "done"}


def validate_path(file_path: Path) -> bool:
    """
    校验路径是否在 vault 内

    Args:
        file_path: 要校验的文件路径

    Returns:
        True 如果路径安全（在 vault 内），否则 False
    """
    try:
        resolved = file_path.resolve()
        vault_resolved = VAULT_PATH.resolve()
        return vault_resolved in resolved.parents or resolved == vault_resolved
    except Exception:
        return False


def read_frontmatter(file_path: str | Path) -> Optional[dict]:
    """
    读取 Markdown 文件的 frontmatter

    Args:
        file_path: 笔记文件路径

    Returns:
        frontmatter 字典，如果不存在 frontmatter 则返回 None

    Raises:
        ValueError: 路径不在 vault 内
    """
    file_path = Path(file_path)

    if not validate_path(file_path):
        raise ValueError(f"路径不安全: {file_path}，必须在 vault 内")

    if not file_path.exists():
        return None

    content = file_path.read_text(encoding="utf-8")

    # 检查是否有 frontmatter
    if not content.startswith("---"):
        return None

    # 提取 frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None

    frontmatter_text = parts[1]

    try:
        frontmatter = yaml.safe_load(frontmatter_text)
        return frontmatter if frontmatter else None
    except yaml.YAMLError:
        return None


def write_frontmatter(
    file_path: str | Path,
    frontmatter: dict,
    keep_existing: bool = True,
) -> None:
    """
    写入/更新 frontmatter

    Args:
        file_path: 笔记文件路径
        frontmatter: 要写入的 frontmatter 字典
        keep_existing: True 保留现有 frontmatter（合并），False 完全覆盖

    Raises:
        ValueError: 路径不在 vault 内或字段值无效
    """
    file_path = Path(file_path)

    if not validate_path(file_path):
        raise ValueError(f"路径不安全: {file_path}，必须在 vault 内")

    # 校验字段值
    _validate_frontmatter(frontmatter)

    if not file_path.exists():
        # 新建文件
        content = _build_frontmatter_content(frontmatter)
        file_path.write_text(content, encoding="utf-8")
        return

    existing_frontmatter = {}
    body_content = ""

    # 读取现有内容
    original_content = file_path.read_text(encoding="utf-8")

    if original_content.startswith("---"):
        parts = original_content.split("---", 2)
        if len(parts) >= 3:
            # 解析现有 frontmatter
            try:
                existing_frontmatter = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                existing_frontmatter = {}
            body_content = parts[2] if len(parts) > 2 else ""

            # 确保 body_content 去除前导空白
            body_content = body_content.lstrip("\n")
    else:
        body_content = original_content

    # 合并 frontmatter
    if keep_existing:
        merged = {**existing_frontmatter, **frontmatter}
    else:
        merged = frontmatter

    # 写入文件
    new_content = _build_frontmatter_content(merged, body_content)
    file_path.write_text(new_content, encoding="utf-8")


def _validate_frontmatter(frontmatter: dict) -> None:
    """
    校验 frontmatter 字段值

    Raises:
        ValueError: 字段值无效
    """
    # 校验 type
    if "type" in frontmatter:
        if frontmatter["type"] not in VALID_TYPES:
            raise ValueError(
                f"type 无效: {frontmatter['type']}，有效值: {VALID_TYPES}"
            )

    # 校验 source
    if "source" in frontmatter:
        if frontmatter["source"] not in VALID_SOURCES:
            raise ValueError(
                f"source 无效: {frontmatter['source']}，有效值: {VALID_SOURCES}"
            )

    # 校验 status
    if "status" in frontmatter:
        if frontmatter["status"] not in VALID_STATUSES:
            raise ValueError(
                f"status 无效: {frontmatter['status']}，有效值: {VALID_STATUSES}"
            )

    # 校验 created 日期格式
    if "created" in frontmatter:
        _validate_date(frontmatter["created"], "created")

    # 校验 next_review 日期格式
    if "next_review" in frontmatter:
        _validate_date(frontmatter["next_review"], "next_review")


def _validate_date(date_str: str, field_name: str) -> None:
    """校验日期格式 YYYY-MM-DD"""
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        raise ValueError(
            f"{field_name} 格式无效: {date_str}，应为 YYYY-MM-DD"
        )


def _build_frontmatter_content(frontmatter: dict, body: str = "") -> str:
    """构建 frontmatter 和正文内容"""
    # 移除 None 值
    clean_frontmatter = {k: v for k, v in frontmatter.items() if v is not None}

    # 按字段顺序排序
    field_order = [
        "title", "type", "domain", "tags", "source",
        "created", "status", "next_review", "interval", "ease", "reps"
    ]

    sorted_frontmatter = {}
    for field in field_order:
        if field in clean_frontmatter:
            sorted_frontmatter[field] = clean_frontmatter[field]
    # 添加其他字段
    for field in clean_frontmatter:
        if field not in sorted_frontmatter:
            sorted_frontmatter[field] = clean_frontmatter[field]

    # 转换为 YAML
    yaml_content = yaml.dump(
        sorted_frontmatter,
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )

    # 确保 YAML 块格式
    if yaml_content.strip():
        content = f"---\n{yaml_content}---\n"
    else:
        content = "---\n---\n"

    if body:
        content += "\n" + body

    return content


def get_or_create_note(file_path: str | Path) -> dict:
    """
    获取笔记的 frontmatter，如果不存在则创建默认 frontmatter

    Args:
        file_path: 笔记文件路径

    Returns:
        frontmatter 字典
    """
    fm = read_frontmatter(file_path)
    if fm is None:
        # 从文件名生成默认 title
        title = Path(file_path).stem
        fm = {
            "title": title,
            "created": datetime.now().strftime("%Y-%m-%d"),
            "status": "draft",
        }
        write_frontmatter(file_path, fm)
    return fm


def update_field(
    file_path: str | Path,
    field: str,
    value,
) -> None:
    """
    更新单个字段

    Args:
        file_path: 笔记文件路径
        field: 字段名
        value: 字段值

    Raises:
        ValueError: 字段无效或值无效
    """
    if field not in FRONTMATTER_FIELDS:
        raise ValueError(f"未知字段: {field}，支持: {list(FRONTMATTER_FIELDS.keys())}")

    frontmatter = read_frontmatter(file_path) or {}
    frontmatter[field] = value
    write_frontmatter(file_path, frontmatter)


if __name__ == "__main__":
    # 测试
    test_file = VAULT_PATH / "00-收集箱" / "test-note.md"

    # 写入测试
    write_frontmatter(test_file, {
        "title": "测试笔记",
        "type": "concept",
        "domain": ["编程语言", "Python"],
        "tags": ["test", "demo"],
        "source": "notebooklm",
        "created": "2026-03-15",
        "status": "draft",
    })

    # 读取测试
    fm = read_frontmatter(test_file)
    print("读取 frontmatter:", fm)

    # 更新测试
    update_field(test_file, "status", "review")
    fm = read_frontmatter(test_file)
    print("更新后 frontmatter:", fm)

    # 清理测试文件
    if test_file.exists():
        test_file.unlink()
