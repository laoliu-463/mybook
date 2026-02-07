# Obsidian Vault 规范 (CLAUDE.md)

本文件定义 Claude Code 在此 Vault 中的行为规范。

## PARA 目录结构

| 目录 | 用途 | 示例 |
|------|------|------|
| `00-收集箱/` | 待处理的原始输入 | 临时笔记、语音转写 |
| `10-项目/` | 有明确截止日期的项目 | 求职准备、课程作业 |
| `20-领域/` | 持续关注的责任领域 | 健康、财务、职业发展 |
| `30-资源/` | 可复用的知识资产 | 技术笔记、学习资料 |
| `40-交付物/` | 可发布的输出成果 | 博客文章、PPT、面试回答 |
| `70-NotebookLM导入/` | NotebookLM 导出文件暂存 | - |
| `80-模板/` | 笔记模板 | Capture/Distill 模板 |
| `99-归档/` | 已完成或不再活跃的内容 | - |

## 文件命名规范

- 日期前缀格式：`YYYY-MM-DD-标题.md`
- 技术笔记：`30-资源/{{技术栈}}/{{主题}}.md`
- 面试笔记：`30-资源/Interview/{{技术栈}}/{{主题}}.md`
- 博客文章：`40-交付物/Blog/{{主题}}.md`

## Frontmatter 规范（必须）

```yaml
---
title: 笔记标题
type: concept | overview | interview | blog | capture
tags: [标签1, 标签2]
source: notebooklm | web | book | voice
created: YYYY-MM-DD
status: draft | review | done
---
```

### 可选字段（复习系统）

```yaml
next_review: YYYY-MM-DD
interval: 1
ease: 2.5
reps: 0
```

## 写入规则

1. **新捕获内容** → 默认放入 `00-收集箱/`
2. **技术笔记** → 按技术栈分类到 `30-资源/{{技术栈}}/`
3. **面试材料** → 放入 `30-资源/Interview/`
4. **可发布内容** → 放入 `40-交付物/`
5. **目录不存在时** → 自动创建

## Obsidian 语法规范

- 使用 `[[wikilink]]` 建立双向链接
- 使用 `> [!tip]` `> [!warning]` `> [!danger]` 创建 Callout
- 使用 Mermaid 代码块创建图表
- 引用标注格式：`^[1,2,3]`

## 禁止事项

- ❌ 不要在根目录创建笔记文件
- ❌ 不要使用绝对路径的图片链接
- ❌ 不要删除 `80-模板/` 中的模板文件
- ❌ 不要在 Frontmatter 中使用中文冒号

## 技能调用

| 技能 | 用途 |
|------|------|
| `/sb-capture` | 抓取输入到收集箱 |
| `/sb-organize` | 整理收集箱到 PARA |
| `/sb-distill` | 提取核心洞见 |
| `/sb-express` | 转化为交付物 |
| `/sb-visualize` | 生成 Canvas 可视化 |
| `/transform` | NotebookLM → Obsidian 结构化笔记 |

## 工具选择

| 场景 | 推荐工具 |
|------|----------|
| 读写 Obsidian 笔记 | Claude Code 内置 `Read`/`Write`/`Edit` |
| 查阅 NotebookLM 资料 | NotebookLM MCP `ask_question` |
| 创建 Canvas | 内置 `Write` + JSON Canvas 格式 |
