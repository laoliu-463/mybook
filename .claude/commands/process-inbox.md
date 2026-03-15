---
description: 处理 Obsidian 收件箱
argument-hint: [scan|process|status|verify] [--dry-run] [--limit N]
allowed-tools: Bash
---

# 执行命令

在 `D:\Docs\Notes\ObsidianVault` 下执行：

```bash
bash 脚本/初始化环境.sh

python 脚本/cli.py $ARGUMENTS
```

如果没有参数，默认执行：

```bash
python 脚本/主流程.py --limit 1
```

## 可用参数

| 参数 | 说明 |
|------|------|
| scan | 扫描收件箱 |
| process | 处理下一批（默认 1 篇，最大 3 篇） |
| status | 查看状态 |
| verify | E2E 验证 |
| --dry-run | 预览模式 |

## 执行后用中文总结

1. 当前处理状态
2. 若是 `process --dry-run`，给出预览重点
3. 若是实际处理，说明源文件、目标路径和是否更新了 `系统/处理队列.json`、`系统/运行日志.md`、`系统/运行进度.md`
