---
title: JavaScript 核心概念
type: concept
domain: [编程语言, 前端]
tags: [JavaScript, ES6, 闭包, 原型链, 异步, 事件循环, 作用域]
source: web
created: 2026-02-17
status: draft
next_review: 2026-02-21
interval: 1
ease: 2.5
reps: 0
---

# JavaScript 核心概念

## TL;DR

JavaScript 是一门动态弱类型语言，核心机制包括：原型继承、词法作用域、闭包、事件循环。ES6+ 引入块级作用域、类语法、Promise/async-await，使代码更易维护。理解执行上下文和单线程异步模型是掌握 JS 的关键。

## 背景与问题定义

### 为什么需要 JavaScript

JavaScript 最初设计用于网页交互，现已发展为全栈语言。它解决了：

1. **DOM 操作**：动态修改页面内容和样式
2. **事件处理**：响应用户交互（点击、输入、滚动）
3. **异步通信**：AJAX/Fetch 实现无刷新数据交换
4. **跨平台**：Node.js 扩展至服务端，Electron 支持桌面应用

### 常见痛点

| 痛点 | 本质原因 |
|------|----------|
| this 指向混乱 | 动态绑定，不同调用方式结果不同 |
| 变量提升 Bug | var 的函数作用域 + 提升机制 |
| 异步回调地狱 | 早期只有回调，代码嵌套过深 |
| 类型隐式转换 | == 的强制类型转换规则复杂 |
| 闭包内存泄漏 | 引用未被释放，导致内存占用 |

## 数据类型与变量

### 基本类型 vs 引用类型

```javascript
// 基本类型（值存储在栈中）
let str = 'hello';
let num = 42;
let bool = true;
let nil = null;
let und = undefined;
let sym = Symbol('desc');
let big = 9007199254740991n;

// 引用类型（值存储在堆中，变量存引用）
let obj = { name: 'Tom' };
let arr = [1, 2, 3];
let fn = function() {};
```

### var / let / const 对比

| 特性 | var | let | const |
|------|-----|-----|-------|
| 作用域 | 函数 | 块级 | 块级 |
| 变量提升 | 是（初始化为 undefined） | 否（暂时性死区） | 否 |
| 重复声明 | 允许 | 不允许 | 不允许 |
| 重新赋值 | 允许 | 允许 | 不允许 |

```javascript
// var 的坑：变量提升
console.log(a); // undefined（不会报错）
var a = 1;

// let 的暂时性死区
console.log(b); // ReferenceError
let b = 1;

// const 必须初始化
const c; // SyntaxError
const c = 1; // OK
```

## 作用域与闭包

### 词法作用域

```javascript
let global = 'global';

function outer() {
  let outerVar = 'outer';
  
  function inner() {
    let innerVar = 'inner';
    console.log(global);  // 可以访问
    console.log(outerVar); // 可以访问
  }
  
  inner();
}

outer();
```

### 闭包（Closure）

> 函数能够记住并访问其词法作用域，即使函数在当前作用域外执行

```javascript
function createCounter() {
  let count = 0;
  
  return {
    increment: () => ++count,
    decrement: () => --count,
    getCount: () => count
  };
}

const counter = createCounter();
console.log(counter.increment()); // 1
console.log(counter.increment()); // 2
console.log(counter.getCount());  // 2
```

### 闭包的应用场景

```javascript
// 1. 数据私有化（模拟私有变量）
function Person(name) {
  let _name = name; // 私有变量
  
  return {
    getName: () => _name,
    setName: (newName) => { _name = newName; }
  };
}

// 2. 函数柯里化
function add(a) {
  return function(b) {
    return a + b;
  };
}
const add5 = add(5);
console.log(add5(3)); // 8

// 3. 防抖 Debounce
function debounce(fn, delay) {
  let timer;
  return function(...args) {
    clearTimeout(timer);
    timer = setTimeout(() => fn.apply(this, args), delay);
  };
}
```

## this 绑定

### 四种绑定规则

```javascript
// 1. 默认绑定（非严格模式指向全局，严格模式 undefined）
function foo() {
  console.log(this);
}
foo(); // Window / undefined

// 2. 隐式绑定（谁调用指向谁）
const obj = {
  name: 'Tom',
  greet() {
    console.log(this.name);
  }
};
obj.greet(); // 'Tom'

// 3. 显式绑定（call/apply/bind）
function greet() {
  console.log(this.name);
}
const person = { name: 'Jerry' };
greet.call(person); // 'Jerry'

// 4. new 绑定
function Person(name) {
  this.name = name;
}
const p = new Person('Tom');
console.log(p.name); // 'Tom'
```

### 箭头函数的 this

```javascript
const obj = {
  name: 'Tom',
  // 普通函数：this 指向调用者
  greetNormal: function() {
    console.log(this.name); // 'Tom'
  },
  // 箭头函数：this 继承外层作用域
  greetArrow: () => {
    console.log(this.name); // undefined（继承全局作用域）
  }
};

// 箭头函数的经典用法
const obj2 = {
  name: 'Jerry',
  friends: ['Tom', 'Spike'],
  greetFriends() {
    // 这里的 this 指向 obj2
    this.friends.forEach(friend => {
      // 箭头函数继承 greetFriends 的 this
      console.log(`${this.name} says hi to ${friend}`);
    });
  }
};
```

## 原型链与继承

### 原型对象

```javascript
// 每个函数都有 prototype 属性
function Person(name) {
  this.name = name;
}

// 实例通过 __proto__ 访问原型
Person.prototype.greet = function() {
  console.log(`Hello, I'm ${this.name}`);
};

const tom = new Person('Tom');
tom.greet(); // 'Hello, I'm Tom'

// 原型链
console.log(tom.__proto__ === Person.prototype); // true
console.log(Person.prototype.__proto__ === Object.prototype); // true
console.log(Object.prototype.__proto__); // null
```

### ES6 Class 语法糖

```javascript
class Person {
  constructor(name) {
    this.name = name;
  }
  
  greet() {
    console.log(`Hello, I'm ${this.name}`);
  }
  
  // 静态方法
  static isPerson(obj) {
    return obj instanceof Person;
  }
}

class Student extends Person {
  constructor(name, grade) {
    super(name); // 调用父类构造函数
    this.grade = grade;
  }
  
  study() {
    console.log(`${this.name} is studying`);
  }
}

const student = new Student('Tom', 3);
student.greet(); // 继承自 Person
student.study(); // Student 自己的方法
```

## 异步编程

### 回调函数（Callback）

```javascript
// 传统回调方式
function fetchData(callback) {
  setTimeout(() => {
    const data = { id: 1, name: 'Tom' };
    callback(null, data);
  }, 1000);
}

fetchData((err, data) => {
  if (err) {
    console.error(err);
  } else {
    console.log(data);
  }
});
```

### Promise

```javascript
// 创建 Promise
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    const success = true;
    if (success) {
      resolve('Data loaded');
    } else {
      reject('Error');
    }
  }, 1000);
});

// 使用 Promise
promise
  .then(result => {
    console.log(result);
    return 'Next step';
  })
  .then(next => console.log(next))
  .catch(err => console.error(err))
  .finally(() => console.log('Done'));

// Promise.all / Promise.race
Promise.all([fetchUser(), fetchPosts()])
  .then(([user, posts]) => {
    console.log(user, posts);
  });
```

### async / await

```javascript
// 用 async/await 改写
async function loadData() {
  try {
    const user = await fetchUser();
    const posts = await fetchPosts(user.id);
    return { user, posts };
  } catch (err) {
    console.error('Failed to load:', err);
    throw err;
  }
}

// 并行执行
async function loadParallel() {
  const [user, posts] = await Promise.all([
    fetchUser(),
    fetchPosts()
  ]);
  return { user, posts };
}
```

## 事件循环（Event Loop）

### 执行模型

```javascript
console.log('1'); // 同步

setTimeout(() => {
  console.log('2'); // 宏任务
}, 0);

Promise.resolve().then(() => {
  console.log('3'); // 微任务
});

console.log('4'); // 同步

// 输出顺序：1 → 4 → 3 → 2
```

### 任务优先级

1. **同步代码**：直接执行
2. **微任务（Microtask）**：Promise.then/catch/finally, queueMicrotask, MutationObserver
3. **宏任务（Macrotask）**：setTimeout/setInterval, I/O, UI rendering

```javascript
// 复杂示例
console.log('script start');

setTimeout(() => {
  console.log('timeout 1');
}, 0);

Promise.resolve().then(() => {
  console.log('promise 1');
}).then(() => {
  console.log('promise 2');
});

setTimeout(() => {
  console.log('timeout 2');
}, 0);

console.log('script end');

// 输出：
// script start
// script end
// promise 1
// promise 2
// timeout 1
// timeout 2
```

## ES6+ 常用特性

### 解构赋值

```javascript
// 数组解构
const [a, b, ...rest] = [1, 2, 3, 4, 5];

// 对象解构
const { name, age = 18 } = { name: 'Tom' };

// 嵌套解构
const { user: { email } } = { user: { email: 'tom@example.com' } };

// 函数参数解构
function greet({ name, greeting = 'Hello' }) {
  console.log(`${greeting}, ${name}!`);
}
```

### 展开运算符

```javascript
// 数组展开
const arr1 = [1, 2];
const arr2 = [...arr1, 3, 4]; // [1, 2, 3, 4]

// 对象展开
const obj1 = { a: 1 };
const obj2 = { ...obj1, b: 2 }; // { a: 1, b: 2 }

// 函数参数
const nums = [1, 2, 3];
Math.max(...nums); // 3
```

### 模板字符串

```javascript
const name = 'Tom';
const age = 25;

// 多行字符串
const html = `
  <div>
    <h1>${name}</h1>
    <p>Age: ${age}</p>
  </div>
`;

// 标签模板
function highlight(strings, ...values) {
  return strings.reduce((result, str, i) => {
    const value = values[i] ? `**${values[i]}**` : '';
    return result + str + value;
  }, '');
}

const text = highlight`Hello ${name}, you are ${age} years old`;
```

### 模块化

```javascript
// math.js
export const add = (a, b) => a + b;
export const subtract = (a, b) => a - b;
export default class Calculator { }

// main.js
import Calculator, { add, subtract } from './math.js';
import * as math from './math.js';

// 动态导入
const module = await import('./math.js');
```

## 常见坑

| 坑点 | 解决方案 |
|------|----------|
| == 的隐式类型转换 | 始终使用 === 进行严格相等比较 |
| typeof null === 'object' | 用 `value === null` 判断 null |
| 数组/对象比较是引用比较 | 使用深度比较或序列化 |
| for...in 遍历数组得到字符串索引 | 数组用 for...of 或 forEach |
| setTimeout 延迟不准确 | 不用于精确计时，使用 Date 计算 |
| 闭包导致内存泄漏 | 及时释放不再使用的引用 |
| this 指向丢失 | 使用箭头函数或 bind |

## 示例

### 深拷贝实现

```javascript
function deepClone(obj, hash = new WeakMap()) {
  if (obj === null || typeof obj !== 'object') return obj;
  
  // 处理 Date
  if (obj instanceof Date) return new Date(obj);
  
  // 处理 RegExp
  if (obj instanceof RegExp) return new RegExp(obj);
  
  // 处理循环引用
  if (hash.has(obj)) return hash.get(obj);
  
  // 处理数组
  if (Array.isArray(obj)) {
    const arrCopy = [];
    hash.set(obj, arrCopy);
    obj.forEach((item, index) => {
      arrCopy[index] = deepClone(item, hash);
    });
    return arrCopy;
  }
  
  // 处理对象
  const objCopy = {};
  hash.set(obj, objCopy);
  Object.keys(obj).forEach(key => {
    objCopy[key] = deepClone(obj[key], hash);
  });
  
  return objCopy;
}
```

### 实现 Promise.all

```javascript
function myPromiseAll(promises) {
  return new Promise((resolve, reject) => {
    if (!Array.isArray(promises)) {
      return reject(new TypeError('Argument must be an array'));
    }
    
    const results = [];
    let completed = 0;
    
    if (promises.length === 0) {
      return resolve(results);
    }
    
    promises.forEach((promise, index) => {
      Promise.resolve(promise)
        .then(result => {
          results[index] = result;
          completed++;
          if (completed === promises.length) {
            resolve(results);
          }
        })
        .catch(reject);
    });
  });
}
```

## 面试追问

### 基础问题
1. **JS 有哪些数据类型？** - 7 种基本类型 + Object
2. **let/const/var 的区别？** - 作用域、提升、重复声明
3. **什么是闭包？应用场景？** - 函数+词法作用域，数据私有化、柯里化
4. **this 的绑定规则？** - 默认、隐式、显式、new 绑定
5. **== 和 === 的区别？** - 宽松相等会类型转换，严格相等不会

### 进阶问题
6. **原型链是什么？如何实现继承？** - __proto__ 链接，class extends
7. **事件循环机制？宏任务和微任务？** - 先同步→微任务→宏任务
8. **Promise 解决了什么问题？async/await 优势？** - 回调地狱，同步写法
9. **如何实现一个 new 操作符？** - 创建对象、绑定原型、绑定 this、返回对象
10. **防抖和节流的区别？** - 防抖是延迟执行，节流是间隔执行

## 知识网络

### 前置知识
- [[HTML]] - DOM 操作基础
- [[CSS]] - 样式操作

### 相关概念
- [[TypeScript]] - JS 的超集，类型系统
- [[React]] / [[Vue]] - 基于 JS 的框架
- [[Node.js]] - 服务端 JS 运行时

### 深入阅读
- [[V8 引擎原理]] - JS 执行机制
- [[前端性能优化]] - 代码优化实践

## References

- [MDN: JavaScript](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript)
- [MDN: 闭包](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Closures)
- [MDN: this](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Operators/this)
- [MDN: Promise](https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Promise)
- [MDN: async/await](https://developer.mozilla.org/zh-CN/docs/Learn/JavaScript/Asynchronous/Promises)
- [JavaScript.info](https://javascript.info/)
- [You Don't Know JS](https://github.com/getify/You-Dont-Know-JS)

---

【需要人工复核】：事件循环的执行顺序示例在最新规范下的行为
