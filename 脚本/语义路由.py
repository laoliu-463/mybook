from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RouteResult:
    skill: str
    score: float
    reason: str


SKILL_RULES = {
    "springboot-patterns": ["spring boot", "controller", "service", "mybatis", "jwt", "swagger"],
    "api-design": ["api", "接口", "rest", "requestmapping", "endpoint"],
    "backend-patterns": ["数据库", "redis", "mq", "消息队列", "repository"],
    "frontend-patterns": ["react", "vue", "next.js", "前端", "css"],
    "database-migrations": ["migration", "ddl", "schema", "索引", "表结构"],
    "mermaid-visualizer": ["mermaid", "流程图", "diagram"],
    "obsidian-canvas-creator": ["canvas", "whiteboard", "白板", "思维导图"],
    "obsidian-note-organizer": ["obsidian", "收集箱", "para", "双链", "moc"],
}


def select_skill(text: str) -> RouteResult:
    haystack = text.lower()
    best_skill = "obsidian-note-organizer"
    best_matches = 0

    for skill, keywords in SKILL_RULES.items():
        matches = sum(1 for keyword in keywords if keyword.lower() in haystack)
        if matches > best_matches:
            best_skill = skill
            best_matches = matches

    if best_matches == 0:
        return RouteResult(
            skill=best_skill,
            score=0.0,
            reason="未命中更具体的规则，使用默认 Obsidian 工作流 Skill。",
        )

    max_keywords = len(SKILL_RULES[best_skill])
    score = round(best_matches / max_keywords, 2)
    return RouteResult(
        skill=best_skill,
        score=score,
        reason=f"命中 {best_matches} 个相关关键词。",
    )
