---
type: daily-news
date: {{date}}
status: published
approved_count: {{approved_count}}
needs_verify_count: {{needs_verify_count}}
---

# 📅 {{date}} 资讯日报（入门成长版）

## ✅ 今日我批准的学习要点（{{approved_count}}）

{% for item in approved %}
{{loop.index}}) **{{item.basic_concept}}**：{{item.one_sentence}}
   - 大白话：{{item.plain_explanation}}
   - MOC：[[{{item.target_moc}}]]
   - 来源：{{item.sources_markdown}}

{% endfor %}

## ⚠️ 待核实（{{needs_verify_count}}）

{% for item in needs_verify %}
- **{{item.basic_concept}}**：{{item.title}}
  - 为什么存疑：{{item.verify_reason}}
  - 来源：{{item.sources_markdown}}

{% endfor %}

## 🧱 今日建议生成的知识卡草稿

{% for k in knowledge_drafts %}
- [[{{k.file}}|{{k.title}}]]
{% endfor %}

---

## 📈 转化追踪
- 候选包条目：{{total_candidates}}
- 批准：{{approved_count}}
- 待核实：{{needs_verify_count}}
- 拒绝：{{rejected_count}}
- 批准率：{{approval_rate}}%
