# 微服务项目实战

## 项目简介

基于 Spring Cloud Alibaba 的分布式微服务架构实战，教务管理系统（EAMS）。

## 技术栈

| 分类 | 技术 |
|------|------|
| 微服务框架 | Spring Cloud Alibaba |
| 注册/配置中心 | Nacos |
| 网关 | Spring Cloud Gateway |
| 数据库 | MySQL 8.0 |
| 缓存 | Redis |
| 文档数据库 | MongoDB |
| 消息队列 | RocketMQ |
| 对象存储 | FastDFS |
| ORM | MyBatis-Plus |
| 验证码 | Captcha |

## 核心模块

### 已完成模块

- [x] 基础架构搭建
- [x] 分层领域模型
- [x] Nacos服务注册与配置
- [x] Swagger API文档
- [x] 验证码集成
- [x] Validation参数校验
- [x] MapStruct对象转换

### 待开发模块

- [ ] 登录认证模块
- [ ] 网关认证授权
- [ ] 教务管理模块
- [ ] 订单模块
- [ ] 消息通知

## 开发规范

### 分层领域模型

参考 [[20-知识库/架构与工程实践/02-Java项目架构实战]]

- **DO**: Data Object，与数据库表一一对应
- **DTO**: Data Transfer Object，层间数据传输
- **Query**: 查询条件封装
- **VO**: View Object，返回前端数据

### 包名规范

```
com.zerotask.eams.{模块名}
```

### 命名规范

| 层级 | 前缀 |
|------|------|
| Controller | get / list / add / update / delete |
| Service | getXxx / listXxx / pageXxx |
| DAO | selectById / selectList / selectPage |

## 学习路径

| 步骤 | 内容 | 笔记 |
|------|------|------|
| 1 | 环境搭建 - JDK、Maven、Docker | [[10-项目/微服务项目实战/01-环境搭建]] |
| 2 | 项目结构理解 | - |
| 3 | 分层领域模型掌握 | [[10-项目/微服务项目实战/02-分层领域模型]] |
| 4 | Nacos服务注册与配置管理 | [[10-项目/微服务项目实战/01-环境搭建]] |
| 5 | MyBatis-Plus CRUD操作 | [[10-项目/微服务项目实战/03-代码生成]] |
| 6 | Swagger API文档配置 | [[10-项目/微服务项目实战/06-Swagger配置]] |
| 7 | Validation参数校验 | [[10-项目/微服务项目实战/04-参数校验]] |
| 8 | 验证码集成 | [[10-项目/微服务项目实战/05-验证码集成]] |
| 9 | 网关与认证授权 | (待更新) |

## 相关笔记

- [[20-知识库/架构与工程实践/02-Java项目架构实战]]
- [[20-知识库/编程语言/Java/Java基础]]
- [[20-知识库/数据库/MySQL]]

## References

- [Spring Cloud Alibaba](https://spring.io/projects/spring-cloud-alibaba)
- [Nacos](https://nacos.io/)
- [MyBatis-Plus](https://baomidou.com/)
