"""
语义路由脚本 - 分析笔记内容并映射到对应领域/子目录
"""
import re
from pathlib import Path
from typing import Optional

# 领域关键词映射规则
DOMAIN_KEYWORDS = {
    "编程语言": [
        r"\bpython\b", r"\bjava\b", r"\bgo\b", r"\bgolang\b", r"\bc\+\+\b",
        r"\brust\b", r"\bjavascript\b", r"\btypescript\b", r"\bjs\b", r"\bts\b",
        r"\bc\b(?!\+\+)", r"\bruby\b", r"\bphp\b", r"\bswift\b", r"\bkotlin\b"
    ],
    "数据结构与算法": [
        r"算法", r"数据结构", r"leetcode", r"刷题", r"时间复杂度",
        r"空间复杂度", r"复杂度分析", r"动态规划", r"贪心", r"回溯",
        r"分治", r"排序", r"搜索", r"图论", r"树", r"堆", r"栈", r"队列"
    ],
    "操作系统": [
        r"linux", r"windows", r"kernel", r"内核", r"进程", r"线程",
        r"内存管理", r"文件系统", r"系统调用", r"进程调度", r"死锁",
        r"并发", r"同步", r"锁", r"信号量"
    ],
    "计算机网络": [
        r"tcp\b", r"udp\b", r"http\b", r"https\b", r"dns", r"网络协议",
        r"socket", r"三次握手", r"四次挥手", r"滑动窗口", r"拥塞控制",
        r"路由器", r"交换机", r"ip\b", r"mac\b", r"arp\b", r"http/2", r"http/3"
    ],
    "数据库": [
        r"mysql", r"postgresql", r"redis", r"elasticsearch", r"es\b",
        r"mongodb", r"数据库", r"sql", r"索引", r"事务", r"锁",
        r"主从复制", r"读写分离", r"分库分表", r"缓存", r"持久化"
    ],
    "中间件": [
        r"kafka", r"rabbitmq", r"mq", r"消息队列", r"发布订阅",
        r"rocketmq", r"pulsar", r"activemq", r"消息中间件"
    ],
    "分布式与微服务": [
        r"微服务", r"分布式", r"服务治理", r"负载均衡", r"熔断",
        r"限流", r"降级", r"服务发现", r"注册中心", r"rpc",
        r"dubbo", r"grpc", r"spring\s*cloud", r"服务网格", r"consul"
    ],
    "云原生": [
        r"docker", r"k8s", r"kubernetes", r"service\s*mesh", r"istio",
        r"容器", r"容器化", r"pod", r"deployment", r"helm", r"ingress",
        r"service\s*mesh", r"envoy", r"containerd", r"镜像", r"镜像仓库"
    ],
    "安全": [
        r"web安全", r"密码学", r"攻防", r"xss", r"csrf", r"sql注入",
        r"加密", r"解密", r"哈希", r"对称加密", r"非对称加密",
        r"数字签名", r"证书", r"pki", r"渗透测试", r"安全加固",
        r"防火墙", r"waf", r"越权", r"零日", r"漏洞"
    ],
    "编译原理": [
        r"编译器", r"解释器", r"ast", r"抽象语法树", r"词法分析",
        r"语法分析", r"语义分析", r"代码生成", r"目标代码", r"优化",
        r"虚拟机", r"jit", r"正则表达式", r"有限状态自动机", r"lr\s*分析"
    ],
    "架构与工程实践": [
        r"性能", r"测试", r"可观测性", r"devops", r"cicd", r"监控",
        r"日志", r"链路追踪", r"压测", r"负载测试", r"高并发",
        r"架构设计", r"系统设计", r"技术选型", r"代码审查", r"重构"
    ],
    "AI-ML": [
        r"机器学习", r"深度学习", r"llm", r"大语言模型", r"人工智能",
        r"神经网络", r"transformer", r"bert", r"gpt", r"自然语言处理",
        r"nlp", r"计算机视觉", r"cnn", r"rnn", r"lstm", r"强化学习",
        r"模型训练", r"模型推理", r"aigc", r"chatgpt"
    ]
}

# 领域到子目录的映射
DOMAIN_TO_SUBDIR = {
    "编程语言": "20-知识库/编程语言",
    "数据结构与算法": "20-知识库/数据结构与算法",
    "操作系统": "20-知识库/操作系统",
    "计算机网络": "20-知识库/计算机网络",
    "数据库": "20-知识库/数据库",
    "中间件": "20-知识库/中间件",
    "分布式与微服务": "20-知识库/分布式与微服务",
    "云原生": "20-知识库/云原生",
    "安全": "20-知识库/安全",
    "编译原理": "20-知识库/编译原理",
    "架构与工程实践": "20-知识库/架构与工程实践",
    "AI-ML": "20-知识库/AI-ML"
}

# 编译正则表达式
COMPILED_PATTERNS = {domain: [re.compile(p, re.I) for p in patterns]
                     for domain, patterns in DOMAIN_KEYWORDS.items()}


def analyze_content(content: str) -> dict:
    """
    分析笔记内容，返回领域和子目录路径

    Args:
        content: 笔记内容

    Returns:
        dict: {domain: str, sub_path: str, confidence: float}
    """
    scores = {}

    for domain, patterns in COMPILED_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = pattern.findall(content)
            score += len(matches)
        if score > 0:
            scores[domain] = score

    if not scores:
        return {
            "domain": "未分类",
            "sub_path": "00-收集箱",
            "confidence": 0.0
        }

    # 返回得分最高的领域
    best_domain = max(scores, key=scores.get)
    max_score = scores[best_domain]
    total_score = sum(scores.values())
    confidence = max_score / total_score if total_score > 0 else 0

    return {
        "domain": best_domain,
        "sub_path": DOMAIN_TO_SUBDIR.get(best_domain, "00-收集箱"),
        "confidence": round(confidence, 2),
        "all_scores": scores
    }


def analyze_file(file_path: str) -> dict:
    """
    分析笔记文件，返回路由结果

    Args:
        file_path: 笔记文件路径

    Returns:
        dict: {domain: str, sub_path: str}
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"文件不存在: {file_path}")

    # 尝试读取 frontmatter 和正文
    content = path.read_text(encoding="utf-8")

    # 跳过 frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            content = parts[2]

    return analyze_content(content)


def analyze_title(title: str) -> Optional[str]:
    """
    根据标题快速判断领域

    Args:
        title: 笔记标题

    Returns:
        str: 领域名称，如果无法判断返回 None
    """
    for domain, patterns in COMPILED_PATTERNS.items():
        for pattern in patterns:
            if pattern.search(title):
                return domain
    return None


def get_route_suggestion(content: str, title: str = "") -> dict:
    """
    获取路由建议（综合标题和内容）

    Args:
        content: 笔记正文
        title: 笔记标题（可选）

    Returns:
        dict: {domain: str, sub_path: str}
    """
    # 优先从标题判断
    if title:
        domain_from_title = analyze_title(title)
        if domain_from_title:
            return {
                "domain": domain_from_title,
                "sub_path": DOMAIN_TO_SUBDIR.get(domain_from_title, "00-收集箱")
            }

    # 从内容分析
    return analyze_content(content)


if __name__ == "__main__":
    # 测试示例
    test_content = """
    Python 是一种高级编程语言，广泛用于 Web 开发、数据科学和机器学习。
    在分布式系统中，我们需要使用微服务架构和容器化技术。
    Docker 和 Kubernetes 是云原生应用的核心组件。
    """

    result = analyze_content(test_content)
    print(f"分析结果: {result}")
