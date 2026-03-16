---
description: 恢复 Obsidian Harness 开发态上下文
argument-hint: [verify]
allowed-tools: Bash
---

在 `D:\Docs\Notes\ObsidianVault` 下执行：

```bash
python 脚本/cli.py develop
```

如果显式追加 `verify`，再执行：

```bash
python 脚本/cli.py verify --changed-only
```

执行后用中文总结：

1. 当前开发态上下文
2. git 工作区摘要
3. 下一个未完成功能点
