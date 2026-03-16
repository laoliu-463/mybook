# CLAUDE.md

工作区根目录：`D:\Docs\Notes\ObsidianVault`

所有读写必须限制在当前仓库内。禁止越界路径、禁止删除笔记、禁止批量改写历史正文。

## 1. 输出约束

- 默认中文输出，代码、命令、路径保留原文。
- 优先给出可执行结果、明确结论和可核验信息。
- 讨论自动化时，区分“开发态 harness”与“运行态 pipeline”。

## 2. 当前目录约定

| 路径 | 用途 |
|---|---|
| `00-收集箱/` | 自动化唯一默认输入目录 |
| `10-项目/` | 项目类笔记与行动项 |
| `20-知识库/` | 技术知识、概念总结、结构化问答笔记 |
| `30-资源/` | 资料、论文、课程、素材 |
| `40-交付物/` | 可发布内容、图表、交付稿 |
| `70-NotebookLM提示词使用/` | NotebookLM 相关资料与提示词 |
| `80-模板/` | 模板目录，禁止删除 |
| `99-归档/` | 归档内容，禁止自动批量改写 |
| `系统/` | 状态文件、schema、规范文档、日志、测试样例 |
| `脚本/` | Python/PowerShell 自动化入口 |

## 3. Source Of Truth

自动化相关规则优先级如下：

1. `脚本/` 中的真实执行逻辑
2. `系统/frontmatter_schema.yaml`
3. `系统/技术类笔记规范.md`
4. `.claude/skills/`
5. 本文件

如果本文件和代码不一致，以代码与 schema 为准，并同步修正本文件。

## 4. 双循环模型

### 开发态

目标：改进 Obsidian 自动化系统本身。

- 读取：`系统/运行进度.md`、`系统/功能清单.json`
- 入口：`/develop-harness` 或 `python 脚本/cli.py develop`
- 规则：每轮只推进一个未完成能力点

### 运行态

目标：处理收集箱中的笔记。

- 读取：`系统/运行进度.md`、`系统/处理队列.json`
- 入口：`/process-inbox` 或 `python 脚本/主流程.py --scan-first --limit 1`
- 规则：每轮只处理 `1-3` 篇，默认 `1`

## 5. 当前状态文件

| 文件 | 用途 |
|---|---|
| `系统/功能清单.json` | 开发态能力清单 |
| `系统/处理队列.json` | 运行态任务队列 |
| `系统/运行进度.md` | 开发态与运行态进度摘要 |
| `系统/运行日志.md` | 每轮处理审计日志 |
| `系统/健康度报告.md` | 运行健康度统计 |
| `系统/frontmatter_schema.yaml` | 自动化输出校验规则 |
| `系统/技术类笔记规范.md` | 技术类文章/知识笔记整理规范 |

说明：仓库里可能还存在 `feature_list.json`、`progress.md`、`task_queue.json`、`run_log.md` 等旧文件；当前主流程以中文状态文件为准。

## 6. 可用入口

### Claude Code

- `/process-inbox`
- `/develop-harness`

### CLI

```bash
python 脚本/cli.py init
python 脚本/cli.py scan
python 脚本/cli.py process --dry-run --limit 1
python 脚本/cli.py process --limit 1
python 脚本/cli.py status
python 脚本/cli.py verify --changed-only
python 脚本/cli.py develop
python 脚本/cli.py e2e
```

### 主流程

```bash
python 脚本/主流程.py --scan-first --limit 1
python 脚本/主流程.py --dry-run --scan-first --limit 1
```

### 持续运行入口

```bash
python autorun_scheduler.py --once
python 脚本/自动调度器.py --daemon --interval 30
powershell -ExecutionPolicy Bypass -File 脚本/注册计划任务.ps1
```

## 7. 运行态硬约束

- 只自动处理 `00-收集箱/` 下的 Markdown 笔记。
- `--dry-run` 只允许扫描、分类、预测路由和目标路径；禁止写文件、移动文件、更新 MOC。
- 不允许删除笔记。
- 不允许批量改写 `99-归档/` 或历史正文。
- 每轮结束后必须更新 `系统/处理队列.json`、`系统/运行日志.md`、`系统/运行进度.md`。
- 失败任务必须留痕，不能静默吞掉。

## 8. 自动化粗整理契约

自动化当前输出的是“可继续精整理”的中间产物，不强制等于最终技术问答笔记。

### Frontmatter

自动化输出至少保证这些字段：

- `title`
- `type`
- `domain`
- `tags`
- `source`
- `created`
- `status`
- `summary`
- `processed_at`

自动化通常还会补充：

- `skill`
- `topic`
- `question`
- `source_title`
- `source_section`
- `updated`

说明：

- `domain` 当前允许字符串或列表。
- `status` 自动化默认常见值为 `review`。
- 字段合法性最终以 `系统/frontmatter_schema.yaml` 和 `脚本/校验frontmatter.py` 为准。

### 正文

自动化写入后的正文至少应兼容这些分区：

- `TL;DR`
- `References`
- `【需要人工复核】`

如有子代理增强，还可能追加：

- `示例说明`
- `关键技术点`
- `常见坑与边界`
- `相关笔记`

## 9. 技术类文章/知识笔记精整理规范

适用场景：

- 整理 JavaGuide、技术博客、面试题
- 一篇笔记回答一个问题
- 需要代码示例、代码注释、易错点、延伸链接

详细规范见 [技术类笔记规范.md](/D:/Docs/Notes/ObsidianVault/系统/技术类笔记规范.md)。

核心要求：

- 一篇笔记只讲一个问题
- 标题格式：`领域 - 问题`
- 区别类问题必须有 `## 对比` 表格
- 代码示例控制在 `10-25` 行，并同时具备行内注释与代码说明
- 技术笔记至少包含：
  - `一句话结论`
  - `标准回答`
  - `为什么`
  - `易错点`
  - `参考来源`

推荐模板：

- [Distill-模板.md](/D:/Docs/Notes/ObsidianVault/80-模板/Distill-模板.md)

说明：

- 自动化粗整理完成后，如要沉淀成长期知识笔记，应按上述模板进行精整理。
- `脚本/校验frontmatter.py` 已兼容自动化产物与这套技术类笔记模板。

## 10. 子代理路由

当前运行时内容子代理为：

- `process-paper`
- `process-code-snippet`
- `process-meeting-notes`

规则路由示例：

- `Abstract / Introduction / Conclusion / DOI / arXiv` -> `process-paper`
- `def / import / class / function / 代码块` -> `process-code-snippet`
- `会议 / Agenda / Action Item / TODO` -> `process-meeting-notes`

说明：`.claude/agents/initializer.md`、`.claude/agents/pipeline-agent.md`、`.claude/agents/reviewer.md` 当前主要用于 harness 说明，不是运行态自动编排入口。

## 11. 验证要求

修改自动化相关文件后，至少执行以下之一：

```bash
python 脚本/cli.py verify --changed-only
python 脚本/cli.py e2e
```

涉及主流程、队列、frontmatter、subagent、MOC 的修改，优先跑 `e2e`。

## 12. 不再使用的旧约定

以下内容不再作为当前主入口：

- `/pkm sync`
- `/pkm status`
- `/transform`
- “所有笔记都必须只有自动化中间产物格式” 这种假设
- “技术类知识笔记必须完全等于自动化粗整理结构” 这种假设
