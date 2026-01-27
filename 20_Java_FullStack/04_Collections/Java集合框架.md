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
> - 面试一句话结论：ArrayList/HashMap 源码与并发集合是高频考点；理解“结构 + 复杂度 + 扩容 + 线程安全”即可通关大部分问题。
> - 关键点：底层数据结构、扩容机制、时间复杂度、线程安全策略、fail-fast 机制。

> [!tip]
> **工程师思维自检**：
> 1. 我能清晰描述 HashMap 的 put/get 流程吗？
> 2. 我能说出 ArrayList 扩容带来的性能影响吗？
> 3. 我能解释 ConcurrentHashMap 的并发控制思路吗？

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
> - **为什么需要集合框架**：统一接口（Collection/Map）降低学习与切换成本；多种实现覆盖不同性能需求。
> - **工程关注点**：关注访问/修改复杂度、内存占用与扩容成本；并发场景关注可见性与一致性。
> - **面试关注点**：ArrayList/HashMap/ConcurrentHashMap 的结构与扩容、迭代器的 fail-fast 触发条件、红黑树树化/退化条件。

> [!SUCCESS] 核心详解
> **总体对比**
> | 体系 | 结构核心 | 是否有序 | 是否允许重复 | 典型场景 |
> | :-- | :-- | :-- | :-- | :-- |
> | List | 数组/链表 | 有序 | 允许 | 顺序存储、按索引访问 |
> | Set | Hash/Tree | 无序/有序 | 不允许 | 去重、集合运算 |
> | Map | Hash/Tree | 无序/有序 | Key 不重复 | 快速检索、缓存、映射 |
>
> **复杂度速记**
> | 操作 | ArrayList | LinkedList | HashMap/HashSet | TreeMap/TreeSet |
> | :-- | :-- | :-- | :-- | :-- |
> | 随机访问 | O(1) | O(n) | O(1) 平均 | O(log n) |
> | 插入/删除（中间） | O(n) | O(1) | O(1) 平均 | O(log n) |
> | 查找 | O(n) | O(n) | O(1) 平均 | O(log n) |
>
> **关键机制清单**
> - **扩容**：触发 rehash/数组复制，带来性能抖动。
> - **散列冲突**：链表/红黑树处理冲突，影响最坏复杂度。
> - **线程安全**：同步容器保证安全但牺牲吞吐；并发容器采用更细粒度策略。
> - **fail-fast**：迭代器检测到结构性修改立即抛异常。

> [!EXAMPLE] 工业实验室
> 未请求“源码底层实现”，本笔记不提供源码级示例。

> [!QUESTION] 八股深挖
> 1. **问题：ArrayList 和 LinkedList 区别？**  
>    **答案：** ArrayList 基于数组，随机访问快但中间插入慢；LinkedList 基于双向链表，插入删除快但随机访问慢。
> 2. **问题：ArrayList 扩容机制？**  
>    **答案：** 新容量为旧容量的 1.5 倍左右，数组复制成本高，频繁扩容会影响性能。
> 3. **问题：HashMap 底层结构？**  
>    **答案：** 数组 + 链表 + 红黑树（冲突严重时树化）。
> 4. **问题：HashMap 扩容触发条件？**  
>    **答案：** size 超过阈值（capacity * loadFactor）时触发扩容并 rehash。
> 5. **问题：HashMap 为什么线程不安全？**  
>    **答案：** 并发修改导致数据覆盖或丢失，旧版本还存在扩容死循环风险。
> 6. **问题：ConcurrentHashMap 的并发策略？**  
>    **答案：** JDK 7 分段锁；JDK 8 使用 CAS + synchronized 控制节点级并发。
> 7. **问题：fail-fast 是什么？**  
>    **答案：** 迭代过程中检测到结构性修改就抛 ConcurrentModificationException。

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

**详细讲解**：
- **ArrayList**：
  - 底层为可变长数组，索引访问 O(1)。
  - 追加元素通常是摊还 O(1)，中间插入/删除需要移动元素，O(n)。
  - 扩容需要新建数组并复制旧数据，扩容成本集中爆发。
- **LinkedList**：
  - 底层双向链表，插入/删除只需调整指针，O(1)。
  - 查找需要遍历，O(n)；不适合高频随机访问。
- **Vector**：
  - 与 ArrayList 类似，但方法同步，线程安全，性能较低。
  - 多数情况下已被并发集合替代。

**工程建议**：
- 读多写少、需要随机访问时用 ArrayList。
- 频繁插入/删除、访问模式偏顺序时用 LinkedList。
- 并发读多写少可用 CopyOnWriteArrayList。

**高频考点**：
- ArrayList 和 LinkedList 区别？
- ArrayList 扩容策略与性能影响？
- 线程安全 List 的实现方式？

### 2. Map

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[HashMap源码分析]] | put流程/扩容/红黑树 | ⭐⭐⭐⭐⭐ |
| [[ConcurrentHashMap源码分析]] | 线程安全实现 | ⭐⭐⭐⭐⭐ |
| [[LinkedHashMap与LRU]] | 顺序Map/LRU缓存 | ⭐⭐⭐⭐ |

**详细讲解**：
- **HashMap**：
  - 通过 hash 将 key 映射到桶；冲突时链表/红黑树处理。
  - 扩容触发 rehash，JDK 8 通过高位判断减少重算。
  - 负载因子越小冲突越少但空间浪费更多。
- **LinkedHashMap**：
  - 在 HashMap 基础上维护双向链表。
  - 可按插入顺序或访问顺序迭代，适合实现 LRU。
- **TreeMap**：
  - 基于红黑树，key 有序，适合范围查询。
- **Hashtable**：
  - 全表同步，线程安全但性能差且设计过时。
- **ConcurrentHashMap**：
  - 低锁粒度并发控制；高并发下吞吐优于同步 Map。

**高频考点**：
- HashMap 的 put/get 流程？
- HashMap 1.7 与 1.8 区别？
- LinkedHashMap 如何实现 LRU？
- ConcurrentHashMap 如何保证线程安全？

### 3. Set

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[HashSet实现原理]] | 基于HashMap | ⭐⭐⭐ |
| [[TreeSet与比较器]] | 红黑树/Comparable | ⭐⭐⭐ |

**详细讲解**：
- **HashSet**：
  - 基于 HashMap，元素作为 key，天然去重。
  - 无序，平均查找 O(1)。
- **LinkedHashSet**：
  - 保持插入顺序，适合需要“去重 + 维持顺序”的场景。
- **TreeSet**：
  - 基于红黑树，有序集合，支持范围操作。

**高频考点**：
- HashSet 为什么能去重？
- TreeSet 排序依赖什么？

### 4. Queue

**详细讲解**：
- **PriorityQueue**：
  - 基于堆实现，最小/最大优先级出队。
  - 适合调度、TOP K 等场景。
- **ArrayDeque**：
  - 基于循环数组的双端队列，性能优于 LinkedList 作为队列使用。
- **BlockingQueue**：
  - 并发场景常用，支持阻塞 put/take。

---

## 经典面试题速查

| 问题 | 简答 | 细化说明 |
| :--- | :--- | :--- |
| ArrayList vs LinkedList？ | 数组 vs 链表 | ArrayList 适合读多写少；LinkedList 适合频繁插入删除 |
| ArrayList 扩容？ | 1.5 倍左右 | 扩容会数组复制，建议预估容量 |
| HashMap 底层结构？ | 数组 + 链表 + 红黑树 | 树化需链表长度与容量条件 |
| HashMap 扩容？ | 容量翻倍，rehash | 影响性能，频繁扩容不推荐 |
| HashMap 线程不安全？ | 并发修改导致问题 | 旧版本可能死循环，现版本数据覆盖 |
| ConcurrentHashMap 原理？ | CAS + synchronized | 锁粒度更细，提高并发吞吐 |
| fail-fast 是什么？ | 结构修改抛异常 | 迭代器检测 modCount 改变 |

---

## 相关笔记（双向链接）

- [[Java基础]]
- [[Java并发编程]]
- [[数据结构与算法]]