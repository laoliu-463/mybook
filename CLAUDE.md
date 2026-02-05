# Java 全栈学习 PKM 系统

## 系统概述
这是一个专为 Java 全栈学习（后端 Java + 前端 Vue3）设计的个人知识管理系统。

## 目录结构
```
ObsidianVault/
├── 00-Inbox/              # 入口（含 NotebookLM/ 子目录）
├── 10-Learn/              # 学知识（按技术栈组织）
├── 20-Build/              # 做项目（进行中的实战）
├── 30-Interview/          # 备面试（题库+八股）
├── 40-Output/             # 输出端（博客/复盘）
├── 80-Templates/          # 模板库
└── 99-Archive/            # 归档区
```

## 可用指令

### /capture - 采集器
从 NotebookLM 或网页采集内容，生成结构化摘要并建议归档路径。
- 输入：粘贴文本/链接
- 输出：结构化笔记 + 路由建议
- 保存到：`00-Inbox/`

### /concept - 概念笔记
整理技术概念为标准化笔记。
- 输入：概念名称（如 "Spring IoC"）
- 输出：定义 + 要点 + 代码 + 常见坑
- 保存到：`10-Learn/{{技术栈}}/`

### /project-log - 项目日志
记录每日开发日志。
- 输入：项目名 + 今日工作
- 输出：完成项 + 踩坑 + 明日计划
- 保存到：`20-Build/{{项目名}}/`

### /interview-card - 面试题卡
生成面试题卡片。
- 输入：主题 + 难度
- 输出：Q&A + 追问预判
- 保存到：`30-Interview/{{技术栈}}/`

### /weekly-review - 周复盘
生成周复盘报告。
- 输入：周次
- 输出：进度表格 + 下周计划
- 保存到：`40-Output/Weekly/`

### /quick-lookup - 快速查询
快速查询技术问题。
- 输入：具体问题
- 输出：直接答案（不生成文件）

## 技术栈
- **后端**: Java SE, Spring, MyBatis, Redis
- **前端**: Vue3, TypeScript
- **数据库**: MySQL
- **工程化**: DevOps, Docker, Git

## 工作流
```
NotebookLM → 00-Inbox → /capture
                ↓
    ┌───────────┼───────────┐
    ↓           ↓           ↓
10-Learn    20-Build   30-Interview
/concept   /project-log /interview-card
    └───────────┼───────────┘
                ↓
          /weekly-review
                ↓
           40-Output
```

## 写作规范
1. 代码示例：后端用 Java，前端用 TypeScript/Vue
2. 文件命名：小写+连字符，如 `spring-ioc.md`
3. 标签规范：技术栈标签 + 类型标签（concept/interview/project-log）
4. 链接使用 Obsidian 双链语法 `[[]]`

## 模板位置
- `80-Templates/tpl-concept.md`
- `80-Templates/tpl-project-log.md`
- `80-Templates/tpl-interview-card.md`
- `80-Templates/tpl-weekly-review.md`
- `80-Templates/tpl-project-board.md`
