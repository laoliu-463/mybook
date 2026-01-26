---
title: "Java集合框架"
aliases: ["Java集合 八股", "Collections 面试", "集合源码"]
tags: [Java, 八股, Interview/高频, 索引, MOC, Collections]
created: 2026-01-26
level: interview
status: active
---

# Java集合框架

> [!summary] TL;DR
> - 一句话定义：Java 集合框架提供统一的数据结构接口与实现，包括 List、Set、Map 三大体系。
> - 面试一句话结论：ArrayList/HashMap 源码、线程安全集合是高频考点。
> - 关键点：底层数据结构、扩容机制、线程安全、fail-fast 机制。
>
> [!tip]
> **工程师思维自检**：
> 1. 我能说清楚 HashMap 的 put 流程吗？
> 2. 我能解释 ConcurrentHashMap 如何保证线程安全吗？

> [!ABSTRACT] 体系概览
> ```mermaid
> mindmap
>   root((集合框架))
>     Collection接口
>       List
>         ArrayList
>           数组实现
>           扩容1.5倍
>           随机访问O(1)
>         LinkedList
>           双向链表
>           增删O(1)
>           查找O(n)
>         Vector
>           线程安全
>           已过时
>       Set
>         HashSet
>           HashMap实现
>           无序不重复
>         LinkedHashSet
>           保持插入顺序
>         TreeSet
>           红黑树
>           有序
>       Queue
>         LinkedList
>         PriorityQueue
>         ArrayDeque
>     Map接口
>       HashMap
>         数组+链表+红黑树
>         扩容机制
>         hash计算
>         1.7 vs 1.8区别
>       LinkedHashMap
>         保持顺序
>         LRU实现
>       TreeMap
>         红黑树
>         有序Map
>       Hashtable
>         线程安全
>         已过时
>       ConcurrentHashMap
>         分段锁(1.7)
>         CAS+synchronized(1.8)
>     工具类
>       Collections
>       Arrays
>     线程安全
>       CopyOnWriteArrayList
>       ConcurrentHashMap
>       BlockingQueue
> ```

> [!INFO] 前世今生
> - **为什么需要集合框架**：统一接口让上层只关心“抽象类型”，不同实现可替换；同时提供常见数据结构的标准化实现与算法。
> - **工程关注点**：性能主要由“底层结构 + 扩容机制 + 访问/修改复杂度”决定；并发场景必须关注线程安全与一致性。
> - **面试关注点**：高频围绕 ArrayList/HashMap 的底层结构与扩容、并发集合的线程安全策略、fail-fast 触发条件。

> [!SUCCESS] 核心详解
> **集合三大体系定位**
> | 体系 | 典型特征 | 使用场景 |
> | :-- | :-- | :-- |
> | List | 有序、可重复、索引访问 | 需要顺序与随机访问 | 
> | Set | 无序、不重复 | 去重、集合运算 | 
> | Map | Key-Value 映射 | 快速检索、缓存 | 
>
> **关键机制清单**
> - **底层结构**：数组/链表/红黑树/散列表组合决定复杂度与空间成本。
> - **扩容机制**：容量增长与 rehash 会引发性能抖动。
> - **线程安全**：同步容器与并发容器的策略不同，影响吞吐与一致性。
> - **fail-fast**：结构性修改导致迭代器快速失败。

> [!EXAMPLE] 工业实验室
> 本笔记未提出“源码底层实现”请求，故不提供代码示例。

> [!QUESTION] 八股深挖
> 1. **问题：ArrayList 和 LinkedList 区别？**  
>    **答案：** ArrayList 底层数组，随机访问快；LinkedList 底层双向链表，插入删除快但查找慢。
> 2. **问题：ArrayList 扩容机制？**  
>    **答案：** 扩容为原容量的 1.5 倍，伴随数组复制，频繁扩容会带来性能波动。
> 3. **问题：HashMap 底层结构？**  
>    **答案：** 数组 + 链表 + 红黑树（链表过长且数组容量达到阈值时树化）。
> 4. **问题：HashMap 扩容？**  
>    **答案：** 容量翻倍后重新分配桶位置，影响性能。
> 5. **问题：HashMap 为什么线程不安全？**  
>    **答案：** 并发修改可能导致数据丢失或覆盖；旧版本还有扩容死循环风险。
> 6. **问题：ConcurrentHashMap 原理？**  
>    **答案：** 旧版本分段锁；新版本使用 CAS + synchronized 控制节点级并发。
> 7. **问题：fail-fast 是什么？**  
>    **答案：** 迭代时检测到结构修改立即抛出 ConcurrentModificationException。

---

## 知识体系总览

见上方 Mermaid 知识地图。

---

## 核心模块导航

### 1. List

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[ArrayList源码分析]] | 扩容机制/随机访问 | ⭐⭐⭐⭐⭐ |
| [[LinkedList源码分析]] | 双向链表/队列实现 | ⭐⭐⭐ |

**核心内容补全**：
- **ArrayList**：顺序存储，尾插通常较快；中间插入/删除需要移动元素；扩容会触发数组复制。
- **LinkedList**：节点分散存储，插入/删除只改指针；随机访问需遍历，性能随长度下降。
- **Vector**：线程安全但性能较低，已逐渐被并发集合替代。

**高频考点**：
- ArrayList 和 LinkedList 区别？
- ArrayList 扩容机制？
- 如何实现线程安全的 List？

### 2. Map

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[HashMap源码分析]] | put流程/扩容/红黑树 | ⭐⭐⭐⭐⭐ |
| [[ConcurrentHashMap源码分析]] | 线程安全实现 | ⭐⭐⭐⭐⭐ |
| [[LinkedHashMap与LRU]] | 顺序Map/LRU缓存 | ⭐⭐⭐⭐ |

**核心内容补全**：
- **HashMap**：散列到桶，碰撞用链表/红黑树处理；扩容带来 rehash 与性能抖动。
- **LinkedHashMap**：在 HashMap 基础上维护顺序，可用于 LRU。
- **TreeMap**：有序映射，基于红黑树，适合范围查询。
- **Hashtable**：同步方法保证线程安全，但性能较差且设计过时。
- **ConcurrentHashMap**：并发友好，降低锁粒度，提高吞吐。

**高频考点**：
- HashMap 的 put 过程？
- HashMap 1.7 和 1.8 的区别？
- ConcurrentHashMap 如何保证线程安全？

### 3. Set

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[HashSet实现原理]] | 基于HashMap | ⭐⭐⭐ |
| [[TreeSet与比较器]] | 红黑树/Comparable | ⭐⭐⭐ |

**核心内容补全**：
- **HashSet**：底层依赖 HashMap，元素作为 Key；天然去重但无序。
- **LinkedHashSet**：在 HashSet 基础上保持插入顺序。
- **TreeSet**：有序集合，基于红黑树，适合排序与范围操作。

---

## 经典面试题速查

| 问题 | 简答 | 细化说明 |
| :--- | :--- | :--- |
| ArrayList vs LinkedList？ | 数组 vs 链表，随机访问 vs 增删效率 | ArrayList 适合读多写少；LinkedList 适合频繁插入删除但不适合随机访问 |
| HashMap 底层结构？ | 数组 + 链表 + 红黑树 | 发生 hash 冲突时用链表/红黑树；树化需满足阈值条件 |
| HashMap 扩容？ | 容量翻倍，重新 hash 分配位置 | 扩容成本高，适合预估容量避免频繁扩容 |
| HashMap 为什么线程不安全？ | 并发修改会数据丢失/覆盖 | 旧版本还存在扩容死循环风险 |
| ConcurrentHashMap 原理？ | 分段锁 / CAS + synchronized | 降低锁粒度，提高并发性能 |
| fail-fast 是什么？ | 迭代时结构修改抛异常 | 迭代器检测到 modCount 变化即抛异常 |

---

## 相关笔记（双向链接）

- [[Java基础]]
- [[Java并发编程]]
- [[数据结构与算法]]