---
title: CSS 核心概念
type: concept
domain: [编程语言, 前端]
tags: [CSS, 选择器, 布局, 盒模型, 动画, 变量, BEM]
source: web
created: 2026-02-15
updated: 2026-02-16
status: draft
next_review: 2026-03-01
interval: 1
ease: 2.5
reps: 0
---

# CSS 核心概念

## TL;DR

CSS（Cascading Style Sheets）用于控制 HTML 元素的样式。核心机制包括：选择器匹配、盒模型布局、特异性计算、层叠规则和继承。掌握这些基础才能避免样式冲突和布局问题。

## 背景与问题定义

### 为什么需要 CSS

HTML 负责结构，CSS 负责样式。没有 CSS，网页将只有原始的文本和元素堆砌。CSS 解决了以下核心问题：

1. **样式分离**：将内容与表现解耦
2. **复用性**：同一套样式可应用于多个页面
3. **响应式**：适配不同屏幕尺寸
4. **维护性**：集中管理样式，修改一处全局生效

### 常见痛点

| 痛点 | 本质原因 |
|------|----------|
| 样式不生效 | 特异性冲突 |
| 布局错乱 | 盒模型理解偏差 |
| 移动端适配差 | 响应式设计缺失 |
| 样式污染 | 缺乏作用域管理 |

## 选择器

### 基础选择器

```css
/* 元素选择器 */
p { color: blue; }

/* 类选择器 */
.box { padding: 10px; }

/* ID 选择器 */
#header { position: fixed; }

/* 通配符 */
* { margin: 0; }
```

### 属性与伪类

```css
/* 属性选择器 */
[type="text"] { border: 1px solid gray; }

/* 伪类 */
:hover { color: red; }
:first-child { margin-top: 0; }
:nth-child(2n) { background: #f0f0f0; }

/* 伪元素 */
::before { content: ""; }
::after { content: ""; }
```

### 选择器优先级（特异性）

| 类型 | 示例 | 权重 |
|------|------|------|
| ID | `#nav` | 1,0,0 |
| class/属性/伪类 | `.active`, `[type]` | 0,1,0 |
| 元素/伪元素 | `div`, `::before` | 0,0,1 |

```css
/* 权重计算示例 */
#nav .item a:hover  /* ID(1) + class(1) + element(1) = 1,2,1 */
```

## 盒模型

### 标准盒模型 vs IE 盒模型

```css
/* 标准盒模型（默认） */
box-sizing: content-box;
/* width = 内容宽度，不含 padding/border */

/* IE 盒模型 */
box-sizing: border-box;
/* width = 内容 + padding + border */
```

### 盒模型属性

```css
.box {
  margin: 10px;      /* 外边距 */
  padding: 15px;    /* 内边距 */
  border: 1px solid #ccc;  /* 边框 */
  width: 200px;     /* 宽度 */
  height: 100px;    /* 高度 */
}
```

## 布局系统

### Flexbox

```css
.container {
  display: flex;
  justify-content: space-between;  /* 主轴对齐 */
  align-items: center;             /* 交叉轴对齐 */
  gap: 10px;                       /* 间距 */
  flex-wrap: wrap;                 /* 换行 */
}

.item {
  flex: 1;           /* 伸展 */
  flex-shrink: 0;   /* 禁止收缩 */
}
```

### Grid

```css
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto;
  gap: 20px;
}

/* 区域布局 */
grid-template-areas:
  "header header header"
  "sidebar main main"
  "footer footer footer";
```

## 层叠与继承

### 层叠顺序（优先级从低到高）

1. **来源顺序**：同样特异性时，后定义的生效
2. **特异性**：ID > class > element
3. **重要性**：`!important` 最高

### 继承控制

```css
/* 强制继承 */
color: inherit;

/* 恢复初始值 */
color: initial;

/* 恢复浏览器默认 */
color: unset;
```

### 层叠层（Cascade Layers）

```css
@layer reset, components, utilities;

/* reset 层最先应用 */
@layer reset {
  * { margin: 0; }
}

/* utilities 层最后应用 */
@layer utilities {
  .mt-1 { margin-top: 1rem; }
}
```

## 常见坑

| 坑点 | 解决方案 |
|------|----------|
| 样式不生效 | 检查特异性是否被覆盖 |
| margin 折叠 | 使用 `overflow: hidden` 或 `padding` |
| Flex 项目不换行 | 检查 `flex-wrap` 和 `flex-shrink` |
| Grid 间隙不一致 | 统一使用 `gap` 而非 `margin` |
| 高度百分比失效 | 父元素需有明确高度 |
| CSS 变量不生效 | 检查定义作用域和变量名拼写（区分大小写） |
| z-index 无效 | 确认元素已定位（非 static），检查父级堆叠上下文 |
| 动画不触发 | 检查是否有初始状态和结束状态的差异 |
| transition 对 display 无效 | display 不支持过渡，可用 opacity + visibility 替代 |

## CSS 变量（自定义属性）

### 定义与使用

```css
:root {
  --primary-color: #3498db;
  --spacing-unit: 8px;
  --border-radius: 4px;
}

.button {
  background-color: var(--primary-color);
  padding: calc(var(--spacing-unit) * 2);
  border-radius: var(--border-radius);
}

/* 带默认值 */
.button {
  color: var(--text-color, #333);
}
```

### 动态修改（JS 操作）

```javascript
// 设置变量
document.documentElement.style.setProperty('--primary-color', '#e74c3c');

// 读取变量
const color = getComputedStyle(element).getPropertyValue('--primary-color');
```

## 过渡与动画

### Transition（过渡）

```css
.button {
  background-color: blue;
  transition: background-color 0.3s ease, transform 0.2s ease-in-out;
}

.button:hover {
  background-color: red;
  transform: scale(1.05);
}
```

### Animation（关键帧动画）

```css
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.element {
  animation: fadeInUp 0.5s ease-out forwards;
}

/* 复杂动画 */
.loading {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
```

## 定位系统

### Position 属性

```css
/* 相对定位（保留原位置） */
.relative { position: relative; top: 10px; left: 20px; }

/* 绝对定位（相对于最近的非 static 祖先） */
.absolute { position: absolute; top: 0; right: 0; }

/* 固定定位（相对于视口） */
.fixed { position: fixed; bottom: 20px; right: 20px; }

/* 粘性定位（滚动吸附） */
.sticky { position: sticky; top: 0; }
```

### z-index 堆叠上下文

```css
/* 创建新的堆叠上下文 */
.context {
  position: relative;
  z-index: 1;
  /* 或 opacity < 1, transform, filter 等 */
}

/* 子元素在父上下文中层叠 */
.child {
  position: absolute;
  z-index: 999; /* 只在父 context 内有效 */
}
```

> [!tip] z-index 只对定位元素（非 static）生效

## 现代 CSS 函数

### 响应式计算

```css
/* clamp: 最小值、首选值、最大值 */
.title {
  font-size: clamp(1.5rem, 5vw, 3rem);
}

/* min/max */
.container {
  width: min(100% - 2rem, 1200px);
  margin-inline: max(1rem, (100% - 1200px) / 2);
}
```

### 颜色函数

```css
/* oklch: 更好的颜色空间 */
.primary { color: oklch(60% 0.2 250); }

/* color-mix */
.mixed {
  background: color-mix(in oklch, blue 50%, red);
}
```

## BEM 命名规范

### 命名规则

```css
/* Block（块） */
.card { }

/* Element（元素） */
.card__title { }
.card__image { }
.card__content { }

/* Modifier（修饰符） */
.card--large { }
.card--dark { }
.card__button--disabled { }
```

### 示例

```html
<div class="card card--large">
  <h2 class="card__title">标题</h2>
  <img class="card__image" src="..." alt="...">
  <div class="card__content">
    <button class="card__button card__button--disabled">
      提交
    </button>
  </div>
</div>
```

## 性能优化

### 关键 CSS

```html
<!-- 内联关键 CSS -->
<style>
  /* 首屏必需的样式 */
  .header, .hero { ... }
</style>

<!-- 异步加载非关键 CSS -->
<link rel="preload" href="non-critical.css" as="style" onload="this.onload=null;this.rel='stylesheet'">
```

### 选择器性能

```css
/* 避免深层嵌套（从右向左解析） */
/* 差 */
.header .nav .menu .item a { }

/* 好 */
.nav-link { }

/* 避免通配符选择器 */
/* 差 */
.header * { margin: 0; }

/* 好 */
.header > * { margin: 0; }
```

### 硬件加速

```css
/* 开启 GPU 加速 */
.animated {
  will-change: transform, opacity;
  transform: translateZ(0);
}

/* 动画结束后移除 will-change */
.animated {
  will-change: auto;
}
```

## 示例

### 居中布局

```css
/* 水平垂直居中 */
.center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 绝对定位居中 */
.abs-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}
```

### 响应式断点

```css
/* 移动优先 */
.container {
  width: 100%;
}

@media (min-width: 768px) {
  .container {
    width: 750px;
  }
}

@media (min-width: 1024px) {
  .container {
    width: 970px;
  }
}
```

## 样式引入方式

| 方式 | 位置 | 示例 |
|------|------|------|
| 内联样式 | 标签内 | `<h1 style="color: red;">` |
| 内部样式 | `<style>` 标签 | `<style>h1 { color: blue; }</style>` |
| 外部样式 | `<link>` 引入 | `<link rel="stylesheet" href="style.css">` |

优先级：内联 > 内部 > 外部（后加载覆盖前同优先级规则）

## 面试追问

### 基础问题
1. **CSS 选择器优先级如何计算？** - ID > class > element，组合时累加
2. **什么是盒模型？** - content-box vs border-box 的区别
3. **Flex 和 Grid 的适用场景？** - 一维布局 vs 二维布局
4. **margin 折叠是什么？** - 垂直外边距合并现象
5. **如何实现垂直居中？** - Flex / Grid / 绝对定位 + transform

### 进阶问题
6. **CSS 变量和普通预处理器变量（Sass/Less）的区别？** - CSS 变量运行时可用，可动态修改；预处理器变量编译时确定
7. **z-index 为什么不生效？** - 只在定位元素上生效，受父级堆叠上下文限制
8. **BEM 命名规范的优点？** - 避免命名冲突、语义清晰、可维护性强
9. **transition 和 animation 的区别？** - transition 状态变化触发，animation 可自动播放、循环、控制进度
10. **clamp() 函数的作用？** - 设置最小值、首选值、最大值，实现流体排版

## References

- [MDN: CSS 自定义属性](https://developer.mozilla.org/zh-CN/docs/Web/CSS/--*)
- [MDN: CSS 过渡](https://developer.mozilla.org/zh-CN/docs/Web/CSS/transition)
- [MDN: CSS 动画](https://developer.mozilla.org/zh-CN/docs/Web/CSS/animation)
- [MDN: CSS 定位](https://developer.mozilla.org/zh-CN/docs/Web/CSS/position)
- [MDN: Cascade, specificity, and inheritance](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_and_inheritance)
- [MDN: Specificity](https://developer.mozilla.org/en-US/docs/Web/CSS/Specificity)
- [MDN: Cascade layers](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Cascade_layers)
- [BEM 命名规范](https://en.bem.info/methodology/naming-convention/)

---

【需要人工复核】：选择器优先级示例中的权重计算方式
