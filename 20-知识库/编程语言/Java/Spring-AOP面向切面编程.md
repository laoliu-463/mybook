---
title: Spring - AOP 面向切面编程是什么
aliases:
  - AOP
  - Spring AOP
tags:
  - Java
  - Java/Spring
  - 设计模式
type: note
domain: java
topic: Spring
question: AOP 面向切面编程是什么
source: https://javaguide.cn
source_title:
created: 2026-02-27
updated: 2026-02-27
status: evergreen
---

# Spring - AOP 面向切面编程是什么

## 一句话结论
AOP（面向切面编程）通过横向切割方式，将分散在业务代码中的日志、事务等横切关注点抽取到独立模块，实现解耦。

## 标准回答
- **核心概念**：切面(Aspect)、通知(Advice)、切入点(Pointcut)、连接点(Jointpoint)、织入(Weaving)
- **通知类型**：前置、后置、环绕、异常、最终
- **实现方式**：Spring AOP 基于代理模式，AspectJ 支持编译期织入

## 为什么
业务代码中散落的日志、事务、权限等重复代码：
- 代码重复，维护困难
- 业务逻辑与横切关注点耦合
- 难以修改和扩展

AOP 将这些横切关注点抽取为独立切面，实现关注点分离。

## 对比
| 特性 | Spring AOP | AspectJ |
|---|---|---|
| 实现 | 动态代理 | 编译期/编译后织入 |
| 侵入性 | 无侵入 | 有侵入 |
| 性能 | 略低 | 更高 |
| 适用范围 | 方法级别 | 全部 |

## AOP 术语
| 术语 | 说明 |
|---|---|
| **连接点** | 程序中插入横切关注点的扩展点，Spring 仅支持方法执行 |
| **切入点** | 选择相关连接点的模式 |
| **通知** | 连接点上执行的行为（Before/After/Around） |
| **切面** | 通知 + 切入点的组合 |
| **织入** | 将切面连接到目标对象的过程 |

## 通知类型
1. **前置通知 (Before)**：方法执行前，不能阻止流程
2. **后置通知 (After Returning)**：方法正常完成后执行
3. **异常通知 (After Throwing)**：方法抛出异常时执行
4. **最终通知 (After finally)**：无论正常还是异常都执行
5. **环绕通知 (Around)**：最强大，可在方法调用前后自定义行为

## 代码示例
```java
@Aspect
@Component
public class LogAspect {
    // 切入点：匹配 controller 包下所有方法
    @Pointcut("execution(* com.example.controller..*.*(..))")
    public void controllerPointcut() {}

    // 环绕通知
    @Around("controllerPointcut()")
    public Object logAround(ProceedingJoinPoint joinPoint) {
        long start = System.currentTimeMillis();

        try {
            Object result = joinPoint.proceed();
            long cost = System.currentTimeMillis() - start;
            log.info("执行: {} 耗时: {}ms", joinPoint.getSignature(), cost);
            return result;
        } catch (Throwable e) {
            log.error("异常: {}", joinPoint.getSignature(), e);
            throw e;
        }
    }
}
```

### 代码说明
- `@Aspect` 声明这是一个切面
- `@Pointcut` 定义切入点表达式
- `@Around` 环绕通知，可以控制方法执行

## 易错点
- Spring AOP 只支持方法级别的代理
- 同一个类中方法互相调用不会触发代理（this 绑定问题）
- 私有方法无法被 AOP 增强
- 大量使用 AOP 会增加调试难度

## 延伸链接
- [[Spring - IoC 容器原理]]
- [[Java - 代理模式]]

## 参考来源
- Spring 官方文档
- JavaGuide: https://javaguide.cn
