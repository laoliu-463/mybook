"""
安全检查脚本
功能：路径安全校验 + 敏感信息检测
"""

import re
import os
from pathlib import Path
from typing import Dict, List, Any

# Vault 根目录
VAULT_ROOT = Path(r"D:\Docs\Notes\ObsidianVault")

# 敏感信息模式（不区分大小写）
SENSITIVE_PATTERNS = {
    "api_key": [
        r"api[_-]?key",
        r"apikey",
        r"api[_-]?secret",
    ],
    "password": [
        r"password",
        pwd := r"pwd",
        r"passwd",
    ],
    "token": [
        r"token",
        r"access[_-]?token",
        r"auth[_-]?token",
    ],
    "secret": [
        r"secret",
        r"client[_-]?secret",
    ],
    "cookie": [
        r"cookie",
        r"session[_-]?id",
    ],
}

# 编译正则表达式
COMPILED_PATTERNS = {
    key: [re.compile(p, re.IGNORECASE) for p in patterns]
    for key, patterns in SENSITIVE_PATTERNS.items()
}

# 排除的文件/目录
EXCLUDE_DIRS = {".obsidian", ".git", "__pycache__", "node_modules"}
EXCLUDE_EXTENSIONS = {".pyc", ".pyo", ".exe", ".dll", ".so", ".dylib"}


def is_path_safe(file_path: str) -> bool:
    """检查路径是否在 vault 内"""
    try:
        abs_path = Path(file_path).resolve()
        vault_abs = VAULT_ROOT.resolve()
        # 检查路径是否在 vault 目录下
        return str(abs_path).startswith(str(vault_abs))
    except (ValueError, OSError):
        return False


def detect_sensitive_info(content: str) -> List[Dict[str, Any]]:
    """
    检测内容中的敏感信息
    返回: [{type, matched, line_number, context}]
    """
    issues = []
    lines = content.split("\n")

    for line_num, line in enumerate(lines, start=1):
        for info_type, patterns in COMPILED_PATTERNS.items():
            for pattern in patterns:
                match = pattern.search(line)
                if match:
                    # 提取匹配上下文（前后各20字符）
                    start = max(0, match.start() - 20)
                    end = min(len(line), match.end() + 20)
                    context = line[start:end].strip()

                    issues.append({
                        "type": info_type,
                        "matched": match.group(),
                        "line_number": line_num,
                        "context": context,
                    })
                    break  # 每行只报一次

    return issues


def check_file(file_path: str) -> Dict[str, Any]:
    """
    检查单个文件
    返回: {path, is_safe, issues}
    """
    result = {
        "path": file_path,
        "is_safe": True,
        "issues": [],
    }

    # 1. 路径安全校验
    if not is_path_safe(file_path):
        result["is_safe"] = False
        result["issues"].append({
            "severity": "error",
            "type": "path_violation",
            "message": f"路径超出 vault 范围: {file_path}",
        })
        return result

    # 2. 检查文件是否在排除目录
    rel_path = Path(file_path).relative_to(VAULT_ROOT)
    if any(part in EXCLUDE_DIRS for part in rel_path.parts):
        return result

    # 3. 检查文件扩展名
    if rel_path.suffix.lower() in EXCLUDE_EXTENSIONS:
        return result

    # 4. 敏感信息检测（仅文本文件）
    text_extensions = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".xml", ".html", ".css", ".js", ".ts"}
    if rel_path.suffix.lower() not in text_extensions:
        return result

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        result["issues"].append({
            "severity": "warning",
            "type": "read_error",
            "message": f"读取文件失败: {str(e)}",
        })
        return result

    # 检测敏感信息
    sensitive_issues = detect_sensitive_info(content)
    if sensitive_issues:
        result["is_safe"] = False
        for issue in sensitive_issues:
            result["issues"].append({
                "severity": "warning",
                "type": "sensitive_info",
                "info_type": issue["type"],
                "line": issue["line_number"],
                "context": issue["context"],
                "message": f"检测到敏感信息 [{issue['type']}] 在第 {issue['line_number']} 行",
            })

    return result


def check_path(path: str) -> Dict[str, Any]:
    """
    检查指定路径（文件或目录）
    返回: {is_safe, issues, files_checked}
    """
    result = {
        "is_safe": True,
        "issues": [],
        "files_checked": 0,
    }

    target_path = Path(path)

    # 处理文件
    if target_path.is_file():
        file_result = check_file(str(target_path))
        result["files_checked"] = 1
        result["is_safe"] = file_result["is_safe"]
        result["issues"].extend(file_result["issues"])
        return result

    # 处理目录
    if target_path.is_dir():
        for file_path in target_path.rglob("*"):
            if file_path.is_file():
                result["files_checked"] += 1
                file_result = check_file(str(file_path))
                if not file_result["is_safe"]:
                    result["is_safe"] = False
                result["issues"].extend(file_result["issues"])

        return result

    # 路径不存在
    result["is_safe"] = False
    result["issues"].append({
        "severity": "error",
        "type": "path_not_found",
        "message": f"路径不存在: {path}",
    })

    return result


def check(text: str) -> Dict[str, Any]:
    """
    主入口函数 - 检查文本内容中的敏感信息
    返回: {is_safe, issues}
    """
    result = {
        "is_safe": True,
        "issues": [],
    }

    # 检测敏感信息
    sensitive_issues = detect_sensitive_info(text)
    if sensitive_issues:
        result["is_safe"] = False
        for issue in sensitive_issues:
            result["issues"].append({
                "severity": "warning",
                "type": "sensitive_info",
                "info_type": issue["type"],
                "line": issue["line_number"],
                "context": issue["context"],
                "message": f"检测到敏感信息 [{issue['type']}] 在第 {issue['line_number']} 行",
            })

    return result


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        target = str(VAULT_ROOT)

    print(f"检查路径: {target}")
    result = check_path(target)

    print(f"\n文件检查数: {result['files_checked']}")
    status = "PASS" if result["is_safe"] else "WARN"
    print(f"安全状态: {status}")

    if result["issues"]:
        print("\n问题列表:")
        for i, issue in enumerate(result["issues"], 1):
            print(f"  {i}. [{issue['severity']}] {issue['type']}: {issue.get('message', '')}")

    print(f"\n{{is_safe: {result['is_safe']}, issues: {len(result['issues'])}}}")
