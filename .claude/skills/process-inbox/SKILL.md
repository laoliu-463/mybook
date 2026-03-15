# Process Inbox Skill

显式触发 Obsidian 收件箱处理流程。当前仓库沿用现有 PARA 目录命名：

- 收件箱：`00-收集箱/`
- 项目：`10-项目/`
- 知识库：`20-知识库/`
- 资源：`30-资源/`
- 交付物：`40-交付物/`

## 使用方式

```text
/process-inbox
/process-inbox scan
/process-inbox process --dry-run
/process-inbox process --limit 1
/process-inbox status
/process-inbox verify --changed-only
```

## 执行顺序

1. 读取 `系统/运行进度.md`
2. 读取 `系统/功能清单.json`
3. 读取 `系统/处理队列.json`
4. 运行 `bash 脚本/初始化环境.sh`
5. 若用户显式要求扫描，则运行 `python 脚本/cli.py scan`
6. 否则运行 `python 脚本/主流程.py --limit 1`
7. 最后运行 `python 脚本/自检.py --changed-only`

## 何时调用子代理

- 笔记包含 `Abstract/Introduction/Conclusion` 等论文结构时，调用 `process-paper`
- 笔记包含大量代码块、`def/import/class/function` 等时，调用 `process-code-snippet`
- 笔记包含 `会议/Agenda/Action Item/决议` 等时，调用 `process-meeting-notes`

## 约束

- 只自动处理 `00-收集箱/` 下的 Markdown 笔记
- 每轮最多处理 1-3 篇，默认 1 篇
- 不允许删除笔记
- 不允许批量修改历史正文
- 处理后必须更新 `系统/处理队列.json`、`系统/运行日志.md`、`系统/运行进度.md`
