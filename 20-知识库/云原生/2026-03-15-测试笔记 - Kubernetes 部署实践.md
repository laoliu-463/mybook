---
title: Kubernetes - 核心概念和部署流程是什么
aliases:
  - K8s 入门
  - Kubernetes 基础
tags:
  - Kubernetes
  - K8s/基础
  - 云原生
type: note
domain: 云原生
topic: K8s
question: Kubernetes 核心概念和部署流程是什么
source:
source_title:
created: 2026-03-15
updated: 2026-03-15
status: evergreen
---

# Kubernetes - 核心概念和部署流程是什么

## 一句话结论
Kubernetes（K8s）是开源的容器编排平台，核心概念包括 Pod、Deployment、Service，通过声明式配置实现自动化部署、扩缩容和管理。

## 标准回答
- **Pod**：K8s 最小部署单元，一个 Pod 可包含一个或多个容器
- **Deployment**：管理 Pod 副本数，支持滚动更新和回滚
- **Service**：为 Pod 提供稳定的网络访问入口
- **ConfigMap / Secret**：配置管理
- **Ingress**：HTTP/HTTPS 路由

## 为什么
手动管理大量容器十分复杂，K8s 提供了：
1. 自动化容器调度和部署
2. 自动扩缩容
3. 负载均衡
4. 服务发现
5. 滚动更新和回滚

## 核心概念对比
| 概念 | 作用 | 层级 |
|---|---|---|
| Pod | 最小部署单元 | 容器 |
| Deployment | 管理 Pod 副本 | Pod |
| Service | 网络入口 | Pod |
| ConfigMap | 配置 | 应用 |

## 部署流程
```bash
# 1. 编写 Dockerfile
docker build -t myapp:v1 .

# 2. 推送镜像
docker push myapp:v1

# 3. 编写 deployment.yaml
kubectl apply -f deployment.yaml

# 4. 查看状态
kubectl get pods
kubectl get svc
```

## Deployment YAML 示例
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3  # 3个副本
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: myapp
        image: myapp:v1
        ports:
        - containerPort: 8080
```

### 代码说明
- `replicas: 3` 表示运行 3 个 Pod 副本
- `selector` 用于关联 Deployment 和 Pod
- `image` 指定容器镜像

## 易错点
- Pod 是临时性的，重启后 IP 会变，必须用 Service
- Deployment 管理的是 Pod，不是容器
- 默认的调度策略可能不满足生产环境需求
- 生产环境需要配置资源限制（requests/limits）

## 延伸链接
- [[Docker - 常用命令有哪些]]
- [[K8s - Service 类型有什么区别]]

## 参考来源
- Kubernetes 官方文档：https://kubernetes.io/docs/
- 《Kubernetes in Action》
