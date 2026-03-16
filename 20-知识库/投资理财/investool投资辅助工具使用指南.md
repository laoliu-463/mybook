---
title: investool 投资辅助工具使用指南
aliases:
  - investool
  - investool教程
tags:
  - 投资理财
  - 投资理财/工具
  - 投资理财/股票
  - 投资理财/基金
type: note
domain: 投资理财
topic: investool工具
question: investool工具如何配置和使用
source: 手动整理
created: 2026-03-16
updated: 2026-03-16
status: evergreen
summary: investool 是一个以基本面选股、股票检测、基金筛选为主的个人投资分析工具，不构成投资建议，只是辅助工具。
processed_at: "2026-03-16T19:48:00"
---

# investool 投资辅助工具使用指南

---

## 一、核心功能定位

最适合做三件事：

1. **查一只股票值不值得继续研究** — 用 `checker`
2. **批量筛出一批候选股票/基金** — 用 `exportor`
3. **把"冲动买入"变成"先检查再决定"** — 建立投资检查流程

---

## 二、配置方式

### 方案 A：下载可执行文件（推荐）

1. 打开项目 GitHub 仓库下载适合系统的最新版本
2. 解压后得到 `investool` 可执行文件
3. 把仓库里的 `config.toml` 放在同目录
4. 终端进入目录运行命令

### 方案 B：自己编译

```
git clone https://github.com/axiaoxin-com/investool.git
cd investool
go build
```

---

## 三、基础命令

### 1. 查看帮助

```
./investool -h
```

### 2. 启动 Web 界面

```
./investool webserver
```

指定配置文件：

```
./investool webserver --config ./config.toml
```

### 3. 检查单只股票

```
./investool checker -k 比亚迪
```

一次查多个（用 `/` 分隔）：

```
./investool checker -k 招商银行/中国平安/600519
```

### 4. 批量导出候选池

导出 Excel：
```
./investool -l error exportor -f ./stocks.xlsx
```

导出 CSV：
```
./investool -l error exportor -f ./stocks.csv
```

导出 JSON：
```
./investool -l error exportor -f ./stocks.json
```

---

## 四、核心参数理解

### 1. min_roe — 净资产收益率

- 含义：净资产收益率至少多少
- 直觉：公司拿股东的钱赚钱的效率怎么样
- 默认值：8%

```
--checker.min_roe=8
```

### 2. check_years — 连续增长年数

- 含义：连续几年增长
- 直觉：不是今年突然好，而是连续几年都不错
- 默认值：3 年

### 3. max_debt_asset_ratio — 资产负债率

- 含义：最大资产负债率
- 直觉：欠债别太重
- 默认值：60%（非金融股）

### 4. max_peg — PEG 估值

- 含义：PEG 不要太高
- 直觉：成长性和估值别太不匹配
- 默认值：1.5
- PEG > 1.5 通常偏贵

### 5. min_byys_ratio / max_byys_ratio — 本业营收比

- 含义：主营业务收入占比
- 直觉：赚钱是不是主要靠主营业务
- 默认值：0.9 ~ 1.1

### 6. is_check_price_by_calc — 合理价检测

- 含义：要不要拿"估算合理价"来过滤
- 默认：关闭
- 建议：初学者先不开，先学会看公司质量

---

## 五、实用命令模板

### 模板 1：保守型观察池

```
./investool -l error exportor -f ./stable.xlsx \
  --checker.min_roe=10 \
  --checker.check_years=3 \
  --checker.max_debt_asset_ratio=50 \
  --checker.max_peg=1.2
```

### 模板 2：宽松学习版

```
./investool -l error exportor -f ./learn.xlsx \
  --filter.min_roe=6 \
  --checker.min_roe=6 \
  --checker.check_years=2 \
  --checker.max_peg=2
```

### 模板 3：查指定公司

```
./investool -l error exportor -f ./focus.xlsx \
  --filter.special_security_name_abbr_list 福莱特 \
  --filter.special_security_name_abbr_list 旗滨集团 \
  --disable_check
```

---

## 六、日常使用流程

### 场景 1：朋友推荐股票

先用 `checker` 检查：
- ROE 是否稳定
- 负债是否轻
- 利润和营收是否持续增长
- PEG 是否离谱
- 估值是否已经很高

**把"听说不错"变成"先检查再说"**

### 场景 2：每周候选池

每周末跑一次：

```
./investool -l error exportor -f ./weekly_watchlist.xlsx
```

然后：
1. 删掉完全看不懂行业的公司
2. 留下 10-20 只
3. 每只写一句话：为什么值得继续观察

### 场景 3：基金筛选

启动 Web 界面后使用：
- 4433 筛选
- 基金检测
- 基金经理筛选
- 股票选基
- 持仓相似度

---

## 七、投资决策检查清单

### 买入前问 3 个问题

1. 这家公司我能一句话讲清商业模式吗？
2. investool 检查结果里最弱的一项是什么？
3. 就算跌 20%，我还愿不愿意继续持有？

### 卖出前问 3 个问题

1. 当初买入理由还在不在？
2. 现在卖，是因为逻辑变了，还是只是我害怕？
3. 有没有更好的资金用途？

---

## 八、每周 30 分钟流程

### 周日晚上

1. **导出候选池**：`./investool -l error exportor -f ./weekly_watchlist.xlsx`
2. **挑 5 只认识名字的公司**
3. **逐个跑 checker**：`./investool checker -k 招商银行/美的集团/伊利股份`
4. **手写结论**：每只只写一句
5. **只保留 3 个继续跟踪**

---

## 九、注意事项

1. **别把它当"买入信号机"**：只是缩小范围，不是替你下判断
2. **别迷信参数**：ROE 高不代表一定值得买，PEG 低也可能是行业见顶
3. **别拿短期要用的钱做实验**：只研究长期投资，不赌下周涨跌

---

## 十、相关笔记

- [[投资新手入门]]
- [[股票入门]]
- [[Mermaid-投资新手思维导图]]

## 参考来源

- https://github.com/axiaoxin-com/investool

## 参考来源

- https://github.com/axiaoxin-com/investool
