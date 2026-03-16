---
title: CSS - 核心概念是什么
aliases:
  - CSS 入门
  - 盒模型
  - 选择器
tags:
  - 前端
  - 前端/CSS
  - 面试题
type: note
domain: 前端
topic: CSS
question: CSS 核心概念是什么
source:
source_title:
created: 2026-02-15
updated: 2026-02-16
status: evergreen
---

# CSS - 核心概念是什么

## 一句话结论
CSS 控制 HTML 元素样式，核心包括：选择器、盒模型、特异性计算、层叠规则。

## 标准回答
- **选择器**：匹配 HTML 元素
- **盒模型**：内容 + 内边距 + 边框 + 外边距
- **特异性**：ID > 类 > 标签
- **层叠**：同优先级后胜出

## 为什么
HTML 负责结构，CSS 负责样式：
- 样式分离：内容与表现解耦
- 复用性：一套样式多页面使用
- 响应式：适配不同屏幕

## 盒模型
```
┌─────────────────────────────────┐
│            margin               │
│  ┌───────────────────────────┐  │
│  │        border             │  │
│  │  ┌─────────────────────┐  │  │
│  │  │      padding         │  │  │
│  │  │  ┌───────────────┐   │  │  │
│  │  │  │   content    │   │  │  │
│  │  │  └───────────────┘   │  │  │
│  │  └─────────────────────┘   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## 选择器优先级
| 优先级 | 选择器 | 示例 |
|---|---|---|
| 1 | 标签 | div |
| 10 | 类 | .box |
| 100 | ID | #header |
| 1000 | 内联 | style="" |

## Flex 布局
```css
.container {
    display: flex;
    justify-content: center;  /* 主轴居中 */
    align-items: center;      /* 交叉轴居中 */
}
```

## 易错点
- box-sizing: border-box 更好控制尺寸
- float 已淘汰，用 flex/grid
- margin 垂直方向会折叠
- !important 慎用，破坏优先级

## 延伸链接
- [[HTML - 核心概念]]
- [[CSS - Flex 布局]]

## 参考来源
- MDN Web Docs
