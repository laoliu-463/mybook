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
| `20-知识库/` | 概念、总结、代码类知识笔记 |
| `30-资源/` | 资料、论文、课程、素材 |
| `40-交付物/` | 可发布内容、图表、交付稿 |
| `70-NotebookLM提示词使用/` | NotebookLM 相关资料与提示词 |
| `80-模板/` | 模板目录，禁止删除 |
| `99-归档/` | 归档内容，禁止自动批量改写 |
| `系统/` | 状态文件、schema、日志、测试样例 |
| `脚本/` | Python/PowerShell 自动化入口 |

## 3. Source Of Truth

自动化相关规则以当前实现为准，优先级如下：

1. `脚本/` 中的真实执行逻辑
2. `系统/frontmatter_schema.yaml`
3. `.claude/skills/`
4. 本文件

如果本文件和代码不一致，以代码与 schema 为准，并应同步修正本文件。

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
| `系统/frontmatter_schema.yaml` | frontmatter 与正文分区校验规则 |

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

## 8. Frontmatter 与正文契约

自动化笔记以当前 pipeline 为准，不再使用旧版“固定技术问答模板”作为唯一标准。

### Frontmatter

至少保证这些字段与当前流水线一致：

- `title`
- `type`
- `domain`
- `tags`
- `source`
- `created`
- `status`

自动化通常会补充：

- `summary`
- `skill`
- `processed_at`

说明：

- `domain` 当前按列表处理，不应假设为单值字符串。
- `status` 由自动化默认写为 `review`，人工整理后再提升状态。
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

## 9. 子代理路由

当前运行时内容子代理为：

- `process-paper`
- `process-code-snippet`
- `process-meeting-notes`

规则路由示例：

- `Abstract / Introduction / Conclusion / DOI / arXiv` -> `process-paper`
- `def / import / class / function / 代码块` -> `process-code-snippet`
- `会议 / Agenda / Action Item / TODO` -> `process-meeting-notes`

说明：`.claude/agents/initializer.md`、`.claude/agents/pipeline-agent.md`、`.claude/agents/reviewer.md` 当前主要用于 harness 说明，不是运行态自动编排入口。

## 10. 验证要求

修改自动化相关文件后，至少执行以下之一：

```bash
python 脚本/cli.py verify --changed-only
python 脚本/cli.py e2e
```

涉及主流程、队列、frontmatter、subagent、MOC 的修改，优先跑 `e2e`。

## 11. 禁止继续沿用的旧约定

以下内容不再作为当前主入口：

- `/pkm sync`
- `/pkm status`
- `/transform`
- “只允许 `type: note` 且 `status: evergreen`” 这类旧版 frontmatter 假设
- “所有笔记必须固定输出一套技术问答模板” 这类旧版正文模板假设
