---
title: CSS3 全局内容结构化梳理
date: 2026-01-12
tags: [CSS3, Frontend, 基础]
status: 进行中
---

# CSS3 全局内容结构化梳理（零基础友好版）

> CSS3 让网页“好看且好布局”，重点是**选择器**、**布局**、**动画**。

---

## 学习目标

- 会写常用选择器
- 会用 Flex/Grid 布局
- 理解过渡与动画的区别

---

## 第一部分：选择器（选中元素的方式）

### 属性选择器
```css
input[type="text"] {
    border: 1px solid #ccc;
}

a[href^="https"] {
    color: green;
}
```

### 结构伪类
```css
tr:nth-child(odd) {
    background-color: #f9f9f9;
}

li:last-child {
    border-bottom: none;
}
```

### 状态伪类
```css
input:focus {
    outline: none;
    border-color: #3498db;
}

button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
```

### 伪元素
```css
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

## 第二部分：盒模型与视觉装饰

### 盒模型调整
```css
* {
    box-sizing: border-box;
}
```

### 视觉装饰
```css
.card {
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

---

## 第三部分：现代布局系统

### Flexbox（一维布局）
```css
.flex-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
```

### Grid（二维布局）
```css
.grid-container {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-gap: 20px;
}
```

---

## 第四部分：变换与动画

### 过渡
```css
.btn {
    transition: all 0.3s ease;
}
.btn:hover {
    transform: scale(1.1);
}
```

### 动画
```css
@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-icon {
    animation: spin 2s linear infinite;
}
```

---

## 第五部分：响应式设计

```css
@media screen and (max-width: 768px) {
    .container {
        flex-direction: column;
    }
    .sidebar {
        display: none;
    }
}
```

---

## 易混淆点速查

| 概念 | 作用 | 区别 |
| --- | --- | --- |
| Transform | 变形 | 改变形态，不脱离文档流 |
| Transition | 过渡 | 只有开始/结束，需要触发 |
| Animation | 动画 | 多个关键帧，可自动播放 |
| Display: none | 隐藏 | 元素消失，不占位置 |
| Visibility: hidden | 隐藏 | 元素不可见，但占位置 |

---

## 新手练习

1. 用 Flexbox 把一个按钮放到页面正中间。
2. 用 Grid 排成三列卡片。
3. 做一个 hover 时放大的按钮。
