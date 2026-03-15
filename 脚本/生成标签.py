"""
标签生成脚本
从笔记内容中提取已有标签并基于关键词生成新标签
"""
import re
from typing import List, Set

# 关键词到标签的映射
KEYWORD_TAG_MAP = {
    "python": "python",
    "java": "java",
    "go": "go",
    "golang": "go",
    "docker": "docker",
    "k8s": "kubernetes",
    "kubernetes": "kubernetes",
    "mysql": "mysql",
    "redis": "redis",
    "ai": "ai",
    "机器学习": "机器学习",
    "深度学习": "深度学习",
    "tcp": "tcp",
    "http": "http",
    "dns": "dns",
    "linux": "linux",
    "windows": "windows",
    "nginx": "nginx",
    "rabbitmq": "rabbitmq",
    "kafka": "kafka",
    "elasticsearch": "elasticsearch",
    "mongodb": "mongodb",
    "postgresql": "postgresql",
    "git": "git",
    "微服务": "微服务",
    "分布式": "分布式",
    "安全": "安全",
    "算法": "算法",
    "数据结构": "数据结构",
}


def extract_existing_tags(content: str) -> Set[str]:
    """从笔记内容中提取已有的 #tag"""
    # 匹配 #tag 格式（支持中英文标签）
    pattern = r"#([a-zA-Z\u4e00-\u9fa5][a-zA-Z0-9_\u4e00-\u9fa5-]*)"
    tags = re.findall(pattern, content)
    return set(tags)


def generate_tags_from_content(content: str) -> Set[str]:
    """基于关键词匹配生成新标签"""
    content_lower = content.lower()
    generated_tags = set()

    for keyword, tag in KEYWORD_TAG_MAP.items():
        # 单词边界匹配，避免部分匹配
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, content_lower, re.IGNORECASE):
            generated_tags.add(tag)

    return generated_tags


def generate_tags(content: str) -> List[str]:
    """
    生成标签列表
    1. 提取已有 #tag
    2. 基于关键词生成新标签
    3. 合并并去重

    Args:
        content: 笔记内容

    Returns:
        排序后的标签列表
    """
    existing_tags = extract_existing_tags(content)
    generated_tags = generate_tags_from_content(content)

    # 合并已有标签和生成标签
    all_tags = existing_tags | generated_tags

    # 排序返回
    return sorted(all_tags)


if __name__ == "__main__":
    # 测试示例
    test_content = """
    # Python Docker MySQL

    这是一篇关于 Python 和 Docker 的笔记。
    使用 MySQL 数据库进行数据存储。
    同时涉及 Kubernetes 部署。

    ## 机器学习

    我们使用深度学习模型进行预测。
    """

    tags = generate_tags(test_content)
    print("生成的标签:", tags)
