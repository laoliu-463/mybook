---
title: "MyBatis框架"
aliases: ["MyBatis 八股", "MyBatis 面试", "ORM"]
tags: [Java, 八股, Interview/高频, 索引, MOC, MyBatis]
created: 2026-01-26
level: interview
status: active
---

# MyBatis框架

> [!summary] TL;DR
> - 一句话定义：MyBatis 是半自动化 ORM 框架，通过 XML 或注解配置 SQL 映射。
> - 面试一句话结论：#{}/${}区别、缓存机制、动态 SQL、插件原理是高频考点。
> - 关键点：SQL 映射、参数绑定、缓存机制、延迟加载、插件拦截器。

> [!tip]
> **工程师思维自检**：
> 1. 我能解释 #{} 和 ${} 的区别吗？
> 2. 我能说清楚 MyBatis 一级缓存和二级缓存吗？

---

## 知识体系总览

```mermaid
mindmap
  root((MyBatis))
    核心组件
      SqlSessionFactory
      SqlSession
      Executor
        SimpleExecutor
        ReuseExecutor
        BatchExecutor
      StatementHandler
      ParameterHandler
      ResultSetHandler
      TypeHandler
    映射配置
      Mapper接口
      XML映射
      注解映射
      结果映射
        resultMap
        association
        collection
    参数处理
      #{}预编译
        防SQL注入
        类型安全
      ${}字符串替换
        动态表名
        ORDER BY
    动态SQL
      if
      choose/when/otherwise
      where/set/trim
      foreach
      bind
    缓存机制
      一级缓存
        SqlSession级别
        默认开启
        清除条件
      二级缓存
        namespace级别
        需要配置
        序列化要求
    延迟加载
      lazyLoadingEnabled
      aggressiveLazyLoading
      实现原理
    插件机制
      Interceptor接口
      拦截点
        Executor
        StatementHandler
        ParameterHandler
        ResultSetHandler
      分页插件
      SQL打印
    与Spring集成
      SqlSessionFactoryBean
      MapperScannerConfigurer
      @MapperScan
```

---

## 核心模块导航

### 1. 核心原理

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[MyBatis执行流程]] | 核心组件/执行过程 | ⭐⭐⭐⭐ |
| [[Mapper代理机制]] | 动态代理实现 | ⭐⭐⭐⭐ |

### 2. 参数与SQL

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[参数绑定机制]] | #{} vs ${} | ⭐⭐⭐⭐⭐ |
| [[动态SQL详解]] | if/foreach/where | ⭐⭐⭐⭐ |

### 3. 缓存机制

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[MyBatis缓存机制]] | 一级/二级缓存 | ⭐⭐⭐⭐⭐ |

### 4. 高级特性

| 笔记 | 核心内容 | 面试频率 |
| :--- | :--- | :--- |
| [[MyBatis插件原理]] | 拦截器链 | ⭐⭐⭐⭐ |
| [[延迟加载原理]] | 懒加载实现 | ⭐⭐⭐ |

---

## 经典面试题速查

| 问题 | 简答 |
| :--- | :--- |
| #{} 和 ${} 区别？ | #{} 预编译防注入，${} 字符串替换用于动态列名 |
| MyBatis 执行流程？ | SqlSession → Executor → StatementHandler → 数据库 |
| 一级缓存作用域？ | SqlSession 级别，默认开启，commit/close/update 清除 |
| 二级缓存作用域？ | namespace 级别，需配置，对象需序列化 |
| 延迟加载原理？ | CGLIB 代理，访问关联属性时触发查询 |
| 插件原理？ | 责任链模式，拦截四大核心对象 |
| resultMap 作用？ | 复杂结果映射，支持嵌套对象和集合 |
| MyBatis vs Hibernate？ | 前者半自动灵活控制SQL，后者全自动 |

---

## 相关笔记（双向链接）

- [[Spring框架]]
- [[MySQL数据库]]
- [[Java基础]]
