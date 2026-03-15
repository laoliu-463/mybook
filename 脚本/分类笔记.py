from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ClassificationResult:
    target_dir: str
    note_type: str
    domains: list[str]
    reason: str


RULES = [
    {
        "keywords": ["项目", "会议", "任务", "需求", "接口设计", "模型设计", "开发规范", "模块"],
        "target_dir": "10-项目/自动归档",
        "note_type": "project",
        "domains": ["项目"],
        "reason": "命中项目型关键词，优先归档到 10-项目。",
    },
    {
        "keywords": ["python", "java", "go", "代码", "编程", "spring", "jdk", "mybatis"],
        "target_dir": "20-知识库/编程语言",
        "note_type": "concept",
        "domains": ["编程语言"],
        "reason": "命中编程语言与工程实现关键词。",
    },
    {
        "keywords": ["tcp", "http", "网络", "协议", "dns", "socket"],
        "target_dir": "20-知识库/计算机网络",
        "note_type": "concept",
        "domains": ["计算机网络"],
        "reason": "命中网络协议关键词。",
    },
    {
        "keywords": ["mysql", "redis", "sql", "数据库", "表结构", "索引"],
        "target_dir": "20-知识库/数据库",
        "note_type": "concept",
        "domains": ["数据库"],
        "reason": "命中数据库关键词。",
    },
    {
        "keywords": ["docker", "k8s", "容器", "kubernetes", "cloud native"],
        "target_dir": "20-知识库/云原生",
        "note_type": "concept",
        "domains": ["云原生"],
        "reason": "命中云原生关键词。",
    },
    {
        "keywords": ["机器学习", "ai", "深度学习", "llm", "agent", "prompt"],
        "target_dir": "20-知识库/AI-ML",
        "note_type": "concept",
        "domains": ["AI-ML"],
        "reason": "命中 AI/ML 关键词。",
    },
    {
        "keywords": ["论文", "课程", "教程", "资料", "文档", "book", "paper"],
        "target_dir": "30-资源/自动归档",
        "note_type": "resource",
        "domains": ["资源"],
        "reason": "命中资源型关键词。",
    },
]


DEFAULT_RESULT = ClassificationResult(
    target_dir="30-资源/待分类",
    note_type="resource",
    domains=["资源"],
    reason="未命中明确规则，暂存到 30-资源/待分类。",
)


def classify_note(title: str, body: str) -> ClassificationResult:
    haystack = f"{title}\n{body}".lower()

    best_score = 0
    best_rule: dict[str, object] | None = None
    for rule in RULES:
        score = sum(1 for keyword in rule["keywords"] if keyword.lower() in haystack)
        if score > best_score:
            best_score = score
            best_rule = rule

    if not best_rule:
        return DEFAULT_RESULT

    return ClassificationResult(
        target_dir=str(best_rule["target_dir"]),
        note_type=str(best_rule["note_type"]),
        domains=list(best_rule["domains"]),
        reason=str(best_rule["reason"]),
    )
