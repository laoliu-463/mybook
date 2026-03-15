---
description: 启动 Anthropic Harness，处理 Obsidian 收件箱
argument-hint: [scan|process|status|verify] [--dry-run]
allowed-tools: Bash
---

# 执行命令（唯一入口）

在 `D:\Docs\Notes\ObsidianVault` 下执行 Python CLI：

```bash
# 初始化（首次运行）
bash init.sh

# 运行流水线
python 脚本/cli.py $ARGUMENTS
```

## 可用参数

| 参数 | 说明 |
|------|------|
| scan | 扫描收件箱 |
| process | 处理下一条 |
| status | 查看状态 |
| verify | E2E 验证 |
| --dry-run | 预览模式 |

## 执行后用中文总结

1. 当前处理状态
2. 若是 `process --dry-run`，给出预览重点
3. 若是实际处理，说明源文件、目标路径和是否更新了 MOC
