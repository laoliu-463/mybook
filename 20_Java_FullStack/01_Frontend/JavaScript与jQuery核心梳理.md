这是一份 **JavaScript (ES6+) 与 jQuery** 的核心知识结构化梳理。

JavaScript 是 Web 的编程语言，而 jQuery 是它的经典类库。
**现代开发趋势：** 新项目首选原生 ES6+，但维护旧项目或追求极简 DOM 操作时，jQuery 依然好用。

---

### 🚀 第一板块：ES6+ 现代语法核心 (Modern JS)

**关注点：** 告别 `var`，拥抱更简洁、更安全的语法。

#### 1. 变量声明
* **`let`**：块级作用域，可修改。取代 `var`。
* **`const`**：常量，不可重新赋值（但如果存的是对象，对象内部属性可改）。

#### 2. 箭头函数 (Arrow Functions)
```javascript
// 旧写法
const sum = function(a, b) { return a + b; };

// 新写法 (更简洁，且不绑定 this)
const sum = (a, b) => a + b;
```

#### 3. 模板字符串 (Template Literals)
```javascript
const name = "Alice";
// 使用反引号 ``，支持换行和变量嵌入 ${}
console.log(`Hello, ${name}! 
Welcome to our site.`);
```

#### 4. 解构赋值 (Destructuring)
```javascript
const user = { id: 1, name: "Bob", age: 25 };
// 快速提取属性
const { name, age } = user; 
console.log(name); // "Bob"
```

#### 5. 模块化 (Modules)
* `export`：导出模块。
* `import ... from ...`：导入模块。

---

### 🌳 第二板块：DOM 操作 (原生 vs jQuery 对照)

**关注点：** 如何增删改查页面元素。

| 操作 | **原生 JavaScript (Modern)** | **jQuery** |
| :--- | :--- | :--- |
| **选取元素** | `document.querySelector('.box')` | `$('.box')` |
| **选取多个** | `document.querySelectorAll('li')` | `$('li')` |
| **修改文本** | `el.textContent = 'Hello'` | `el.text('Hello')` |
| **修改 HTML** | `el.innerHTML = '<b>Hi</b>'` | `el.html('<b>Hi</b>')` |
| **修改样式** | `el.style.color = 'red'` | `el.css('color', 'red')` |
| **添加类名** | `el.classList.add('active')` | `el.addClass('active')` |
| **移除类名** | `el.classList.remove('active')` | `el.removeClass('active')` |
| **事件监听** | `el.addEventListener('click', fn)` | `el.on('click', fn)` 或 `el.click(fn)` |
| **显示/隐藏** | `el.style.display = 'none'` | `el.hide()` / `el.show()` |

> **jQuery 核心优势：** 链式调用 (Chaining)。
> `$('.box').addClass('active').css('color', 'red').slideDown();`

---

### ⚡ 第三板块：jQuery 特色功能

**关注点：** jQuery 最擅长的领域，写起来比原生快很多。

#### 1. 动画效果
```javascript
// 淡入淡出
$('#msg').fadeIn(500);
$('#msg').fadeOut(500);

// 滑动折叠
$('.menu').slideUp();
$('.menu').slideDown();
```

#### 2. 文档就绪 (Ready)
防止 JS 在 HTML 加载完之前执行。
```javascript
// 简写形式
$(function() {
    console.log("DOM is ready!");
});
```

#### 3. 简化 Ajax
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

### ⏳ 第四板块：异步编程 (Asynchronous)

**关注点：** 处理耗时任务（如请求后端接口），避免界面卡死。

#### 1. Promise (承诺)
代表一个未来会结束的操作。
```javascript
const fetchData = new Promise((resolve, reject) => {
    // 模拟异步操作
    setTimeout(() => {
        resolve("Data loaded");
    }, 1000);
});

fetchData.then(data => console.log(data));
```

#### 2. async / await (终极解决方案)
基于 Promise，但写起来像同步代码，极易阅读。
```javascript
async function getData() {
    try {
        // 等待 fetch 结果回来，再往下执行
        let response = await fetch('https://api.example.com/user');
        let data = await response.json();
        console.log(data);
    } catch (error) {
        console.error("Oops:", error);
    }
}
```

---

### 💡 极简复习总结

1.  **变量：** 能用 `const` 就用 `const`，变的时候才用 `let`，别用 `var`。
2.  **选择器：** 原生用 `querySelector`，jQuery 用 `$`。
3.  **交互：** 简单的类名切换用 `classList` 或 `addClass/removeClass`。
4.  **Ajax：** 新项目用原生的 `fetch` 配合 `async/await`，旧项目用 `$.ajax`。
5.  **jQuery 现状：** 依然是快速开发原型和操作复杂 DOM 的利器，但在 React/Vue 等框架中通常不需要引入它。

