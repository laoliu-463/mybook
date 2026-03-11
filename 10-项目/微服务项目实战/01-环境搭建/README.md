# 环境搭建

## TL;DR

开发环境需要配置 JDK 1.8、Maven 3.6+、IDEA 2022+，服务器环境需要 MySQL、Redis、Nacos（Docker部署）。

---

## 一、开发环境

### 1.1 必备工具

| 工具 | 版本要求 | 用途 |
|------|----------|------|
| JDK | 1.8+ | Java运行时，最低JDK8 |
| Maven | 3.6+ | 项目构建 |
| IDEA | 2022+ | 开发IDE |
| Docker | - | 容器环境 |
| Navicat | - | MySQL客户端 |
| RDM | - | Redis客户端 |

### 1.2 Maven配置

关键配置：使用阿里云制品库

```xml
<!-- settings.xml 配置 -->
<mirrors>
    <mirror>
        <id>aliyun</id>
        <mirrorOf>*</mirrorOf>
        <name>阿里云公共仓库</name>
        <url>https://maven.aliyun.com/repository/public</url>
    </mirror>
</mirrors>
```

> **注意**：必须使用项目提供的settings.xml，否则无法下载依赖

---

## 二、服务器环境

### 2.1 基础环境

- 操作系统：CentOS 8.6 / 阿里云龙蜥8
- Docker容器
- Linux基础命令（与Ubuntu通用）

### 2.2 必需服务

| 服务 | 端口 | 说明 |
|------|------|------|
| MySQL | 3306 | 数据库 |
| Redis | 6379 | 缓存 |
| Nacos | 8848/9848 | 注册/配置中心 |

### 2.3 Nacos端口说明

- 控制台：8848
- GRPC通讯：9848
- 防火墙需放行这些端口

---

## 三、项目导入

### 3.1 克隆项目

```bash
git clone <仓库地址>
```

### 3.2 切换分支

```bash
git checkout -b <分支名> origin/java-architecture
```

### 3.3 IDEA配置

1. File → Open → 选择项目根目录
2. 配置Maven：Settings → Maven → 指向项目settings.xml
3. 配置JDK：Project Structure → Project SDK → JDK 8

### 3.4 注意事项

- **不要放中文目录**：项目路径不要包含中文
- **resource目录颜色**：IDEA中resource目录颜色必须是正常颜色，否则配置不生效

---

## 四、Nacos配置

### 4.1 创建命名空间

在Nacos控制台创建命名空间，ID与名称保持一致，如：`eams-dev`

### 4.2 创建配置文件

创建以下配置文件：
- `system.yml` - Spring基础配置
- `datasource.yml` - 数据库配置
- `redis.yml` - Redis配置
- `third-party.yml` - 第三方服务配置

### 4.3 配置示例

```yaml
# system.yml
spring:
  application:
    name: eams-simple

# datasource.yml
spring:
  datasource:
    driver-class-name: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/eams?useUnicode=true
    username: root
    password: xxx
```

---

## References

- [Nacos官方文档](https://nacos.io/)
- [阿里云Maven仓库](https://maven.aliyun.com/)
