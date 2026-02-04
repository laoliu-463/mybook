---
type: candidate-pack
date: {{date}}
status: 待Review
gate: 0
sources: [GitHub, YouTube, HuggingFace]
---

# 📦 候选包 - {{date}}（0基础入门版）

> [!rule] 必读规则
> 只看"能让我学会一个基础点"的内容；看不懂就 skip；不确定就 needs-verify。

---

{% for item in items %}
## 🟢 基础点：{{item.basic_concept}}

- **一句话白话**：{{item.plain_one_liner}}
- **生活类比**：像 {{item.analogy}} 一样
- **新手今天只学这个**：{{item.learn_one_point}}
- **术语表**：
{% for t in item.terms %}
  - {{t.term}}：{{t.explain}}
{% endfor %}

### ✅ 事实（必须带来源）
- {{item.fact_1}} [Source]({{item.url}})
- {{item.fact_2}} [Source]({{item.url}})

### 📌 原文摘录（1~2句）
> {{item.excerpt}}
> [Source]({{item.url}})

### 🧭 归档建议（严格中文目录）
- **建议挂载**：[[{{item.target_moc}}]]

### Gate1 Review（你来勾选）
- [ ] approve
- [ ] skip
- [ ] needs-verify

---
{% endfor %}
