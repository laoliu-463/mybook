#!/usr/bin/env python3
"""
质量扫描器：拦截"版本流水账" + 强制来源可追溯
"""
import json, sys, os, re, datetime
from pathlib import Path

def load_event():
    try:
        data = sys.stdin.read()
        return json.loads(data) if data.strip() else {}
    except:
        return {}

def read_file(path: Path):
    try:
        return path.read_text(encoding="utf-8")
    except:
        return ""

def main():
    event = load_event()
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    today = datetime.date.today().isoformat()

    # 查找今日候选包
    cand_path = project_dir / "00-收集箱" / "News-Inbox" / today / "00-candidate-pack.md"

    if not cand_path.exists():
        sys.exit(0)  # 候选包不存在，放行（可能还没生成）

    text = read_file(cand_path)
    if not text:
        sys.exit(0)

    # ========== 检查1：版本流水账拦截 ==========
    # 统计 /releases/tag/ 出现次数
    release_hits = len(re.findall(r"/releases/tag/", text))

    # 降低阈值：从3降到2（更严格）
    if release_hits >= 2:
        print(json.dumps({
            "decision": "block",
            "reason": f"""❌ 候选包质量不合格：疑似版本流水账

【检测结果】
- 发现 /releases/tag/ 链接数：{release_hits}（阈值：≥2）

【问题分析】
你的系统设计目标是"资讯喂养"，不是"版本更新追踪"。
资讯必须满足以下任意一条：
1. 安全事故/CVE/漏洞复盘
2. 性能回归/Bug争议/架构讨论
3. 最佳实践/踩坑案例/社区分歧
4. 可直接转化为面试题/知识卡的技术事件

【修复建议】
请改用以下来源类型：
- GitHub Issues: label:bug OR regression OR security OR performance
- GitHub Discussions: 架构争论、最佳实践讨论
- GitHub Security Advisories: severity≥moderate
- 不要抓取 /releases/ 页面，除非作为"证据链接"

【下一步】
删除当前候选包，重新抓取符合"资讯标准"的来源。
"""
        }, ensure_ascii=False))
        sys.exit(2)

    # ========== 检查2：来源可追溯性 ==========
    # 提取所有事件标题（### 事件 N:）
    events = re.findall(r"### 事件 \d+[：:](.*?)\n", text)

    # 粗略检查：每个事件段落是否包含URL
    sections = re.split(r"\n### 事件 \d+[：:]", text)
    missing_source = []

    for i, section in enumerate(sections[1:], 1):
        # 检查该段落是否有 http:// 或 https://
        if "http://" not in section and "https://" not in section:
            title = events[i-1] if i <= len(events) else f"事件{i}"
            missing_source.append(title.strip())

    if missing_source:
        print(json.dumps({
            "decision": "block",
            "reason": f"""❌ 候选包质量不合格：缺少来源链接

【检测结果】
以下事件缺少可追溯的来源URL：
{chr(10).join(f"- {title}" for title in missing_source[:10])}

【修复建议】
每条事件必须包含至少1个来源链接（github.com / youtube.com / huggingface.co）
如果来源中没有提供细节，必须标注"【推测】"或"【需人工确认】"

【反幻觉约束】
- 禁止脑补事实
- 禁止注入常识扩写
- 所有推断必须有依据并明确标注
"""
        }, ensure_ascii=False))
        sys.exit(2)

    # ========== 检查3：知识喂养结构完整性 ==========
    # 检查是否包含"基础概念映射"相关字段
    has_basic_concept = bool(re.search(r"基础概念|basic_concept|概念映射", text, re.I))
    has_plain_explanation = bool(re.search(r"大白话|plain_explanation|通俗解释", text, re.I))

    if not (has_basic_concept and has_plain_explanation):
        print(json.dumps({
            "decision": "block",
            "reason": f"""⚠️ 候选包缺少知识喂养结构

【检测结果】
- 基础概念映射：{'✅' if has_basic_concept else '❌'}
- 大白话解释：{'✅' if has_plain_explanation else '❌'}

【要求】
每条事件必须包含：
1. basic_concept：映射到基础概念（thread/cache/index/transaction/jvm等）
2. plain_explanation：大白话比喻（比如：缓存=便利贴、索引=目录）
3. why_matters：为什么要懂（挂钩到hmdp项目或面试场景）

【修复】
重新生成候选包时，强制按模板填充这3个字段。
"""
        }, ensure_ascii=False))
        sys.exit(2)

    # 所有检查通过
    sys.exit(0)

if __name__ == "__main__":
    main()
