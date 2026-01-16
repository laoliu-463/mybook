# 短链系统需求分析与设计（第 7-12 步，零基础友好版）

> 一句话解释：**短链**就是把很长的网址压缩成很短的链接，访问短链时会自动跳转到原始链接。

---

## 适合人群

- 第一次看项目需求文档的人
- 想知道“短链系统要做什么”的人

---

## 术语小抄

- **PV/UV**：访问量/独立访客数。
- **302 重定向**：浏览器自动跳转到另一个地址。
- **Redis**：常用的高速缓存。
- **Bloom Filter**：一种“快速判断不存在”的数据结构。
- **MQ**：消息队列，用来异步处理耗时任务。

---

## 最小可行流程（先看这个）

1. 用户提交长链接 → 系统生成短码 → 返回短链接  
2. 访客访问短链接 → 系统查到长链接 → 302 跳转  
3. 系统记录访问 → 生成统计报表

---

## 第 7 步：用例图与用例描述

### 7.1 参与者（Actor）

- **普通用户**：创建/管理自己的短链，查看统计
- **访客（匿名）**：访问短链并跳转
- **管理员（可选）**：全局管理短链、封禁、查看全站统计

### 7.2 用例列表（Use Case List）

- UC-01 用户注册/登录
- UC-02 创建短链
- UC-03 管理短链（查询/筛选/分页/禁用/删除）
- UC-04 访问短链并跳转
- UC-05 查看统计（PV/UV/趋势/按标签聚合）
- UC-06 管理员审核与封禁（可选）

### 7.3 用例描述模板

#### UC-02 创建短链

- **参与者**：普通用户
- **前置条件**：用户已登录
- **触发**：用户输入长链接并点击“生成”
- **基本流程**：
  1. 系统校验长链接格式与协议（http/https）
  2. 用户选择分组/标签，填写过期时间（可选）
  3. 系统生成唯一短码并写入数据库
  4. 系统返回短链接并展示复制按钮
- **异常流程**：
  - 长链接非法 → 返回参数错误
  - 短码冲突 → 重新生成并重试（最多 N 次）
- **后置条件**：短链记录创建成功，可用于跳转

#### UC-04 访问短链并跳转

- **参与者**：访客（匿名）
- **前置条件**：短链存在且未禁用/未过期
- **触发**：访客打开短链接
- **基本流程**：
  1. 系统根据短码查询映射（优先缓存）
  2. 系统返回 302 重定向到长链接
  3. 系统记录一次访问事件（可异步）
- **异常流程**：
  - 短链不存在/过期/禁用 → 返回 404 或提示页
- **后置条件**：访问记录进入统计系统

#### UC-05 查看统计

- **参与者**：普通用户
- **前置条件**：用户已登录且拥有该短链权限
- **基本流程**：
  1. 用户选择时间范围（7/30 天）
  2. 系统查询聚合数据（按天 PV/UV）
  3. 系统返回趋势图数据与渠道/标签占比
- **异常流程**：
  - 数据延迟 → 提示“统计可能存在延迟”，但仍返回现有数据

---

## 第 8 步：核心业务流程

### 8.1 创建短链流程

1. 用户提交长链接、标签、过期时间
2. 后端校验参数（格式、长度、协议、黑名单域名可选）
3. 生成短码（Base62 + ID）
4. 写入数据库（short_code 唯一索引）
5. 写入缓存（Redis：short_code → long_url，设置 TTL）
6. 返回短链接

### 8.2 跳转流程（高性能路径）

1. 访客请求 `/s/{code}`
2. 先查 Bloom Filter（不存在直接返回 404）
3. 查 Redis 缓存命中 → 302 跳转
4. 缓存未命中 → 查 DB → 写回缓存 → 302 跳转
5. 记录访问事件（异步投递 MQ / 或先写日志队列）

### 8.3 统计流程（异步）

1. 跳转接口生成访问事件（code、time、ip、ua、referer、visitorId）
2. 生产者写入 MQ
3. 消费者批量写入 `click_event`（或直接聚合到日表）
4. 定时任务按天聚合更新 `link_stat_day`
5. 前端查询 `link_stat_day` 展示趋势图

---

## 第 9 步：数据字典（表结构说明）

### 9.1 表：link（短链主表）

- `id`：主键
- `user_id`：所属用户
- `short_code`：短码（唯一）
- `long_url`：原始链接
- `group_name`：分组（活动/渠道）
- `status`：状态（1=启用，0=禁用）
- `expire_time`：过期时间（可空）
- `created_at` / `updated_at`

### 9.2 表：click_event（访问明细表，可分区/按天归档）

- `id`
- `short_code`
- `access_time`
- `ip`
- `ua`
- `referer`
- `visitor_id`（用于 UV 的匿名标识）

### 9.3 表：link_stat_day（按天聚合表）

- `id`
- `short_code`
- `stat_date`（日期）
- `pv`
- `uv`
- `group_name`（可选，用于维度聚合）

---

## 第 10 步：数据库 DDL

```sql
CREATE TABLE link (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  short_code VARCHAR(16) NOT NULL,
  long_url VARCHAR(2048) NOT NULL,
  group_name VARCHAR(64) DEFAULT NULL,
  status TINYINT NOT NULL DEFAULT 1,
  expire_time DATETIME DEFAULT NULL,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_short_code (short_code),
  KEY idx_user_id (user_id),
  KEY idx_group_name (group_name)
);

CREATE TABLE click_event (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  short_code VARCHAR(16) NOT NULL,
  access_time DATETIME NOT NULL,
  ip VARCHAR(64) DEFAULT NULL,
  ua VARCHAR(512) DEFAULT NULL,
  referer VARCHAR(1024) DEFAULT NULL,
  visitor_id VARCHAR(64) DEFAULT NULL,
  KEY idx_code_time (short_code, access_time)
);

CREATE TABLE link_stat_day (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  short_code VARCHAR(16) NOT NULL,
  stat_date DATE NOT NULL,
  pv BIGINT NOT NULL DEFAULT 0,
  uv BIGINT NOT NULL DEFAULT 0,
  group_name VARCHAR(64) DEFAULT NULL,
  UNIQUE KEY uk_code_date (short_code, stat_date),
  KEY idx_date (stat_date)
);
```

---

## 第 11 步：接口清单（REST API）

- `POST /api/auth/register` 注册
- `POST /api/auth/login` 登录
- `POST /api/links` 创建短链
- `GET /api/links` 分页查询短链（支持 group/status 条件）
- `PUT /api/links/{id}/status` 启用/禁用
- `DELETE /api/links/{id}` 删除
- `GET /s/{code}` 跳转（302）
- `GET /api/stats/link/{code}` 获取该短链 7/30 天 PV/UV 趋势

---

## 第 12 步：验收标准与测试用例

### 12.1 验收标准

- 能成功创建短链并返回可访问短链接
- 短链访问能正确 302 跳转到原始链接
- 不存在/禁用/过期短链能返回正确提示
- 后台能查看短链列表并支持分页与筛选
- 能查看 PV/UV 与近 7 天趋势（统计允许延迟）

### 12.2 测试用例示例

- TC-01 输入合法长链 → 返回短链并可跳转
- TC-02 输入非法 URL → 返回参数错误
- TC-03 禁用短链后访问 → 返回 404/提示页
- TC-04 创建短链后查看列表 → 列表存在该短链
- TC-05 连续访问同一短链 → PV 增加，UV 按 visitor_id 去重
- TC-06 Redis 失效（模拟）→ 仍可查 DB 跳转成功
- TC-07 缓存未命中后访问 → 写回缓存，下次命中
- TC-08 统计接口查询 7 天 → 返回 7 个点的趋势数据
