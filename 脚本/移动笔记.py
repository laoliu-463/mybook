"""
Obsidian 笔记移动脚本

功能：
- 移动文件到目标目录
- 文件名冲突：添加数字后缀 (filename - 1.md)
- 内容冲突：保留两者（创建副本）
- 移动后更新 frontmatter 中的路径引用
- 返回 {success: bool, new_path: str, old_path: str}

Vault 路径: D:\\Docs\\Notes\\ObsidianVault
收件箱: 00-收集箱/
"""

import re
import shutil
import yaml
from pathlib import Path
from typing import Optional


VAULT_PATH = Path(r"D:\Docs\Notes\ObsidianVault")
INBOX_PATH = VAULT_PATH / "00-收集箱"


def extract_frontmatter(content: str) -> tuple[Optional[dict], str]:
    """
    提取 frontmatter 和正文内容

    返回: (frontmatter_dict, body_content)
    """
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2]
                return frontmatter, body
            except yaml.YAMLError:
                pass
    return None, content


def update_frontmatter_paths(frontmatter: dict, old_path: str, new_path: str) -> dict:
    """
    更新 frontmatter 中可能存在的路径引用
    需要更新的字段：path, file, aliases 中的路径
    """
    if not frontmatter:
        return frontmatter

    old_stem = Path(old_path).stem
    new_stem = Path(new_path).stem

    # 更新 path 字段
    if 'path' in frontmatter and old_stem in str(frontmatter['path']):
        frontmatter['path'] = str(new_path)

    # 更新 file 字段
    if 'file' in frontmatter and old_stem in str(frontmatter['file']):
        frontmatter['file'] = str(new_path)

    # 更新 aliases（如果有路径相关的别名）
    if 'aliases' in frontmatter and isinstance(frontmatter['aliases'], list):
        new_aliases = []
        for alias in frontmatter['aliases']:
            if old_stem in str(alias):
                new_aliases.append(str(alias).replace(old_stem, new_stem))
            else:
                new_aliases.append(alias)
        frontmatter['aliases'] = new_aliases

    return frontmatter


def rebuild_content(frontmatter: Optional[dict], body: str) -> str:
    """
    重建带 frontmatter 的内容
    """
    if not frontmatter:
        return body

    yaml_content = yaml.dump(frontmatter, allow_unicode=True, sort_keys=False)
    return f"---\n{yaml_content}---{body}"


def check_content_conflict(source_content: str, target_path: Path) -> bool:
    """
    检查内容是否冲突（相同内容）
    """
    if not target_path.exists():
        return False

    try:
        target_content = target_path.read_text(encoding='utf-8')
        return source_content.strip() == target_content.strip()
    except Exception:
        return False


def get_unique_filename(target_dir: Path, filename: str) -> Path:
    """
    生成唯一文件名，处理数字后缀冲突
    例如: test.md 存在则尝试 test - 1.md, test - 2.md 等
    """
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    target_path = target_dir / filename

    counter = 1
    while target_path.exists():
        new_name = f"{stem} - {counter}{suffix}"
        target_path = target_dir / new_name
        counter += 1

    return target_path


def move_note(source_path: str, target_dir: str) -> dict:
    """
    移动笔记到目标目录

    参数:
        source_path: 源文件路径（绝对路径或相对路径）
        target_dir: 目标目录路径

    返回:
        {success: bool, new_path: str, old_path: str}
    """
    source = Path(source_path)
    target_directory = Path(target_dir)

    # 验证源文件存在
    if not source.exists():
        return {
            "success": False,
            "new_path": "",
            "old_path": str(source)
        }

    # 转换为绝对路径
    source = source.resolve()

    # 确保目标目录存在
    target_directory.mkdir(parents=True, exist_ok=True)

    # 读取源文件内容
    source_content = source.read_text(encoding='utf-8')

    # 提取 frontmatter
    frontmatter, body = extract_frontmatter(source_content)

    # 目标文件路径
    target_path = target_directory / source.name

    # 检查文件名冲突
    if target_path.exists():
        target_path = get_unique_filename(target_directory, source.name)

        # 检查内容冲突（如果原名已存在）
        if check_content_conflict(source_content, target_path):
            # 内容冲突，添加 copy 后缀
            stem = target_path.stem
            suffix = target_path.suffix
            target_path = target_directory / f"{stem} - copy{suffix}"

    # 移动文件
    try:
        shutil.move(str(source), str(target_path))
    except Exception as e:
        # 如果移动失败，尝试复制后删除
        try:
            shutil.copy2(str(source), str(target_path))
            source.unlink()
        except Exception:
            return {
                "success": False,
                "new_path": "",
                "old_path": str(source)
            }

    # 更新 frontmatter 中的路径引用（如果有变化）
    if frontmatter and str(source) != str(target_path):
        updated_frontmatter = update_frontmatter_paths(
            frontmatter, str(source), str(target_path)
        )
        if updated_frontmatter != frontmatter:
            new_content = rebuild_content(updated_frontmatter, body)
            target_path.write_text(new_content, encoding='utf-8')

    return {
        "success": True,
        "new_path": str(target_path),
        "old_path": str(source)
    }


def move_from_inbox(filename: str, target_dir: str = None) -> dict:
    """
    从收件箱移动笔记的便捷函数

    参数:
        filename: 文件名（不含路径）
        target_dir: 目标目录（默认使用 VAULT_PATH）

    返回:
        {success: bool, new_path: str, old_path: str}
    """
    if target_dir is None:
        target_dir = VAULT_PATH

    source_path = INBOX_PATH / filename
    return move_note(str(source_path), str(target_dir))


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("用法: python 移动笔记.py <源文件> <目标目录>")
        print("或:   python 移动笔记.py <文件名>  # 从收件箱移动到根目录")
        sys.exit(1)

    if len(sys.argv) == 3:
        result = move_note(sys.argv[1], sys.argv[2])
    else:
        result = move_from_inbox(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

    print(result)
