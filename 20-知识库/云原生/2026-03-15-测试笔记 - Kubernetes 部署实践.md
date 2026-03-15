---
title: 测试笔记 - Kubernetes 部署实践
type: concept
domain: [云原生]
tags: [云原生]
source: voice
created: 2026-03-15
status: review
---

# Kubernetes 部署实践学习

## TL;DR

- Kubernetes 部署实践学习
- 什么是 Kubernetes
- Kubernetes（K8s）是一个开源的容器编排平台，用于自动化容器化应用的部署、扩展和管理。

## 什么是 Kubernetes

Kubernetes（K8s）是一个开源的容器编排平台，用于自动化容器化应用的部署、扩展和管理。

## 核心概念

### Pod

Pod 是 Kubernetes 的最小部署单元，一个 Pod 可以包含一个或多个容器。

### Deployment

Deployment 负责管理 Pod 的副本数、滚动更新和回滚。

### Service

Service 为 Pod 提供稳定的网络访问入口。

### ConfigMap 和 Secret

用于配置管理。

## 部署流程

1. 编写 Dockerfile
2. 构建镜像
3. 编写 Deployment YAML
4. 使用 kubectl apply 部署

## 参考

- Kubernetes 官方文档
- 《Kubernetes in Action》

## 相关笔记

- [[10-项目/自动归档/2026-03-15-正确使用姿势|正确使用姿势]]

## References

- 待补充来源或外部引用。

## 【需要人工复核】

- 自动生成的摘要、标签、分类和相关链接需要人工确认。
