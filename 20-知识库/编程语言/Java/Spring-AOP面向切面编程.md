---
title: Spring AOP 面向切面编程
type: concept
domain: [编程语言, Java]
tags: [Spring, AOP, 面向切面编程, 代理模式]
source: web
created: 2026-02-27
status: review
---

## TL;DR

AOP（面向切面编程）是一种通过预编译方式和运行期动态代理实现统一维护的技术。主要概念包括：切面(Aspect)、通知(Advice)、切入点(Pointcut)、连接点(Jointpoint)、织入(Weaving)。Spring AOP基于代理模式实现，支持前置通知、后置通知、环绕通知、异常通知、最终通知五种类型。

## 背景与问题

分散在业务逻辑代码中的相同代码（如日志记录、事务管理、性能监控）导致：
- 代码重复，维护困难
- 业务逻辑与横切关注点耦合
- 难以修改和扩展

AOP理念：将分散在各业务模块中的相同代码通过**横向切割**方式抽取到独立模块，实现解耦。

## 核心机制

### AOP 术语

| 术语 | 说明 |
|------|------|
| **连接点 (Jointpoint)** | 程序中插入横切关注点的扩展点，Spring仅支持方法执行 |
| **切入点 (Pointcut)** | 选择相关连接点的模式，即连接点集合 |
| **通知 (Advice)** | 连接点上执行的行为（Before/After/Around等） |
| **切面 (Aspect)** | 通知+引入+切入点的组合，横切关注点的模块化 |
| **引入 (Introduction)** | 为已有类添加新字段或方法 |
| **目标对象 (Target)** | 需要被织入横切关注点的对象 |
| **织入 (Weaving)** | 将切面连接到目标对象的过程 |
| **AOP代理** | AOP框架创建的代理对象 |

### 通知类型

1. **前置通知 (Before)**：连接点之前执行，不能阻止流程
2. **后置通知 (After Returning)**：方法正常完成后执行
3. **异常通知 (After Throwing)**：方法抛出异常时执行
4. **最终通知 (After finally)**：无论正常还是异常退出都执行
5. **环绕通知 (Around)**：最强大，可在方法调用前后自定义行为

### Spring AOP 与 AspectJ 关系

- **AspectJ**：更强的AOP框架，实际意义上的AOP标准，支持编译期织入
- **Spring AOP**：纯Java实现，运行期动态代理，无侵入性
- Spring使用与AspectJ 5相同的注解，但运行时仍是纯Spring AOP

## 示例

### XML配置方式

```xml
<beans>
    <bean id="demoService" class="tech.pdai.springframework.service.AopDemoServiceImpl"/>
    <bean id="logAspect" class="tech.pdai.springframework.aspect.LogAspect"/>
    
    <aop:config>
        <aop:aspect ref="logAspect">
            <aop:pointcut id="pointCutMethod" expression="execution(* tech.pdai.springframework.service.*.*(..))"/>
            <aop:around method="doAround" pointcut-ref="pointCutMethod"/>
            <aop:before method="doBefore" pointcut-ref="pointCutMethod"/>
            <aop:after-returning method="doAfterReturning" pointcut-ref="pointCutMethod" returning="result"/>
            <aop:after-throwing method="doAfterThrowing" pointcut-ref="pointCutMethod" throwing="e"/>
            <aop:after method="doAfter" pointcut-ref="pointCutMethod"/>
        </aop:aspect>
    </aop:config>
</beans>
```

### AspectJ注解方式

```java
@Aspect
@Component
public class LogAspect {
    
    @Pointcut("execution(* tech.pdai.springframework.service.*.*(..))")
    public void pointCutMethod() {}
    
    @Before("pointCutMethod()")
    public void doBefore() {
        System.out.println("前置通知");
    }
    
    @AfterReturning(pointcut = "pointCutMethod()", returning = "result")
    public void doAfterReturning(Object result) {
        System.out.println("后置通知, 返回值: " + result);
    }
    
    @Around("pointCutMethod()")
    public Object doAround(ProceedingJoinPoint pjp) throws Throwable {
        System.out.println("环绕通知: 进入方法");
        Object o = pjp.proceed();
        System.out.println("环绕通知: 退出方法");
        return o;
    }
}
```

### 切入点表达式

- `execution(* com.demo.Service(..))` - 方法执行
- `within(com.demo.*)` - 某包下所有类
- `this(com.demo.Service)` - 代理对象为某类型
- `args(param)` - 参数匹配

## 常见问题

> [!tip] 切入点表达式建议使用execution而非within，后者粒度较粗

> [!warning] 环绕通知需注意调用proceed()，否则会跳过原方法

- **Spring AOP 和 AspectJ 区别**：Spring AOP基于代理（运行时），AspectJ编译时织入，功能更强大但侵入性高
- **JDK代理 vs CGLIB代理**：接口用JDK动态代理，类用CGLIB（Spring默认）

## References

- [Spring AOP - Spring Framework Docs](https://docs.spring.io/spring-framework/reference/core/aop.html)
- [pdai.tech - Spring核心之面向切面编程](https://pdai.tech/md/spring/spring-x-framework-aop.html)
