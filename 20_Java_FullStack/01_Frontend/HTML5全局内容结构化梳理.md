---
title: HTML5 全局内容结构化梳理
date: 2026-01-12
tags: [HTML5, Frontend, 基础]
status: 进行中
---

# HTML5 全局内容结构化梳理（零基础友好版）

> HTML5 是“写网页的语言”，重点是**结构清晰**、**语义正确**、**更少 JS**。

---

## 学习目标

- 看懂常见 HTML5 标签做什么
- 能写出一个结构清晰的页面骨架
- 知道表单/多媒体/本地存储的基本用法

---

## 先理解 3 个概念

- **语义化标签**：标签名字说明它的意义（如 `<header>` 是页眉）。
- **表单控件**：输入框、按钮、日期选择等。
- **Web API**：浏览器提供给 JS 的能力（如定位、拖拽）。

---

## 第一板块：语义化结构 (Semantics)

**核心理念**：用正确的标签做正确的事，机器更容易读懂网页结构。

### 经典语义化布局
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>语义化页面示例</title>
</head>
<body>

    <!-- 页眉 -->
    <header>
        <h1>我的个人博客</h1>
        <nav>
            <a href="#">首页</a> | <a href="#">关于我</a>
        </nav>
    </header>

    <!-- 主要内容区域 -->
    <main>
        <article>
            <h2>HTML5 学习笔记</h2>
            <p>这是我的第一篇文章...</p>
        </article>

        <section>
            <h3>评论区</h3>
            <p>这里是评论...</p>
        </section>
    </main>

    <!-- 侧边栏 -->
    <aside>
        <h3>推荐链接</h3>
        <ul><li>Google</li></ul>
    </aside>

    <!-- 页脚 -->
    <footer>
        <p>&copy; 2026 My Blog. All rights reserved.</p>
    </footer>

</body>
</html>
```

---

## 第二板块：增强型表单 (Smart Forms)

**核心理念**：减少 JavaScript 校验，移动端体验更好。

```html
<form action="/submit" method="post">

    <!-- 邮箱校验 -->
    <label>邮箱：</label>
    <input type="email" name="email" required placeholder="请输入邮箱">

    <!-- 数字范围 -->
    <label>年龄 (18-99)：</label>
    <input type="number" min="18" max="99" step="1">

    <!-- 日期选择 -->
    <label>生日：</label>
    <input type="date" name="birthday">

    <!-- 滑块 -->
    <label>音量：</label>
    <input type="range" min="0" max="100" value="50">

    <!-- 搜索建议 -->
    <label>选择城市：</label>
    <input list="cities">
    <datalist id="cities">
        <option value="Beijing">
        <option value="Shanghai">
        <option value="Shenzhen">
    </datalist>

    <button type="submit">提交</button>
</form>
```

---

## 第三板块：多媒体与图形 (Multimedia & Graphics)

**核心理念**：不再依赖 Flash，浏览器原生支持音视频和绘图。

### 视频播放
```html
<video src="movie.mp4" controls autoplay muted loop width="400">
    您的浏览器不支持 video 标签。
</video>
```

### Canvas 简单绘图
```html
<canvas id="myCanvas" width="200" height="100" style="border:1px solid #000;"></canvas>

<script>
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");

    ctx.fillStyle = "#FF0000";
    ctx.fillRect(0, 0, 150, 75);
</script>
```

---

## 第四板块：本地存储 (Web Storage)

**核心理念**：比 Cookie 更大、更安全、更易用。

| 特性 | Cookie | localStorage | sessionStorage |
| --- | --- | --- | --- |
| 数据生命周期 | 可设置过期时间 | 永久有效 | 仅当前窗口有效 |
| 应用场景 | Session ID | 购物车/配置 | 临时表单数据 |

```javascript
localStorage.setItem("username", "JohnDoe");
let user = localStorage.getItem("username");
console.log(user);
localStorage.removeItem("username");
```

---

## 第五板块：核心 API (Web APIs)

**核心理念**：让网页拥有“原生 APP”能力。

### 地理定位
```javascript
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        console.log("纬度: " + position.coords.latitude);
        console.log("经度: " + position.coords.longitude);
    });
}
```

### 拖拽
```html
<div draggable="true" ondragstart="event.dataTransfer.setData('text/plain', 'This is text')">
    拖拽我试试
</div>
```

---

## 新手自测

1. 语义化标签有什么用？说出 3 个例子。
2. `localStorage` 和 `sessionStorage` 有什么区别？
3. 你能写出一个包含 `header/main/footer` 的页面结构吗？
