# -*- coding: utf-8 -*-
"""
笔记分类脚本 - 基于关键词匹配
"""

from typing import Optional


# 分类规则：关键词 -> 目标目录
CLASSIFICATION_RULES = {
    "20-知识库/编程语言": ["python", "java", "go", "代码", "编程", "rust", "javascript", "typescript", "c++", "cpp"],
    "20-知识库/计算机网络": ["tcp", "http", "网络", "协议", "dns", "https", "socket", "udp", "ip"],
    "20-知识库/数据库": ["mysql", "redis", "sql", "postgresql", "mongodb", "数据库", "索引", "事务"],
    "20-知识库/云原生": ["docker", "k8s", "kubernetes", "容器", "pod", "helm", "service mesh"],
    "20-知识库/AI-ML": ["机器学习", "ai", "深度学习", "神经网络", "ml", "llm", "gpt", "transformer", "人工智能"],
    "20-知识库/操作系统": ["linux", "windows", "操作系统", "进程", "线程", "内核", "文件系统"],
    "20-知识库/安全": ["安全", "加密", "渗透", "漏洞", "xss", "sql注入", "认证", "授权"],
    "10-项目": ["项目", "会议", "任务", "todo", "prd", "周报", "复盘"],
    "30-资源": ["论文", "课程", "教程", "书籍", "文档", "视频"],
}

# 默认目录
DEFAULT_DIRECTORY = "20-知识库/"


def classify_note(content: str) -> str:
    """
    根据笔记内容分类，返回最佳匹配目录

    Args:
        content: 笔记内容（标题 + 正文）

    Returns:
        目标目录路径
    """
    if not content:
        return DEFAULT_DIRECTORY

    # 转小写用于匹配
    content_lower = content.lower()

    # 统计每个分类的匹配次数
    match_scores = {}
    for directory, keywords in CLASSIFICATION_RULES.items():
        score = 0
        for keyword in keywords:
            # 精确匹配关键词
            if keyword.lower() in content_lower:
                score += 1

        if score > 0:
            match_scores[directory] = score

    if not match_scores:
        return DEFAULT_DIRECTORY

    # 返回匹配分数最高的分类
    best_match = max(match_scores.items(), key=lambda x: x[1])
    return best_match[0] + "/"


def classify_note_with_confidence(content: str) -> tuple[str, float]:
    """
    根据笔记内容分类，返回最佳匹配目录及置信度

    Args:
        content: 笔记内容（标题 + 正文）

    Returns:
        (目标目录路径, 置信度 0-1)
    """
    if not content:
        return DEFAULT_DIRECTORY, 0.0

    content_lower = content.lower()

    match_scores = {}
    for directory, keywords in CLASSIFICATION_RULES.items():
        score = 0
        for keyword in keywords:
            if keyword.lower() in content_lower:
                score += 1

        if score > 0:
            match_scores[directory] = score

    if not match_scores:
        return DEFAULT_DIRECTORY, 0.0

    best_match = max(match_scores.items(), key=lambda x: x[1])
    total_score = sum(match_scores.values())
    confidence = best_match[1] / total_score if total_score > 0 else 0.0

    return best_match[0] + "/", confidence


if __name__ == "__main__":
    # 测试示例
    test_cases = [
        "Python 编程实战 - Django 框架学习笔记",
        "TCP/IP 协议栈详解",
        "Redis 缓存设计与优化",
        "Docker 容器化部署实践",
        "机器学习入门指南",
        "项目启动会议纪要",
        "深度学习论文阅读笔记",
        "这是一篇普通笔记",
    ]

    print("笔记分类测试：")
    print("-" * 50)
    for content in test_cases:
        result, conf = classify_note_with_confidence(content)
        print(f"内容: {content[:30]}...")
        print(f"分类: {result} (置信度: {conf:.2f})")
        print()
