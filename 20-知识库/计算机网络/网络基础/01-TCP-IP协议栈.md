---
title: Network - TCP/IP 协议栈是什么
aliases:
  - TCP/IP
  - 网络分层
tags:
  - 计算机网络
  - TCP/IP
  - 面试题
type: note
domain: 计算机网络
topic: 网络基础
question: TCP/IP 协议栈是什么
source:
source_title:
created: 2026-02-08
updated: 2026-02-08
status: evergreen
---

# Network - TCP/IP 协议栈是什么

## 一句话结论
TCP/IP 是互联网的实际标准，采用四层模型：应用层、传输层、网络层、网络接口层。数据发送时逐层封装，接收时逐层解封装。

## 标准回答
- **四层模型**：应用层、传输层、网络层、网络接口层
- **每层职责**：应用处理 → 传输可靠 → 网络路由 → 物理传输
- **封装/解封装**：发送加头部，接收去头部

## 为什么
分层职责明确，每层只关注自己的功能：
- 降低复杂度
- 模块化设计
- 便于标准化

## TCP/IP vs OSI 对比
| TCP/IP 四层 | OSI 七层 | 典型协议 |
|---|---|---|
| 应用层 | 应用层、表示层、会话层 | HTTP, DNS, FTP |
| 传输层 | 传输层 | TCP, UDP |
| 网络层 | 网络层 | IP, ICMP |
| 网络接口层 | 数据链路层、物理层 | Ethernet |

## 数据封装过程
```
应用层: HTTP 请求
  ↓ 加 TCP 头部
传输层: TCP 段
  ↓ 加 IP 头部
网络层: IP 数据报
  ↓ 加帧头/帧尾
网络接口层: 以太网帧
```

## 各层典型协议
```python
# 应用层
HTTP, HTTPS, DNS, FTP, SSH, SMTP

# 传输层
TCP, UDP

# 网络层
IP, ICMP, ARP

# 网络接口层
Ethernet, Wi-Fi
```

## 易错点
- OSI 是理论模型，TCP/IP 是实际标准
- TCP 可靠，UDP 不可靠但快
- IP 是逻辑地址，MAC 是物理地址
- 路由器工作在网络层，交换机工作在数据链路层

## 延伸链接
- [[TCP - 三次握手]]
- [[HTTP - 工作原理]]

## 参考来源
