---
title: Agent - 长时运行 Agent 的 Harness 设计
aliases:
  - Agent 状态持久化
  - 上下文管理
tags:
  - AI-ML
  - AI-ML/Agent
  - 工程实践
type: note
domain: AI-ML
topic: Agent
question: 长时运行 Agent 如何设计 Harness
source:
source_title:
created: 2026-02-23
updated: 2026-02-23
status: evergreen
---

# Agent - 长时运行 Agent 的 Harness 设计

## 一句话结论
长时运行 Agent 的核心问题是跨上下文窗口无记忆，解决方案是双 Agent 分工（Initializer + Coding）配合 Git 提交和进度文件实现状态持久化。

## 标准回答
- **问题**：每个新 session Agent 没有前序记忆
- **失败模式**：一次性做太多超出上下文 / 过早宣布完成
- **方案**：双 Agent 分工 + 结构化进度文件 + Git 提交

## 为什么
Claude Code 等 Agent 基于上下文窗口运行，无法记住跨 session 的信息。需要外部存储实现：
- 进度追踪
- 上下文恢复
- 增量开发

## 双 Agent 分工
| Agent | 职责 | 产出 |
|---|---|---|
| Initializer | 首次 session | init.sh、进度文件、Git commit |
| Coding | 后续 session | 增量功能、测试、commit |

### Initializer 工作
- 创建 `init.sh`：环境初始化脚本
- 创建 `claude-progress.txt`：进度追踪日志
- 建立初始 Git commit
- 生成完整功能列表

### Coding Agent 工作
- 每次只做一个功能（增量）
- 完成后 commit + 更新进度文档
- 标记完成前必须做端到端测试

## Session 启动例程
```bash
# 1. 读取进度文件
cat claude-progress.txt

# 2. 读取功能列表
cat 功能清单.json

# 3. 选择下一个功能
# 4. 实现并测试
# 5. 提交并更新进度
```

## 易错点
- 不要一次做太多功能
- 每次 commit 要有清晰 message
- 进度文件要及时更新
- 端到端测试是必须的

## 延伸链接
- [[Claude - 使用技巧]]
- [[Git - 工作流]]

## 参考来源
