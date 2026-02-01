---
type: guide
created: 2026-01-29
---

# Skill 使用指南

> 项目学习过程中可调用的 AI 辅助技能

## 可用 Skill 列表

### 1. `/sourcecode-organize` - 源码阅读辅助
**用途**: 梳理代码入口、调用链路、核心类图
**适用场景**:
- Task 1.6: 阅读 `UserController` → `UserService` 登录链路
- 分析 Redis 缓存相关代码结构
- 理解 Redisson 分布式锁源码

**示例调用**:
```
/sourcecode-organize 分析 hmdp 项目的登录链路，从 UserController 到 Redis Token 存储
```

---

### 2. `/project-planner` - 项目规划器
**用途**: 将模糊目标拆解为可执行的阶段任务
**适用场景**:
- 规划新的学习阶段
- 拆解复杂功能的学习步骤

**示例调用**:
```
/project-planner 规划 Redis 分布式锁的学习路径
```

---

### 3. `/project-retro` - 项目复盘器
**用途**: 从过程日志中提取可复用经验卡片
**适用场景**:
- P4 阶段：面试复述与总结
- 每个阶段结束时的复盘

**示例调用**:
```
/project-retro 复盘 P1 阶段的环境配置经验
```

---

### 4. `/json-canvas` - Canvas 可视化
**用途**: 创建和编辑 JSON Canvas 文件
**适用场景**:
- Task 1.7: 绘制核心请求链路图
- 创建知识结构图

**示例调用**:
```
/json-canvas 创建 hmdp 登录链路的流程图
```

---

### 5. `/note-polish` - 笔记整理
**用途**: 将原始笔记整理为符合 PKM 规范的成品
**适用场景**:
- 整理学习笔记
- 规范化交付物文档

---

### 6. `/interview-extract` - 面试题提取
**用途**: 从笔记中提取面试/自测题对
**适用场景**:
- P4 阶段：生成面试复盘白皮书
- 从 Redis 笔记中提取面试题

---

## 推荐工作流

1. **源码阅读**: `/sourcecode-organize` → 生成调用链路图
2. **知识整理**: `/note-polish` → 规范化笔记
3. **可视化**: `/json-canvas` → 创建 Canvas 图
4. **阶段复盘**: `/project-retro` → 提取经验卡片
5. **面试准备**: `/interview-extract` → 生成题对
