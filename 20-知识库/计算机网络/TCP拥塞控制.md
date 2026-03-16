---
title: TCP - 拥塞控制机制是什么
aliases:
  - 拥塞控制
  - Congestion Control
tags:
  - 计算机网络
  - TCP/IP
  - 面试题
type: note
domain: 计算机网络
topic: TCP
question: TCP 拥塞控制机制是什么
source:
source_title:
created: 2026-02-08
updated: 2026-02-08
status: evergreen
---

# TCP - 拥塞控制机制是什么

## 一句话结论
TCP 拥塞控制通过动态调整发送速率（cwnd），避免网络过载。核心算法包括：慢启动、拥塞避免、快重传、快恢复。

## 标准回答
- **cwnd**：拥塞窗口，发送方自行估算
- **ssthresh**：慢启动阈值
- **四大算法**：慢启动、拥塞避免、快重传、快恢复
- **发送速率 = min(cwnd, rwnd) / RTT**

## 为什么
网络是共享资源，多个发送方同时发包会导致：
- 路由器缓冲区溢出
- 丢包率上升
- 延迟增加
- 网络吞吐量下降（拥塞崩溃）

## 对比
| 控制类型 | 目的 | 控制变量 |
|---|---|---|
| 流量控制 | 防止压垮接收方 | rwnd |
| 拥塞控制 | 防止压垮网络 | cwnd |

## 四大核心算法

### 1. 慢启动
- cwnd 从 1 开始
- 每收到一个 ACK，cwnd 加 1
- 指数增长，直到 ssthresh

### 2. 拥塞避免
- cwnd 达到 ssthresh 后
- 每 RTT 增加 1 个 MSS
- 线性增长

### 3. 超时重传
- 超时：cwnd = 1，ssthresh = cwnd/2
- 重新开始慢启动

### 4. 快重传 + 快恢复
- 收到 3 个重复 ACK
- ssthresh = cwnd/2
- cwnd = ssthresh + 3
- 进入拥塞避免

## 流程图
```
开始
  ↓
慢启动 (cwnd=1)
  ↓ (cwnd >= ssthresh)
拥塞避免
  ↓ (超时)
cwnd=1, 重新慢启动
  ↓ (3个重复ACK)
快恢复
```

## 易错点
- 拥塞控制是发送方行为，不需要接收方参与
- 超时比重复 ACK 更严重
- cwnd 单位是 MSS（最大报文段）
- 实际发送受 cwnd 和 rwnd 共同限制

## 延伸链接
- [[TCP - 滑动窗口]]
- [[TCP - 三次握手]]

## 参考来源
- RFC 5681
- 《计算机网络：自顶向下方法》
