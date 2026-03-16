---
title: Spring - IOC 容器原理是什么
aliases:
  - IOC
  - 依赖注入
  - DI
tags:
  - Java
  - Java/Spring
  - 面试题
type: note
domain: java
topic: Spring
question: Spring IOC 容器原理是什么
source:
source_title:
created: 2026-03-10
updated: 2026-03-10
status: evergreen
---

# Spring - IOC 容器原理是什么

## 一句话结论
IOC（控制反转）将对象创建交给 Spring 容器管理，通过依赖注入（DI）动态注入依赖，实现解耦。

## 标准回答
- **控制反转**：将对象创建权交给 Spring 容器
- **依赖注入**：动态注入依赖对象到目标 Bean
- **实现原理**：反射 + 工厂模式
- **注入方式**：构造器注入、Setter 注入、字段注入

## 为什么
传统开发中对象依赖硬编码，耦合度高。IOC 容器统一管理对象生命周期，实现：
- 降低耦合度
- 提高可测试性
- 便于单例/原型切换

## 对比
| 注入方式 | 优点 | 缺点 |
|---|---|---|
| 构造器注入 | 不可变、依赖必填 | 构造函数膨胀 |
| Setter 注入 | 灵活、可选依赖 | 可选依赖不明确 |
| 字段注入 | 简洁 | 不支持 final、难以测试 |

## IOC 容器工作流程
```
1. 扫描 Bean 定义（XML/注解）
   ↓
2. 解析并注册 BeanDefinition
   ↓
3. 实例化 Bean（反射）
   ↓
4. 依赖注入（属性填充）
   ↓
5. 生命周期回调（初始化）
   ↓
6. 放入容器缓存
```

## 代码示例
```java
// Service 层
@Service
public class UserService {
    private UserRepository userRepository;

    // 构造器注入（推荐）
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}

// Repository 层
@Repository
public class UserRepository {
    public User findById(Long id) {
        // 查询逻辑
        return new User();
    }
}
```

### 代码说明
- `@Service` 声明 Service 类为 Bean
- `@Repository` 声明 Repository 类为 Bean
- 构造器注入确保依赖不可变

## 易错点
- IOC 容器只管理单例 Bean（默认）
- 依赖注入发生在 Bean 初始化时
- 循环依赖会导致 BeanCurrentlyInCreationException
- 字段注入无法使用 final

## 延伸链接
- [[Spring - AOP 面向切面编程]]
- [[Spring - Bean 生命周期]]

## 参考来源
- Spring 官方文档
- JavaGuide
