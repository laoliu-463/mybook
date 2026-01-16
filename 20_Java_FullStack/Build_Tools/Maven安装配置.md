# Maven：Java 项目的“超级管家” (0基础版)

> **核心心法**：不要把 Maven 想复杂了。它就是一个**帮你干杂活的管家**。
>
> 你只需要告诉它：“我要用 Spring 框架，版本 5.0”。它就会自动去网上帮你把这个包（以及这个包依赖的别的包）统统下载下来，摆在正确的位置。
> 此外，它还能帮你**编译代码**、**跑测试**、**打包成 exe/jar**，一键搞定。

---

## 一、 为什么需要 Maven？

在没有 Maven 的黑暗时代，开发一个 Java 项目是这样的：
1.  **手动下载 jar 包**：去各个官网找 `commons-lang.jar`, `spring-core.jar`...
2.  **手动管理依赖**：A 包依赖 B 包，B 包依赖 C 包，你得一个一个找齐，少一个就报错。
3.  **手动编译打包**：写一大堆复杂的脚本。

**Maven 的出现，就是为了解决这些痛点。**
它引入了一个核心文件：**`pom.xml` (项目对象模型)**。
你可以把它看作**“购物清单”**。你只要在清单上写上名字，Maven 管家就会自动去仓库（超市）帮你把东西买回来。

---

## 二、 安装与配置 (Windows 版)

### 1. 下载与解压
1.  去 [Maven 官网](https://maven.apache.org/download.cgi) 下载 `Binary zip archive`。
2.  解压到一个**没有中文、没有空格**的路径，例如：`D:\DevTools\Maven`。

### 2. 配置环境变量 (让电脑认识 mvn 命令)
*   **新建系统变量** `MAVEN_HOME` -> 值为你解压的路径（例如 `D:\DevTools\Maven`）。
*   **修改 Path 变量** -> 添加 `%MAVEN_HOME%\bin`。
*   **验证**：打开 CMD，输入 `mvn -v`，看到版本号即成功。

### 3. 配置“本地仓库” (你的私人储物间)
Maven 下载的 jar 包默认放在 C 盘用户目录下。为了不占 C 盘，建议改到 D 盘。
1.  打开 `conf/settings.xml` 文件。
2.  找到 `<localRepository>` 标签，修改为：
    ```xml
    <localRepository>D:\Repositories\MavenRepo</localRepository>
    ```

### 4. 配置阿里云镜像 (极其重要！)
Maven 默认连接国外服务器，下载速度慢如蜗牛。必须换成国内阿里云镜像。
在 `settings.xml` 的 `<mirrors>` 标签里加入：
```xml
<mirror>
    <id>aliyunmaven</id>
    <mirrorOf>*</mirrorOf>
    <name>阿里云公共仓库</name>
    <url>https://maven.aliyun.com/repository/public</url>
</mirror>
```

---

## 三、 核心概念：GAV 坐标

世界上有几百万个 jar 包，Maven 怎么知道你要哪一个？
通过 **GAV 坐标**（就像身份证一样唯一）。

*   **G (GroupId)**：**组织名**（通常是公司域名的倒写）。
    *   例如：`com.google`, `org.springframework`
*   **A (ArtifactId)**：**项目名**（具体的产品名字）。
    *   例如：`guava`, `spring-boot-starter-web`
*   **V (Version)**：**版本号**。
    *   例如：`31.0-jre`, `2.7.5`

**例子：我要引入 Google 的 Guava 工具包**
```xml
<dependency>
    <groupId>com.google.guava</groupId>
    <artifactId>guava</artifactId>
    <version>31.0.1-jre</version>
</dependency>
```

---

## 四、 常用命令 (管家口令)

在项目文件夹下打开命令行，输入这些指令，管家就会干活：

| 命令 | 口令含义 | 实际作用 |
| :--- | :--- | :--- |
| **`mvn clean`** | **“大扫除”** | 删除 `target` 目录（清理掉上次编译产生的垃圾）。 |
| **`mvn compile`** | **“翻译”** | 把 `.java` 源码翻译成 `.class` 字节码。 |
| **`mvn test`** | **“体检”** | 运行 `src/test` 下的所有测试用例，看看代码有没有病。 |
| **`mvn package`** | **“打包”** | 把编译好的代码打成一个 `.jar` 或 `.war` 包。 |
| **`mvn install`** | **“入库”** | 把打好的包存到你的本地仓库，供其他项目使用。 |

> **💡 万能组合拳**：
> `mvn clean install` —— 先打扫干净，再重新编译、测试、打包、入库。（最常用）

---

## 五、 总结

Maven 其实就干两件事：
1.  **管包**：根据 `pom.xml` 自动下载 jar 包。
2.  **管事**：通过命令帮你编译、测试、打包。

等你熟悉了 Maven，后面还有更高级的 **Gradle** 等着你，但原理都是一样的。