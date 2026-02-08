# CLAUDE.md — ObsidianVault 行政命令（全领域 PARA）

工作区根目录：D:\Docs\Notes\ObsidianVault
你必须把所有读写限制在该目录内，禁止越界路径。

---

## 1) 语言
- 所有笔记中文输出（代码/术语除外）。
- 禁止空话；优先结构化、可核验、可复习。

---

## 2) PARA 目录职责

| 目录 | 用途 | 示例 |
|------|------|------|
| `00-收集箱/` | 临时摘录、未分类草稿 | 待处理输入 |
| `10-项目/` | 项目推进/设计/复盘/TODO | 求职准备、课程作业 |
| `20-知识库/` | 体系化概念（可复用、可链接、可面试） | 技术知识 |
| `30-资源/` | 外部资料与技术点沉淀（偏"素材库"） | 学习资料 |
| `40-交付物/` | 博客/PPT/可公开文档 | 博客文章 |
| `70-NotebookLM导入/` | NotebookLM 导出文件暂存 | - |
| `80-模板/` | 笔记模板 | Capture/Distill 模板 |
| `99-归档/` | 已完成或不再活跃的内容 | - |

---

## 3) 领域分类目录（全领域统一）

在 10-项目 / 20-知识库 / 30-资源 下按领域建子目录：

| 领域 | 示例子目录 |
|------|-----------|
| 编程语言 | Java, Python, Go, C++, Rust, JS-TS |
| 数据结构与算法 | - |
| 操作系统 | Linux, Windows |
| 计算机网络 | TCP, HTTP, DNS |
| 数据库 | MySQL, PostgreSQL, Redis, ES |
| 中间件 | Kafka, RabbitMQ, MQ |
| 分布式与微服务 | - |
| 云原生 | Docker, K8s, Service Mesh |
| 安全 | Web安全, 密码学, 攻防 |
| 编译原理 | - |
| 架构与工程实践 | 性能, 测试, 可观测性, DevOps |
| AI-ML | - |

若领域不确定，先放 00-收集箱，后续迁移。

---

## 4) 文件命名规范

- 日期前缀格式：`YYYY-MM-DD-标题.md`
- 技术笔记：`20-知识库/{{领域}}/{{主题}}.md`
- 面试笔记：`20-知识库/Interview/{{技术栈}}/{{主题}}.md`
- 博客文章：`40-交付物/Blog/{{主题}}.md`
- 同名冲突：`<主题> - <YYYYMMDD>.md`

---

## 5) Frontmatter 规范（强制）

```yaml
---
title: xxx
type: concept | overview | interview | project | resource
domain: [领域1, 领域2]
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

---

## 6) 笔记正文规范（必须）

每篇笔记正文必须包含：
- TL;DR（<=5 行）
- 背景与问题定义（为什么重要）
- 核心机制拆解（分步骤/流程）
- 示例（代码/配置/命令/伪代码/流程）
- 常见坑与边界
- References（逐条引用/来源）
- 【需要人工复核】（如有）

---

## 7) 去幻觉校验（必须）

- 所有事实性结论必须有来源支撑（NotebookLM 引用标识必须进入 References）。
- 没有来源：必须标记【需要人工复核】，不得当作确定事实。
- 允许推断：必须标注"推断"，并给出核验关键词。

---

## 8) Obsidian 语法规范

- 使用 `[[wikilink]]` 建立双向链接
- 使用 `> [!tip]` `> [!warning]` `> [!danger]` 创建 Callout
- 使用 Mermaid 代码块创建图表
- 引用标注格式：`^[1,2,3]`

---

## 9) 双向链接与索引（推荐）

重要概念尽量使用 [[双向链接]] 指向相关笔记。建议维护 MOC：
- 20-知识库/MOC-计算机网络.md
- 20-知识库/MOC-操作系统.md
- 20-知识库/MOC-数据库.md
- 20-知识库/MOC-分布式.md
- 20-知识库/MOC-安全.md
- 20-知识库/MOC-编译原理.md
- 20-知识库/MOC-编程语言.md
- 20-知识库/MOC-工程实践.md

---

## 10) 禁止事项

- ❌ 不要在根目录创建笔记文件
- ❌ 不要使用绝对路径的图片链接
- ❌ 不要删除 `80-模板/` 中的模板文件
- ❌ 不要在 Frontmatter 中使用中文冒号
- ❌ 不要写入任何 API Key、Cookie、隐私信息到笔记

---

## 11) 技能调用

| 技能 | 用途 |
|------|------|
| `/pkm sync <主题>` | NotebookLM → Obsidian 全领域同步 |
| `/pkm status` | 检查 NotebookLM 连接状态 |
| `/transform` | NotebookLM → Obsidian 结构化笔记 |

---

## 12) 工具选择

| 场景 | 推荐工具 |
|------|----------|
| 读写 Obsidian 笔记 | Claude Code 内置 `Read`/`Write`/`Edit` |
| 查阅 NotebookLM 资料 | NotebookLM MCP `ask_question` |
| 创建 Canvas | 内置 `Write` + JSON Canvas 格式 |
