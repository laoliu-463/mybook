---
title: Session 启动例程
type: project
domain: [内容创作]
tags: [Agent, SOP, Harness]
created: 2026-02-23
status: done
---

## TL;DR

每次开始新 session 前必须执行此例程。只做一个任务，完成后更新进度文件，停止。

---

## 启动步骤（每次必须）

```
1. 读取 content-progress.json
2. 找到第一个 status != "done" 的 episode
3. 找到该 episode 中按 A1→A7 顺序第一个 status = "pending" 的 Agent 任务
4. 只完成该单个 Agent 任务
5. 完成后：
   - 更新 content-progress.json 中该 Agent 的 status 为 "done"
   - 在对应期刊文件中补充该 Agent 的输出内容
6. 停止，等待下一个 session
```

> [!warning] 禁止跨任务
> 不允许在一个 session 中连续完成多个 Agent 任务。每次只做一个，防止上下文崩溃和质量失控。

---

## 完成标准（质量门控）

episode 的 status 改为 `"done"` 的唯一条件：

- [ ] A1–A6 全部 `"done"`
- [ ] **A7 质检通过**（无夸大承诺、无敏感词、引流表述合规）

A7 未通过 → 对应 Agent 任务退回 `"pending"`，重新执行。

---

## Agent 任务定义

| Agent | 输入 | 输出 | 完成标准 |
|-------|------|------|----------|
| A1 | 赛道+人群 | 选题+爆点角度+标题备选 | 有3个以上标题备选 |
| A2 | 选题 | 5个可验证来源+关键摘录 | 每条摘录有出处 |
| A3 | A2资料包 | 观点-证据-边界一页纸 | 每条观点有来源标注 |
| A4 | A3结论 | 双人播客脚本大纲 | 含开场钩子+CTA |
| A5 | A3结论+选题 | 标题×10+正文+9张分镜 | CTA合规 |
| A6 | 选题+产品 | 欢迎语+7天SOP+分流话术 | 无硬广表达 |
| A7 | A4+A5+A6全部输出 | 质检报告 | 0个高风险项 |

---

## 新增一期的流程

在 `content-progress.json` 的 `episodes` 数组中追加：

```json
{
  "id": "ep02",
  "topic": "[填入选题]",
  "keyword": "[填入私域关键词]",
  "file": "期刊/第02期-xxx.md",
  "status": "pending",
  "agents": {
    "A1": { "status": "pending", "note": "" },
    "A2": { "status": "pending", "note": "" },
    "A3": { "status": "pending", "note": "" },
    "A4": { "status": "pending", "note": "" },
    "A5": { "status": "pending", "note": "" },
    "A6": { "status": "pending", "note": "" },
    "A7": { "status": "pending", "note": "" }
  }
}
```
