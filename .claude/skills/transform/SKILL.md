---
name: transform
description: 从 NotebookLM 抽取带引用的材料，转写为 Obsidian 结构化笔记，自动归档到 PARA 目录。零幻觉、可追溯。
invocation: user
---

# /transform - NotebookLM → Obsidian 知识转化

你正在执行 /transform 技能。

## 核心原则（强制）

1. **零幻觉**：所有事实性内容必须来自 NotebookLM 返回的带引用材料
2. **可追溯**：每条关键结论标注来源引用
3. **落盘优先**：必须写入 Obsidian 文件，禁止只在对话中给文本
4. **不确定标注**：无法确认的信息标注 [待核验]

## 输入格式

/transform <主题>
--type <类型>        # overview | concept | interview | blog（默认 concept）
--to <输出路径>      # 可选，默认按 PARA 自动归档
--tags <标签>        # 可选，逗号分隔
--notebook <链接>    # 可选，指定 NotebookLM 链接

### 示例

/transform Spring AOP 原理
/transform Redis 持久化 --type interview --tags redis,八股
/transform 分布式事务 --type overview --notebook https://notebooklm.google.com/xxx

## 执行流程（严格按顺序）

### Step 1：从 NotebookLM 抽取材料

调用 NotebookLM MCP 工具查询，要求返回：
- 核心定义（1-2句话）
- 关键要点（3-5条，带引用）
- 代码示例（如有）
- 常见误区/易错点
- 每条结论带来源标识

**若 NotebookLM 返回"找不到相关信息"**：
- 立即停止
- 建议用户：1) 换关键词 2) 确认 Notebook 已包含相关文档

### Step 2：生成 Obsidian 笔记

#### Frontmatter（必须）

---
title: {{主题}}
type: {{overview|concept|interview|blog}}
tags: [{{用户标签}}, notebooklm]
source: notebooklm
created: {{YYYY-MM-DD}}
status: draft
next_review: {{YYYY-MM-DD}}
interval: 1
ease: 2.5
reps: 0
---

#### 正文结构（按类型）

**A) concept（默认）** - 单点深挖，含定义、要点、代码、常见坑、面试角度、知识网络、引用

**B) overview** - 全局视野，含 TL;DR、Mermaid 知识地图、概念清单、面试问法

**C) interview** - 八股考点，含高频考点、30秒答案、深入解释、追问预判、速记口诀

**D) blog** - 可发布文章，含引子、正文章节、总结、行动清单

### Step 3：确定输出路径（PARA 归档）

| 类型 | 默认路径 |
|------|----------|
| concept | 30-资源/{{技术栈}}/{{主题}}.md |
| overview | 30-资源/{{技术栈}}/{{主题}}-概览.md |
| interview | 30-资源/Interview/{{技术栈}}/{{主题}}.md |
| blog | 40-交付物/Blog/{{主题}}.md |

### Step 4：写入文件

1. 检查目标路径是否存在同名文件（存在则询问）
2. 写入文件内容
3. 读取验证：Frontmatter 可解析、标题层级正确、引用区存在

### Step 5：后续建议

输出完成后给出：
- 用 /sb-visualize 生成 Canvas
- 检查知识网络链接，用 /concept 补充
- 用 /review 安排复习

## 终端输出（简短）

✅ 已转化：{{主题}} → {{输出路径}}
📚 来源：NotebookLM（{{N}} 条引用）
🔗 知识网络：{{M}} 个关联概念

## 错误处理

| 情况 | 处理 |
|------|------|
| NotebookLM 未登录 | 提示：请先运行 Log me in to NotebookLM |
| 找不到相关材料 | 停止并建议换关键词 |
| 目标目录不存在 | 自动创建目录 |
| 同名文件存在 | 询问：覆盖 / 新版本 / 取消 |

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| /sb-capture | transform 是升级版，从 NotebookLM 抽取 |
| /concept | 生成的笔记格式兼容 |
| /sb-distill | 已内置 distill 逻辑 |
| /sb-visualize | 建议后续调用生成 Canvas |
| /review | 笔记含复习元数据，可直接复习 |
