---
name: sb-distill
description: 第二大脑-提取：基于笔记原文追加"核心洞见/执行摘要"，形成可复用资产；若缺来源则添加待确认警告。自动生成 Canvas 可视化。
invocation: user
---

# sb-distill - 提取技能

你正在执行 /sb-distill 或被调用 sb-distill skill。

## 目标
读取目标文件，在末尾**追加** `80-模板/Distill-模板.md` 的结构内容（不覆盖原文），并自动生成 Canvas 可视化。

## 参数
- 参数1：目标文件路径（必须）
- 参数2（可选）：
  - `--no-canvas`：跳过 Canvas 生成
  - `--canvas-type <type>`：指定 Canvas 类型（mindmap/flow/concept）

## 步骤（强制，自动执行）
1. 读取目标文件全文
2. 读取模板 `80-模板/Distill-模板.md`
3. 仅基于原文内容生成：
   - Executive Summary 3 句话（必须可落地、可复用、全中文）
   - 关键要点（2~6条）
   - 可复用资产（至少勾选 1 类，并给出内容草案）
4. 来源检查：
   - 如果原文没有"source/来源/链接/引用"信息，必须在模板中的 WARNING 段写：
     "待确认：来源缺失，建议将原材料导入 NotebookLM 验证后再下结论"
5. 将生成内容追加到文件末尾
6. **自动调用 /sb-visualize 生成 Canvas**（除非指定 --no-canvas）
7. 终端输出：
   - ✅ 已提取：<文件名>（已追加 Distill 区块）
   - ✅ 已生成 Canvas：<文件名>.canvas
   - 🎉 完整流程已完成

## 严谨性
- 禁止引入原文不存在的事实细节
- 不确定就写"待确认 + 核对方向"
- Canvas 只基于笔记实际内容生成
