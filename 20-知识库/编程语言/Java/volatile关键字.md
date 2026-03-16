---
title: Java - volatile 关键字的作用是什么
aliases:
  - volatile
  - volatile 可见性
  - volatile 有序性
tags:
  - Java
  - Java/并发
  - 面试题
type: note
domain: java
topic: 并发
question: volatile 关键字的作用是什么
source:
source_title:
created: 2026-02-18
updated: 2026-02-18
status: evergreen
---

# Java - volatile 关键字的作用是什么

## 一句话结论
volatile 是 Java 并发轻量级关键字，保证变量的**可见性**和**有序性**，但不保证**原子性**。

## 标准回答
- **可见性**：写 volatile 变量立即刷新到主内存，读从主内存获取最新值
- **有序性**：禁止指令重排序（通过内存屏障实现）
- **不保证原子性**：i++ 等复合操作仍不安全
- **happens-before**：对 volatile 的写 happens-before 后续读

## 为什么
Java 线程有自己的工作内存（本地缓存），普通变量修改可能只存在工作内存中，对其他线程不可见。volatile 通过内存屏障强制刷新到主内存，解决可见性问题。

## 对比
| 特性 | volatile | synchronized |
|---|---|---|
| 作用范围 | 变量 | 代码块/方法 |
| 可见性 | ✅ | ✅ |
| 有序性 | ✅ | ✅ |
| 原子性 | ❌ | ✅ |
| 性能 | 高 | 低 |

## 代码示例
```java
public class VolatileDemo {
    // 状态标志：一个线程写，多个线程读
    volatile boolean running = true;

    public void stop() {
        running = false;  // 立即刷新到主内存
    }

    public void run() {
        while (running) {
            // 能看到最新的 running 值
        }
    }
}
```

### 代码说明
- `volatile` 保证线程 B 能看到线程 A 对 `running` 的修改
- 如果不用 volatile，线程 B 可能一直循环（读到旧值）

### 不适用场景
```java
volatile int count = 0;

// ❌ 不安全：i++ 是复合操作（读-改-写）
count++;

// ✅ 安全：使用原子类
AtomicInteger count = new AtomicInteger(0);
count.incrementAndGet();
```

## 易错点
- volatile 不能保证 i++ 等复合操作的线程安全
- 只能修饰变量，不能修饰方法或代码块
- 双重检查锁定（DCL）单例中必须用 volatile，防止指令重排序
- 读多写少场景适合 volatile

## 延伸链接
- [[Java - synchronized 和 ReentrantLock 有什么区别]]
- [[Java - happens-before 规则]]

## 参考来源
- 《Java 并发编程实战》
- JDK 官方文档
