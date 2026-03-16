from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FormatResult:
    optimized_body: str
    has_code: bool
    has_mermaid: bool
    code_blocks: list[str]
    mermaid_blocks: list[str]


# 代码语言映射（用于语法高亮）
CODE_LANGUAGE_MAP = {
    "python": "python",
    "py": "python",
    "javascript": "javascript",
    "js": "javascript",
    "typescript": "typescript",
    "ts": "typescript",
    "java": "java",
    "go": "go",
    "rust": "rust",
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "csharp": "csharp",
    "c#": "csharp",
    "ruby": "ruby",
    "rb": "ruby",
    "php": "php",
    "swift": "swift",
    "kotlin": "kotlin",
    "scala": "scala",
    "sql": "sql",
    "html": "html",
    "css": "css",
    "xml": "xml",
    "json": "json",
    "yaml": "yaml",
    "yml": "yaml",
    "bash": "bash",
    "sh": "bash",
    "shell": "bash",
    "dockerfile": "dockerfile",
    "markdown": "markdown",
    "md": "markdown",
}


def detect_language(code: str) -> str:
    """根据代码内容检测语言"""
    code_lower = code.lower().strip()

    # 常见模式匹配
    patterns = [
        (r"^import\s+\w+", "python"),
        (r"^from\s+\w+\s+import", "python"),
        (r"^const\s+\w+\s*=", "javascript"),
        (r"^let\s+\w+\s*=", "javascript"),
        (r"^function\s+\w+\s*\(", "javascript"),
        (r"^def\s+\w+\s*\(", "python"),
        (r"^class\s+\w+.*\{", "java"),
        (r"^public\s+class", "java"),
        (r"^package\s+\w+;", "java"),
        (r"^func\s+\w+\s*\(", "go"),
        (r"^fn\s+\w+\s*\(", "rust"),
        (r"^struct\s+\w+\s*\{", "rust"),
        (r"^<\?php", "php"),
        (r"^select\s+.*from", "sql"),
        (r"^create\s+table", "sql"),
        (r"^<!DOCTYPE\s+html", "html"),
        (r"^<html", "html"),
        (r"^\{[\s\n]*\"", "json"),
        (r"^---\s*$", "yaml"),
        (r"^#!\/bin\/(bash|sh)", "bash"),
    ]

    for pattern, lang in patterns:
        if re.search(pattern, code_lower, re.MULTILINE):
            return CODE_LANGUAGE_MAP.get(lang, "")

    return ""


def extract_code_blocks(text: str) -> tuple[str, list[str]]:
    """提取并标准化代码块"""
    code_blocks = []

    # 匹配 ```...``` 格式
    pattern = r"```(\w*)\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    for lang, code in matches:
        # 检测语言
        if not lang:
            detected = detect_language(code)
            if detected:
                lang = detected
        code_blocks.append(code.strip())

        # 标准化语言标识
        if lang and lang.lower() in CODE_LANGUAGE_MAP:
            lang = CODE_LANGUAGE_MAP[lang.lower()]

    return text, code_blocks


def extract_mermaid_blocks(text: str) -> tuple[str, list[str]]:
    """提取并标准化 Mermaid 块"""
    mermaid_blocks = []

    # 匹配 ```mermaid ...``` 格式
    pattern = r"```mermaid\n(.*?)```"
    matches = re.findall(pattern, text, re.DOTALL)

    for diagram in matches:
        mermaid_blocks.append(diagram.strip())

    return text, mermaid_blocks


def format_code_block(code: str, language: str = "") -> str:
    """格式化单个代码块"""
    # 清理代码
    cleaned = code.strip()

    # 检测语言
    if not language:
        language = detect_language(cleaned)

    # 返回标准化格式
    if language:
        return f"```{language}\n{cleaned}\n```"
    return f"```\n{cleaned}\n```"


def format_mermaid_block(diagram: str, diagram_type: str = "") -> str:
    """格式化单个 Mermaid 块"""
    cleaned = diagram.strip()

    # 检测图表类型并设置更具体的类型
    if not diagram_type:
        if "graph" in cleaned or "flowchart" in cleaned:
            diagram_type = "mermaid"
        elif "sequenceDiagram" in cleaned:
            diagram_type = "mermaid"
        elif "classDiagram" in cleaned:
            diagram_type = "mermaid"
        elif "stateDiagram" in cleaned:
            diagram_type = "mermaid"
        elif "erDiagram" in cleaned:
            diagram_type = "mermaid"
        elif "pie" in cleaned:
            diagram_type = "mermaid"
        elif "mindmap" in cleaned:
            diagram_type = "mermaid"
        elif "gitGraph" in cleaned:
            diagram_type = "mermaid"
        else:
            diagram_type = "mermaid"

    # 确保使用 mermaid 语言标识
    return f"```mermaid\n{cleaned}\n```"


def normalize_all_mermaid_blocks(body: str) -> str:
    """标准化所有 Mermaid 块"""
    # 匹配没有语言标识的 Mermaid 图
    pattern = r"```\n(graph|sequenceDiagram|classDiagram|stateDiagram|erDiagram|pie|mindmap|gitGraph)"
    body = re.sub(pattern, r"```mermaid\n\1", body)

    # 匹配已有其他标识的 Mermaid 图 (忽略原有标识)
    pattern2 = r"```\w*\n(graph|sequenceDiagram|classDiagram|stateDiagram|erDiagram|pie|mindmap|gitGraph)"
    body = re.sub(pattern2, r"```mermaid\n\1", body)

    return body


def add_code_fence_sections(body: str) -> str:
    """添加代码块索引分区"""
    # 提取所有代码块
    code_pattern = r"```(\w*)\n(.*?)```"
    code_blocks = re.findall(code_pattern, body, re.DOTALL)

    if not code_blocks:
        return body

    # 生成代码块索引
    code_index = []
    for i, (lang, code) in enumerate(code_blocks, 1):
        first_line = code.strip().split('\n')[0][:50]
        lang_display = lang if lang else "text"
        code_index.append(f"- 代码块 {i}: `{lang_display}` - `{first_line}...`")

    # 添加分区
    index_text = "\n".join(code_index)

    # 如果已有分区，更新它
    if "## 代码块索引" in body:
        # 替换现有分区
        pattern = r"## 代码块索引\n.*?(?=\n## |\Z)"
        body = re.sub(pattern, f"## 代码块索引\n{index_text}\n", body, flags=re.DOTALL)
    else:
        # 在标题后添加
        lines = body.split('\n')
        insert_idx = 1
        for i, line in enumerate(lines):
            if line.startswith('# '):
                insert_idx = i + 2
                break

        lines.insert(insert_idx, f"\n## 代码块索引\n{index_text}\n")
        body = '\n'.join(lines)

    return body


def add_mermaid_index_section(body: str) -> str:
    """添加 Mermaid 图表索引分区"""
    # 提取所有 Mermaid 块
    mermaid_pattern = r"```mermaid\n(.*?)```"
    mermaid_blocks = re.findall(mermaid_pattern, body, re.DOTALL)

    if not mermaid_blocks:
        return body

    # 生成图表索引
    diagram_index = []
    for i, diagram in enumerate(mermaid_blocks, 1):
        # 检测图表类型
        if "graph" in diagram or "flowchart" in diagram:
            dtype = "流程图"
        elif "sequenceDiagram" in diagram:
            dtype = "时序图"
        elif "classDiagram" in diagram:
            dtype = "类图"
        elif "stateDiagram" in diagram:
            dtype = "状态图"
        elif "erDiagram" in diagram:
            dtype = "ER图"
        elif "pie" in diagram:
            dtype = "饼图"
        elif "mindmap" in diagram:
            dtype = "思维导图"
        else:
            dtype = "图表"

        diagram_index.append(f"- 图表 {i}: {dtype}")

    index_text = "\n".join(diagram_index)

    # 如果已有分区，更新它
    if "## Mermaid 图表索引" in body:
        pattern = r"## Mermaid 图表索引\n.*?(?=\n## |\Z)"
        body = re.sub(pattern, f"## Mermaid 图表索引\n{index_text}\n", body, flags=re.DOTALL)
    else:
        lines = body.split('\n')
        insert_idx = 1
        for i, line in enumerate(lines):
            if line.startswith('# '):
                insert_idx = i + 2
                break
        lines.insert(insert_idx, f"\n## Mermaid 图表索引\n{index_text}\n")
        body = '\n'.join(lines)

    return body


def optimize_note_format(body: str) -> FormatResult:
    """优化笔记格式，返回优化后的内容和元信息"""

    # 先标准化所有 Mermaid 块
    body = normalize_all_mermaid_blocks(body)

    # 提取代码块
    body, code_blocks = extract_code_blocks(body)

    # 提取 Mermaid 块
    body, mermaid_blocks = extract_mermaid_blocks(body)

    # 添加索引分区
    body = add_code_fence_sections(body)
    body = add_mermaid_index_section(body)

    # 标准化代码块格式
    for code in code_blocks:
        lang = detect_language(code)
        formatted = format_code_block(code, lang)
        # 替换原始代码块
        pattern = rf"```[\w]*\n{re.escape(code)}\n```"
        body = re.sub(pattern, lambda _: formatted, body)

    return FormatResult(
        optimized_body=body,
        has_code=len(code_blocks) > 0,
        has_mermaid=len(mermaid_blocks) > 0,
        code_blocks=code_blocks,
        mermaid_blocks=mermaid_blocks,
    )


def has_code_block(text: str) -> bool:
    """检查文本是否包含代码块"""
    return bool(re.search(r"```[\s\S]*?```", text))


def has_mermaid_block(text: str) -> bool:
    """检查文本是否包含 Mermaid 图表"""
    return bool(re.search(r"```mermaid\n[\s\S]*?```", text))


def extract_diagram_type(diagram: str) -> str:
    """提取 Mermaid 图表类型"""
    if "graph" in diagram or "flowchart" in diagram:
        return "flowchart"
    if "sequenceDiagram" in diagram:
        return "sequence"
    if "classDiagram" in diagram:
        return "class"
    if "stateDiagram" in diagram:
        return "state"
    if "erDiagram" in diagram:
        return "er"
    if "pie" in diagram:
        return "pie"
    if "mindmap" in diagram:
        return "mindmap"
    if "gitGraph" in diagram:
        return "git"
    return "unknown"
