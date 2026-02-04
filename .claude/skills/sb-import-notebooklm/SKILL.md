---
name: sb-import-notebooklm
description: 从 70-NotebookLM导入/ 读取 NotebookLM 导出文件，按 Capture 模板写入 00-收集箱/，并可选自动执行 /sb-organize 与 /sb-distill。
invocation: user
---

# sb-import-notebooklm - NotebookLM 导入桥接

你正在执行 /sb-import-notebooklm。

## 目标
把 NotebookLM 导出的本地文件导入到 Obsidian 收集箱，并按第二大脑工作流推进。

## 约束（强制）
- 不直接访问 NotebookLM；只读取本地目录：`70-NotebookLM导入/`
- 必须使用模板：`80-模板/Capture-模板.md`
- 输出必须全中文、结构化、可落地
- 若来源缺失：source 写"未提供"，并在正文提醒待确认

## 参数
- `--latest`：导入目录下最新文件（默认）
- `<filename>`：导入指定文件（相对路径或文件名）
- `--then organize`：导入后自动执行 /sb-organize
- `--then distill`：导入后自动执行 /sb-distill（会先 organize）
- `--then all`：导入后自动执行 organize + distill

示例：
- `/sb-import-notebooklm --latest`
- `/sb-import-notebooklm 2026-02-04-哈希表扩容.md --then all`

## 执行步骤（强制）
1) 运行脚本（在 Vault 根目录执行）：
   - `python .claude/skills/sb-import-notebooklm/scripts/import.py $ARGUMENTS`
2) 脚本输出会打印"已创建的收集箱文件路径"
3) 如果用户带了 `--then`：
   - `organize`：调用 `/sb-organize <新文件路径>`
   - `distill`：调用 `/sb-organize <新文件路径>` 后，再调用 `/sb-distill <归位后路径>`
   - `all`：同 distill

## 终端输出（必须简短）
- ✅ 已导入：<源文件> → <收集箱文件>
- （可选）✅ 已归位：…
- （可选）✅ 已提取：…
- 👉 建议下一步：/sb-express …
