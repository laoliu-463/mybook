from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SubagentRoute:
    agent: str
    confidence: float
    reason: str


# Subagent 路由规则
SUBAGENT_RULES = {
    "process-paper": {
        "keywords": ["abstract", "introduction", "conclusion", "references", "doi", "arxiv", "methodology", "研究", "论文", "实验", "结果", "abstract", "摘要"],
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


def route_to_subagent(text: str) -> SubagentRoute | None:
    """
    根据笔记内容路由到对应的 subagent。

    Returns:
        SubagentRoute: 包含 agent 名称、置信度、原因
        None: 如果没有匹配到任何 subagent
    """
    text_lower = text.lower()

    candidates = []

    for agent, rule in SUBAGENT_RULES.items():
        keywords = rule["keywords"]
        weight = rule["weight"]

        matches = sum(1 for kw in keywords if kw.lower() in text_lower)

        if matches > 0:
            confidence = min(matches / len(keywords) * weight, 1.0)
            candidates.append((agent, confidence, matches))

    if not candidates:
        return None

    # 按匹配数排序，选最高的
    candidates.sort(key=lambda x: -x[2])
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
    """
    获取 subagent 的 prompt 模板。
    """
    prompts = {
        "process-paper": """你是一个论文笔记处理专家。请对以下论文笔记进行深度结构化处理：

目标：
- 提取研究问题、研究方法、核心发现、局限性
- 增强 frontmatter（添加 domain、tags）
- 保留原文，只做增强不删除内容
- 添加结构化分区：## 研究问题、## 研究方法、## 核心发现、## 局限与展望

请直接修改笔记内容。""",

        "process-code-snippet": """你是一个代码笔记处理专家。请对以下代码笔记进行处理：

目标：
- 提取代码功能描述、适用场景、依赖说明
- 为无注释代码添加简要说明
- 增强 frontmatter（添加 tags: 编程语言、技术栈）
- 保留原文，只做增强不删除内容

请直接修改笔记内容。""",

        "process-meeting-notes": """你是一个会议笔记处理专家。请对以下会议笔记进行处理：

目标：
- 提取会议主题、时间、参会人
- 识别所有 Action Item / TODO
- 生成会议总结
- 增强 frontmatter（添加 type: project, tags）
- 保留原文，只做增强不删除内容

请直接修改笔记内容。""",
    }

    return prompts.get(agent_name, "请处理这篇笔记。")


def should_invoke_subagent(route: SubagentRoute | None, threshold: float = 0.2) -> bool:
    """
    判断是否应该调用 subagent。
    """
    if route is None:
        return False
    return route.confidence >= threshold
