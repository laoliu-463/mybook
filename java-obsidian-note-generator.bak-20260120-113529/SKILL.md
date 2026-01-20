---
name: java-obsidian-note-generator
description: Generate interview-focused Obsidian-ready Java knowledge notes when the user asks to整理知识点/生成Obsidian笔记/八股笔记/面试笔记 for a topic (e.g., HashMap, 线程池, JVM GC); use for structured Java interview note output with mindmap, comparisons, code example, pitfalls, and follow-up questions.
---

# Java 面试八股 · Obsidian 笔记生成器

Follow this workflow to produce a single Obsidian-ready Markdown note for the user-provided topic.

## Gather input

If the user did not provide a topic, ask once: “要整理的知识点关键词是什么？例如 HashMap / 线程池 / JVM GC。”

## Output requirements (must follow in order)

1) YAML Frontmatter
- Include: `tags` (must include `java`, `八股`, `{topic}`), `aliases` (at least 2), `date` (today), `status` (`draft` or `done`).

2) Title
- `# Java 八股｜{topic}`

3) Mermaid mindmap
- Structure: 底层原理 → 核心特性 → 高频面试题 → 追问链路

4) 核心概念
- Bullet list, precise terms, short sentences, no filler words.

5) 源码/机制复盘（文字流程）
- Explain the mechanism step-by-step; do not paste large source code.

6) 对比表（至少 1 张）
- Focus on interview-relevant comparisons.

7) 可运行 Java 示例（单文件）
- Provide a complete `public class` with `main`.
- Explain critical lines: why written this way, what happens under the hood, and common mistakes.

8) 面试专栏
- ✅ 面试怎么问 (typical question prompts)
- ⚠️ 坑点/误区 (at least 3)
- 追问链路 (at least 5, escalating depth)

9) 一分钟背诵版
- 10–15 short lines suitable for memorization.

10) 面试 Checklist
- Use `- [ ]` checkboxes.

## Obsidian linking

Insert 3–8 `[[相关知识点]]` backlinks, relevant to the topic.

## Style

Be structured, interview-oriented, and conclusion-first. Keep the note concise but complete.
