---
title: Claude Agent Team 使用指南
type: overview
domain: [AI-ML]
tags: [Claude, Agent, AI, 协作]
source: web
created: 2026-02-24
status: draft
---

## TL;DR

Claude Agent Team 是 Claude Code 的实验性功能,允许多个 AI Agent 协作完成复杂任务。通过设置环境变量启用,使用 Task 工具创建专门化的子 Agent,实现并行处理和任务分工。

---

## 背景与问题定义

在处理复杂软件工程任务时,单个 Agent 可能面临:
- 上下文窗口限制
- 任务复杂度过高
- 需要并行处理多个独立子任务
- 需要专门化能力(如代码探索、测试、构建验证等)

Agent Team 通过任务分解和专门化 Agent 协作解决这些问题。

---

## 核心机制

### 1. 启用 Agent Teams

**Windows PowerShell:**
```powershell
$env:CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS = "1"
```

**Windows CMD:**
```cmd
set CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

**Linux/macOS:**
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

### 2. 可用的专门化 Agent 类型

| Agent 类型 | 用途 | 可用工具 |
|-----------|------|---------|
| `Bash` | 命令执行专家 | Bash |
| `general-purpose` | 通用任务处理 | 所有工具 |
| `Explore` | 代码库探索(快速) | 除 Task/Edit/Write 外所有 |
| `Plan` | 实现方案设计 | 除 Task/Edit/Write 外所有 |
| `statusline-setup` | 状态栏配置 | Read, Edit |

### 3. 使用 Task 工具创建子 Agent

**基本语法:**
```python
Task(
    subagent_type="Explore",
    description="探索认证模块",  # 3-5 词简短描述
    prompt="找到所有与用户认证相关的文件、函数和配置",
    model="haiku"  # 可选: haiku(快速便宜) | sonnet(默认) | opus(复杂任务)
)
```

### 4. 并行 vs 串行执行

**并行执行(单个消息多个 Task):**
适用于独立任务,无依赖关系
```
用户请求: "分析前后端架构"
→ 同时启动 2 个 Explore Agent:
  - Agent A: 探索前端 React 组件
  - Agent B: 探索后端 API 路由
```

**串行执行(等待结果后再调用):**
适用于有依赖的任务
```
1. Explore Agent 找到配置文件路径
2. 等待结果
3. 根据路径用 Read 工具读取内容
```

### 5. 后台运行

```python
Task(
    subagent_type="general-purpose",
    description="运行完整测试套件",
    prompt="执行所有单元测试和集成测试",
    run_in_background=True  # 后台运行,不阻塞主 Agent
)
```

后台任务返回 `output_file` 路径,可用 `Read` 或 `Bash tail` 查看进度。

### 6. Agent 恢复(Resume)

```python
# 首次调用返回 agent_id
result = Task(subagent_type="Explore", ...)
# agent_id: "abc123"

# 后续可恢复该 Agent 继续工作
Task(
    resume="abc123",  # 使用之前的 agent_id
    prompt="基于之前的探索,现在分析错误处理逻辑"
)
```

---

## 示例场景

### 场景 1: 代码库探索

```python
# 用户: "这个项目的认证是怎么实现的?"

# 主 Agent 调用:
Task(
    subagent_type="Explore",
    description="探索认证实现",
    prompt="""
    探索代码库中的用户认证实现:
    1. 找到认证相关的文件(login, auth, session)
    2. 识别使用的认证方案(JWT/Session/OAuth)
    3. 找到中间件和路由保护逻辑
    thoroughness: medium
    """
)
```

### 场景 2: 并行多领域探索

```python
# 用户: "分析这个微服务的架构"

# 并行启动 3 个 Agent:
Task(subagent_type="Explore", description="探索 API 层",
     prompt="找到所有 REST/GraphQL 端点定义")
Task(subagent_type="Explore", description="探索数据层",
     prompt="分析数据库模型和 ORM 配置")
Task(subagent_type="Explore", description="探索配置",
     prompt="找到环境变量、配置文件和密钥管理")
```

### 场景 3: 计划-执行模式

```python
# 步骤 1: 用 Plan Agent 设计方案
Task(
    subagent_type="Plan",
    description="设计重构方案",
    prompt="设计将认证从 Session 迁移到 JWT 的实现计划"
)

# 步骤 2: 用户审批计划后,主 Agent 执行实现
# (Plan Agent 不能写代码,只能设计)
```

---

## 常见坑与边界

### 1. 何时使用 Explore Agent vs 直接 Grep/Glob

| 场景 | 推荐工具 |
|------|---------|
| 明确知道文件名/类名 | 直接用 `Glob` 或 `Grep` |
| 开放式探索("找到所有认证相关代码") | 用 `Explore` Agent |
| 需要 3+ 轮搜索才能定位 | 用 `Explore` Agent |

### 2. 避免重复工作

❌ **错误示例:**
```python
# 主 Agent 和子 Agent 都在搜索同一内容
Grep(pattern="authentication")  # 主 Agent 搜索
Task(subagent_type="Explore", prompt="找认证代码")  # 子 Agent 也搜索
```

✅ **正确做法:**
```python
# 委托给子 Agent,主 Agent 等待结果
Task(subagent_type="Explore", prompt="找认证代码")
```

### 3. 上下文隔离

- 子 Agent 可以看到调用前的完整对话历史
- 子 Agent 的工作结果会返回给主 Agent
- 子 Agent 之间**不共享**上下文

### 4. 成本优化

```python
# 简单任务用 haiku(便宜快速)
Task(subagent_type="Explore", model="haiku",
     prompt="找到 package.json 文件")

# 复杂任务用 sonnet(默认)或 opus
Task(subagent_type="Plan", model="opus",
     prompt="设计分布式事务处理方案")
```

### 5. 工具限制

| Agent 类型 | 不能使用的工具 |
|-----------|---------------|
| Explore | Task, Edit, Write, NotebookEdit |
| Plan | Task, Edit, Write, NotebookEdit |
| Bash | 只能用 Bash |

---

## 最佳实践

### 1. 清晰的任务描述

```python
# ❌ 模糊
Task(subagent_type="Explore", description="看看代码",
     prompt="帮我看看")

# ✅ 清晰
Task(subagent_type="Explore", description="探索 API 路由",
     prompt="找到所有 Express 路由定义,列出端点、HTTP 方法和处理函数")
```

### 2. 指定探索深度

```python
Task(
    subagent_type="Explore",
    prompt="""
    探索缓存实现
    thoroughness: quick  # quick | medium | very thorough
    """
)
```

### 3. 任务分解原则

- 每个子 Agent 负责一个明确的子领域
- 独立任务并行执行
- 有依赖的任务串行执行
- 避免过度分解(通信开销)

### 4. 检查 Agent 状态

```python
# 查看后台任务输出
TaskOutput(task_id="abc123", block=False)  # 非阻塞检查

# 停止失控的后台任务
TaskStop(task_id="abc123")
```

---

## References

- Claude Code 官方文档: https://github.com/anthropics/claude-code
- Task 工具定义(系统提示词)
- Agent Teams 实验性功能说明

---

## 【需要人工复核】

- Agent Teams 的具体性能指标(并行加速比、成本对比)
- 不同 Agent 类型的详细工具列表(需查阅最新文档)
- 最大并行 Agent 数量限制
- Agent 间通信机制的底层实现
