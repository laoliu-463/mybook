---
title: "Spring IOC 原理"
type: concept
domain: [编程语言, Java]
tags: [Spring, IOC, 依赖注入]
source: note
created: 2026-03-10
status: draft
---

# Spring IOC 原理

IOC 分为控制反转和依赖注入。

控制反转通过将对象的创建交由 Spring IOC 框架容器决定，底层使用反射和工厂模式实现。

依赖注入是 IOC 的具体实现方式，确定 bean 所需的依赖（一个类正常工作所需要的所有对象及其变量）并进行对象的创建和查找，最后通过特定方式注入到目标 bean 中。

---

## TL;DR

- IOC = 控制反转 + 依赖注入
- 控制反转：将对象创建交给 Spring 容器
- 依赖注入：动态注入依赖对象

---

## Checklist

- [ ] 理解 IOC 和 DI 的区别
- [ ] 掌握 Spring IOC 容器的核心原理
- [ ] 了解反射和工厂模式在 IOC 中的应用
