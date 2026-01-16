# 个人笔记库（零基础友好版）

> 基于 Obsidian + Git 的个人知识管理系统，支持跨设备同步与历史版本回溯。

---

## 适合人群

- 刚开始用 Obsidian 记笔记的人
- 想把笔记同步到 GitHub，但不熟 Git 的人
- 需要一个“能找回旧版本”的笔记库的人

---

## 先了解 3 个概念

- **Vault**：Obsidian 里的“笔记库”，就是一个普通文件夹。
- **Git 仓库**：能记录文件历史的文件夹，用来版本控制。
- **同步**：把本地修改上传到 GitHub，或拉取远端更新。

---

## 快速开始（5 分钟）

### 1. 环境准备
- Obsidian（最新版）
- Git 2.0+
- Obsidian Git 插件

### 2. 克隆到本地
```bash
git clone https://github.com/laoliu-463/mybook.git
cd mybook
```

### 3. 打开笔记库
在 Obsidian 中选择“打开文件夹作为 Vault”，选中 `mybook` 即可。

---

## 目录结构

```
ObsidianVault/
├── .obsidian/              # Obsidian 配置（已忽略）
├── mybook/                 # 子文件夹
├── *.md                    # 各类笔记文档
└── README.md               # 本文档
```

---

## 笔记分类

| 类别 | 说明 |
|------|------|
| 技术文档 | 环境配置、工具使用等 |
| 日常记录 | 每日笔记、随笔 |
| 项目笔记 | 项目相关的知识整理 |

---

## 配置说明

详细配置过程请参阅：`90_Tools_Environment/Obsidian Git 笔记库配置全流程.md`

---

## 常用操作（不会 Git 也能做）

### 手动推送
```
Ctrl + P → Obsidian Git: Push
```

### 手动拉取
```
Ctrl + P → Obsidian Git: Pull
```

### 查看历史
```
Ctrl + P → Obsidian Git: Open history
```

---

## 注意事项（新手必看）

1. 不要在仓库里再创建新的 Git 仓库（避免“仓库套娃”）。
2. 大文件（>10MB）建议用云盘，只在笔记里放链接。
3. 修改后请确认插件有自动推送成功。

---

*最后更新：2026-01-12*
