---
title: Maven 安装与配置指南
date: 2026-01-12
tags: [Java, Maven, 环境配置]
status: 进行中
---

# 🚀 Maven 安装与配置指南

> [!info] 
> 本文档记录了在 D 盘搭建 Maven 开发环境的详细步骤，遵循项目约定的目录结构。

---

## 1. 下载与安装

1.  **下载**：访问 [Maven 官网](https://maven.apache.org/download.cgi) 下载最新版 `Binary zip archive` (例如 `apache-maven-3.9.x-bin.zip`)。
2.  **解压**：将压缩包解压到 `D:\DevTools\Maven\` 目录。
    *   📂 **目标路径**：`D:\DevTools\Maven\apache-maven-3.9.x`

## 2. 环境变量配置

> [!abstract] 环境变量设置
> 1. **MAVEN_HOME**:
>    - **变量名**：`MAVEN_HOME`
>    - **变量值**：`D:\DevTools\Maven\apache-maven-3.9.x` *(请根据实际文件夹名称调整)*
> 2. **Path**:
>    - 在 `Path` 变量中新建：`%MAVEN_HOME%\bin`

## 3. 配置本地仓库

为了节省 C 盘空间并统一管理依赖，将本地仓库迁移至 D 盘。

1.  **创建目录**：确保文件夹 `D:\Repositories\MavenRepo` 已手动创建。
2.  **修改配置**：
    - 编辑文件：`%MAVEN_HOME%\conf\settings.xml`
    - 找到 `<localRepository>` 节点，添加以下配置：
      ```xml
      <localRepository>D:\Repositories\MavenRepo</localRepository>
      ```

## 4. 配置阿里云镜像

> [!tip] 推荐配置
> 国内环境建议配置镜像加速，显著提升依赖下载速度。

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

在终端执行以下命令：

```bash
mvn -v
```

> [!success] 
> 如果输出中包含 **Apache Maven** 版本信息以及 **Java version**，则表示安装成功。

---

## 6. Maven 常用命令

| 命令 | 说明 |
| :--- | :--- |
| `mvn clean` | 清理项目，删除 `target/` 目录 |
| `mvn compile` | 编译主源代码 |
| `mvn test` | 运行单元测试 |
| `mvn package` | 打包项目（生成 jar/war 文件） |
| `mvn install` | 将包安装到本地仓库，供其他项目依赖 |
| `mvn deploy` | 将包发布到远程仓库（如私服） |
| `mvn dependency:tree` | 查看依赖树，用于排查依赖冲突 |
| `mvn clean install -DskipTests` | **常用**：清理并安装，跳过测试 |

---

## 7. Maven 核心知识点

### 📂 标准目录结构
Maven 遵循 **“约定优于配置”** (Convention over Configuration)：
- `src/main/java`: 存放主源码
- `src/main/resources`: 存放主资源文件
- `src/test/java`: 存放测试源码
- `target/`: 编译输出目录
- `pom.xml`: 项目核心配置文件 (Project Object Model)

### 📍 GAV 坐标
- **GroupId**: 组织标识（如 `com.google`）
- **ArtifactId**: 模块名称（如 `guava`）
- **Version**: 版本号（如 `31.0.1-jre`）

### ⚓ 依赖范围 (Scope)
- `compile`: 默认，全阶段有效。
- `test`: 仅测试阶段有效（如 JUnit）。
- `provided`: 运行时由容器（如 Tomcat）提供。
- `runtime`: 运行时有效，编译时不需要。

### 🔄 生命周期
1. **Clean**: 项目清理
2. **Default**: 构建核心（compile -> test -> package -> install -> deploy）
3. **Site**: 生成项目报告站点