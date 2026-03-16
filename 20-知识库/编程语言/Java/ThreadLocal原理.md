---
title: Java - ThreadLocal 原理是什么
aliases:
  - ThreadLocal
  - 线程局部变量
tags:
  - Java
  - Java/并发
  - 面试题
type: note
domain: java
topic: 并发
question: ThreadLocal 原理是什么
source:
source_title:
created: 2026-02-18
updated: 2026-02-18
status: evergreen
---

# Java - ThreadLocal 原理是什么

## 一句话结论
ThreadLocal 为每个线程提供独立的变量副本，实现线程隔离，避免同步开销。但使用不当可能导致内存泄漏。

## 标准回答
- 每个 Thread 内部持有 ThreadLocalMap
- ThreadLocalMap 是定制 HashMap，key 是 ThreadLocal（弱引用），value 是变量副本
- get/set 通过当前线程获取/存储数据
- Entry 使用弱引用防止 ThreadLocal 无法回收
- 不手动 remove() 可能导致内存泄漏

## 为什么
多线程共享变量需要加锁保证线程安全，但加锁有性能开销。ThreadLocal 通过为每个线程创建独立副本，实现无锁的线程隔离。

## 代码示例
```java
public class ThreadLocalDemo {
    // 每个线程独立的变量副本
    ThreadLocal<String> userId = ThreadLocal.withInitial(() -> "default");

    public void setUser(String userId) {
        this.userId.set(userId);  // 只对当前线程可见
    }

    public String getUser() {
        return this.userId.get();  // 获取当前线程的值
    }

    public void remove() {
        this.userId.remove();  // 必须调用，防止内存泄漏
    }
}
```

### 代码说明
- `set()` 只对当前线程可见，其他线程访问不到
- `get()` 获取当前线程的值
- `remove()` 清理数据，防止内存泄漏

## 内存泄漏风险
```
ThreadLocalMap Entry 结构：
key (ThreadLocal<?>) → 弱引用，可能被 GC 回收
value → 强引用，如果不 remove()，会一直存在
```

**风险场景**：线程池中线程复用，不 remove() 会导致数据残留。

## 易错点
- 线程池场景必须手动 remove()
- ThreadLocal 只能解决线程隔离，不能解决线程间通信
- 误用会导致内存泄漏
- Spring 事务管理大量使用 ThreadLocal

## 延伸链接
- [[Java - volatile 关键字的作用]]
- [[Java - 线程池原理]]

## 参考来源
- JDK 官方文档
- 《Java 并发编程实战》
