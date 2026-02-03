---
type: moc
tags:
  - MOC
  - 资讯
  - 日报
created: 2026-02-03
updated: 2026-02-03
---

# 📰 资讯日报 - MOC

> **PKM v2.1 资讯造血系统**
> 信息源：GitHub / YouTube / Hugging Face（白名单制）
> 工作流：候选包 → Review → 日报 + 知识卡草稿

---

## 🎯 系统状态

| 指标 | 数值 |
|------|------|
| 累计日报 | 0 篇 |
| 知识卡草稿 | 0 张 |
| 转化为正式知识卡 | 0 张 |
| 最近更新 | 2026-02-03 |

---

## 📅 日报索引（按日期倒序）

### 2026-02
<!-- 日报链接将在此处自动追加 -->
- _待产出首篇日报_

---

## 🌱 知识卡草稿追踪

### 待加工（00-收集箱/News-Knowledge-Drafts）
<!-- 发布日报时自动记录草稿卡 -->
- _无待加工草稿_

### 已转化为正式知识卡
<!-- 使用 knowledge-extract 后手动更新 -->
- _无转化记录_

---

## 📊 转化漏斗

```mermaid
graph LR
    A[候选包] -->|Review| B[日报]
    B -->|2-3张| C[知识卡草稿]
    C -->|knowledge-extract| D[正式知识卡]
    D -->|moc-index| E[挂载MOC]
    E -->|output-crafter| F[输出作品]
```

---

## 🔗 相关导航

- [[00-总仪表盘|返回总仪表盘]]
- [[01-领域总览-MOC|领域知识总览]]
- [[10-领域知识/01-计算机/Java/Java-MOC|Java 知识地图]]

---

## 📋 使用指南

### 1. 生成候选包
```
触发指令：生成今日候选包（window_hours=24）
输出位置：00-收集箱/News-Inbox/YYYY-MM-DD/00-candidate-pack.md
```

### 2. Review 候选包
在候选包中勾选：
- `[x] approve` - 批准发布
- `[x] reject` - 拒绝
- `[x] needs-verify` - 需要人工验证

### 3. 发布日报与草稿
```
触发指令：我已 review，请发布
输出：
  - 02-学习记录/01-日报/YYYY-MM-DD-资讯日报.md
  - 00-收集箱/News-Knowledge-Drafts/*.md
  - 更新本 MOC
```

### 4. 草稿卡加工流程
```
inbox-triage → knowledge-extract → moc-index → output-crafter
```

---

*最后更新：2026-02-03*
