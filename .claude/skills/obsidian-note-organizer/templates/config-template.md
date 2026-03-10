# Obsidian 笔记整理自定义配置（增强版）

## 1. 基础路径配置

```yaml
# 默认收集箱目录（相对于库根路径）
default_inbox_folder: 00-收集箱
# 默认归档目标根目录（相对于库根路径）
default_target_base_folder: 20-知识库
```

## 2. 收集箱笔记分类规则

格式：目标子目录: [关键词1, 关键词2, 关键词3]
笔记内容包含任一关键词则归档到对应目录

```yaml
category_rules:
  编程语言: [python, java, go, c++, rust, javascript, 编程, 代码, 开发]
  数据结构与算法: [算法, algorithm, leetcode, 数据结构, 动态规划]
  操作系统: [linux, windows, os, 进程, 线程, 内存, kernel]
  计算机网络: [network, TCP, HTTP, DNS, socket, 网络, 协议]
  数据库: [database, mysql, redis, mongodb, sql, 数据库]
  中间件: [kafka, rabbitmq, 消息队列, message queue]
  分布式与微服务: [distributed, 微服务, spring cloud, 分布式]
  云原生: [docker, kubernetes, k8s, 容器, cloud native]
  安全: [security, 安全, 加密, 攻击, 防御]
  编译原理: [compiler, 编译, lexer, parser, ast]
  架构与工程实践: [architecture, 架构, 性能, devops, 测试]
  AI-ML: [machine learning, 机器学习, 深度学习, neural network, AI]
  项目: [项目, project, 任务, task]
  面试: [面试, interview, 求职]
  00-未分类: []
```

## 3. 已整理标记配置

标记方式：可多选，支持 tag/frontmatter/filename

```yaml
mark_methods:
  - tag          # 添加 #已整理 标签
  - frontmatter  # 将 status 字段改为 已整理
  # - filename    # 文件名添加 [已整理] 后缀（谨慎开启）

# 已整理标签名称
organized_tag: 已整理
# Frontmatter状态字段值
organized_status: 已整理
```

## 4. 标签合并规则

```yaml
tag_merge:
  todo: [待办, 待处理, todo-list]
  学习笔记: [学习, 笔记, 学习记录]
```

## 5. Frontmatter 自定义字段

```yaml
custom_frontmatter:
  category: 未分类
  cssclass: []
```

## 6. 额外排除文件夹

```yaml
exclude_folders:
  - 99-归档
  - 00-模板
```

## 7. 整理开关

```yaml
enable_frontmatter_standard: true
enable_inbox_archive: true
enable_organized_mark: true
enable_tag_optimize: true
enable_link_check: true
enable_content_format: true
```
