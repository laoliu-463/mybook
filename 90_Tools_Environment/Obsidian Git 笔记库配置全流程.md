---
title: Obsidian Git 笔记库配置全流程
date: 2026-01-12
tags: [Obsidian, Git, 环境配置, 版本控制]
status: 已完成
---

# Obsidian Git 笔记库配置全流程（零基础版）

> 目标：把本地笔记库和 GitHub 同步起来，自动备份、可回滚、可跨设备使用。

---

## 适合人群

- 只会用 Obsidian 记笔记，但不会 Git 的人
- 想要“自动备份”和“历史版本”的人

---

## 你需要准备

1. 安装 Obsidian（最新版）
2. 安装 Git（2.0+）
3. Obsidian Git 插件（插件市场可安装）
4. 一个 GitHub 仓库地址（例如 `https://github.com/laoliu-463/mybook.git`）

---

## 概念小抄（不懂就看这里）

- **本地仓库**：你电脑上的文件夹。
- **远程仓库**：GitHub 上的仓库。
- **push**：把本地改动上传到 GitHub。
- **pull**：把 GitHub 改动拉回本地。
- **.gitignore**：告诉 Git 哪些文件不要上传。

---

## 配置步骤（一步一步来）

### Step 1：确认本地路径
本文以 `d:\Docs\Notes\ObsidianVault` 为例：
```bash
cd d:\Docs\Notes\ObsidianVault
```

### Step 2：关联远程仓库
```bash
git remote add origin https://github.com/laoliu-463/mybook.git
```
解释：这一步是在“告诉 Git：远端地址在哪里”。

### Step 3：配置 .gitignore
在仓库根目录创建 `.gitignore`：
```gitignore
.obsidian/
**/workspace.json
**/workspaces-mobile.json
```
解释：Obsidian 的配置文件经常变，通常不需要上传。

### Step 4：初次提交并推送
```bash
git add .
git commit -m "feat: init obsidian notes"
git push -u origin main
```
解释：  
`add` 收集变更，`commit` 生成历史记录，`push` 上传到 GitHub。

---

## 插件自动同步设置（简单版）

如果你不想命令行，直接在 Obsidian Git 插件设置中：
- Auto Save Interval = 5
- Auto Push Interval = 5
- Auto Pull on Startup = 开启

> 如果想用脚本快速改（可选）：
```bash
node -e "const fs = require('fs'); const path = 'd:/Docs/Notes/ObsidianVault/.obsidian/plugins/obsidian-git/data.json'; const data = JSON.parse(fs.readFileSync(path, 'utf8')); data.autoSaveInterval = 5; data.autoPushInterval = 5; data.autoPullOnStart = true; fs.writeFileSync(path, JSON.stringify(data, null, 2));"
```

---

## 常见问题与解决方案

### 问题 1：`[rejected] (non-fast-forward)`
**原因**：远程已有内容，本地落后。  
**解决**：先 `git pull`，如果你确认远程不重要再考虑强制推送。

> 注意：`git push --force` 会覆盖远程内容，谨慎使用。

### 问题 2：嵌套 Git 仓库冲突
**原因**：子目录里有自己的 `.git`。  
**解决**：
```bash
Remove-Item -Recurse -Force "d:\Docs\Notes\ObsidianVault\mybook\.git"
```

### 问题 3：自动推送不生效
**原因**：插件配置未生效或未启用。  
**解决**：检查插件设置并重启 Obsidian。

---

## 快速检查清单

- 能打开仓库 `git status`，没有报错
- Obsidian 状态栏能看到 Git 图标
- 修改笔记后 5 分钟内 GitHub 有新提交

---

*配置完成时间：2026-01-12 23:50*  
*仓库地址：[laoliu-463/mybook](https://github.com/laoliu-463/mybook.git)*
