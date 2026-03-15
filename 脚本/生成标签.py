from __future__ import annotations

import re


TAG_RULES = {
    "java": ["java", "jdk", "spring boot", "mybatis"],
    "springboot": ["spring boot", "@restcontroller", "requestmapping"],
    "api": ["api", "接口", "controller", "swagger", "knife4j"],
    "业务设计": ["业务", "设计", "流程图", "模型设计"],
    "数据库": ["mysql", "redis", "sql", "数据库"],
    "安全": ["jwt", "security", "鉴权", "权限"],
    "项目": ["项目", "会议", "需求", "任务"],
    "ai": ["ai", "agent", "llm", "prompt"],
    "云原生": ["docker", "k8s", "容器"],
}


def generate_tags(text: str, existing_tags: list[str] | None = None, limit: int = 8) -> list[str]:
    tags = {normalize_tag(tag) for tag in (existing_tags or []) if normalize_tag(tag)}
    haystack = text.lower()

    for tag, keywords in TAG_RULES.items():
        if any(keyword.lower() in haystack for keyword in keywords):
            tags.add(tag)

    inline_tags = re.findall(r"(?<!\w)#([\w\-/\u4e00-\u9fff]+)", text)
    tags.update(normalize_tag(tag) for tag in inline_tags)

    ordered = sorted(tags)
    return ordered[:limit]


def normalize_tag(tag: str) -> str:
    return tag.strip().lstrip("#")
