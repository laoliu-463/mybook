---
title: Linux - 目录结构是怎样的
aliases:
  - Linux 目录
  - Linux 文件系统
tags:
  - Linux
  - Linux/基础
  - 面试题
type: note
domain: 操作系统
topic: Linux
question: Linux 目录结构是怎样的
source:
source_title:
created: 2026-03-10
updated: 2026-03-10
status: evergreen
---

# Linux - 目录结构是怎样的

## 一句话结论
Linux 目录结构是树形组织，常见目录包括 /home（用户）、/etc（配置）、/var（日志）、/usr（程序）、/proc（进程信息）等。

## 标准回答
- **/home**：普通用户家目录
- **/etc**：系统和服务配置文件
- **/var**：经常变化的数据（日志、缓存、数据库）
- **/usr**：系统安装的程序和库
- **/tmp**：临时文件（重启可能清空）
- **/bin**：基本命令（ls、cp、mv）
- **/sbin**：系统管理命令
- **/root**：root 用户家目录
- **/dev**：设备文件（硬盘、网卡等）
- **/proc**：进程/内核信息（虚拟文件系统）

## 为什么
Linux 遵循 FHS（Filesystem Hierarchy Standard）标准，目录职责明确，便于：
- 文件查找和管理
- 权限控制
- 软件安装和维护

## 对比
| 目录 | 用途 | 示例 |
|---|---|---|
| /home | 用户目录 | /home/user |
| /etc | 配置 | /etc/nginx |
| /var | 变化数据 | /var/log |
| /usr | 程序 | /usr/bin |
| /proc | 内核信息 | /proc/cpuinfo |

## 常用目录详解

### /var 日志
```
/var/log/nginx     # Nginx 日志
/var/log/mysql    # MySQL 日志
/var/cache        # 应用缓存
```

### /proc 虚拟文件系统
```bash
/proc/cpuinfo     # CPU 信息
/proc/meminfo    # 内存信息
/proc/processID  # 进程信息
```

## 易错点
- /proc 是虚拟文件系统，不占磁盘空间
- /tmp 文件重启后可能被清空
- 系统配置文件在 /etc，不要随意修改
- /root 需要 root 权限才能访问

## 延伸链接
- [[Linux - 常用命令]]
- [[Linux - 用户和权限管理]]

## 参考来源
- FHS 标准：https://refspecs.linuxfoundation.org/FHS_3.0/
