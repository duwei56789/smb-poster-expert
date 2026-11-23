---
name: poster-generation
description: "Poster generation toolkit. Use when producing print-ready posters from a content plan. Two routes: (A) commercial posters via HTML/CSS + Playwright rendering with precise Chinese typography; (B) academic conference posters via the posterly LaTeX-to-PDF skill. Includes local environment paths, commands, reusable templates and hard-won gotchas."
---

# 海报生成工具箱

把海报内容方案落地为印刷级成品。根据海报类型选择两条路径之一：

- **路径 A｜商业海报**（促销 / 活动 / 品牌 / 门店物料）—— 绝大多数中小企业需求走这条。
- **路径 B｜学术海报**（论文会议 Poster，LaTeX 源码）—— 仅当用户明确提供论文/LaTeX 且要开会展示时走这条。

## 决策树

```
用户要海报成品？
├─ 学术会议 / 论文 / LaTeX 源码 → 路径 B（posterly）
└─ 商业宣传 / 促销 / 活动 / 品牌 → 路径 A（HTML + Playwright）
   └─ 只要内容方案、不要成品 → 不调用本技能，直接输出方案
```

## 路径 A：商业海报（HTML/CSS + Playwright）

适合中文排版精确可控、配色字距可调、要快速出成品的场景。

### A1. 确定尺寸

先定尺寸再排版。常用规格：

| 用途 | 尺寸 | 画布（@96dpi 换算） |
|---|---|---|
| A4 竖版 | 210×297mm | 794×1123 px |
| A3 竖版 | 297×420mm | 1123×1587 px |
| A2 竖版 | 420×594mm | 1587×2245 px |
| 易拉宝 | 800×1800mm | —（按比例） |
| 朋友圈竖图 | 1080×1920 px | 1:1 像素 |

A2 竖版是线下海报常用规格，画布很高，内容量要足够撑满，否则底部大片留白。

### A2. 构建 HTML

以 `templates/build_skeleton.html` 为骨架，改配色、替换占位文案；主视觉图片用 `templates/build.py` 转 base64 注入 `{{IMAGE_DATA}}` 占位符：

```bash
python templates/build.py --image 主视觉.png --template templates/build_skeleton.html --out poster.html
```

核心要点：

1. **画布**：`.poster { width:420mm; height:594mm; display:flex; flex-direction:column; overflow:hidden; }`，用 mm 单位，与印刷尺寸一一对应。
2. **主色变量**：在 `:root` 定义品牌主色/辅助色/墨色/纸色，全篇引用变量，方便换配色。
3. **分区**：顶部品牌条 → 主标题区 → 主视觉 → 数据条 → 卖点区 → 补充区 → 页脚，用 flex 纵向排列，页脚用 `margin-top:auto` 贴底。
4. **主视觉内嵌**：用 `build.py` 把图片转 base64 写入 `<img src="{{IMAGE_DATA}}">`（相对路径 + file:// 常失败，必须内嵌）。
5. **水印遮盖**：AI 生成图右下角常有水印，在图片区右下角叠一个 `.wm-cover` 渐变色块遮盖。
6. **撑满版面**：骨架的 `.visual` 用 `flex:1 1 150mm` 弹性吸收剩余高度，避免 A2 等高画布底部留白；内容过多时收缩到 `min-height:120mm`。若仍留白，增加真实卖点/场景区块，不要靠拉大间距。

配色参考 `references/design-playbook.md`。

### A3. 渲染

用 `templates/render.py`：Playwright 启动 Chromium，viewport 设为目标尺寸像素，`emulate_media(media="print")`，`page.pdf()` 输出 PDF（width/height 设为目标 mm，margin 全 0，`print_background=True`），`locator(".poster").screenshot()` 输出 PNG 预览。

成品 PDF 用 `pdfinfo.exe` 校验页数与尺寸（见「本地环境」）。

### A4. 视觉自检

渲染后必须用看图工具检查：主视觉是否正常显示、水印是否遮住、文字有无重叠溢出、底部是否留白、整体是否专业。发现问题改 HTML 重渲染。

## 路径 B：学术海报（posterly）

仓库 `Chenruishuo/posterly`，只用于 LaTeX 论文 → 学术会议海报。详见 `references/posterly-guide.md`。

标准流程：
```
cp templates/landscape_hero_neutral.html poster.html
→ 改 :root 设计令牌 → 替换 TODO → run_gates.py → 按 GATE_REPORT 迭代修排版 → render_preview.py 出 PDF → verify-final 校验
```

## 本地环境（Windows，已部署）

| 项目 | 值 |
|---|---|
| Python 解释器 | `D:/workbuddy/2026-11-22-21-40-48/.venv-posterly/Scripts/python.exe` |
| posterly 仓库 | `D:/workbuddy/2026-11-22-21-40-48/posterly` |
| 渲染依赖 | Playwright 1.65.2 + Chromium 159 |
| PDF 校验 | pypdf 打包的 `pdfinfo.exe`，在 venv 的 `Scripts/` 下 |
| pip 源 | 阿里云 `https://mirrors.aliyun.com/pypi/simple/`（官方/清华源本机不通） |

`verify-final` 需在 PowerShell 中先把 Scripts 目录加入 PATH：
```powershell
$env:PATH = "D:\workbuddy\2026-11-22-21-40-48\.venv-posterly\Scripts;" + $env:PATH
```

> 换机器/换工作区时，上面的绝对路径需相应调整；核心是要有 Playwright + Chromium，PDF 校验需 `pdfinfo`（真 poppler 或兼容 shim）。

## 关键坑（必读）

1. **零内联样式**（posterly）：模板 style 规则禁止任何 `style=` 属性，只能用 utility class（fs-N / mt-N）。商业海报模板无此限制。
2. **图片用 base64 内嵌**：相对路径在 file:// 下易失败，导致 PDF 里图片空白。
3. **改文字会改变排版**：文案长度变化会影响区块高度与对齐，改完必须重渲染 + 重校验。
4. **measure 硬闸门**（posterly）：spread < 5px、卡片间距 ∈ [12,50]px、到 footer 间距 ∈ [30,50]px。调父容器 `gap`、列 `padding-bottom`、卡片内容量可收敛。
5. **模型 effort 不超过 high**（posterly 官方建议）：过高反而使排版质量下降。
6. **许可**：posterly 为 AGPL-3.0，内部用无碍，对外分发衍生品须开源源码。

## 资源

- `templates/build_skeleton.html` —— 商业海报 HTML 骨架（分区布局，含 {{IMAGE_DATA}} 占位符）
- `templates/build.py` —— 图片转 base64 注入骨架，生成最终 poster.html
- `templates/render.py` —— Playwright 渲染脚本（PDF + PNG）
- `templates/landscape_hero_neutral.html` —— 学术海报模板（路径 B，posterly 配套）
- `references/design-playbook.md` —— 配色、字号层级、版式分区、尺寸对照
- `references/posterly-guide.md` —— 学术海报完整流程与闸门说明
