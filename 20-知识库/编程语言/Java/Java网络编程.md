---
title: Java - Socket 网络编程
aliases:
  - Java Socket
  - TCP 编程
  - UDP 编程
tags:
  - Java
  - Java/网络
  - 面试题
type: note
domain: java
topic: 网络编程
question: Java Socket 网络编程如何实现
source:
source_title:
created: 2026-02-15
updated: 2026-02-15
status: evergreen
---

# Java - Socket 网络编程

## 一句话结论
Java 网络编程基于 Socket 抽象，支持 TCP（可靠连接）和 UDP（无连接）两种协议。TCP 用于 HTTP、文件传输等可靠传输场景，UDP 用于实时音视频等容忍丢包场景。

## 标准回答
- **Socket**：网络通信端点 = IP 地址 + 端口号
- **TCP Socket**：面向连接、可靠传输、三次握手
- **UDP Socket**：无连接、快速、可能丢包
- 核心类：ServerSocket、Socket、DatagramSocket

## 为什么
网络应用需要进程间通信，Socket 提供标准 API：
- TCP 实现可靠通信（HTTP、RPC）
- UDP 实现低延迟通信（直播、游戏）

## 对比
| 特性 | TCP | UDP |
|---|---|---|
| 连接性 | 面向连接 | 无连接 |
| 可靠性 | 可靠、保证顺序 | 不可靠、可能丢包 |
| 速度 | 较慢 | 快 |
| 适用场景 | HTTP、文件传输 | 视频、语音、游戏 |

## TCP 服务端代码示例
```java
import java.io.*;
import java.net.*;

public class Server {
    public static void main(String[] args) throws IOException {
        // 创建服务端 Socket，监听 8080 端口
        ServerSocket serverSocket = new ServerSocket(8080);
        System.out.println("服务端启动，监听 8080 端口");

        // 等待客户端连接
        Socket clientSocket = serverSocket.accept();
        System.out.println("客户端连接: " + clientSocket.getInetAddress());

        // 获取输入流
        BufferedReader in = new BufferedReader(
            new InputStreamReader(clientSocket.getInputStream())
        );

        // 获取输出流
        PrintWriter out = new PrintWriter(
            clientSocket.getOutputStream(), true
        );

        // 处理请求
        String message = in.readLine();
        System.out.println("收到: " + message);
        out.println("服务器回复: " + message);

        // 关闭连接
        in.close();
        out.close();
        clientSocket.close();
        serverSocket.close();
    }
}
```

### 代码说明
- `ServerSocket` 创建服务端监听
- `accept()` 阻塞等待客户端连接
- `Socket` 代表客户端连接
- 流操作实现数据读写

## TCP 客户端代码
```java
Socket socket = new Socket("localhost", 8080);
PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
BufferedReader in = new BufferedReader(
    new InputStreamReader(socket.getInputStream())
);

out.println("Hello Server");
System.out.println("收到: " + in.readLine());
```

## 易错点
- TCP 必须先启动服务端再启动客户端
- 流使用完要关闭
- UDP 不建立连接，直接发数据包
- 注意处理异常和超时

## 延伸链接
- [[TCP - 三次握手]]
- [[Java - NIO 和 BIO]]

## 参考来源
