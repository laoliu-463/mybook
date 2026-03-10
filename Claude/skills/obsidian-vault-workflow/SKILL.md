# Obsidian Vault Workflow

操作当前 Obsidian 笔记库（Vault）的完整工作流。

**Vault 根目录**: `D:\Docs\Notes\ObsidianVault`

## 适用场景

- 搜索、读取、创建、修改笔记文件
- 管理 Frontmatter 元数据
- 分析和维护笔记间的链接关系
- 按标签、文件夹、内容进行高级搜索

---

## 1. 笔记文件操作 (Note Operations)

### 1.1 获取所有 Markdown 文件

```bash
Glob pattern: "**/*.md"
```

**示例**:
```
列出 Vault 中所有 .md 文件
```

### 1.2 按路径获取笔记

使用 Glob 配合路径前缀：

```bash
Glob pattern: "20-知识库/**/*.md"
```

**示例**:
```
获取 20-知识库 目录下所有笔记
获取 20-知识库/计算机网络 目录下的笔记
```

### 1.3 读取笔记内容

```bash
Read file_path: "D:\Docs\Notes\ObsidianVault\20-知识库\计算机网络\TCP协议\00-overview.md"
```

### 1.4 创建/修改笔记

**创建新笔记**:
```bash
Write file_path: "D:\Docs\Notes\ObsidianVault\20-知识库\Java\ThreadLocal详解.md"
content: |
  ---
  title: ThreadLocal 详解
  type: concept
  domain: [Java, 并发编程]
  tags: [ThreadLocal, Java, Concurrency]
  source: notebooklm
  created: 2026-03-10
  status: draft
  ---

  # ThreadLocal 详解

  ## TL;DR
  ...
```

**修改现有笔记**:
```bash
Edit file_path: "D:\Docs\Notes\ObsidianVault\20-知识库\Java\ThreadLocal详解.md"
old_string: "## TL;DR\n..."
new_string: "## TL;DR\n- ThreadLocal 提供线程局部变量\n- 每个线程有自己的变量副本\n- 常用于解决线程安全问题"
```

### 1.5 重命名/移动笔记

1. 使用 Read 读取原文件内容
2. 使用 Write 创建新路径的文件
3. 更新所有引用该文件的链接（见链接操作）
4. 删除原文件

---

## 2. Frontmatter 操作 (Frontmatter Operations)

### 2.1 解析 Frontmatter

Frontmatter 位于笔记开头的 `---` 之间：

```yaml
---
title: xxx
type: concept
domain: [领域1, 领域2]
tags: [标签1, 标签2]
source: notebooklm
created: YYYY-MM-DD
status: draft
---
```

**解析方式**: 使用正则表达式 `^---\n([\s\S]*?)\n---` 提取 YAML 内容。

### 2.2 更新 Frontmatter 字段

使用 Edit 工具替换特定字段：

```bash
# 更新 status
Edit old_string: "status: draft"
new_string: "status: done"
replace_all: true

# 更新 tags
Edit old_string: "tags: [Java]"
new_string: "tags: [Java, Concurrency]"
```

### 2.3 删除 Frontmatter 属性

直接删除对应行：

```bash
Edit old_string: "next_review: 2026-03-15\n"
new_string: ""
```

### 2.4 按 Frontmatter 条件筛选文件

使用 Grep 搜索特定字段：

```bash
Grep pattern: "^status: draft$"
glob: "**/*.md"

Grep pattern: "^type: concept$"
glob: "20-知识库/**/*.md"

Grep pattern: "domain:.*Java"
glob: "20-知识库/**/*.md"
```

---

## 3. 链接与标签操作 (Link & Tag Operations)

### 3.1 获取笔记的所有出站链接

Wikilink 格式: `[[笔记名称]]` 或 `[[路径/笔记名称]]`

```bash
Grep pattern: "\[\["
path: "D:\Docs\Notes\ObsidianVault\20-知识库\Java\ThreadLocal详解.md"
output_mode: content
```

### 3.2 获取反向链接

搜索哪些笔记引用了当前笔记：

```bash
Grep pattern: "\[\[ThreadLocal详解\]\]"
path: "D:\Docs\Notes\ObsidianVault"
glob: "**/*.md"
```

### 3.3 获取所有标签

```bash
Grep pattern: "#[a-zA-Z0-9_-]+"
path: "D:\Docs\Notes\ObsidianVault"
glob: "**/*.md"
output_mode: content
```

### 3.4 按标签筛选文件

```bash
Grep pattern: "#Java"
glob: "20-知识库/**/*.md"

Grep pattern: "#并发"
glob: "20-知识库/**/*.md"
```

### 3.5 更新链接（目标重命名时）

当重命名笔记后，需要更新所有引用：

1. 查找所有反向链接
2. 使用 Edit 替换所有 `[[原名称]]` 为 `[[新名称]]`

```bash
# 替换所有引用
Edit old_string: "[[ThreadLocal详解]]"
new_string: "[[ThreadLocal 详解]]"
replace_all: true
```

---

## 4. 搜索与查询 (Search & Query)

### 4.1 文件名模糊搜索

```bash
Glob pattern: "**/*Thread*.md"
Glob pattern: "**/*TCP*.md"
```

### 4.2 内容全文搜索

```bash
Grep pattern: "volatile"
path: "D:\Docs\Notes\ObsidianVault\20-知识库"

Grep pattern: "synchronized"
glob: "20-知识库/**/*.md"
output_mode: files_with_matches
```

### 4.3 多条件高级搜索

**按文件夹 + 内容**:
```bash
Grep pattern: "TCP"
glob: "20-知识库/计算机网络/**/*.md"
```

**按多个标签**:
```bash
Grep pattern: "#Java.*#并发"
path: "D:\Docs\Notes\ObsidianVault"
```

**按 Frontmatter domain**:
```bash
Grep pattern: "domain:.*Java"
glob: "20-知识库/**/*.md"
output_mode: files_with_matches
```

---

## 5. 常用工作流示例

### 5.1 创建新笔记模板

```bash
# 1. 确定路径和文件名
# 20-知识库/<领域>/<主题>.md

# 2. 写入带 Frontmatter 的笔记
Write content: """---
title: <标题>
type: concept|overview|interview|project|resource
domain: [<领域1>, <领域2>]
tags: [<标签1>, <标签2>]
source: notebooklm|web|book|voice
created: 2026-03-10
status: draft
---

# <标题>

## TL;DR

## 背景与问题定义

## 核心机制拆解

## 示例

## 常见坑与边界

## References

---
"""
file_path: "D:\Docs\Notes\ObsidianVault\20-知识库\Java\新主题.md"
```

### 5.2 检查笔记完整性

1. 列出某目录所有笔记
2. 检查 Frontmatter 必需字段
3. 列出缺失字段的笔记

```bash
# 获取目录所有笔记
Glob pattern: "20-知识库/Java/**/*.md"

# 搜索缺少 type 字段的笔记
Grep glob: "20-知识库/**/*.md"
output_mode: files_with_matches
pattern: "^---\n(?!.*^type:)"
multiline: true
```

### 5.3 链接修复扫描

1. 搜索所有 wikilink
2. 验证链接目标是否存在
3. 报告断裂链接

```bash
# 查找所有 wikilink
Grep glob: "**/*.md"
output_mode: content
pattern: "\[\[([^\]]+)\]\]"
```

---

## 6. 工具映射表

| Obsidian API | Claude Code 工具 |
|--------------|------------------|
| `app.vault.getMarkdownFiles()` | `Glob` |
| `app.vault.read(file)` | `Read` |
| `app.vault.modify(file, content)` | `Edit` |
| `app.vault.create(path, content)` | `Write` |
| `app.metadataCache.getFileCache(file).links` | `Grep` |
| `app.metadataCache.getFileCache(file).tags` | `Grep` |
| `app.vault.getAbstractFileByPath(path)` | `Glob` + `Read` |

---

## 7. 注意事项

1. **路径分隔符**: Windows 使用 `\`，但在 Glob/Grep 模式中使用 `/`
2. **Vault 根目录**: 始终使用完整路径 `D:\Docs\Notes\ObsidianVault\`
3. **Frontmatter 格式**: 严格遵循 YAML 格式，避免中文冒号
4. **双向链接**: 使用 `[[笔记名称]]` 格式，名称避免特殊字符

---

## 8. 快速命令速查

| 操作 | 命令 |
|------|------|
| 列出所有笔记 | `Glob pattern: "**/*.md"` |
| 列出某目录笔记 | `Glob pattern: "20-知识库/**/*.md"` |
| 读取笔记 | `Read file_path: "完整路径"` |
| 搜索内容 | `Grep pattern: "关键词"` |
| 按标签搜索 | `Grep pattern: "#标签名"` |
| 创建笔记 | `Write file_path: "路径" content: "内容"` |
| 修改笔记 | `Edit file_path: "路径" old_string: "原文本" new_string: "新文本"` |
