---
title: JavaScript 与 jQuery 核心梳理
date: 2026-01-12
tags: [JavaScript, jQuery, Frontend, 基础]
status: 进行中
---

# JavaScript 与 jQuery 核心梳理（零基础友好版）

> JavaScript 是网页的编程语言；jQuery 是帮助你更快操作 DOM 的经典库。

---

## 学习目标

- 理解 ES6+ 常用语法
- 能用原生 JS 操作页面元素
- 知道何时使用/不使用 jQuery

---

## 第一板块：ES6+ 现代语法核心

### 1. 变量声明
- `let`：块级作用域，可修改。
- `const`：常量，不可重新赋值（对象内部属性可改）。

### 2. 箭头函数
```javascript
const sum = (a, b) => a + b;
```

### 3. 模板字符串
```javascript
const name = "Alice";
console.log(`Hello, ${name}!`);
```

### 4. 解构赋值
```javascript
const user = { id: 1, name: "Bob", age: 25 };
const { name, age } = user;
```

### 5. 模块化
- `export`：导出模块
- `import ... from ...`：导入模块

---

## 第二板块：DOM 操作（原生 vs jQuery）

| 操作 | 原生 JavaScript | jQuery |
| :--- | :--- | :--- |
| 选取元素 | `document.querySelector('.box')` | `$('.box')` |
| 选取多个 | `document.querySelectorAll('li')` | `$('li')` |
| 修改文本 | `el.textContent = 'Hello'` | `el.text('Hello')` |
| 修改 HTML | `el.innerHTML = '<b>Hi</b>'` | `el.html('<b>Hi</b>')` |
| 修改样式 | `el.style.color = 'red'` | `el.css('color', 'red')` |
| 添加类名 | `el.classList.add('active')` | `el.addClass('active')` |
| 移除类名 | `el.classList.remove('active')` | `el.removeClass('active')` |
| 事件监听 | `el.addEventListener('click', fn)` | `el.on('click', fn)` |
| 显示/隐藏 | `el.style.display = 'none'` | `el.hide()` / `el.show()` |

---

## 第三板块：jQuery 常用功能

### 动画效果
```javascript
$('#msg').fadeIn(500);
$('#msg').fadeOut(500);
```

### 文档就绪
```javascript
$(function() {
    console.log("DOM is ready!");
});
```

### Ajax 请求
```javascript
$.ajax({
    url: '/api/data',
    type: 'GET',
    success: function(response) {
        console.log("Data:", response);
    },
    error: function(err) {
        console.error("Error:", err);
    }
});
```

---

## 第四板块：异步编程基础

### Promise
```javascript
const fetchData = new Promise((resolve) => {
    setTimeout(() => {
        resolve("Data loaded");
    }, 1000);
});

fetchData.then(data => console.log(data));
```

### async / await
```javascript
async function getData() {
    try {
        let response = await fetch('https://api.example.com/user');
        let data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Oops:", error);
    }
}
```

---

## 新手建议

1. 新项目优先用原生 JS（ES6+）。
2. 老项目或简单页面可以继续用 jQuery。
3. 先熟悉 `querySelector` / `addEventListener` 再看框架。

---

## 自测问题

1. `let` 和 `const` 有什么区别？
2. 如何在 JS 中给元素添加类名？
3. `async/await` 解决了什么问题？
