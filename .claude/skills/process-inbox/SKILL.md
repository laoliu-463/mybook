# Process Inbox Skill

显式触发 Obsidian 收件箱处理流程。当前仓库沿用现有 PARA 命名：
- 收件箱：`00-收集箱/`
- 项目：`10-项目/`
- 知识库：`20-知识库/`
- 资源：`30-资源/`
- 交付物：`40-交付物/`

## 用法

```text
/process-inbox
/process-inbox process --dry-run
/process-inbox process --limit 1
/process-inbox status
/process-inbox verify --changed-only
```

## 执行顺序

1. 读取 `系统/运行进度.md`
2. 读取 `系统/功能清单.json`
3. 读取 `系统/处理队列.json`
4. 运行 `python 脚本/cli.py init`
5. 如需显式扫描，运行 `python 脚本/cli.py scan`
6. 正式执行时运行 `python 脚本/主流程.py --limit 1`
7. 预演时运行 `python 脚本/cli.py process --dry-run --limit 1`
8. 最后运行 `python 脚本/自检.py --changed-only`

## 约束

- 只自动处理 `00-收集箱/` 下的 Markdown 笔记
- 每轮最多处理 `1-3` 篇，默认 `1`
- `--dry-run` 只能输出预测结果，不能写文件、移动文件或更新主题地图
- 不允许删除笔记
- 不允许批量修改历史正文
- 处理后必须更新 `系统/处理队列.json`、`系统/运行日志.md`、`系统/运行进度.md`
