这是一份关于 **HTML5 全局内容**的结构化整理，附带**核心代码示例**。

HTML5 不仅仅是“新一代的 HTML”，它实际上是一个**技术集合**，包括了**新标签、新样式支持（CSS3）以及新的 JavaScript API**。对于新手来说，理解 HTML5 是从“写静态页面”向“开发 Web 应用”转变的关键。

---

### 🏗️ 第一板块：语义化结构 (Semantics)

**核心理念：** 用正确的标签做正确的事。机器（搜索引擎、屏幕阅读器）能读懂网页结构。

#### 1. 经典语义化布局
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

### 📝 第二板块：增强型表单 (Smart Forms)

**核心理念：** 减少 JavaScript 的校验工作，移动端体验更佳。

#### 1. 智能输入框示例
```html
<form action="/submit" method="post">
    
    <!-- 1. 邮箱校验 (手机端会弹出带 @ 的键盘) -->
    <label>邮箱：</label>
    <input type="email" name="email" required placeholder="请输入邮箱">
    
    <!-- 2. 数字范围 (min/max/step) -->
    <label>年龄 (18-99)：</label>
    <input type="number" min="18" max="99" step="1">

    <!-- 3. 日期选择器 (原生弹窗) -->
    <label>生日：</label>
    <input type="date" name="birthday">

    <!-- 4. 滑块 -->
    <label>音量：</label>
    <input type="range" min="0" max="100" value="50">

    <!-- 5. 搜索建议 (Datalist) -->
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

### 🎬 第三板块：多媒体与图形 (Multimedia & Graphics)

**核心理念：** 摆脱 Flash 插件，原生支持音视频和绘图。

#### 1. 视频播放
```html
<!-- 自动播放(muted静音才行)、循环、显示控件 -->
<video src="movie.mp4" controls autoplay muted loop width="400">
    您的浏览器不支持 video 标签。
</video>
```

#### 2. Canvas 简单绘图
```html
<canvas id="myCanvas" width="200" height="100" style="border:1px solid #000;"></canvas>

<script>
    var c = document.getElementById("myCanvas");
    var ctx = c.getContext("2d");
    
    // 画一个红色的矩形
    ctx.fillStyle = "#FF0000";
    ctx.fillRect(0, 0, 150, 75);
</script>
```

---

### 💾 第四板块：本地存储 (Web Storage)

**核心理念：** 比 Cookie 更大、更安全、更易用的客户端存储。

| 特性 | Cookie | localStorage | sessionStorage |
| --- | --- | --- | --- |
| **数据生命周期** | 可设置过期时间 | **永久有效** | **仅当前窗口有效** |
| **应用场景** | Session ID | 购物车/配置 | 临时表单数据 |

#### 代码示例
```javascript
// 1. 存数据 (键, 值)
localStorage.setItem("username", "JohnDoe");

// 2. 取数据
let user = localStorage.getItem("username");
console.log(user); // 输出: JohnDoe

// 3. 删数据
localStorage.removeItem("username");
// localStorage.clear(); // 清空所有
```

---

### ⚡ 第五板块：核心 API (Web APIs)

**核心理念：** 让网页拥有“原生 APP”的能力。

#### 1. 地理定位 (Geolocation)
```javascript
if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
        console.log("纬度: " + position.coords.latitude); 
        console.log("经度: " + position.coords.longitude);
    });
}
```

#### 2. 拖拽 (Drag and Drop)
```html
<div draggable="true" ondragstart="event.dataTransfer.setData('text/plain', 'This is text')">
    拖拽我试试
</div>
```

---

### 💡 极简复习总结 (考试/面试 必背点)

1. **语义化：** 知道 `<header>`, `<footer>`, `<section>`，为了 SEO 和可读性。
2. **多媒体：** 知道 `<video>` 和 `<audio>` 取代了 Flash。
3. **存储：** 必须分清 `Cookie` vs `localStorage` vs `sessionStorage` 的区别。
4. **文档声明：** HTML5 的声明非常简单：`<!DOCTYPE html>`。
5. **DOM 操作：** 新增了 `document.querySelector()` 和 `document.querySelectorAll()` (类似 jQuery 的选择器)。
