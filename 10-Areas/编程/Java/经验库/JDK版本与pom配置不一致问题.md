---
type: experience-card
category: bug-fix
source: "[[20-Projects/P01-hmdp黑马点评/00-项目看板]]"
created: 2026-01-28
tags:
  - JDK
  - Maven
  - 版本兼容
  - 踩坑
---

# JDK 版本与 pom.xml 配置不一致问题

## 🎯 场景
> 克隆老项目后，本地 JDK 版本与项目 pom.xml 配置的版本不一致

## 🔥 问题/需求
> - 本地环境：OpenJDK 17.0.1
> - 项目 pom.xml：配置为 Java 8
> - 现象：项目可能编译失败，或运行时出现版本不兼容错误

## ✅ 解决方案

### 方案 A：保持 Java 8（兼容模式）
```xml
<!-- pom.xml -->
<properties>
    <java.version>1.8</java.version>
</properties>

<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <configuration>
        <source>1.8</source>
        <target>1.8</target>
    </configuration>
</plugin>
```
JDK 17 可向下兼容编译 Java 8 代码，大多数情况可直接运行。

### 方案 B：升级到 Java 17（推荐，若计划升级 Boot 3）
```xml
<properties>
    <java.version>17</java.version>
</properties>
```
**注意**：升级 Boot 3 必须使用 Java 17+，需同步修改。

### 检查清单
1. `java -version` 确认本地版本
2. 检查 `pom.xml` 中的 `<java.version>` 或 `maven-compiler-plugin`
3. 若不一致，决定是升级项目还是切换本地 JDK

## 💡 核心教训
> 克隆老项目后，**第一件事**检查 pom.xml 的 JDK 版本配置，避免后续莫名其妙的编译/运行错误。

## 🔗 相关
- [[Spring Boot 2→3 配置差异]]
- [[20-Projects/P01-hmdp黑马点评/00-项目看板]]
