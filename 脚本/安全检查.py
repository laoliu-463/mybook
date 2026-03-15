from __future__ import annotations

from pathlib import Path
import re

import 读写笔记 as note_io


ALLOWED_WRITE_ROOTS = {
    "00-收集箱",
    "10-项目",
    "20-知识库",
    "30-资源",
    "40-交付物",
    "系统",
}

PROTECTED_ROOTS = {
    ".git",
    ".obsidian",
    ".claude",
    "80-模板",
    "99-归档",
}

SENSITIVE_PATTERNS = [
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"(?i)(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9._/\-+=]{12,}"),
    re.compile(r"(?i)authorization:\s*bearer\s+[A-Za-z0-9._\-]{12,}"),
    re.compile(r"(?i)^cookie:\s*.+$", re.MULTILINE),
]


class SecurityViolation(ValueError):
    pass


def ensure_safe_read(path: Path) -> None:
    resolved = path.resolve()
    vault_root = note_io.get_vault_root().resolve()
    try:
        resolved.relative_to(vault_root)
    except ValueError as exc:
        raise SecurityViolation(f"路径越界: {path}") from exc


def ensure_safe_write(path: Path) -> None:
    ensure_safe_read(path)
    relative = note_io.relative_vault_path(path)
    top_level = relative.split("/", 1)[0]

    if top_level in PROTECTED_ROOTS:
        raise SecurityViolation(f"禁止写入受保护目录: {relative}")
    if top_level not in ALLOWED_WRITE_ROOTS:
        raise SecurityViolation(f"禁止写入未授权目录: {relative}")


def validate_note_for_processing(path: Path, text: str) -> None:
    ensure_safe_read(path)
    relative = note_io.relative_vault_path(path)
    if not relative.startswith("00-收集箱/"):
        raise SecurityViolation(f"只允许处理收件箱中的笔记: {relative}")

    findings = detect_sensitive_content(text)
    if findings:
        raise SecurityViolation(f"检测到疑似敏感信息，已停止处理: {'; '.join(findings)}")


def detect_sensitive_content(text: str) -> list[str]:
    findings: list[str] = []
    for pattern in SENSITIVE_PATTERNS:
        match = pattern.search(text)
        if match:
            findings.append(match.group(0)[:40])
    return findings
