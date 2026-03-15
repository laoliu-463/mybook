# Process Inbox Skill

处理 Obsidian 收件箱笔记的自动化流程。

## 使用方式

```
/process-inbox [scan|process|status|verify] [--dry-run]
```

## 执行流程

1. **读取状态**：先读取 `系统/运行进度.md` 和 `系统/处理队列.json`
2. **初始化环境**：运行 `bash init.sh`
3. **执行流水线**：`python 脚本/cli.py $COMMAND`
4. **自检**：`python 脚本/cli.py verify`
5. **更新日志**：追加到 `系统/运行日志.md`

## 约束

- 只处理 `00-收集箱/` 目录下的笔记
- 每次运行最多处理 1-3 篇
- 处理完成后必须更新队列和日志
- 不允许删除笔记
- 不允许批量修改历史笔记正文
- 先运行 `自检.py` 验证
