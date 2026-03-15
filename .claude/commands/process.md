---
description: 处理 Obsidian 收件箱
argument-hint: [scan|process|status|verify] [--dry-run] [--limit N]
allowed-tools: Bash
---

在 `D:\Docs\Notes\ObsidianVault` 下执行：

```bash
python 脚本/cli.py init
python 脚本/cli.py $ARGUMENTS
```

如果没有参数，默认执行：

```bash
python 脚本/主流程.py --limit 1
```
