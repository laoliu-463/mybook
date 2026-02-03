#!/usr/bin/env python3
"""
会话启动提醒：每次开始时重申news-educator规则
"""
import sys

REMINDER = """
═══════════════════════════════════════════════════════════════
📋 news-educator 系统规则（每次会话必读）
═══════════════════════════════════════════════════════════════

🔒 白名单约束（硬性）
  仅允许来源：github.com / youtube.com / huggingface.co
  任何其他域名一律拒绝

📰 资讯定义（非版本更新）
  资讯 = 满足以下任意一条：
  ✓ 安全事故/CVE/漏洞/供应链问题
  ✓ 性能回归/严重Bug/架构争议
  ✓ 最佳实践/踩坑案例/社区分歧
  ✓ 可转化为面试题/知识卡的技术事件

  ✗ 不是资讯：
    - 纯版本号发布（/releases/tag/）
    - 无实质内容的changelog
    - 营销/炒作/流水账

🚪 Gate流程（强制）
  Gate0: 生成候选包 → 写入 News-Inbox
  Gate1: 人工Review → 必须勾选 approve/skip/needs-verify
  Gate2: 发布 → 仅发布 approve 内容

  ⚠️ 未完成 Gate1 Review 禁止发布

🎯 知识喂养结构（必填）
  每条事件必须包含：
  - basic_concept: 映射到基础概念（thread/cache/index/transaction...）
  - plain_explanation: 大白话比喻（缓存=便利贴、索引=目录）
  - why_matters: 为什么要懂（挂钩hmdp项目/面试场景）

🚫 反幻觉约束
  - 事实仅来自来源标题/摘要/正文可引用片段
  - 任何推断必须标注【推测】
  - 来源未提供信息 → 明确写"尚不明确（来源未提供）"
  - 禁止注入常识扩写、禁止脑补细节

═══════════════════════════════════════════════════════════════
"""

def main():
    print(REMINDER, file=sys.stderr)
    sys.exit(0)

if __name__ == "__main__":
    main()
