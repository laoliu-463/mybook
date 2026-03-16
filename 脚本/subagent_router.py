from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import subprocess


@dataclass(frozen=True, slots=True)
class SubagentRoute:
    agent: str
    confidence: float
    reason: str


@dataclass(frozen=True, slots=True)
class StructuredSection:
    heading: str
    content: str


@dataclass(frozen=True, slots=True)
class SubagentExecutionResult:
    agent: str
    invoked: bool
    mode: str
    fallback_used: bool
    fallback_reason: str | None
    tags: list[str]
    domains: list[str]
    note_type: str | None
    sections: list[StructuredSection]
    review_notes: list[str]
    error: str | None


SUBAGENT_RULES = {
    "process-paper": {
        "keywords": ["abstract", "introduction", "conclusion", "references", "doi", "arxiv", "methodology", "研究", "论文", "实验", "结果", "摘要"],
        "weight": 1.0,
    },
    "process-code-snippet": {
        "keywords": ["def ", "import ", "class ", "function ", "```", "code", "代码", "python", "java", "javascript", "go", "rust", "api", "sdk"],
        "weight": 1.0,
    },
    "process-meeting-notes": {
        "keywords": ["会议", "meeting", "agenda", "action item", "todo", "待办", "参会", "决议", "讨论", "会议纪要"],
        "weight": 1.0,
    },
}


CLAUDE_JSON_SCHEMA = json.dumps(
    {
        "type": "object",
        "properties": {
            "summary": {"type": "string"},
            "tags": {"type": "array", "items": {"type": "string"}},
            "domains": {"type": "array", "items": {"type": "string"}},
            "note_type": {"type": "string"},
            "sections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "heading": {"type": "string"},
                        "content": {"type": "string"},
                    },
                    "required": ["heading", "content"],
                    "additionalProperties": False,
                },
            },
            "review_notes": {"type": "array", "items": {"type": "string"}},
        },
        "required": ["summary", "tags", "sections", "review_notes"],
        "additionalProperties": False,
    },
    ensure_ascii=False,
)


def route_to_subagent(text: str) -> SubagentRoute | None:
    text_lower = text.lower()
    candidates: list[tuple[str, float, int]] = []

    for agent, rule in SUBAGENT_RULES.items():
        keywords = rule["keywords"]
        weight = rule["weight"]
        matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
        if matches > 0:
            confidence = min(matches / len(keywords) * weight, 1.0)
            candidates.append((agent, confidence, matches))

    if not candidates:
        return None

    candidates.sort(key=lambda item: (-item[2], -item[1], item[0]))
    best_agent, best_confidence, best_matches = candidates[0]
    reason_map = {
        "process-paper": f"命中论文结构关键词 {best_matches} 个",
        "process-code-snippet": f"命中代码关键词 {best_matches} 个",
        "process-meeting-notes": f"命中会议关键词 {best_matches} 个",
    }
    return SubagentRoute(
        agent=best_agent,
        confidence=best_confidence,
        reason=reason_map.get(best_agent, f"匹配 {best_matches} 个关键词"),
    )


def get_subagent_prompt(agent_name: str) -> str:
    prompts = {
        "process-paper": """你是一个论文笔记处理专家。请对以下论文笔记进行结构化增强。

目标：
- 提取研究问题、研究方法、核心发现、局限性
- 推荐更合适的 tags/domain/type
- 输出 2-4 个结构化分区，便于稍后写回 Markdown
- 保留不确定信息并写入 review_notes
""",
        "process-code-snippet": """你是一个代码笔记处理专家。请对以下代码笔记进行结构化增强。

目标：
- 解释代码用途与上下文
- 提取关键技术栈标签和领域
- 输出 2-4 个结构化分区，优先包含“示例”或“常见坑与边界”
- 将无法确认的细节写入 review_notes
""",
        "process-meeting-notes": """你是一个会议笔记处理专家。请对以下会议笔记进行结构化增强。

目标：
- 提取会议决议、行动项、风险和待确认项
- 推荐 project 类型和合适 tags
- 输出 2-4 个结构化分区，适合后续写回 Markdown
- 将缺失负责人或时间的信息写入 review_notes
""",
    }
    return prompts.get(agent_name, "请结构化处理这篇笔记，并返回 JSON。")


def should_invoke_subagent(route: SubagentRoute | None, threshold: float = 0.2) -> bool:
    if route is None:
        return False
    return route.confidence >= threshold


def execute_subagent(
    agent_name: str,
    *,
    title: str,
    body: str,
    timeout_seconds: int = 90,
    allow_claude: bool = True,
) -> SubagentExecutionResult:
    if allow_claude and shutil.which("claude"):
        try:
            return invoke_claude_subagent(
                agent_name,
                title=title,
                body=body,
                timeout_seconds=timeout_seconds,
            )
        except Exception as exc:  # pragma: no cover - fallback path is the important behavior here
            return build_fallback_result(agent_name, title=title, body=body, error=summarize_error(str(exc)))
    return build_fallback_result(agent_name, title=title, body=body, error="claude-cli-unavailable")


def invoke_claude_subagent(
    agent_name: str,
    *,
    title: str,
    body: str,
    timeout_seconds: int,
) -> SubagentExecutionResult:
    prompt = build_structured_prompt(agent_name, title=title, body=body)
    working_root = Path(os.environ.get("OBSIDIAN_VAULT_ROOT", Path(__file__).resolve().parent.parent)).resolve()
    completed = subprocess.run(
        [
            "claude",
            "-p",
            "--agent",
            agent_name,
            "--output-format",
            "json",
            "--json-schema",
            CLAUDE_JSON_SCHEMA,
            "--permission-mode",
            "default",
            "--allowedTools",
            "",
            "--setting-sources",
            "project",
            "--add-dir",
            str(working_root),
            prompt,
        ],
        cwd=working_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout_seconds,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or completed.stdout.strip() or "unknown-claude-error"
        raise RuntimeError(summarize_error(stderr))

    payload = json.loads(completed.stdout)
    return normalize_claude_payload(agent_name, payload)


def build_structured_prompt(agent_name: str, *, title: str, body: str) -> str:
    return (
        f"{get_subagent_prompt(agent_name)}\n"
        "请基于下面的笔记内容返回 JSON，不要修改文件，也不要输出 schema 之外的字段。\n\n"
        f"标题：{title}\n\n"
        "正文：\n"
        f"{body.strip()}\n"
    )


def normalize_claude_payload(agent_name: str, payload: dict[str, object]) -> SubagentExecutionResult:
    sections = [
        StructuredSection(
            heading=str(item.get("heading", "")).strip(),
            content=str(item.get("content", "")).strip(),
        )
        for item in payload.get("sections", [])
        if isinstance(item, dict) and str(item.get("heading", "")).strip() and str(item.get("content", "")).strip()
    ]
    return SubagentExecutionResult(
        agent=agent_name,
        invoked=True,
        mode="claude",
        fallback_used=False,
        fallback_reason=None,
        tags=normalize_string_list(payload.get("tags")),
        domains=normalize_string_list(payload.get("domains")),
        note_type=normalize_note_type(payload.get("note_type")),
        sections=sections,
        review_notes=normalize_string_list(payload.get("review_notes")),
        error=None,
    )


def build_fallback_result(agent_name: str, *, title: str, body: str, error: str) -> SubagentExecutionResult:
    fallback_reason = classify_fallback_reason(error)
    lines = extract_meaningful_lines(body)
    if agent_name == "process-paper":
        sections = [
            StructuredSection("研究问题", first_nonempty(lines, "需要人工补充研究问题。")),
            StructuredSection("研究方法", nth_or_default(lines, 1, "需要人工补充研究方法与实验设计。")),
            StructuredSection("核心发现", nth_or_default(lines, 2, "需要人工补充核心结论与实验结果。")),
            StructuredSection("局限与展望", "自动路由识别为论文类笔记，具体结论与局限需要人工复核。"),
        ]
        tags = ["论文", "研究"]
        domains = ["资源"]
        note_type = "resource"
        review_notes = ["论文类笔记已走本地降级增强，研究结论需人工复核。"]
    elif agent_name == "process-meeting-notes":
        sections = [
            StructuredSection("会议决议", first_nonempty(lines, "需要人工补充会议决议。")),
            StructuredSection("行动项", nth_or_default(lines, 1, "需要人工补充行动项、负责人和截止时间。")),
            StructuredSection("风险与待确认", "自动路由识别为会议纪要，未识别的责任人与时间线需人工确认。"),
        ]
        tags = ["会议纪要", "待办"]
        domains = ["项目"]
        note_type = "project"
        review_notes = ["会议类笔记已走本地降级增强，负责人和时间线需人工复核。"]
    else:
        sections = [
            StructuredSection("示例说明", first_nonempty(lines, f"{title} 识别为代码片段类笔记，建议人工补充完整使用场景。")),
            StructuredSection("关键技术点", nth_or_default(lines, 1, "需要人工补充关键 API、依赖和技术栈。")),
            StructuredSection("常见坑与边界", "自动路由识别为代码片段，异常处理、边界条件和运行环境需人工复核。"),
        ]
        tags = ["代码片段", "示例"]
        domains = ["编程语言"]
        note_type = "concept"
        review_notes = ["代码类笔记已走本地降级增强，依赖和边界条件需人工复核。"]

    return SubagentExecutionResult(
        agent=agent_name,
        invoked=True,
        mode="fallback",
        fallback_used=True,
        fallback_reason=fallback_reason,
        tags=tags,
        domains=domains,
        note_type=note_type,
        sections=sections,
        review_notes=review_notes,
        error=error,
    )


def normalize_string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    items: list[str] = []
    seen: set[str] = set()
    for raw in value:
        text = str(raw).strip()
        if not text:
            continue
        key = text.casefold()
        if key in seen:
            continue
        seen.add(key)
        items.append(text)
    return items


def normalize_note_type(value: object) -> str | None:
    text = str(value).strip()
    if text in {"concept", "overview", "interview", "project", "resource"}:
        return text
    return None


def extract_meaningful_lines(body: str) -> list[str]:
    lines: list[str] = []
    for raw_line in body.splitlines():
        line = raw_line.strip().strip("-").strip()
        if not line or line.startswith("#") or line.startswith("```"):
            continue
        lines.append(line)
    return lines


def first_nonempty(lines: list[str], default: str) -> str:
    return lines[0] if lines else default


def nth_or_default(lines: list[str], index: int, default: str) -> str:
    if 0 <= index < len(lines):
        return lines[index]
    return default


def summarize_error(message: str, limit: int = 240) -> str:
    compact = " ".join(message.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 1].rstrip() + "…"


def classify_fallback_reason(error: str) -> str:
    lowered = error.casefold()
    if "timeout" in lowered:
        return "timeout"
    if "json" in lowered or "schema" in lowered or "parse" in lowered:
        return "invalid output"
    if "empty" in lowered:
        return "empty response"
    if "route" in lowered or "mismatch" in lowered:
        return "routing mismatch"
    return "subagent error"
