# News-Educator Review 操作规范

## Review 决策标准

### ✅ approve（批准）
必须同时满足 A≥2 且 B≥2

### ⏭️ skip（跳过）
版本发布/营销/无关内容

### ⚠️ needs-verify（需要核实）
来源可信但信息缺失/冲突

## 每日配额
- approve: 3~5条
- needs-verify: ≤2条
- 每周转正: 2张知识卡

## 操作流程
1. 打开候选包
2. 逐条勾选决策
3. 更新frontmatter: `gate: gate1_reviewed`
4. 对Claude说："我已 review，请发布"

---
*v1.0 | 2026-02-03*
