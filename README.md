# MindGym v1.0.0 · 两学题库刷题应用

[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-v1.0.0-blue.svg)](https://github.com/AlbertSong1024/MindGym)
[![Stars](https://img.shields.io/badge/stars-⭐-yellow.svg)](https://github.com/AlbertSong1024/MindGym)

纯前端、零依赖的刷题 + 背题应用，题库来自《两学题库-合成版.docx》。覆盖 **高等教育学** 与 **高等教育心理学** 两科共 **973 道题**（单选 / 多选 / 判断三种题型），适配 PC 端和移动端，双击即可使用，无需服务器、无需联网。

---

## ✨ 在线预览

👉 [https://albertsong1024.github.io/MindGym/](https://albertsong1024.github.io/MindGym/)

---

## 📚 题库一览

| 学科 | 单选 | 多选 | 判断 | 合计 |
|---|---|---|---|---|
| 高等教育学 | 227 | 83 | 85 | 395 |
| 高等教育心理学 | 212 | 109 | 257 | 578 |
| **合计** | **439** | **192** | **342** | **973** |

应用按「学科 × 题型」自动拆为 6 个分类，可单独刷 / 背，也可全库随机练习。

---

## 🚀 功能特性

| 功能 | 说明 |
|---|---|
| 刷题模式 | 即时判分，答错红、答对绿，支持答题卡跳题、错题本、收藏夹 |
| **背题模式** | 不判分，正确答案直接标绿展示，附醒目答案 pill 和解析；选项禁用交互避免"可点错觉" |
| 顺序 / 随机 | 顺序刷题自动记忆进度；随机刷题每次乱序 |
| 进度记忆 | 顺序模式记住上次刷到的题号，下次续接；背题进度独立存储 |
| 错题本 | 答错自动收录，重刷答对自动移出 |
| 收藏夹 | 刷题 / 背题均可收藏，支持刷收藏、逐题取消、一键清空 |
| 答题卡 | 四色数字网格（答对 / 答错 / 当前 / 未做）点击即跳；背题模式自动隐藏对/错图例 |
| 数据持久化 | 答题记录、收藏、进度、模式全部存 localStorage，关闭不丢失 |
| 完成统计 | 刷题完成弹出正确率统计；背题完成弹出浏览题数 |
| 🔥 二维码 Lightbox | 首页二维码点击放大查看，支持右键另存为图片 |
| PC 快捷键 | A–D / 1–4 选择，回车确认或下一题，← / → 切换题目，Esc 关闭弹窗 |
| 移动端适配 | 单列布局、大触控按钮、底部固定操作条（避开 iOS 安全区） |

---

## 🎯 快速开始

### 方式一：直接打开（最简单）

双击 `index.html`，用任意现代浏览器打开即可。手机端把整个目录（至少 `index.html` + `questions.js`）发送到手机后用浏览器打开。

`file://` 方式功能完好，无需启动服务器。

### 方式二：本地 HTTP 服务器（可选）

```bash
python -m http.server 8000
# 浏览器访问 http://localhost:8000/
```

### 方式三：部署到静态托管

仓库 push 到 GitHub 后，在仓库 **Settings → Pages** 里把 Source 选 `main` 分支根目录，保存后即可通过 `https://<user>.github.io/<repo>/` 访问。Gitee Pages 同理。

> 注意：部署时**必须**同时上传 `index.html` 和 `questions.js`（题库数据，275 KB）；`questions.json` 和 `parse_bank.py` 可选。原始 docx 不上传。

---

## 🏠 首页图解

```
┌─────────────────────────────────────────────┐
│ 统计卡：已刷题数 正确率 错题 收藏          │
│─────────────────────────────────────────────│
│ 顺序|随机   │   刷题|背题   ← 紧凑一行      │
│─────────────────────────────────────────────│
│ 按分类：教育学·单选 · 多选 · 判断           │
│        心理学·单选 · 多选 · 判断            │
│        每张卡带进度条                       │
│─────────────────────────────────────────────│
│ 快捷：错题本 · 收藏夹 · 全库随机 100 题     │
│─────────────────────────────────────────────│
│ 📜 Footer: 版本号 · 版权 · 题库声明        │
│ ☕ 打赏：微信 + 支付宝二维码（可点击放大）  │
└─────────────────────────────────────────────┘
```

---

## 📝 两种模式操作对比

### 刷题模式（判分）

| 题型 | 作答方式 | 判分时机 |
|---|---|---|
| 单选 | 点一个选项 | 点击立即判分 |
| 多选 | 点若干选项（可取消）后点「确认（选 N 项）」 | 点「确认」后判分 |
| 判断 | 点「对」/「错」大按钮 | 点击立即判分 |

判分后：绿色 = 答对，红色 = 答错；答错显示正确答案 pill，有解析的题自动展开。每道题只能作答一次（锁定）。

### 背题模式（只浏览）

进入背题后：

- **选项全部展开**，正确答案项标绿，**不可点击**（cursor: default），消除"可点错觉"
- 题干下方直接出现绿色渐变「**正确答案：X**」pill 卡片；带解析的题自动附解析
- 答题卡隐藏"答对 / 答错"图例（背题不判分，这两项无意义）
- 进度条、上一题、下一题、收藏均可用
- 走完最后一题弹出「背题完成！共浏览 N 题。」

### PC 快捷键

| 按键 | 作用 | 刷题模式 | 背题模式 |
|---|---|---|---|
| `A` `B` `C` `D` 或 `1` `2` `3` `4` | 选择选项 | ✅ | ❌（禁用作答） |
| `Enter` | 多选确认 / 下一题 | ✅ | ✅ 下一题 |
| `←` / `→` | 上一题 / 下一题 | ✅ | ✅ |
| `Esc` | 关闭弹窗（如 Lightbox） | ✅ | ✅ |

---

## 💾 数据存储

所有状态存在浏览器 localStorage（本机、仅当前浏览器、key 前缀 `mg_*`）：

| key | 含义 |
|---|---|
| `mg_status` | 每道题的作答对错（`1`=对, `2`=错），供统计和错题本 |
| `mg_fav` | 收藏的题目 id 数组 |
| `mg_pos` | 各分类的顺序刷题 / 背题进度（key 形如 `"高等教育学/单选"` 或 `"back:高等教育学/单选"`） |
| `mg_mode` | 刷题顺序模式：`"order"` / `"random"` |
| `mg_back` | 学习方式：`true` = 背题模式，`false` = 刷题模式 |

**隐私**：数据只存在本机，不上传。

**重置**：浏览器控制台（F12 → Console）执行 `localStorage.clear()` 后刷新即可清零。

---

## 📁 目录结构

```
MindGym/
├── index.html              # 主入口（单页应用）
├── questions.js            # 题库数据（≈275 KB）
├── questions.json          # 题库 JSON 版（可选）
├── parse_bank.py           # 题库解析脚本（docx → JSON + JS）
├── wechat-pay.jpg          # 微信支付二维码（Footer 打赏区）
├── alipay.jpg              # 支付宝二维码（Footer 打赏区）
├── README.md               # 本文档
└── .gitignore              # 忽略原始 docx 等
```

**GitHub / Pages 部署时**：至少上传 `index.html` + `questions.js`。

---

## 🔧 二次开发 / 题库更新

题库由 `parse_bank.py` 从 docx 解析生成。原文档更新后运行：

```bash
pip install python-docx   # 依赖
python parse_bank.py
```

脚本会自动完成：
1. 读取 docx 全部段落
2. 按「题号回 1」切分 6 段，前段按题号 231 拆分学科
3. 解析题干、A–D 选项、判断题（对 / 错）、答案与解析
4. 校验并输出 `questions.json`，同时生成可被 `index.html` 引用的 `questions.js`

### 题目数据字段

```json
{
  "id": 1,
  "subject": "高等教育学",
  "type": "单选",
  "question": "以下哪项属于高等教育基本职能？",
  "options": { "A": "教学", "B": "科研", "C": "服务社会", "D": "军训" },
  "answer": "C",
  "explanation": null
}
```

| 字段 | 类型 | 说明 |
|---|---|---|
| `id` | int | 全局递增 |
| `subject` | str | `高等教育学` / `高等教育心理学` |
| `type` | str | `单选` / `多选` / `判断` |
| `question` | str | 题干文本 |
| `options` | obj / null | `{"A": "...", "B": "..."}`，判断题为 `null` |
| `answer` | str | 单选/多选：`A` / `ABCD`；判断：`对` / `错` |
| `explanation` | str / null | 解析（原文档仅少量题附解析，多数为 `null`） |

---

## 🏗️ 技术实现要点（面向开发者）

- **零依赖**：原生 HTML / CSS / ES5 兼容写法，无构建工具
- **单页应用**：通过 `show('view-xxx')` 切换三个视图（首页 / 刷题 / 收藏列表）
- **题库注入**：`questions.js` 暴露全局 `QUESTIONS` 数组，`index.html` 用 `<script src>` 加载
- **判分规则**：单选 / 判断字符串精确匹配；多选将用户所选与答案按字母排序后比较（顺序无关）
- **背题模式开关**：`session.sMode`（bool）驱动分支；背题时走 `renderBack()`，选项元素加 `reveal` 类禁用 hover 反馈，答题卡 legend 隐藏对/错
- **响应式**：媒体查询阈值 560px；移动端启用单列卡片 + `position: fixed` 底部操作条，用 `env(safe-area-inset-bottom)` 适配全面屏
- **Lightbox**：全局 click 代理 `.ft-qr img`，弹出全屏遮罩 + 缩放动画；Esc / 点空白 / 点 ✕ 关闭
- **会话管理**：`session` 对象存储当前题组 list、索引、作答记录、答题卡开关；不同分类用独立 key 写入 `posMap`，刷题 / 背题各自维护进度

已通过桌面视口（≥1280px）与移动视口（390 × 844）实测：全部核心功能正常、无横向滚动、零 JS 报错。

---

## 🤔 常见问题

**Q：双击打开后页面什么都没显示？**
A：确认 `questions.js` 与 `index.html` 在同一目录且未改名。也可用 `python -m http.server 8000` 起服务后访问 `http://localhost:8000/` 并查看控制台。

**Q：换电脑 / 换浏览器，进度没同步？**
A：数据存在浏览器 localStorage，跨设备默认不同步。需要多端同步可自行接入后端或云端存储（本项目未包含）。

**Q：背题时选项能点吗？**
A：不能。背题模式下选项是纯展示，cursor 默认、hover 不变色，避免误操作错觉。

**Q：怎么清空错题本 / 收藏？**
A：错题本无单独清空（答对即自动移出）；收藏夹在「我的收藏」页有红色「清空收藏」按钮。整体清零用 `localStorage.clear()`。

**Q：多选题怎么确认？**
A：选完选项后，底部「确认（选 N 项）」按钮会亮起，点击即判分。背题模式下此按钮隐藏。

**Q：打赏二维码怎么保存？**
A：直接点击二维码放大后右键「图片另存为」即可。

---

## 👤 开发信息

- **版本**：MindGym v1.0.0
- **GitHub**：[https://github.com/AlbertSong1024/MindGym](https://github.com/AlbertSong1024/MindGym)
- **部署地址**：[https://albertsong1024.github.io/MindGym/](https://albertsong1024.github.io/MindGym/)
- **技术交流 / 反馈邮箱**：[albert.song@foxmail.com](mailto:albert.song@foxmail.com)

---

## 📜 版权声明

© 2026 柠檬茶有力气 · All rights reserved.

题库内容仅供学习参考，如有侵权请联系删除。

---

## ☕ 打赏支持

如果这个工具帮到了你，请我喝杯咖啡吧～

<div align="center">
  <table>
    <tr>
      <td align="center">
        <img src="wechat-pay.jpg" width="140" alt="微信支付"/><br/>
        <sub>微信</sub>
      </td>
      <td align="center">
        <img src="alipay.jpg" width="140" alt="支付宝"/><br/>
        <sub>支付宝</sub>
      </td>
    </tr>
  </table>
</div>
