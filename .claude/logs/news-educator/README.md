# News-Educator 测试与验收系统

## 系统架构

```
Gate0: 生成候选包 → 自动校验（白名单+Review复选框）
  ↓
Gate1: 人工 Review → 勾选 approve/skip/needs-verify
  ↓
Gate2: Publish → 生成日报+草稿卡+更新MOC
```

## 测试清单（一次性验收）

### 1. Gate0 测试：生成候选包

**触发指令**：
```
请根据 .claude/logs/news-educator/sources.yaml 生成今日候选包
目标文件：00-收集箱/News-Inbox/2026-02-03-candidates.md
```

**预期结果**：
- ✅ 所有 URL 只来自 `github.com` / `youtube.com` / `huggingface.co`
- ✅ 每条资讯包含来源链接
- ✅ 每条资讯有 Review 复选框：`[ ] approve` `[ ] skip` `[ ] needs-verify`
- ✅ **内容是"事故/争议/复盘/实战"，而非"版本更新流水账"**
- ✅ 自动校验通过（PostToolUse hook 输出 `✅ [news_validate] OK`）

**反例（应该被拦截）**：
- ❌ 出现 `reddit.com` / `twitter.com` / 短链
- ❌ 标题是 "PyTorch v2.3 Released" / "TypeScript 5.4 What's New"
- ❌ 缺少 Review 复选框

---

### 2. Gate1 测试：人工 Review

**操作步骤**：
1. 打开 `00-收集箱/News-Inbox/2026-02-03-candidates.md`
2. 只勾选 3 条：`[x] approve`
3. 其余标记 `[x] skip`

**触发指令**：
```
请将我勾选 approve 的条目发布到日报
```

**预期结果**：
- ✅ 日报只包含 3 条（你勾选的）
- ✅ 生成文件：`02-学习记录/01-日报/2026-02-03-Tech-News.md`

---

### 3. Gate2 测试：Publish + 草稿卡

**预期结果**：
- ✅ 日报文件生成（3 条资讯）
- ✅ 草稿卡生成：`00-收集箱/News-Knowledge-Drafts/2026-02-03-*.md`（2~3 张）
- ✅ `01-导航索引/News-MOC.md` 更新了"最近日报"链接

---

### 4. 极限输出测试

**触发指令**：
```
请将今日所有 approve 的资讯扩展成 10 张知识卡草稿
目标文件：.claude/logs/news-educator/big_output.md
每张卡 800-1500 字，分块写入，持续到完成
```

**预期结果**：
- ✅ 文件持续增长（每次分块写入 12k~20k 字）
- ✅ Stop hook 阻止过早停止（`⚠️ Output file only 2.3KB, continue...`）
- ✅ 最终文件 >5KB 后才允许停止

---

## 校验器说明

### `news_validate.py`（PostToolUse hook）
- **触发时机**：每次 Edit/Write 后自动运行
- **检查项**：
  1. URL 白名单（只允许 GitHub/YouTube/HF）
  2. Review 复选框存在性
  3. 版本流水账告警（命中 5+ 关键词）

### `stop_guard.py`（Stop hook，按需启用）
- **用途**：强制"极限输出"模式
- **启用方法**：在 `.claude/settings.json` 的 `hooks.Stop` 添加配置
- **行为**：文件 <5KB 时阻止 Claude 停止

---

## 常见问题

### Q: 如何临时禁用校验器？
A: 编辑 `.claude/settings.json`，注释掉 `PostToolUse` 部分

### Q: Stop hook 导致无限循环？
A: 检查 `big_output.md` 是否确实在增长。如果卡住，手动创建 >5KB 的文件即可放行

### Q: 白名单需要添加新域名？
A: 编辑 `news_validate.py` 的 `ALLOWED_DOMAINS` 集合

---

## 下一步

**现在你可以运行第一个测试**：
```
请生成今日候选包（Gate0）
```

校验器会自动运行，输出类似：
```
✅ [news_validate] OK: 2026-02-03-candidates.md
```

或者：
```
❌ [news_validate] FAIL: Non-whitelist domains found:
   - reddit.com in https://reddit.com/r/programming/...
```
