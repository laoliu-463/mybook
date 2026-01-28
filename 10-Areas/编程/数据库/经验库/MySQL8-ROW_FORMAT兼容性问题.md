---
type: experience-card
category: bug-fix
source: "[[20-Projects/P01-hmdp黑马点评/00-项目看板]]"
created: 2026-01-28
tags:
  - MySQL
  - MySQL8
  - ROW_FORMAT
  - 踩坑
  - 数据库迁移
---

# MySQL 8 ROW_FORMAT 兼容性问题

## 🎯 场景
> 在 MySQL 8.0 环境下执行老项目的 SQL 脚本时，遇到行格式 (ROW_FORMAT) 相关错误

## 🔥 问题/需求
> - SQL 脚本包含：`ROW_FORMAT=Compact`
> - MySQL 8.0 默认使用 `DYNAMIC` 格式
> - 现象：执行 SQL 时可能报错或产生警告

**错误示例**：
```
ERROR 1031 (HY000): Table storage engine for 'xxx' doesn't have this option
```

## ✅ 解决方案

### 方案 A：修改 SQL 脚本（推荐）
将所有 `ROW_FORMAT=Compact` 替换为 `ROW_FORMAT=DYNAMIC`：

```sql
-- 修改前
CREATE TABLE `tb_user` (
  ...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=Compact;

-- 修改后
CREATE TABLE `tb_user` (
  ...
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;
```

**批量替换命令**：
```bash
sed -i 's/ROW_FORMAT=Compact/ROW_FORMAT=DYNAMIC/g' hmdp.sql
```

### 方案 B：移除 ROW_FORMAT 配置
直接删除 `ROW_FORMAT=xxx`，让 MySQL 8 使用默认值：
```bash
sed -i 's/ROW_FORMAT=Compact//g' hmdp.sql
```

### 方案 C：修改 MySQL 配置（不推荐）
```ini
# my.cnf
[mysqld]
innodb_default_row_format=compact
```
不推荐：会影响所有新建表，且 Compact 格式在大字段时有限制。

## 💡 核心教训
> 执行老项目 SQL 前，**先搜索 ROW_FORMAT**，MySQL 8 默认不再支持 Compact，需改为 DYNAMIC。

## 🔗 相关
- [[MySQL 8.0 升级注意事项]]
- [[20-Projects/P01-hmdp黑马点评/00-项目看板]]
