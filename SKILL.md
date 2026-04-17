---
name: wechat-sticker-generator
description: 一键生成符合微信规范的动态(GIF)及静态(PNG)系列表情包套件。支持12种画风、10大场景主题、真人照片转Q版，全自动切割合成标准产物。
version: 1.0.0
author: sterlingdon
license: MIT
tags:
  - wechat
  - sticker
  - image-generation
  - gif
  - emoji
  - animation
keywords:
  - 表情包
  - 动图
  - GIF生成
  - 微信贴纸
  - Q版角色
  - 真人转Q版
triggers:
  - "表情包"
  - "动图"
  - "贴纸"
  - "sticker"
  - "做表情"
metadata:
  openclaw:
    requires:
      env:
        - GEMINI_API_KEY
        - DASHSCOPE_API_KEY
      anyBins:
        - python3
        - python
    primaryEnv: GEMINI_API_KEY
    emoji: "🎭"
    homepage: https://github.com/sterlingdon/wechat_skills
    install:
      - kind: pip
        package: rembg onnxruntime pillow requests google-genai dashscope
---

# 📄 WeChat Sticker Generator (微信表情包套件生成器)

## 1. Skill 概述 (Overview)

本 Skill 专为 AI Agent 设计，提供自动化生成极具戏剧张力、符合微信规范的"动态 GIF 表情包"及"静态图集"。

**核心能力：**

- 🎨 **12种预设画风** — 从二次元到3D黏土，像素风到水墨国风
- 🎭 **10大场景主题** — 综合、节日、恋爱、问候、职场、学习、游戏、萌宠、美食、运动
- 👤 **灵活角色系统** — 支持原创角色、知名IP、真人Q版化
- 📸 **真人照片转Q版** — 上传照片→自动转换→生成表情包（保留真人特征）
- 🔒 **角色一致性锁定** — 通过参考图保证多套件角色长相统一
- ⚡ **全自动流水线** — 一键生成宫格图→切片→GIF 合成；支持 **9宫格（0.9秒）** 或 **16宫格（1.6秒）** 动画时长可选；**`origin/`** 为原图仅裁剪缩放，去背景成功时额外多 **`nobg/`**（透明）；自动打包符合微信官方表情包标准规范的上传资产，按要求整理产出 **`wechat_export/`** 目录（包含全套规范主图、缩略图、封面、图标、横幅），方便直达打包导出。

---

## 2. 配置 (Configuration)

### 2.1 支持的图片生成 API

本 Skill 支持多种图片生成 API，可灵活切换：

| Provider          | 特点               | 获取 API Key                                               |
| ----------------- | ------------------ | ---------------------------------------------------------- |
| **gemini** (默认) | 效果好速度快，推荐 | [Google AI Studio](https://aistudio.google.com/app/apikey) |
| **qwen**          | 国内访问稳定       | [阿里云 DashScope](https://dashscope.console.aliyun.com/)  |

### 2.2 配置方式

**方式一：环境变量（推荐）**

```bash
# Gemini
export GEMINI_API_KEY="你的API_Key"

# 或 千问
export DASHSCOPE_API_KEY="你的API_Key"
```

**方式二：手动编辑配置文件**

配置文件位于用户主目录：

| 系统 | 配置文件路径 |
|-----|-------------|
| macOS/Linux | `~/.sticker_generator_config.json` |
| Windows | `C:\Users\你的用户名\.sticker_generator_config.json` |

手动创建或编辑该文件，内容示例：

```json
{
  "default_provider": "gemini",
  "providers": {
    "gemini": {
      "api_key": "你的Gemini_API_Key"
    },
    "qwen": {
      "api_key": "你的千问_API_Key"
    }
  }
}
```

> ⚠️ **安全提示**：请勿在对话中直接提供 API Key。请在终端中自行配置，避免泄露风险。

### 2.3 首次使用检查

在运行任何生成命令前，Agent 应先检查配置：

```bash
python3 sticker_utils.py config
```

如果显示 `❌` 表示缺少 API Key，需要引导用户配置。

### 2.4 背景去除依赖（可选但推荐）

当 `background_type` 设为 `transparent` 时，`process` 阶段会自动执行去背景。默认使用本地模型 `rembg`（默认模型 `isnet-anime`，适合动漫风格）。

```bash
# 推荐安装
pip install rembg

# 如果报 onnxruntime 相关错误，再补一个 CPU 版本
pip install onnxruntime
```

---

## 3. 完整参数结构 (Input Schema)

```json
{
  "mode": "animated",
  "set_name": "打工人龙虾",
  "set_description": "一只每天为了KPI奋斗的Q版龙虾，完美演绎职场辛酸与欢乐！",
  "copyright_info": "OpenClaw 2026",
  "character_name": "虾虾",
  "character_prompt": "角色的外观长相详细设定（只描述外观，不要写动作）",
  "reference_image": "【可选】参考图路径，用于锁定角色长相",
  "style_preset": "2D_KAWAII",
  "custom_style": "【可选】自定义风格描述，仅当 style_preset 为 CUSTOM 时生效",
  "scene_theme": "WORKPLACE",
  "character_type": "HUMAN_CHIBI",
  "color_mood": "BRIGHT_VIBRANT",
  "background_type": "transparent",
  "enable_bg_removal": true,
  "bg_removal_method": "dual",
  "bg_removal_model": "isnet-anime",
  "bg_removal_script_path": "【可选】自定义去背景脚本路径",
  "bg_alpha_matting": true,
  "bg_sharpen_edges": false,
  "bg_sharpen_threshold": 200,
  "grid_size": 9,
  "expressions": [
    {
      "action": "高度戏剧化的动作描述（必须有大幅度的身体运动！）",
      "text": "配文文字（建议2-4个字，醒目有力）"
    }
  ]
}
```

### 3.0 宫格配置 (Grid Size)

| grid_size | 布局 | 帧数 | GIF 时长 | 适用场景 |
| --------- | ---- | ---- | -------- | -------- |
| `9` (默认) | 3×3 | 9 帧 | 0.9 秒 | 标准动画，流畅简洁 |
| `16` | 4×4 | 16 帧 | 1.6 秒 | 更长动画，动作细节更丰富 |

**选择建议：**
- **9帧 (默认)**：适合大多数场景，生成速度快，文件体积小
- **16帧**：适合需要更细腻动作过渡的场景，动画更流畅但文件体积略大

**注意**：微信表情包主图文件大小限制为 **500KB**，16帧动画通常在此范围内，但如果动作复杂、颜色丰富可能接近限制。

### 3.0 背景类型与去除算法 (Background Type & Removal Method)

| 选项          | 背景描述           | 适用场景                               |
| ------------- | ------------------ | -------------------------------------- |
| `transparent` | 透明背景           | **默认值**，微信官方表情包要求透明背景 |
| `white`       | 纯白背景 (#FFFFFF) | 需要纯色背景时的备选                   |

**关于去背景算法配置 (`bg_removal_method`)：**

本项目采用了**三轨背景去除系统**，支持灵活切换：

| `bg_removal_method` | 处理粒度 | 原理与特点 |
|---------------------|---------|----------|
| **`opencv`** | **整图一次性处理** | **质量最优的抗锯齿**：基于漫水填充 (`floodFill`) + 柔和边缘 Alpha 过渡。处理整张宫格大图，确保各帧表情切图后的边缘裁切规则完全一致（有效防止 GIF 边缘闪烁问题）。对字体周边和半透明毛发过渡处理完美。**前提是原图背景必须非常接近纯白**。⚠️ **注意**：浅色前景（水墨、淡彩、浅色皮肤）可能被误删。 |
| **`rembg`** | **单格切分后处理** | **极高的鲁棒性**：基于深度学习（Semantic Segmentation），无视复杂背景强行抠图。由于大图信息量复杂容易导致模型注意力涣散，所以系统会**先切分为小图再分别送入 rembg**。对纯色白底有轻微锯齿感，适合 OpenCV 失败时的智能兜底。⚠️ **注意**：可能误删表情包文字。 |
| **`dual`** (推荐) | **双通道合并** | **最佳平衡方案**：同时运行 OpenCV 和 Rembg，取两者 Alpha 的最大值 (`max(alpha_opencv, alpha_rembg)`)。**优点**：OpenCV 保护文字，Rembg 保护浅色前景（水墨、淡彩、像素风、Q版浅色皮肤）。**适用**：水墨风、水彩风、像素风、Q版等浅色前景场景。 |

**风格与方法推荐映射：**

| 风格 (style_preset) | 推荐方法 | 原因 |
|---------------------|---------|------|
| `CHINESE_INK` (水墨风) | `dual` ⭐ | 淡墨易被 opencv 删除，dual 保护水墨+文字 |
| `WATERCOLOR` (水彩风) | `dual` ⭐ | 淡彩易被 opencv 删除，dual 保护水彩+文字 |
| `PIXEL_ART` (像素风) | `dual` ⭐ | 浅色像素易被删除，dual 保护像素+文字 |
| `CHIBI_SD` (Q版) | `dual` | 浅色皮肤保护+文字保护 |
| `2D_KAWAII` | `dual` 或 `opencv` | 深色角色可用 opencv，浅色用 dual |
| `MEME_STYLE` | `opencv` | 文字保护优先，边缘质量最优 |
| `3D_CLAY` / `3D_PIXAR` | `dual` | 半透明效果保护 |

**执行细节与 Fallback 机制：**
- 微信的官方表情包要求透明背景，去除背景更符合审核要求
- **推荐设置 `bg_removal_method: "dual"`**（最佳平衡，保护浅色前景+文字）
- 对于纯白背景且前景颜色较深的简单图，可使用 `opencv` 获得最佳边缘质量
- **自动降级**：如果配置了 `opencv` 算法，但在执行前系统检测出生成的图表并非纯白背景（AI 幻觉生成了复杂场景图）或执行期间出现错误，系统会自动抛出异常，**并无缝降级使用 `rembg` 进行按格拆分抠图兜底处理**，不用人工介入！
- 去背景失败时会保留该帧原图。
- 去背景开启且成功时，会在同目录下保存 **`original_grid_nobg.png`**：整图去背景之后的 PNG，便于对照 `original_grid.png` 检查抠图效果
- **目录统一**：**`origin/`** 内为**原图输出**（仅裁剪+240 缩放，无去背）；去背景成功时**额外**多 **`nobg/`**；未开去背景或全量失败时只有 `origin/`
- **汇总打包导出**：同一 workspace 在 process 时，会在根目录生成 **`wechat_export/`** 文件夹，包含 `main/`, `thumb/`, `cover.png`, `icon.png`, `banner.png`, 及填单信息文本 `upload_info.txt`。

---

## 3. 参数选项详解 (Parameter Options)

### 3.1 风格预设 (style_preset)

| 选项            | 风格描述                         | 适用场景         |
| --------------- | -------------------------------- | ---------------- |
| `2D_KAWAII`     | 日系二次元，圆润可爱，线条干净   | 通用，最推荐     |
| `2D_ANIME_COOL` | 日系帅气风，锐利线条，炫酷感     | 少年向、热血主题 |
| `3D_CLAY`       | 3D黏土质感，柔软立体，手办感     | 儿童、萌系       |
| `3D_PIXAR`      | 皮克斯风格，欧美3D动画质感       | 欧美风、全年龄   |
| `PIXEL_ART`     | 16bit像素风，复古游戏感          | 极客、游戏主题   |
| `CHINESE_INK`   | 中国水墨风，淡雅意境             | 国风、文艺       |
| `WATERCOLOR`    | 水彩手绘风，温柔治愈             | 文艺、清新       |
| `LINE_ART`      | 极简黑白线条，手绘涂鸦感         | 极简风、表情符号 |
| `CARTOON_WEST`  | 美式卡通风，夸张变形             | 搞笑、欧美风     |
| `CHIBI_SD`      | Q版SD比例，头大身小              | 萌系、游戏角色   |
| `MEME_STYLE`    | 表情包网红风，魔性夸张           | 搞笑、网络流行   |
| `CUSTOM`        | 自定义风格（需填写custom_style） | 特殊需求         |

### 3.2 场景主题 (scene_theme) 【可自由发挥或参考预设】

用户可以**自由发挥**描述任意场景，系统会根据场景自动生成合适的表情配文。以下预设场景可直接映射到微信后台：

| 选项            | 微信后台对应勾选          | 适用场景及配文参考                |
| --------------- | ------------------------- | --------------------------------- |
| `COMPREHENSIVE` | **综合**                  | 日常常用、各类百搭场景            |
| `FESTIVAL`      | **节日节气** / **节日**   | 新年快乐、生日快乐、中秋快乐      |
| `ROMANCE`       | **恋爱交友**              | 想你、爱你、么么哒、在吗、晚安    |
| `GREETING`      | **祝福问候** / **打招呼** | 早安、晚安、谢谢老铁、对不起      |
| `WORKPLACE`     | **职场工作**              | 收到、好的、在忙、下班、KPI、干饭 |
| `STUDY`         | **毕业 / 学生**           | 加油、不想学、过了、求过          |
| `GAMING`        | **游戏电竞**              | 胜利、GG、带飞、菜鸡、上号        |
| `PETS`          | **动物萌宠**              | 萌喵、傻犬相关专属                |
| `FOOD`          | **饮食吃饭**              | 喝奶茶、饿了、大餐                |
| `SPORTS`        | **运动健身**              | 冲刺、流汗、去健身                |

> **💡 提示**：场景主题不限于此表，用户可自由描述想要的场景（如"熬夜党"、"咸鱼躺平"、"吃货日常"等），AI 会智能生成对应的表情动作和配文。

### 3.3 角色类型 (character_type)

| 选项                 | 类型描述     | character_prompt 示例                          |
| -------------------- | ------------ | ---------------------------------------------- |
| `HUMAN_CHIBI`        | Q版人类角色  | "一个戴眼镜的短发女生，穿着蓝色卫衣，圆脸大眼" |
| `HUMAN_ANIME`        | 日系动漫人物 | "银色长发少女，红瞳，哥特萝莉装"               |
| `ANIMAL_CUTE`        | 可爱动物     | "一只橘猫，胖乎乎，大眼睛，尾巴翘起"           |
| `ANIMAL_ANTHRO`      | 拟人化动物   | "穿西装的兔子先生，戴礼帽，绅士风度"           |
| `FANTASY`            | 奇幻生物     | "一只小精灵，透明翅膀，发光，飘浮在空中"       |
| `OBJECT_PERSONIFIED` | 拟人化物品   | "一个有表情的饭团，三角形，海苔脸"             |
| `IP_CHARACTER`       | 知名IP角色   | "皮卡丘，黄色电气鼠，红脸颊，闪电尾巴"         |

### 3.4 配色氛围 (color_mood)

| 选项             | 色调描述                   |
| ---------------- | -------------------------- |
| `BRIGHT_VIBRANT` | 明亮鲜艳，高饱和度（默认） |
| `SOFT_PASTEL`    | 柔和粉彩，马卡龙色系       |
| `WARM_COZY`      | 暖色调，温馨舒适           |
| `COOL_CALM`      | 冷色调，沉稳冷静           |
| `MONOCHROME`     | 黑白单色                   |
| `NEON_CYBER`     | 霓虹赛博，荧光色           |
| `VINTAGE_RETRO`  | 复古怀旧，褪色感           |

---

## 4. 动作描述指南 (Action Description Guide)

**⚠️ 关键原则：动作必须有大幅度的身体运动，决不能是"面瘫"表情！**

### 好的动作描述 ✅

```
"向后仰头大笑，笑到眼泪飞溅，肚子剧烈颤抖"
"整个人趴在地上打滚，四肢乱蹬，撒泼耍赖"
"双手捂脸从指缝偷看，身体扭成麻花状"
"一口吞下整个汉堡，腮帮子鼓成气球，打了个超大的饱嗝"
"像火箭一样冲向屏幕，整个人撞在屏幕上滑下来"
```

### 不好的动作描述 ❌

```
"微笑" → 太静止
"开心地看着" → 缺乏动作
"表示同意" → 太抽象
"做出生气的表情" → 动作幅度太小
```

### 戏剧化公式

```
动作 = 夸张的身体姿态 + 面部表情变化 + (可选)道具/特效

示例：
基础版: "开心地笑"
戏剧版: "整个人跳起来双手比V，笑到嘴巴裂到耳朵，周围炸开烟花特效"
```

---

## 5. 完整示例 (Complete Example)

### 用户请求

> "帮我做一套打工人表情包，角色是一个秃头程序员大叔，要动态的，搞笑一点"

### 最终 params.json

```json
{
  "mode": "animated",
  "set_name": "秃头小猿",
  "set_description": "每天修Bug、抗击KPI的卑微打工人日常，虽然头秃但依然坚强！",
  "copyright_info": "李强制作",
  "character_name": "秃头猿",
  "character_prompt": "一个中年秃头程序员大叔，圆脸，稀疏的头发，戴厚底黑框眼镜，穿着皱巴巴的格子衬衫，黑眼圈很重，一脸疲惫但眼神呆萌",
  "reference_image": "",
  "style_preset": "MEME_STYLE",
  "custom_style": "",
  "scene_theme": "WORKPLACE",
  "character_type": "HUMAN_CHIBI",
  "color_mood": "BRIGHT_VIBRANT",
  "background_type": "transparent",
  "enable_bg_removal": true,
  "bg_removal_method": "dual",
  "bg_removal_model": "isnet-anime",
  "bg_removal_script_path": "",
  "bg_alpha_matting": true,
  "bg_sharpen_edges": false,
  "bg_sharpen_threshold": 200,
  "grid_size": 9,
  "expressions": [
    {"action": "疯狂敲键盘到手指冒烟，眼睛瞪得像铜铃，整个人变成残影", "text": "搬砖"},
    {"action": "看到代码报错，整个人石化碎裂成渣，眼珠子弹出来", "text": "寄!"},
    {"action": "下班时间一到，瞬间变身火箭冲出办公室，留下一道残影", "text": "润了"},
    {"action": "收到甲方需求，整个人瘫倒在桌上，眼睛变成死鱼眼", "text": "好累"},
    {"action": "开会被点名，满头大汗，两只手不知道往哪放", "text": "慌了"},
    {"action": "摸鱼被抓包，表情僵硬，嘴角抽搐，冷汗直流", "text": "完了"},
    {"action": "看到工资条，眼睛变成金钱符号，整个人飘起来", "text": "真香"},
    {"action": "老板走近工位，立刻切换屏幕，假装认真工作", "text": "装忙"},
    {"action": "项目上线成功，双手比V，跳起来庆祝，周围飘彩带", "text": "成了"}
  ]
}
```

> **💡 提示（关于宫格类型与数量的严格要求）**：
> - **静态模式 (static)**：每个宫格包含 **9 或 16 张独立的静态表情**。`expressions` 数组元素个数必须等于 `grid_size`。微信专辑标准需要 **24 张** 静态表情，因此通常需要生成 3 个 9宫格（27 张，截取24张） 或 2 个 16宫格（32 张，截取24张）。
> - **动态模式 (animated)**：每一个宫格（无论9宫格还是16宫格）代表 **1 个 GIF** 的多帧动画。`expressions` 数组元素个数必须等于 `grid_size`。微信专辑标准需要 **24 个 GIF**，因此如果做整套动态表情包，需要生成 **24 个宫格图**（即 `anim_01` 到 `anim_24`，每次对应生成一个 GIF）。
> - 以上 params.json 示例仅展示了部分 expression 作为演示，**智能体在实际执行时，必须将其补全到与 `grid_size` 一致的数量！**（如果是 9 宫格，填 9 个；16 宫格，填 16 个）

### 预期产出

**静态模式 (static) - 24张表情（以9宫格为例，需3个宫格）：**
```
~/Documents/wechat-sticker-output/20260321_120000_gemini/
├── params.json
├── static_01/                     ← 第1个宫格（9张或16张静态表情）
│   ├── original_grid.png
│   ├── origin/                    ← sticker_01~09.png (或 ~16)
│   └── nobg/                      ← 透明背景版
├── static_02/                     ← 第2个宫格
│   └── …
├── static_03/                     ← 第3个宫格
│   └── …
└── wechat_export/
    ├── main/                      ← 01~24.png (240x240)
    └── thumb/                     ← 01~24.png (120x120)
```

**动态模式 (animated) - 24个GIF（需24个宫格）：**
```
~/Documents/wechat-sticker-output/20260321_120000_gemini/
├── params.json
├── anim_01/                       ← 第1个GIF（9帧或16帧动画）
│   ├── original_grid.png
│   ├── origin/
│   │   ├── sticker_01~09.png (或 ~16)
│   │   └── animated_sticker.gif   ← 9帧或16帧合成的GIF
│   └── nobg/
├── anim_02/                       ← 第2个GIF
│   └── …
├── ... (共24个anim_XX目录)
├── anim_24/                       ← 第24个GIF
│   └── …
└── wechat_export/
    ├── main/                      ← 01~24.gif (240x240)
    └── thumb/                     ← 01~24.png (120x120)
```

---

## 6. 真人照片 → Q版表情包 (Photo-to-Chibi Feature)

**🌟 特色功能：将用户的真人照片转换为Q版动画风格的表情包！**

### 使用场景

用户想要：

- 把自己/朋友的照片做成表情包
- 保持真人特征的同时变成可爱Q版
- 情侣头像、闺蜜头像表情包化

### 完整流程

#### 用户请求示例

> "用我这张照片，帮我做一套可爱的表情包，要那种Q版的，3个动图"

### transform_photo 命令详解

```bash
python3 sticker_utils.py transform_photo <photo_path> <style_preset> <output_path> [additional_description]
```

| 参数                     | 说明                                            |
| ------------------------ | ----------------------------------------------- |
| `photo_path`             | 用户提供的真人照片路径                          |
| `style_preset`           | **目标风格** - 支持所有 12 种风格（见下方表格） |
| `output_path`            | 输出的定妆图路径                                |
| `additional_description` | 【可选】额外描述，如"戴眼镜"、"长发"等          |

**🌟 支持所有风格转换：**

| 风格            | 适合场景   | 转换效果           |
| --------------- | ---------- | ------------------ |
| `2D_KAWAII`     | 通用可爱风 | 日系圆润 Q 版      |
| `2D_ANIME_COOL` | 帅气少年   | 锐利线条，酷感十足 |
| `3D_CLAY`       | 儿童/萌系  | 黏土手办质感       |
| `3D_PIXAR`      | 全年龄     | 皮克斯动画风格     |
| `PIXEL_ART`     | 游戏玩家   | 复古像素风         |
| `CHINESE_INK`   | 文艺国风   | 水墨画风格         |
| `WATERCOLOR`    | 清新治愈   | 水彩手绘感         |
| `LINE_ART`      | 极简风     | 黑白线条画         |
| `CARTOON_WEST`  | 搞笑欧美   | 美式夸张卡通风     |
| `CHIBI_SD`      | 超萌 Q 版  | 头超大身超小       |
| `MEME_STYLE`    | 网络流行   | 魔性表情包风       |

**🔒 自动优化：**

Gemini 会自动进行以下处理：

1. **主角识别** - 自动识别照片中的主要人物（无需预处理）
2. **风格转换** - 将真人转换为指定风格的 Q 版角色
3. **特征保留** - 保留真人关键特征（脸型、发型、眼镜等）
4. **尺寸优化** - 输出 512x512 标准尺寸
5. **白底纯净** - 纯白背景，无多余元素

### 关键点说明

**为什么必须用 `draw_with_ref` 而不是普通 `draw`？**

- 普通 `draw` 只发送文字 prompt，模型看不到参考图
- `draw_with_ref` 会把参考图作为多模态输入传给模型
- 模型会"看着"参考图来画，保证角色特征一致

**真人特征保留机制：**

脚本会自动强调保留以下特征：

- 脸型（圆脸/瓜子脸/方脸等）
- 眼睛形状和神态
- 鼻子嘴巴特征
- 发型发色
- 标志性特征（眼镜、胡须、痣等）

### 推荐风格搭配

| 原照片类型 | 推荐风格        | 效果               |
| ---------- | --------------- | ------------------ |
| 普通人像   | `2D_KAWAII`     | 日系可爱风，最通用 |
| 男生照片   | `2D_ANIME_COOL` | 帅气少年风         |
| 儿童照片   | `3D_CLAY`       | 黏土手办感，超萌   |
| 情侣照片   | `2D_KAWAII`     | 甜系 Q 版          |
| 游戏玩家   | `PIXEL_ART`     | 复古游戏风         |
| 搞笑表情   | `MEME_STYLE`    | 网红表情包风       |

---

## 7. 智能体执行流程 (Execution Workflow)

### 【前置检查】模型出图能力检测（优先执行）

在启动流水线前，先检测 API Key 配置状态：

```bash
python3 sticker_utils.py config
```

**情况 A：已配置 API Key**
- 显示 ✅ → 直接继续后续流程

**情况 B：未配置 API Key**

Agent 向用户展示两条路径选择：

| 路径 | 说明 | 后续流程 |
|-----|------|---------|
| **路径A：配置 API** | 获取并配置 API Key，后续全自动 | 推荐 |
| **路径B：手动出图** | 不配置，去外部平台生成图片 | 需用户手动介入 |

---

#### 路径A - 配置 API Key（推荐）

**获取 API Key：**
- Gemini：https://aistudio.google.com/app/apikey
- 千问：https://dashscope.console.aliyun.com/

**配置方式：**
```bash
# Gemini
export GEMINI_API_KEY="你的API_Key"

# 千问
export DASHSCOPE_API_KEY="你的API_Key"
```

配置完成后重新检测，继续后续流程。

---

#### 路径B - 手动出图流程

> **⚠️ 关键：如果用户提供了定妆图，输出 prompt 时必须告知用户带上定妆图去外部平台！**

---

**前置处理：定妆图处理**

| 用户情况 | Agent 处理 |
|---------|-----------|
| **有定妆图（路径）** | `cp <用户路径> $DIR_PATH/base_reference.png` |
| **有定妆图（对话上传）** | Agent 识别图片，移动到 `$DIR_PATH/base_reference.png` |
| **无定妆图** | 纯文字描述生成 prompt，不涉及定妆图 |

---

**步骤 1：生成并输出 prompt**
```bash
python3 sticker_utils.py build_prompts $DIR_PATH
```
- 每个表情生成独立的 `prompt.txt`
- 告知用户文件路径：`$DIR_PATH/anim_XX/prompt.txt`

**步骤 2：引导用户去外部平台生图**

| 定妆图情况 | 引导内容 |
|----------|---------|
| **有定妆图** | 告知用户：带上 `$DIR_PATH/base_reference.png` 去外部平台，作为参考图上传 |
| **无定妆图** | 只需要复制 prompt.txt 内容即可 |

- 详细操作指南见 `reference/external_platform_guide.md`

**步骤 3：接收用户返回的图片** ⭐
- 用户在对话中上传/粘贴图片
- Agent 识别图片并移动到正确位置：
  ```bash
  mv <用户上传图片> $DIR_PATH/anim_XX/original_grid.png
  ```
- **批量场景**：逐张上传 → 逐张处理 → 实时反馈进度

**步骤 4：执行切割处理**
```bash
python3 sticker_utils.py process $DIR_PATH
```

**步骤 5：告知导出位置**
- 导出目录结构及查看方式见 `reference/output_guide.md`

---

### 【第零步】用户需求收集（必须询问）

**⚠️ 在开始任何操作前，必须向用户确认以下信息：**

| 需要询问的信息 | 是否必填 | 说明 |
|---------------|---------|------|
| **定妆图** | 可选 | 白底、正面、无动作的标准基准图（用于锁定角色一致性）。可以是文件路径，也可以在对话中直接上传图片 |
| **角色外观描述** | 推荐 | 如果没有定妆图，需要文字描述角色长相（只写外观，不写动作） |
| **角色名称** | 可选 | 角色的名字，用于表情包命名和文案生成 |
| **风格** | 推荐 | 从 12 种预设风格中选择（见 §3.1 风格预设） |
| **场景主题** | 推荐 | 从 10 大场景主题中选择（见 §3.2 场景主题） |
| **模式** | 推荐 | 选择生成 **静态图集** 还是 **动态GIF** |
| **宫格类型** | 推荐 | 选择 **9宫格**（0.9秒/9帧，速度快）或 **16宫格**（1.6秒/16帧，动作细腻） |
| **表情数量** | 推荐 | 默认 **9个表情**（单套），微信专辑标准需 **24个** |

**询问话术示例：**
> "在开始生成表情包之前，请告诉我以下信息：
> 1. **定妆图**：有现成的角色定妆图吗？（白底、正面、无动作的标准图。如有请提供路径或直接上传图片）
> 2. **角色外观**：如果没有定妆图，请描述角色长相（只写外观，如"胖橘猫，圆脸大眼，戴小领带"）
> 3. **角色名称**：角色叫什么名字？（不提供则自动生成）
> 4. **风格**：选择哪种画风？（水墨风、像素风、水彩风、二次元可爱风等，共12种可选）
> 5. **场景主题**：想要什么场景？（可自由发挥，如职场打工、恋爱、游戏电竞等）
> 6. **模式**：需要**静态表情**（默认）还是**动态GIF**？
> 7. **宫格类型**：需要9宫格（9帧/0.9秒，生成快）还是16宫格（16帧/1.6秒，动作更细腻）？
> 8. **数量**：默认生成 **9个** 表情，微信专辑标准需要 **24个**，需要调整吗？"

**定妆图概念说明：**
- **定妆图** = 白底纯背景、正面姿势、无夸张动作的角色基准图
- **作用**：锁定角色外观一致性，每次生图时让 AI"看着"这张图来画
- **来源方式**：
  - 用户直接提供（对话上传图片 / 文件路径）
  - 用户提供参考图 → Agent 用 AI 生成标准定妆图
  - 用户纯文字描述 → Agent 用 AI 生成定妆图

**处理逻辑：**
- **用户提供定妆图** → Agent 移动图片到 `$DIR_PATH/base_reference.png`
- **用户提供参考图** → Agent 用 AI 生成标准化定妆图（白底、正面、无动作）
- **用户无图，仅文字描述** → Agent 用 AI 生成定妆图
- **用户未指定风格** → 默认使用 `2D_KAWAII`（日系二次元可爱风）
- **用户未指定场景** → 默认使用 `COMPREHENSIVE`（综合场景）
- **用户未指定模式** → 默认使用 **静态模式 (static)**
- **用户未指定宫格类型** → 默认使用 **9宫格** (`grid_size: 9`)
- **用户未指定数量** → 默认生成 **9 个表情**（单套）；微信专辑标准需要 **24 个**

---

### 【第一步】沙盒建站

在启动流水线之前，必须先创建一个隔离的工作站目录。

```bash
DIR_PATH=$(python3 sticker_utils.py create_dir --provider gemini)
```

### 【第二步】角色定妆与入驻（统一生成标准基准图）

**⚠️ 核心定律：所有表情包的生成，必须依赖一张白底、正面、无动作的"定妆图" (`base_reference.png`。**

> 注：定妆图处理已在【第零步】和【前置检查】中说明。本步骤仅适用于 **有 API Key** 的情况。

---

**路径A（有 API Key）- AI 生成定妆图：**

| 用户情况 | Agent 处理 |
|---------|-----------|
| **用户提供定妆图** | 直接复制到 `$DIR_PATH/base_reference.png` |
| **用户提供参考图** | 用 AI 生成标准化定妆图（白底、正面、无动作） |
| **用户无图，纯文字** | 用 AI 生成定妆图 |

**AI 生成定妆图命令：**
```bash
# 无图生成
python3 sticker_utils.py draw_character “角色外观描述” “STYLE” “$DIR_PATH/base_reference.png”

# 有参考图生成
python3 sticker_utils.py draw_with_ref “$DIR_PATH/user_reference.png” “角色外观描述” “STYLE” “$DIR_PATH/base_reference.png”

# 真人照片转Q版
python3 sticker_utils.py transform_photo “$DIR_PATH/user_photo.jpg” “STYLE” “$DIR_PATH/base_reference.png”
```

**路径B（无 API Key）- 手动流程：**
- 定妆图处理已在【前置检查】路径B中说明
- 此步骤跳过，直接进入【第三步】

---

### 【第三步】写入配置

将组装好的 JSON 写入 `$DIR_PATH/params.json`。
**确保 `reference_image` 字段已填入第二步中准备好的 `$DIR_PATH/base_reference.png`！**

```bash
cat > "$DIR_PATH/params.json" << 'EOF'
{
  "mode": "animated",
  "set_name": "表情包名称",
  "set_description": "表情包描述（不超过80字）",
  "copyright_info": "版权信息",
  "character_name": "角色名称",
  "character_prompt": "角色外观描述（只写外观，不写动作）",
  "reference_image": "$DIR_PATH/base_reference.png",
  "style_preset": "2D_KAWAII",
  "custom_style": "",
  "scene_theme": "COMPREHENSIVE",
  "character_type": "HUMAN_CHIBI",
  "color_mood": "BRIGHT_VIBRANT",
  "background_type": "transparent",
  "enable_bg_removal": true,
  "bg_removal_method": "dual",
  "bg_removal_model": "isnet-anime",
  "bg_removal_script_path": "",
  "bg_alpha_matting": true,
  "bg_sharpen_edges": false,
  "bg_sharpen_threshold": 200,
  "grid_size": 9,
  "expressions": [
    {"action": "动作描述1", "text": "配文1"},
    {"action": "动作描述2", "text": "配文2"}
  ]
}
EOF
```

### 【第四步】解析裂变（配置转 Prompt）

为每个表情动作创建独立的生成子目录和 Prompt 文件：
```bash
python3 sticker_utils.py build_prompts $DIR_PATH
```

### 【第五步】批量生图（AI 出宫格原图）

**一条命令自动处理所有 `anim_*` 或 `static_*` 目录，无需手动循环。默认顺序执行（并发数=1），确保角色一致性。**

```bash
# 自动检测是否有 reference_image，顺序生成（推荐，保证角色一致）
python3 sticker_utils.py batch_draw $DIR_PATH

# 可选：并发执行（可能影响角色一致性，慎用）
python3 sticker_utils.py batch_draw $DIR_PATH --concurrent 2 --delay 3.0
```

> **可插拔调试提示**：若目录下已存在人工放入的 `original_grid.png`，可直接跳过此步！

### 【第六步】去背景与切片（生成最终贴纸和 GIF）

根据 `params.json` 的 `bg_removal_method` 执行抠图与切割。
```bash
python3 sticker_utils.py process $DIR_PATH
```

---

### 【第七步】AI 补充微信物料（Banner / Cover / 介绍文案）

**⚠️ 此步骤必须执行，不可跳过！** `process` 命令生成的 `wechat_export/` 中的 banner.png 和 cover.png 只是占位图，必须通过本步骤用 AI 重新生成高质量宣传图。

```bash
python3 sticker_utils.py wechat_meta $DIR_PATH
```

**本步骤的产出（会覆盖 process 的占位内容）：**

| 产物文件 | 规格 | 说明 |
|---|---|---|
| `wechat_export/upload_info.txt` | 文本 | AI 生成的≤80字合集介绍 + 每个表情的4字含义标签 + 风格/主题分类 |
| `wechat_export/banner.png` | 750×400 | AI 专属绘制的横幅（角色与场景主题融合，含合集名称创意排版） |
| `wechat_export/cover.png` | 240×240 | AI 专属绘制的封面（角色特写，直视镜头，高吸引力） |
| `wechat_export/icon.png` | 50×50 | 封面缩小版，用于聊天面板图标 |

**动态读取机制（重要）：** `wechat_meta` 生成功能的所有 AI Prompt 均通过读取 `params.json` 动态组装：
- `set_name`、`character_prompt`、`scene_theme`、`style_preset` 等字段都从 params 文件取值
- 脚本本身不含任何硬编码的角色名或场景，适用于任意表情包套件

---

### 【例外情况：中途失败时的兜底处理】

> 注：若在第四步批量生图时 API 调用失败，可参考上述「前置检查 - 路径B」进行人工干预：用户手动出图 → 返回图片 → Agent 接管切割流程。

**附加彩蛋（直接传图切片）**：
如果用户直接提供一张已画好的宫格网格图（9宫格或16宫格），可跳过生图步骤：新建沙盒文件夹 → 放入 `anim_01/original_grid.png` → 运行 `process` 命令即可！

---

## 8. 输出交付 (Output Handover)

返回沙盒目录路径，并**首要提醒用户**查看直接可以上传的终极发布包：

- 🎁 **微信直接上传规范包 `wechat_export/`（核心产物）**：
  - **`wechat_export/main/`**：包含编号为 `01~24` 的 240x240 主图，满足规范约束。
  - **`wechat_export/thumb/`**：包含编号为 `01~24` 的 120x120 小方块缩略图。
  - **`wechat_export/cover.png`**、**`icon.png`**、**`banner.png`**：引擎自动化截取配置的首发配套资产图。
  - **`wechat_export/upload_info.txt`**：自动生成的表情包名称、介绍、版权信息，可以直接去微信后台复制粘贴。

- ✂️ **过程拆解留档资产（存于 `anim_XX/` 或 `static_XX/` 内）**
  - **`origin/`** 存放各画稿原始提取未抠背产物
  - **`nobg/`** 存放各底稿执行抠背透明提取后的版本
  - **`original_grid_nobg.png`** 为网格整底切除的预览大参考图
