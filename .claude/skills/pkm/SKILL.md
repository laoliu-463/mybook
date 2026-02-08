---
name: pkm
description: 全领域 PKM 同步专家：从 NotebookLM 提取带引用洞见，执行去幻觉校验，并按 PARA + 领域分类写入 Obsidian Vault（中文、可追溯、可复习）。
---

# /pkm — 全领域同步助手（NotebookLM → Obsidian）

## 支持范围
覆盖计算机所有领域：编程语言/数据结构/算法/OS/网络/数据库/中间件/分布式/云原生/安全/AI/编译原理/架构/工程实践/测试/运维/产品技术等。

## 命令
- /pkm sync <主题> [可选: 类型=concept|overview|interview|project|resource] [可选: 输出=相对路径]
- /pkm status

---

## 全局硬约束（必须遵守）
1) 全中文输出（代码/术语除外）
2) 所有关键结论必须能追溯到 NotebookLM 引用；否则标记【需要人工复核】
3) 禁止"百科式编造"；允许推断但必须标注"推断"并给核验关键词
4) 写入范围仅限 Vault（由 CLAUDE.md 定义），禁止越界路径

---

## /pkm sync 工作流（严格顺序）

### Step A: 健康检查与认证
- 调用 mcp__notebooklm__get_health
- 若 Authenticated=false：提示用户执行 notebooklm.auth-setup，认证后再次 get_health，直到 true

### Step B: 绑定 Notebook
- 调用 mcp__notebooklm__list_notebooks
- 若没有 active notebook：要求用户指定 notebook_id，并调用 mcp__notebooklm__select_notebook
- 若用户提供 notebook_url：ask_question 中使用 notebook_url 覆盖

### Step C: 拉取带引用材料（统一提问模板）
调用 mcp__notebooklm__ask_question，question 必须要求 NotebookLM 输出以下结构：
1) 领域判定（最多 3 个）：如 [网络, 分布式] / [操作系统] / [安全] 等
2) 产物类型建议：concept/overview/interview/project/resource
3) 8~12 条要点（定义/机制/工程场景/常见坑/对比）
4) 每条要点都附引用/来源标识
5) 1~2 个示例（代码/配置/命令/伪代码/数据流程），若不适用则明确写"不适用"
6) 术语表（5~15 个）
7) 进一步检索关键词（5 个）

### Step D: 去幻觉校验（A/B/C 分级）
对每条要点做可信度标注：
- A：引用明确且支撑结论
- B：有引用但表述需澄清（补充解释/边界）
- C：无引用或引用不足 → 标记【需要人工复核】+ 核验关键词

### Step E: 自动分类与落盘路径（领域无关）
根据"领域 + 产物类型"决定路径：

1) type=project → `10-项目/<领域>/<主题>.md`
2) type=concept/overview/interview → `20-知识库/<领域>/<主题>.md`
3) type=resource → `30-资源/<领域>/<主题>.md`
4) 无法判定 → `00-收集箱/<主题>.md`

领域目录规范（示例，不限于此）：
- 编程语言、Java、Python、Go、C++、Rust、JS/TS
- 数据结构与算法
- 操作系统
- 计算机网络
- 数据库（MySQL/PostgreSQL/Redis/ES）
- 中间件（MQ/Kafka/RabbitMQ）
- 分布式与微服务
- 云原生（Docker/K8s/Service Mesh）
- 安全（Web/应用/密码学/攻防）
- 编译原理
- 架构与工程实践（性能/测试/可观测性/DevOps）
- AI/ML（如需要）

文件名冲突规则：
- 同名冲突：`<主题> - <YYYYMMDD>.md`

### Step F: 生成 Obsidian 笔记（全领域统一模板）
必须生成 Markdown（含 YAML frontmatter）：

Frontmatter 必须包含：
- title, type, tags, source:[notebooklm], created, status:draft
- domain: [领域列表]
- notebooklm: notebook_id 或 notebook_url

正文必须包含：
- TL;DR（<=5 行）
- 背景与问题定义（为什么重要）
- 核心机制拆解（分步骤/流程）
- 关键要点（带 A/B/C 标注）
- 示例（代码/配置/命令/伪代码/流程图）
- 常见坑与边界
- 面试追问（当 type=interview 或主题偏八股）
- References（逐条引用）
- 【需要人工复核】清单（若有）

### Step G: 写入与回读自检
- 写入文件（创建或覆盖更新）
- 回读校验：frontmatter 存在 + References 非空（除非全部复核）

### Step H: 输出
返回保存路径 + 3~5 条 TODO + 复核清单（含关键词）
