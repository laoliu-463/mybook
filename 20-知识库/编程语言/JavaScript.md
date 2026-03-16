---
title: JavaScript - 核心概念是什么
aliases:
  - JS 入门
  - ES6
tags:
  - 前端
  - 前端/JavaScript
  - 面试题
type: note
domain: 前端
topic: JavaScript
question: JavaScript 核心概念是什么
source:
source_title:
created: 2026-02-17
updated: 2026-02-17
status: evergreen
---

# JavaScript - 核心概念是什么

## 一句话结论
JavaScript 是动态弱类型语言，核心机制包括：原型继承、闭包、事件循环、异步编程。ES6+ 引入块级作用域、类、Promise/async-await。

## 标准回答
- **原型继承**：基于原型链的继承模式
- **闭包**：函数访问外部作用域变量
- **事件循环**：单线程异步非阻塞模型
- **ES6+**：let/const、箭头函数、类、Promise

## 为什么
JavaScript 从网页脚本发展为全栈语言：
- 浏览器端：DOM 操作、事件处理
- 服务端：Node.js
- 移动端：React Native

## 核心概念

### 1. 变量提升
```javascript
console.log(a);  // undefined（不是报错）
var a = 5;

// let/const 不提升
// console.log(b); // ReferenceError
let b = 5;
```

### 2. 闭包
```javascript
function createCounter() {
    let count = 0;
    return function() {
        return ++count;
    };
}
const counter = createCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

### 3. 原型链
```javascript
function Person(name) {
    this.name = name;
}
Person.prototype.sayHi = function() {
    console.log('Hi, I'm ' + this.name);
};

const alice = new Person('Alice');
alice.sayHi(); // 继承自原型
```

### 4. 异步
```javascript
// Promise
fetch('/api')
    .then(res => res.json())
    .then(data => console.log(data));

// async/await
async function getData() {
    const res = await fetch('/api');
    const data = await res.json();
    console.log(data);
}
```

## 易错点
- `var` 可以重复声明，`let/const` 不行
- `this` 在箭头函数中不绑定
- Promise catch 要放在最后
- async/await 是语法糖，本质仍是异步

## 延伸链接
- [[JavaScript - Promise 原理]]
- [[JavaScript - 事件循环]]

## 参考来源
- MDN Web Docs
