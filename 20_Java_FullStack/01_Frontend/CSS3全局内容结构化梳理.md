这是一份关于 **CSS3 全局内容**的结构化整理，附带**核心代码示例**。

CSS3 的核心变革在于：**更强大的选择器**、**模块化的布局系统**（不再依赖 float）以及**原生的动画支持**。

---

### 🎯 第一维度：高级选择器 (Selectors)

**关注点：** 精准选中你想要的元素，减少对 `class` 和 `id` 的过度依赖。

#### 1. 属性选择器
```css
/* 选中所有 type 为 text 的 input */
input[type="text"] {
    border: 1px solid #ccc;
}
/* 选中 href 以 https 开头的链接 (安全链接) */
a[href^="https"] {
    color: green;
}
```

#### 2. 结构伪类
```css
/* 表格隔行变色 */
tr:nth-child(odd) {
    background-color: #f9f9f9;
}
/* 选中列表的最后一个项，去掉底部边框 */
li:last-child {
    border-bottom: none;
}
```

#### 3. 状态伪类
```css
/* 当输入框获得焦点时 */
input:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 5px rgba(52, 152, 219, 0.5);
}
/* 禁用的按钮样式 */
button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
```

#### 4. 伪元素 `::`
```css
/* 在标题前加一个装饰性的竖线 */
h2::before {
    content: "";
    display: inline-block;
    width: 4px;
    height: 1em;
    background-color: red;
    margin-right: 8px;
}
```

---

### 📦 第二维度：现代盒模型与视觉装饰

**关注点：** 摆脱枯燥的矩形，无需 PS 也能做圆角和阴影。

#### 1. 盒模型调整 (Crucial)
```css
/* 【必背】全局设置：让 padding 和 border 包含在 width 之内 */
* {
    box-sizing: border-box;
}
```

#### 2. 视觉装饰
```css
.card {
    /* 圆角 */
    border-radius: 8px;
    /* 盒子阴影: x偏移 y偏移 模糊半径 颜色 */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    /* 渐变背景 */
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

### 📐 第三维度：现代布局系统 (Modern Layouts)

#### 1. Flexbox 弹性布局 (一维布局)
> 也就是后面实战演练的重点。

```css
.flex-container {
    display: flex;
    justify-content: space-between; /* 两端对齐 */
    align-items: center;            /* 垂直居中 */
}
```

#### 2. Grid 网格布局 (二维布局)
```css
.grid-container {
    display: grid;
    /* 定义三列，每列等宽 (1 fraction) */
    grid-template-columns: 1fr 1fr 1fr; 
    grid-gap: 20px; /* 间距 */
}
```

---

### 🎬 第四维度：变换与动画

#### 1. 过渡 (Transition)
```css
.btn {
    background-color: blue;
    /* 所有属性变化在 0.3s 内完成 */
    transition: all 0.3s ease;
}

.btn:hover {
    background-color: darkblue;
    /* 鼠标悬停时稍微放大 */
    transform: scale(1.1); 
}
```

#### 2. 动画 (Animation)
```css
/* 1. 定义剧本 */
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* 2. 调用剧本 */
.loading-icon {
    animation: spin 2s linear infinite; /* 无限循环旋转 */
}
```

---

### 📱 第五维度：响应式设计

```css
/* 当屏幕宽度小于 768px (手机模式) */
@media screen and (max-width: 768px) {
    .container {
        flex-direction: column; /* 原本横向排列的变成纵向 */
    }
    .sidebar {
        display: none; /* 隐藏侧边栏 */
    }
}
```

---

### 💡 极简复习总结表 (易混淆点)

| 概念 | 作用 | 区别 |
| --- | --- | --- |
| **Transform** | 变形 | 改变元素形态（旋转/位移），**不脱离文档流**，不影响其他元素位置。 |
| **Transition** | 过渡 | 只有**开始**和**结束**两个状态，需要触发（如 hover）。 |
| **Animation** | 动画 | 可以有**多个中间状态**（关键帧），可以自动播放和循环。 |
| **Display: None** | 隐藏 | 元素**消失**，不占位置（重排 Reflow）。 |
| **Visibility: Hidden** | 隐藏 | 元素**看不见**，但**占位置**（重绘 Repaint）。 |

---

### 🛠️ 实战演练：Flexbox 经典场景代码

这是你最需要掌握的两个布局，哪怕忘了别的，这两个也要背下来。

#### 场景 1：登录框完美居中
*需求：无论屏幕多大，登录框永远在正中间。*

```html
<div class="background">
    <div class="login-box">Login</div>
</div>

<style>
.background {
    height: 100vh; /* 占满全屏高度 */
    display: flex;
    justify-content: center; /* 主轴(横向)居中 */
    align-items: center;     /* 交叉轴(纵向)居中 */
    background-color: #f0f2f5;
}
.login-box {
    width: 300px;
    height: 200px;
    background: white;
    box-shadow: 0 0 10px rgba(0,0,0,0.1);
}
</style>
```

#### 场景 2：导航栏 (Logo 在左，菜单在右)
*需求：Logo 靠左贴边，菜单靠右贴边，中间留空。*

```html
<nav class="navbar">
    <div class="logo">MySite</div>
    <ul class="menu">
        <li>Home</li>
        <li>About</li>
    </ul>
</nav>

<style>
.navbar {
    display: flex;
    justify-content: space-between; /* 关键：子元素两端对齐 */
    align-items: center;            /* 垂直居中 */
    padding: 0 20px;
    height: 60px;
    background: #333;
    color: white;
}
.menu {
    display: flex; /* 菜单内部也用 flex 让 li 横向排列 */
    gap: 15px;     /* li 之间的间距 */
    list-style: none;
}
</style>
```
