---
title: Maven 安装与配置指南
date: 2026-01-12
tags: [Java, Maven, 环境配置]
status: 进行中
---

# Maven 安装与配置指南（零基础友好版）

> 目标：在 Windows 上安装 Maven，配置环境变量和本地仓库，确保能正常运行 `mvn`。

---

## 适合人群

- 第一次搭建 Java 开发环境的人
- 不熟环境变量设置的人

---

## 先确认：你已安装 JDK

在命令行运行：
```bash
java -version
```
如果能看到 Java 版本信息，说明 JDK 安装成功。否则先安装 JDK 再继续。

---

## 1. 下载与安装

1. 访问 [Maven 官网](https://maven.apache.org/download.cgi)
2. 下载 `Binary zip archive`（例如 `apache-maven-3.9.x-bin.zip`）
3. 解压到：
   - `D:\DevTools\Maven\apache-maven-3.9.x`

> 记住这个路径，后面会用到。

---

## 2. 环境变量配置

### 2.1 新建 MAVEN_HOME
- 变量名：`MAVEN_HOME`
- 变量值：`D:\DevTools\Maven\apache-maven-3.9.x`

### 2.2 修改 Path
在 `Path` 中新增：
```
%MAVEN_HOME%\bin
```

---

## 3. 配置本地仓库（可选但推荐）

目的：节省 C 盘空间并统一管理依赖。

1. 创建目录：`D:\Repositories\MavenRepo`
2. 编辑文件：`%MAVEN_HOME%\conf\settings.xml`
3. 添加配置：
```xml
<localRepository>D:\Repositories\MavenRepo</localRepository>
```

---

## 4. 配置阿里云镜像（国内推荐）

在 `settings.xml` 的 `<mirrors>` 节点内添加：
```xml
<mirror>
    <id>aliyunmaven</id>
    <mirrorOf>*</mirrorOf>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
</mirror>
```

---

## 5. 验证安装

```bash
mvn -v
```

如果输出包含 **Apache Maven** 版本信息和 **Java version**，说明安装成功。

---

## 6. Maven 常用命令（新手常用）

| 命令 | 说明 |
| :--- | :--- |
| `mvn clean` | 清理项目，删除 `target/` |
| `mvn compile` | 编译主源代码 |
| `mvn test` | 运行单元测试 |
| `mvn package` | 打包项目 |
| `mvn install` | 安装到本地仓库 |
| `mvn clean install -DskipTests` | 常用：清理并安装，跳过测试 |

---

## 7. Maven 核心概念速记

### 标准目录结构
- `src/main/java`：主源码
- `src/main/resources`：资源文件
- `src/test/java`：测试源码
- `target/`：编译输出
- `pom.xml`：项目配置文件

### GAV 坐标
- **GroupId**：组织标识（如 `com.google`）
- **ArtifactId**：模块名称（如 `guava`）
- **Version**：版本号（如 `31.0.1-jre`）

### 依赖范围（Scope）
- `compile`：默认，全阶段有效
- `test`：只在测试阶段有效
- `provided`：运行时由容器提供
- `runtime`：运行时有效，编译时不需要

---

## 常见问题

### 1. 终端提示 “mvn 不是内部或外部命令”
通常是 `Path` 没配置好，确认是否加入了 `%MAVEN_HOME%\bin`。

### 2. 下载依赖非常慢
检查是否配置了镜像（如阿里云镜像）。

### 3. Java 版本不匹配
确认 `JAVA_HOME` 指向正确的 JDK 目录。
