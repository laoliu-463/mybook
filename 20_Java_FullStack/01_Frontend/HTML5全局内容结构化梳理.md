这是一关于 **HTML5 全局内容**的结构化整理。

HTML5 不仅仅是“新一代的 HTML”，它实际上是一个**技术集合**，包括了**新标签、新样式支持（CSS3）以及新的 JavaScript API**。对于新手来说，理解 HTML5 是从“写静态页面”向“开发 Web 应用”转变的关键。

我将其分为 **五大核心板块** 进行梳理：

---

### 🏗️ 第一板块：语义化结构 (Semantics)

**核心理念：** 用正确的标签做正确的事。机器（搜索引擎、屏幕阅读器）能读懂网页结构。

1. **布局标签 (Layout)：**
* `<header>`：页眉（Logo、导航）。
* `<nav>`：导航链接区域。
* `<section>`：文档中的节/段落（通用容器）。
* `<article>`：独立的内容块（如一篇博客文章）。
* `<aside>`：侧边栏（广告、相关链接）。
* `<footer>`：页脚（版权信息、联系方式）。
* `<main>`：文档的主要内容（每个页面应只有一个）。


2. **文本语义：**
* `<mark>`：高亮显示（像荧光笔）。
* `<time>`：定义日期/时间。
* `<figure>` & `<figcaption>`：图片及其标题的组合。



---

### 📝 第二板块：增强型表单 (Smart Forms)

**核心理念：** 减少 JavaScript 的校验工作，移动端体验更佳。

1. **新的 Input 类型 (`type="..."`)：**
* `email`：自动校验邮箱格式。
* `url`：自动校验网址。
* `number`：数字输入（配合 `min`, `max`, `step`）。
* `range`：滑块选择器。
* `date` / `time` / `week`：原生日期时间选择器（移动端极其重要）。
* `search`：搜索框。
* `color`：颜色拾取器。


2. **新的表单属性：**
* `placeholder`：输入提示文本。
* `required`：必填项校验。
* `autofocus`：自动聚焦。
* `pattern`：使用正则表达式进行校验。
* `autocomplete`：自动完成提示。


3. **新表单元素：**
* `<datalist>`：为输入框提供预定义的选项列表（类似搜索建议）。
* `<output>`：计算结果的输出容器。



---

### 🎬 第三板块：多媒体与图形 (Multimedia & Graphics)

**核心理念：** 摆脱 Flash 插件，原生支持音视频和绘图。

1. **音视频 (Audio & Video)：**
* `<audio src="...">`：音频播放。
* `<video src="...">`：视频播放。
* **关键属性：** `controls` (显示控件), `autoplay` (自动播放), `loop` (循环), `muted` (静音)。


2. **绘图 (Graphics)：**
* **Canvas (`<canvas>`)：**
* 基于 **位图 (Bitmap)**。
* 依赖 JavaScript 绘制（`getContext('2d')`）。
* *应用：* 游戏、数据可视化图表 (ECharts)、图片编辑。


* **SVG (`<svg>`)：**
* 基于 **矢量图 (Vector)**。
* 基于 XML 标签绘制。
* *应用：* 图标 (Iconfont)、地图、无论怎么放大都不失真的图形。





---

### 💾 第四板块：本地存储 (Web Storage)

**核心理念：** 比 Cookie 更大、更安全、更易用的客户端存储。

| 特性 | Cookie | localStorage | sessionStorage |
| --- | --- | --- | --- |
| **数据生命周期** | 可设置过期时间，否则随浏览器关闭 | **永久有效**，除非手动删除 | **仅当前窗口有效**，关闭标签页即失效 |
| **大小限制** | 很小 (4KB) | 大 (约 5MB) | 大 (约 5MB) |
| **与服务器交互** | 每次请求都会携带 (浪费带宽) | **不参与服务器通信** (纯本地) | **不参与服务器通信** (纯本地) |
| **应用场景** | 身份 Token、Session ID | 购物车数据、用户偏好设置 | 表单临时数据、一次性状态 |

---

### ⚡ 第五板块：核心 API (Web APIs)

**核心理念：** 让网页拥有“原生 APP”的能力。

1. **地理定位 (Geolocation)：**
* `navigator.geolocation`：获取用户经纬度（需用户授权）。


2. **拖拽 (Drag and Drop)：**
* 原生 API 支持元素拖放（`draggable="true"`）。


3. **Web Worker：**
* **多线程**支持。允许在后台运行复杂的 JS 脚本，不阻塞主界面的渲染。


4. **Web Socket：**
* 全双工通信协议。服务器可以**主动**向客户端推送消息（聊天室、股票行情的基石）。


5. **History API：**
* `pushState`, `replaceState`。在不刷新页面的情况下改变 URL（单页应用 SPA 的核心原理）。



---

### 💡 极简复习总结 (考试/面试 必背点)

1. **语义化：** 知道 `<header>`, `<footer>`, `<section>`，为了 SEO 和可读性。
2. **多媒体：** 知道 `<video>` 和 `<audio>` 取代了 Flash。
3. **存储：** 必须分清 `Cookie` vs `localStorage` vs `sessionStorage` 的区别。
4. **文档声明：** HTML5 的声明非常简单：`<!DOCTYPE html>`。
5. **DOM 操作：** 新增了 `document.querySelector()` 和 `document.querySelectorAll()` (类似 jQuery 的选择器)。
