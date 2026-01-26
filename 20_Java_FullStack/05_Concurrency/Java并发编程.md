---
title: "Java并发编程"
aliases: ["Java并发 八股", "JUC 面试", "多线程"]
tags: [Java, 八股, Interview/高频, 索引, MOC, Concurrency]
created: 2026-01-26
level: interview
status: active
---

# Java并发编程

> [!summary] TL;DR
> - 一句话定义：Java 并发编程通过多线程实现程序的并行执行，JUC 包提供丰富的并发工具。
> - 面试一句话结论：线程生命周期、锁机制、线程池是必考核心。
> - 关键点：synchronized/ReentrantLock、volatile、线程池、AQS、并发容器。

> [!tip]
> **工程师思维自检**：
> 1. 我能解释 synchronized 的锁升级过程吗？
> 2. 我能说清楚线程池的核心参数吗？

---

## 知识体系总览

```mermaid
mindmap
  root((并发编程))
    线程基础
      创建方式
        Thread
        Runnable
        Callable
        线程池
      生命周期
        NEW
        RUNNABLE
        BLOCKED
        WAITING
        TIMED_WAITING
        TERMINATED
      常用方法
        start/run
        sleep/yield
        join/interrupt
    锁机制
      synchronized
        对象锁/类锁
        锁升级
          无锁
          偏向锁
          轻量级锁
          重量级锁
        底层实现
      ReentrantLock
        公平/非公平
        可中断
        条件变量
      读写锁
        ReentrantReadWriteLock
        读读共享
        读写/写写互斥
    volatile
      可见性
      禁止重排序
      不保证原子性
    线程池
      核心参数
        corePoolSize
        maximumPoolSize
        keepAliveTime
        workQueue
        handler
      执行流程
      拒绝策略
      常用线程池
    AQS
      CLH队列
      state状态
      独占/共享模式
      Condition
    并发工具
      CountDownLatch
      CyclicBarrier
      Semaphore
      Exchanger
    并发容器
      ConcurrentHashMap
      CopyOnWriteArrayList
      BlockingQueue
    原子类
      AtomicInteger
      AtomicReference
      LongAdder
    ThreadLocal
      原理
      内存泄漏
      应用场景
```

---

## 核心模块导航

### 1. 线程基础

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[线程创建与生命周期]] | 创建方式/状态转换 | ⭐⭐⭐⭐ |
| [[线程通信机制]] | wait/notify/join | ⭐⭐⭐⭐ |

### 2. 锁机制

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[synchronized深入解析]] | 锁升级/底层实现 | ⭐⭐⭐⭐⭐ |
| [[ReentrantLock详解]] | 公平锁/AQS实现 | ⭐⭐⭐⭐⭐ |
| [[volatile关键字]] | 可见性/内存屏障 | ⭐⭐⭐⭐⭐ |

### 3. 线程池

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[线程池核心原理]] | 参数/执行流程/拒绝策略 | ⭐⭐⭐⭐⭐ |
| [[线程池最佳实践]] | 参数配置/监控 | ⭐⭐⭐⭐ |

### 4. JUC工具

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[AQS原理解析]] | CLH队列/state | ⭐⭐⭐⭐ |
| [[并发工具类]] | CountDownLatch/CyclicBarrier | ⭐⭐⭐⭐ |
| [[ThreadLocal原理]] | 实现/内存泄漏 | ⭐⭐⭐⭐⭐ |

---

## 经典面试题速查

| 问题 | 简答 |
| :--- | :--- |
| 线程创建方式？ | Thread/Runnable/Callable/线程池 |
| synchronized vs ReentrantLock？ | 前者JVM层面自动释放，后者API层面需手动释放，支持公平锁 |
| synchronized 锁升级？ | 无锁→偏向锁→轻量级锁→重量级锁，不可降级 |
| volatile 作用？ | 保证可见性和禁止重排序，不保证原子性 |
| 线程池核心参数？ | 核心线程数/最大线程数/存活时间/队列/拒绝策略 |
| 线程池执行流程？ | 核心线程→队列→非核心线程→拒绝策略 |
| ThreadLocal 原理？ | Thread 持有 ThreadLocalMap，key 是弱引用 |
| ThreadLocal 内存泄漏？ | key 被回收但 value 未清理，需手动 remove |

---

## 相关笔记（双向链接）

- [[Java基础]]
- [[JVM基础]]
- [[Java集合框架]]
