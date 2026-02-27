---
title: Java 网络编程
type: concept
domain: [编程语言, Java]
tags: [Java, Socket, TCP, UDP, 网络编程]
source: web
created: 2026-02-15
status: draft
---

# Java 网络编程

## TL;DR

Java 网络编程基于 Socket 抽象，支持 TCP（可靠连接）和 UDP（无连接）两种协议。TCP 用于 HTTP、SMTP 等需要可靠传输的场景，UDP 用于实时性要求高但能容忍丢包的视频/语音场景。

## 核心概念

### Socket 是什么

Socket 是网络通信的端点，包含 IP 地址和端口号，用于建立网络连接和数据传输。

### TCP vs UDP

| 特性 | TCP | UDP |
|------|-----|-----|
| 连接性 | 面向连接 | 无连接 |
| 可靠性 | 可靠传输，保证顺序 | 不可靠，可能丢包 |
| 速度 | 相对较慢 | 快速 |
| 适用场景 | HTTP、SMTP、文件传输 | 视频、语音、实时游戏 |

## TCP 编程

### 服务端

```java
import java.io.*;
import java.net.*;

public class Server {
    public static void main(String[] args) throws IOException {
        // 监听指定端口
        ServerSocket serverSocket = new ServerSocket(8080);
        System.out.println("服务器启动，监听端口 8080...");
        
        // 等待客户端连接
        Socket socket = serverSocket.accept();
        System.out.println("客户端已连接: " + socket.getInetAddress());
        
        // 获取输入输出流
        InputStream in = socket.getInputStream();
        OutputStream out = socket.getOutputStream();
        
        // 读取客户端数据
        BufferedReader reader = new BufferedReader(new InputStreamReader(in));
        String message = reader.readLine();
        System.out.println("收到: " + message);
        
        // 发送响应
        PrintWriter writer = new PrintWriter(out, true);
        writer.println("服务器响应: " + message);
        
        // 关闭连接
        socket.close();
        serverSocket.close();
    }
}
```

### 客户端

```java
import java.io.*;
import java.net.*;

public class Client {
    public static void main(String[] args) throws IOException {
        // 连接服务器
        Socket socket = new Socket("127.0.0.1", 8080);
        System.out.println("已连接服务器");
        
        // 获取输入输出流
        OutputStream out = socket.getOutputStream();
        InputStream in = socket.getInputStream();
        
        // 发送数据
        PrintWriter writer = new PrintWriter(out, true);
        writer.println("Hello Server");
        
        // 接收响应
        BufferedReader reader = new BufferedReader(new InputStreamReader(in));
        String response = reader.readLine();
        System.out.println("服务器响应: " + response);
        
        // 关闭连接
        socket.close();
    }
}
```

### TCP 流程要点

1. **服务端**：创建 `ServerSocket` → `accept()` 等待连接 → 获取 `Socket` → 读写数据 → 关闭
2. **客户端**：创建 `Socket` 连接服务器 → 读写数据 → 关闭
3. 使用 `InputStream`/`OutputStream` 进行流式数据传输

### 常见问题

**粘包问题**：TCP 是流协议，消息边界不明确。解决方案：
- 消息定长
- 使用分隔符
- 消息头 + 消息体（先读长度，再读内容）

## UDP 编程

### 服务端/客户端一体

```java
import java.io.*;
import java.net.*;

public class UDPDemo {
    public static void main(String[] args) throws IOException {
        // 创建 DatagramSocket
        DatagramSocket socket = new DatagramSocket(8080);
        
        // 接收数据
        byte[] buffer = new byte[1024];
        DatagramPacket packet = new DatagramPacket(buffer, buffer.length);
        socket.receive(packet);
        
        String message = new String(packet.getData(), 0, packet.getLength());
        System.out.println("收到: " + message);
        
        // 发送响应
        String response = "UDP 响应";
        DatagramPacket respPacket = new DatagramPacket(
            response.getBytes(),
            response.length(),
            packet.getAddress(),
            packet.getPort()
        );
        socket.send(respPacket);
        
        socket.close();
    }
}
```

### UDP 特点

- 无需建立连接
- 使用 `DatagramSocket` 和 `DatagramPacket`
- 每个数据包独立，包含目标地址
- 适用于实时性要求高的场景

## HTTP 编程

### 使用 HttpURLConnection

```java
import java.net.*;
import java.io.*;

URL url = new URL("https://api.example.com/data");
HttpURLConnection conn = (HttpURLConnection) url.openConnection();
conn.setRequestMethod("GET");

BufferedReader reader = new BufferedReader(
    new InputStreamReader(conn.getInputStream())
);
String line;
StringBuilder response = new StringBuilder();
while ((line = reader.readLine()) != null) {
    response.append(line);
}
reader.close();
conn.disconnect();

System.out.println(response.toString());
```

## 面试追问

1. **TCP 三次握手四次挥手**：建立连接需三次，关闭需四次
2. **Socket 粘包**：原因 + 解决方案
3. **NIO vs BIO**：同步阻塞 vs 同步非阻塞
4. **TCP 长连接 vs 短连接**：Keep-Alive、HTTP Keep-Alive

## References

- [廖雪峰 Java TCP 编程](https://liaoxuefeng.com/books/java/network/tcp/index.html)
- [Java Socket 编程指南 - Baeldung](https://www.baeldung-cn.com/a-guide-to-java-sockets)

---

【需要人工复核】：粘包解决方案的代码示例
