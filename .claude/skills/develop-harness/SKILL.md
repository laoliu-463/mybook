# Develop Harness Skill

显式触发 Obsidian 自动化系统的开发态恢复流程。

## 使用方式

```text
/develop-harness
```

## 执行顺序

1. 读取 `系统/运行进度.md`
2. 读取 `系统/功能清单.json`
3. 运行 `python 脚本/cli.py develop`
4. 只选择一个 `passes=false` 的能力点继续实现
5. 修改完成后运行 `python 脚本/cli.py verify --changed-only`
6. 如该能力通过，再更新 `系统/功能清单.json` 中对应项

## 约束

- 开发态优先处理系统能力，不直接批量整理笔记
- 每轮只推进一个未完成能力点
- 会话开始先恢复 git 上下文、运行进度和功能清单
- 会话结束前必须完成基础自检
