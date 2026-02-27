---
title: 长时运行 Agent 的 Harness 设计
type: concept
domain: [AI-ML]
tags: [Agent, LLM, 工程实践, 上下文管理]
source: web
created: 2026-02-23
status: done
---

## TL;DR

长时运行 Agent 的核心问题是跨上下文窗口无记忆。解决方案是用"初始化 Agent + 编码 Agent"双角色分工，配合结构化进度文件和 Git 提交，实现跨 session 的状态持久化。

---

## 背景与问题定义

每个新 session 开始时 Agent 没有任何前序记忆，导致两种典型失败：
1. 一次性尝试做太多 → 超出上下文崩溃
2. 过早宣布项目完成 → 实际功能未实现

---

## 核心机制拆解

### 双 Agent 分工

**Initializer Agent（首次 session）**
- 创建 `init.sh`：环境初始化脚本
- 创建 `claude-progress.txt`：进度追踪日志
- 建立初始 Git commit
- 生成完整功能列表（200+ 条）

**Coding Agent（后续 session）**
- 每次只做一个功能（增量）
- 完成后 commit + 更新进度文档
- 标记完成前必须做端到端测试

### Session 启动例程

每次新 session 开始时 Agent 必须：
1. 读取工作目录
2. 查看 git log
3. 读取功能列表
4. 验证基础功能可用
5. 再开始实现新功能

---

## 关键设计决策

### 功能列表用 JSON 而非 Markdown

> [!tip] 为什么用 JSON？
> 模型更不容易"不小心覆盖或修改" JSON 文件。Markdown 格式容易被 Agent 当作普通文本随意改写。

```json
{
  "features": [
    { "id": "auth-login", "status": "done", "description": "用户登录" },
    { "id": "auth-register", "status": "pending", "description": "用户注册" }
  ]
}
```

### 测试策略

- 仅验证代码语法 ≠ 测试
- 必须用浏览器自动化工具（如 Puppeteer MCP）做用户视角的端到端测试
- 需要在 prompt 中明确要求 Agent "像用户一样测试"

---

## 失败模式与对策

| 失败模式 | 对策 |
|----------|------|
| 过早宣布完成 | 维护完整功能 checklist，未全部通过不算完成 |
| 进度未记录 | 强制每个功能完成后 Git commit + 更新进度文件 |
| 功能测试不完整 | 要求端到端用户级验证，不接受仅语法检查 |
| 环境配置混乱 | 提供可执行的 `init.sh` 脚本 |

---

## 核心类比

> [!tip] 把 Agent 当作轮班工程师团队
> - 每班交接需要清晰的文档
> - 用结构化任务列表防止范围蔓延
> - 标记完成前必须通过质量门控

---

## 示例（伪代码）

```
# init.sh
git init
echo "[]" > features.json
echo "Session 1 started" > claude-progress.txt

# Coding Agent session 启动 prompt
1. 读取 features.json，找到第一个 status=pending 的功能
2. 实现该功能
3. 用 Puppeteer 做端到端测试
4. 测试通过后：更新 features.json status=done，git commit，更新 progress.txt
5. 停止，等待下一个 session
```

---

## 常见坑与边界

- Agent 倾向于"一次做完所有事"——必须在 prompt 中强制限制每次只做一个功能
- 进度文件必须在 Agent 可读路径内，且格式机器可解析
- 测试工具（Puppeteer 等）需要提前在环境中配置好，不能依赖 Agent 自行安装

---

## References

- [Effective Harnesses for Long-Running Agents - Anthropic Engineering](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
