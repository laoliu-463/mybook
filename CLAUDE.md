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
title: Java - 静态方法和实例方法有什么不同
aliases:
  - 静态方法和实例方法区别
tags:
  - Java
  - Java/基础
  - 面试题
type: note
domain: java
topic: 基础
question: 静态方法和实例方法有什么不同
source: https://javaguide.cn/java/basis/...
source_title: Java基础常见面试题总结(上)
source_section: 基础概念与常识
created: 2026-03-16
updated: 2026-03-16
status: evergreen
---
```

### 必填字段

- `title`：笔记标题，格式：`领域 - 问题`
- `tags`：分类标签，格式：`领域/子主题`
- `type`：固定为 `note`
- `domain`：技术领域，如 `java`、`python`、`网络`
- `topic`：子主题，如 `基础`、`集合`、`并发`
- `question`：当前笔记回答的问题（一句话）
- `created`：创建日期
- `updated`：更新日期
- `status`：`evergreen`（常青笔记）

### 可选字段

- `aliases`：便于搜索的别名
- `source`：原文链接
- `source_title`：原文标题
- `source_section`：原文大章节名

---

## 6) 笔记正文规范（技术类笔记模板）

### 一篇笔记只讲一个问题

- 标题格式：`领域 - 问题`
- 示例：
  - `Java - 静态方法和实例方法有什么不同`
  - `Java - ArrayList 和 LinkedList 有什么区别`
  - `Java 并发 - synchronized 和 ReentrantLock 有什么区别`

### 正文固定结构

```md
# {{title}}

## 一句话结论
用 1 到 2 句话直接回答问题。

## 标准回答
- 点 1
- 点 2
- 点 3
- 点 4

## 为什么
解释底层原因、设计逻辑或适用场景。

## 对比
| 维度 | A | B |
|---|---|---|
| 定义 |  |  |
| 调用方式 |  |  |
| 使用场景 |  |  |

## 代码示例
```java
// 示例标题：说明这段代码要展示什么
class Example {
    // 这里写关键成员
}
````

### 代码说明
* 这段代码演示了什么
* 哪一行体现了核心知识点

## 易错点
* 易错点 1
* 易错点 2

## 延伸链接
* [[相关知识点1]]
* [[相关知识点2]]

## 参考来源
* 原文：xxx
* 补充资料：xxx
```

### 必须包含的部分

- ✅ 一句话结论
- ✅ 标准回答
- ✅ 为什么
- ✅ 易错点（技术笔记必备）
- ✅ 参考来源

### 代码示例规范

- 代码控制在 10–25 行
- 代码块内必须有**行内注释**
- 代码块外必须有**代码说明**
- 示例只展示一个知识点

### 对比类问题规范

标题含以下关键词必须加对比表格：
- 区别 / 不同 / 对比 / compare

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

---

## 13) 自动化处理规则（Anthropic Harness）

### 开发态 vs 运行态

- **开发态循环**：增强系统能力，修改 `系统/功能清单.json`
- **运行态循环**：处理笔记，修改 `系统/处理队列.json`

### 自动化约束

- **只处理 `00-收集箱/`** 目录下的笔记
- **每次最多处理 1-3 篇**
- **处理前先读取状态**：`系统/运行进度.md` 和 `系统/处理队列.json`
- **处理后必须更新状态**
- **不允许删除笔记**
- **不允许批量修改历史笔记正文**

### 启动命令

```bash
/process-inbox scan       # 扫描收件箱
/process-inbox process   # 处理笔记
/process-inbox status    # 查看状态
/process-inbox verify   # E2E 验证
```

### 状态文件

| 文件 | 用途 |
|------|------|
| `系统/功能清单.json` | 系统能力清单（开发态） |
| `系统/处理队列.json` | 待处理笔记队列（运行态） |
| `系统/运行进度.md` | 运行进度日志 |
| `系统/运行日志.md` | 执行审计日志 |

### 子代理路由规则

| 关键词 | 路由到 |
|--------|--------|
| Abstract / Introduction / Conclusion / DOI / arXiv | process-paper |
| def / import / 代码块 / function / class | process-code-snippet |
| 会议 / Agenda / Action Item / TODO | process-meeting-notes |
