# hkustgz-course-pre · 港科广课程 Pre 助手

一个 AI 技能（Skill），**Claude、Codex、DeepSeek Harness 都能用**。装上之后，AI 会按一套固定、靠谱的流程，帮你准备港科广（HKUST(GZ)）课堂上的各种 pre：先讲懂内容，再一起规划怎么讲，最后做出能直接上台用的 PPT，**PowerPoint 和 WPS 都能打开、都能放映**。

> English: An agent skill (Claude, OpenAI Codex, DeepSeek Harness) for planning and building HKUST(GZ) course presentation slides (.pptx) with bilingual speaker notes, click animations and the school logo. Instructions below are in Chinese; the skill itself works in English too.

---

## 这是什么

你可以把它理解成一个"做 pre 的固定搭档"。

平时让 AI 做 PPT，常见问题是：它没搞懂内容就开始做，做出来一堆字，讲的时候也不知道说什么。这个技能把顺序定死了：

1. **先讲懂**：用大白话把论文、项目或者案例给你讲清楚。
2. **再规划**：和你一起定每一页讲什么、配什么图、花多少秒。
3. **你说"开动"才开始做**：在这之前它不会动手做 PPT。

## 能做哪些汇报

| 类型 | 举例 |
|---|---|
| 论文 pre | 按 Author（作者）/ Reviewer（审稿人）/ Researcher（研究者）角色讲一篇论文 |
| 课程项目汇报 | 中期进度汇报、期末成果展示 |
| 开题 / 研究提案 | 讲清楚想研究什么、为什么、怎么做、多久做完 |
| 小组展示 | 多人分工，自动安排谁讲哪几页、怎么交接 |
| 话题 / 案例分析 | 任何专业都能用的通用思路，不需要专业背景 |
| 技术演示 | 展示一个系统或作品，带视频或现场演示 |
| 短 pitch | 1–3 分钟的快速介绍 |

## 怎么安装

先在这个页面点绿色的 **Code → Download ZIP**，下载后解压。然后按你用的工具选一种：

| 你用的工具 | 怎么装 |
|---|---|
| **Claude 网页版 / 桌面版** | 把 `skills/hkustgz-course-pre` 文件夹单独压缩成 zip（Mac：右键 → 压缩；Windows：右键 → 发送到 → 压缩文件夹），在 Claude 设置的 **Skills（技能）** 里上传并打开开关 |
| **Claude Code** | 把 `skills/hkustgz-course-pre` 文件夹放到 `~/.claude/skills/` |
| **Codex** | 把同一个文件夹放到 `~/.agents/skills/` |
| **DeepSeek Harness（dsh）** | 同上，放到 `~/.agents/skills/`（dsh 也认 `~/.dsh/skills/`） |

Mac / Linux 也可以在解压后的文件夹里运行一行命令，三个工具一起装好：

```
bash install.sh
```

装好后让 AI 运行一次 `scripts/check_env.py`，它会告诉你电脑上还缺什么工具、怎么装。

## 怎么开始

装好以后，直接跟 AI 说就行，比如：

- "帮我准备一个港科广课程 pre，8 分钟，我是 Reviewer 角色，论文在附件里。"
- "我们小组下周要做期末项目展示，5 个人，每人 3 分钟。"
- "帮我做一个关于上海垃圾分类政策的案例分析 pre。"

把作业要求、老师的特别要求（比如开头必须讲哪几项）、相关材料一起发给它，效果最好。

## 整个过程

1. **说清楚需求**：AI 会问你缺的信息，比如几分钟、什么角色、PPT 用中文还是英文、喜欢什么颜色。
2. **讲懂内容**：它先用简单的话给你讲，你觉得没听懂就直接说，它会再讲得更简单。
3. **规划大纲**：一张表列清每一页——观众看到什么、你要讲什么、几分钟、怎么过渡到下一页。总时长会控制在限时的九成以内，你满意了再往下走。
4. **说"开动"**：它开始做 PPT。
5. **检查**：它会自己检查有没有文字溢出、时间是否超时、动画和逐字稿是否对得上、PowerPoint 和 WPS 会不会显示不一样。
6. **交付**：你拿到一个 .pptx 文件。
7. **问答准备**（可选）：它预测 5 个最可能被问到的问题，给出 30 秒的回答思路，并标出最难的那个。

## 你需要准备什么

- 作业要求（时长、角色、老师的特别要求）
- 材料：论文 PDF、项目报告、数据、图片等
- 如果想在 PPT 里放视频：**请自己录屏**后发给它（它不会帮你从 YouTube 等网站下载视频）
- 如果想放学校 logo：发一张白底的 logo 图片（本仓库不附带 logo 文件）

## 你会得到什么

- 一份 **.pptx** 文件，PowerPoint 和 WPS 都能打开、放映（字体、图片、视频格式都按两边都支持的来）
- 每页的**备注里有中英双语逐字稿**，演讲者模式下只有你自己看得到
- 逐字稿里标好了 **[CLICK] / 【点击】**，告诉你什么时候该点下一步
- 内容按点击一步步出现的**动画**
- 每页右上角的**学校 logo**，背景深浅会自动换成彩色或白色版本
- 如果有视频，进入那一页会**自动静音循环播放**

## 常用说法

| 你说 | 它会做 |
|---|---|
| "还是没讲清楚" | 换更简单的说法再讲一遍 |
| "开动" | 开始做 PPT |
| "把逐字稿发给我就行" | 只发文字，不改文件 |
| "幽默一点" / "严肃一点" | 调整逐字稿语气 |
| "换个颜色" | 推荐几种配色让你选 |
| "这两个 pre 是同一天的" | 两份逐字稿互相呼应，用"刚才"而不是"上次" |
| "帮我准备问答" | 预测 5 个可能的问题，并给出回答思路 |

## 需要注意的地方

- **内容要自己核对**：AI 可能讲错细节，上台前请对照原文检查一遍关键数字。
- **视频自动播放**：PowerPoint 支持得比较好；WPS 不一定，上台前请先试一下。
- **换了电脑或软件版本**：可以用 `compat_test.js` 生成一份 7 页的测试 PPT，在 PowerPoint 和 WPS 里各放一遍，看字体、备注、动画、视频、logo 是否正常。
- **学校 logo** 属于学校，本仓库不提供，请自己准备。
- 这是学生自发做的工具，**和港科广官方无关**。

## 常见问题

**WPS 怎么打开演讲者模式？**
放映 → 设置放映方式 → 勾选"显示演讲者视图"，然后从头放映。

**不是港科广的学生能用吗？**
能。把 logo 换成你自己学校的就行，其他流程都是通用的。

**我用的是 Codex / DeepSeek，能用吗？**
能。技能没有用任何只有 Claude 才有的功能，只需要 AI 能运行命令。如果你的 AI 不能运行命令，它会把脚本和命令给你，你自己运行就行。

**一定要用英文 PPT 吗？**
不用。开始时告诉它你要中文还是英文就行。

---

## 仓库结构（给想改代码的人）

```
skills/hkustgz-course-pre/
├── SKILL.md            # 技能本体：流程 + 各类 pre 的讲法模板
└── scripts/
    ├── animate.py      # 点击动画、翻页淡入、视频自动循环
    ├── fixnotes.py     # 备注逐行分段（解决 WPS 里挤成一段）
    ├── logo_cutout.py  # 把白底 logo 抠成透明 + 白色两个版本
    ├── fix_fonts.py    # 中文统一用中文字体，PowerPoint 和 WPS 显示一致
    ├── add_logo.py     # 每页右上角加 logo，按背景深浅自动选版本
    ├── check_deck.py   # 检查：点击和逐字稿是否对得上、是否超时、有没有兼容问题
    ├── check_env.py    # 检查电脑上缺什么工具，并给出安装方法
    └── compat_test.js  # 生成 PowerPoint / WPS 兼容性测试 PPT
install.sh              # Mac / Linux 一键安装到 Claude、Codex、dsh
```

脚本依赖：Python 3（`python-pptx`、`Pillow`、`numpy`）和 Node.js（`pptxgenjs`）。LibreOffice、poppler、ffmpeg 是可选的：没有的话少了预览图和自动判断 logo 颜色，PPT 照样能做。

## 致谢

部分做法（每页"观众看到 / 我要讲"的规划表、时间预算、发布前的自动检查）参考了 [歸藏的 guizang-ppt-skill](https://github.com/op7418/guizang-ppt-skill) 的思路，并按 .pptx 和课堂场景重新写过。本仓库没有复制它的代码或文字。

## License

[MIT](LICENSE)
