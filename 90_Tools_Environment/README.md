# 📚 个人笔记库

> 基于 Obsidian + Git 的个人知识管理系统

---

## 📋 仓库简介

这是一个使用 Obsidian 构建的个人笔记库，通过 Git 实现版本控制和跨设备同步。

**仓库地址**：[github.com/laoliu-463/mybook](https://github.com/laoliu-463/mybook.git)

---

## 🗂️ 目录结构

```
ObsidianVault/
├── .obsidian/              # Obsidian 配置（已忽略）
├── mybook/                 # 子文件夹
├── *.md                    # 各类笔记文档
└── README.md               # 本文档
```

---

## ✨ 功能特性

- 🔄 **自动同步**：每 5 分钟自动备份到 GitHub
- 📝 **版本控制**：完整的 Git 历史记录
- 🌐 **跨设备访问**：支持多设备同步
- 🔍 **双向链接**：Obsidian 原生支持知识图谱

---

## 🚀 快速开始

### 环境要求
- Obsidian (最新版)
- Git 2.0+
- Obsidian Git 插件

### 克隆到本地
```bash
git clone https://github.com/laoliu-463/mybook.git
cd mybook
```

在 Obsidian 中打开该文件夹作为 Vault 即可。

---

## 📖 笔记分类

| 类别 | 说明 |
|------|------|
| 📘 技术文档 | 环境配置、工具使用等 |
| 📝 日常记录 | 每日笔记、随笔 |
| 🗂️ 项目笔记 | 项目相关的知识整理 |

---

## 🔧 配置说明

详细配置过程请参阅：[Obsidian Git 笔记库配置全流程.md](Obsidian%20Git%20%E7%AC%94%E8%AE%B0%E5%BA%93%E9%85%8D%E7%BD%AE%E5%85%A8%E6%B5%81%E7%A8%8B.md)

---

## 📌 常用操作

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

## ⚠️ 注意事项

1. 请勿在此仓库内创建新的 Git 仓库
2. 大文件（>10MB）建议使用外部存储
3. 修改后请确认插件自动推送成功

---

*最后更新：2026-01-12*
