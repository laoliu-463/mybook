---
type: candidate-pack
date: {{date}}
window_hours: {{window_hours}}
sources: [github, youtube, huggingface]
status: gate0_waiting_review
---

# 🐣 今日知识喂养包（{{date}}）

> [!note] 规则
> 你只需要关心：这条信息帮我理解哪个"基础概念"。

---

{% for item in items %}
## 🟢 知识点：{{item.basic_concept}}
- **标题**：{{item.title}}
- **发生了什么（只复述来源）**：{{item.what_happened}}
- **为什么我要懂这个（可含【推测】）**：{{item.why_it_matters}}
- **大白话解释**：
  > {{item.plain_explanation}}
- **建议挂载**：[[{{item.target_moc}}]]
- **来源**：
{{item.sources_markdown}}

### Review（Gate1）
- [ ] approve
- [ ] skip
- [ ] needs-verify

---
{% endfor %}

## 📊 统计
- 抓取条数：{{total_fetched}}
- 去重后：{{after_dedup}}
- 本次候选：{{candidate_count}}
