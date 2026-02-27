---
title: HTML 核心概念
type: concept
domain: [编程语言, 前端]
tags: [HTML, 标签, 语义化, DOM]
source: web
created: 2026-02-16
status: draft
next_review: 2026-02-20
interval: 1
ease: 2.5
reps: 0
---

# HTML 核心概念

## TL;DR

HTML（HyperText Markup Language）是网页的骨架，通过标签描述页面结构和内容。核心包括：文档结构、块级/行内元素、语义化标签、表单交互。HTML5 引入了更多语义化标签和 API。

## 背景与问题定义

### 为什么需要 HTML

HTML 是 Web 的基石，解决了以下核心问题：

1. **结构描述**：用标签定义内容的层次和含义
2. **超链接**：通过锚点实现页面间跳转
3. **多媒体嵌入**：图片、音频、视频的原生支持
4. **表单交互**：用户输入和数据提交的基础

### 常见痛点

| 痛点 | 本质原因 |
|------|----------|
| 页面无样式时结构混乱 | 缺乏语义化标签 |
| SEO 效果差 | 未使用 header/nav/main 等语义标签 |
| 表单验证繁琐 | 未使用原生验证属性 |
| 可访问性差 | 缺少 alt/aria 等辅助属性 |

## 文档基础结构

### 标准 HTML5 模板

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
</head>
<body>
  <!-- 页面内容 -->
</body>
</html>
```

### 关键元素说明

| 元素 | 作用 |
|------|------|
| `<!DOCTYPE html>` | 声明 HTML5 文档类型 |
| `<html>` | 根元素，包含整个页面 |
| `<head>` | 元数据（字符集、视口、标题、外链资源） |
| `<body>` | 可见内容主体 |

## 块级与行内元素

### 块级元素（Block）

> 独占一行，可设置宽高

| 标签 | 用途 |
|------|------|
| `<div>` | 通用容器 |
| `<p>` | 段落 |
| `<h1>`~`<h6>` | 标题（1 最大） |
| `<ul>/<ol>` | 无序/有序列表 |
| `<li>` | 列表项 |
| `<header>/<footer>` | 页眉/页脚 |
| `<section>/<article>` | 文档分区/独立文章 |

### 行内元素（Inline）

> 不换行，宽高由内容决定

| 标签 | 用途 |
|------|------|
| `<span>` | 通用行内容器 |
| `<a>` | 超链接 |
| `<strong>/<em>` | 加粗/斜体（语义化） |
| `<img>` | 图片 |
| `<input>` | 输入框 |
| `<br>` | 换行 |

### 转换方式

```css
/* 块级 → 行内 */
display: inline;

/* 行内 → 块级 */
display: block;

/* 行内块级（可设宽高但不独占行） */
display: inline-block;
```

## 语义化标签（HTML5）

### 布局语义标签

```html
<header>
  <!-- 页眉：logo、导航 -->
</header>

<nav>
  <!-- 导航链接 -->
</nav>

<main>
  <!-- 页面主要内容（每页仅一个） -->
  <article>
    <!-- 独立文章 -->
  </article>
  
  <aside>
    <!-- 侧边栏/附加信息 -->
  </aside>
</main>

<footer>
  <!-- 页脚：版权、联系信息 -->
</footer>
```

### 语义化的好处

1. **SEO 优化**：搜索引擎更好理解页面结构
2. **可访问性**：屏幕阅读器更准确解析
3. **代码可读性**：开发者更易理解结构
4. **维护性**：结构清晰，易于修改

## 常用表单元素

### 基础输入

```html
<!-- 文本输入 -->
<input type="text" placeholder="请输入">

<!-- 密码 -->
<input type="password">

<!-- 邮箱（带格式验证） -->
<input type="email" required>

<!-- 数字 -->
<input type="number" min="0" max="100">

<!-- 日期选择器 -->
<input type="date">

<!-- 单选/多选 -->
<input type="radio" name="gender" value="male">
<input type="checkbox" name="hobby" value="reading">
```

### 表单结构

```html
<form action="/submit" method="POST">
  <label for="username">用户名：</label>
  <input id="username" name="username" required>
  
  <label for="country">国家：</label>
  <select id="country" name="country">
    <option value="cn">中国</option>
    <option value="us">美国</option>
  </select>
  
  <textarea name="comment" rows="4"></textarea>
  
  <button type="submit">提交</button>
</form>
```

## 多媒体标签

```html
<!-- 图片 -->
<img src="photo.jpg" alt="描述文字" width="300">

<!-- 音频 -->
<audio controls>
  <source src="music.mp3" type="audio/mpeg">
</audio>

<!-- 视频 -->
<video width="320" height="240" controls>
  <source src="movie.mp4" type="video/mp4">
</video>
```

## 常见坑

| 坑点 | 解决方案 |
|------|----------|
| `img` 没写 `alt` | 必须添加描述文字，SEO 和无障碍要求 |
| 表单 `label` 未关联 `input` | 使用 `for` 属性或包裹 |
| 滥用 `<div>` | 优先使用语义化标签（header/nav/main） |
| 表格用于布局 | 表格只用于数据展示，布局用 Flex/Grid |
| 行内元素嵌套块级元素 | HTML5 禁止，会导致布局异常 |

## 示例

### 完整页面结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>我的博客</title>
</head>
<body>
  <header>
    <h1>我的博客</h1>
    <nav>
      <a href="#home">首页</a>
      <a href="#about">关于</a>
    </nav>
  </header>
  
  <main>
    <article>
      <h2>文章标题</h2>
      <p>文章内容...</p>
    </article>
  </main>
  
  <footer>
    <p>&copy; 2026 版权所有</p>
  </footer>
</body>
</html>
```

## 面试追问

1. **HTML5 新特性有哪些？** - 语义标签、多媒体、Canvas、本地存储、地理定位
2. **块级和行内元素的区别？** - 是否独占一行、宽高设置
3. **什么是语义化？为什么重要？** - 结构含义清晰，利于 SEO 和无障碍
4. **`<strong>` 和 `<b>` 的区别？** - strong 是语义化强调，b 是纯样式
5. **如何实现图片懒加载？** - `loading="lazy"` 属性

## 知识网络

### 相关概念
- [[CSS]] - 样式控制
- [[JavaScript]] - 交互逻辑
- [[DOM]] - 文档对象模型

## References

- [MDN: HTML 基础](https://developer.mozilla.org/zh-CN/docs/Learn/HTML)
- [MDN: HTML 元素参考](https://developer.mozilla.org/zh-CN/docs/Web/HTML/Element)
- [HTML5 规范](https://html.spec.whatwg.org/)

---

【需要人工复核】：表单验证属性的浏览器兼容性

