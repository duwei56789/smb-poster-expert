# 中小企业的海报生成专家

根据中小企业提供的品牌信息、活动主题、目标受众、宣传重点和海报尺寸要求，生成结构清晰、可直接使用的海报内容方案，并可落地为印刷级海报成品。

## 类型

Agent 型（单个 AI 专家） · 分类：营销增长（05-MarketingGrowth）

## 功能

- **需求结构化**：一次性补全五项核心输入（品牌、主题、受众、宣传重点、尺寸），不反复打断。
- **内容方案生成**：主标题 / 副标题 / 卖点 / 数据锚点 / CTA 的完整文案体系，分层清晰。
- **版式与视觉建议**：分区布局、字号层级、配色、留白与主视觉素材建议。
- **方案落地渲染**：需要成品时，用 HTML/CSS + Playwright 渲染印刷级 PDF；学术论文走 posterly 流程。
- **合规把关**：提示素材版权、数据真实性、二维码占位等风险。

## 输入参数

| 参数 | 必需 | 说明 |
|---|---|---|
| 品牌信息 | 建议 | 品牌名、Slogan、行业、主色、资质 |
| 活动主题 | 必需 | 促销/开业/新品/品牌宣传等 |
| 目标受众 | 建议 | 人群画像、消费场景、地域 |
| 宣传重点 | 必需 | 3-6 个核心卖点/数字/优惠 |
| 海报尺寸 | 必需 | 如 A4/A3/A2、易拉宝、朋友圈竖图 |

## 输出内容

1. 方案概览（定位、主视觉方向、调性）
2. 文案层级（主标题 / 副标题 / 卖点 / 数据 / CTA）
3. 版式建议（分区、字号、配色、留白）
4. 素材清单（图片、二维码/Logo 待补项）
5. 落地成品（按需：印刷级 PDF + PNG 预览）
6. 风险提示（版权、数据真实性、二维码占位）

## 适用场景

促销海报、门店开业/周年庆、新品发布、品牌宣传、招商物料、朋友圈竖图、易拉宝、学术会议论文海报。

## 使用示例

- 我要为新产品做一张促销海报，帮我出一份内容方案
- 根据我的品牌信息和目标受众，设计一张门店活动海报
- 把这份海报方案渲染成 A2 印刷级 PDF

## 附带资源

- `skills/poster-generation/SKILL.md` —— 生成工具箱（商业海报路径 A / 学术海报路径 B）
- `skills/poster-generation/references/design-playbook.md` —— 配色、字号、版式、尺寸对照
- `skills/poster-generation/references/posterly-guide.md` —— 学术海报流程与闸门说明
- `skills/poster-generation/templates/build_skeleton.html` —— 商业海报 HTML 骨架
- `skills/poster-generation/templates/render.py` —— Playwright 渲染脚本

## 头像

头像位于 `avatars/expert.png`。如需替换：PNG/JPG，512×512 px，≤500KB。

## 安装与注册

将专家包放到专家目录后注册使其可见：

```
C:\Users\pc\.workbuddy\plugins\marketplaces\my-experts\plugins\smb-poster-expert\
```

```bash
python3 scripts/register_expert.py <expert-dir>
```

## 注意事项

- 数据/资质/Slogan 不编造，来自用户或公开信息，不确定处标注「需确认」。
- 商用物料建议用品牌官方素材，AI 生成图需遮盖水印。
- 渲染依赖本机 Playwright + Chromium + pdfinfo，详见技能文档。
- posterly 为 AGPL-3.0，对外分发衍生品须开源源码。
