---
title: HTML - 核心概念是什么
aliases:
  - HTML 入门
  - HTML5
tags:
  - 前端
  - 前端/HTML
  - 面试题
type: note
domain: 前端
topic: HTML
question: HTML 核心概念是什么
source:
source_title:
created: 2026-02-16
updated: 2026-02-16
status: evergreen
---

# HTML - 核心概念是什么

## 一句话结论
HTML（超文本标记语言）是网页骨架，通过标签描述页面结构。核心包括：文档结构、块级/行内元素、语义化标签、表单交互。

## 标准回答
- **标签**：HTML 基本组成单元
- **块级元素**：div、p、h1-h6、ul、li（独占一行）
- **行内元素**：span、a、img、input（不独占一行）
- **语义化标签**：header、nav、article、section、footer
- **表单**：用户输入和数据提交

## 为什么
HTML 定义网页内容和结构：
- 结构描述：标签定义内容层次
- 超链接：页面间跳转
- 多媒体：图片、音频、视频
- 表单交互：用户输入

## 对比
| 类型 | 特点 | 示例 |
|---|---|---|
| 块级元素 | 独占一行 | div, p, h1 |
| 行内元素 | 不独占一行 | span, a, img |
| 行内块元素 | 不独占一行但可设宽高 | button, input |

## 语义化标签
```html
<header>头部</header>
<nav>导航</nav>
<main>
    <article>
        <section>文章内容</section>
    </article>
</main>
<footer>底部</footer>
```

## 表单元素
```html
<form action="/submit" method="POST">
    <input type="text" name="username">
    <input type="email" name="email">
    <input type="password" name="password">
    <button type="submit">提交</button>
</form>
```

## 易错点
- div 是无意义块，语义化用 header/footer/main
- img 需要 alt 属性（无障碍）
- a 标签是链接，button 是按钮，别混用
- 表单提交需要 name 属性

## 延伸链接
- [[CSS - 盒模型]]
- [[JavaScript - DOM 操作]]

## 参考来源
- MDN Web Docs
