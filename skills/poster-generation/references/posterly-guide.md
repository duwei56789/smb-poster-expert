# posterly 学术海报完整指南

仓库：`Chenruishuo/posterly`（AGPL-3.0）。用途：LaTeX 论文源码 → 印刷级学术会议海报（ICML / NeurIPS / ICLR / CVPR 或自定义尺寸）。**仅用于学术论文场景**，商业海报请走路径 A。

## 一、环境（Windows 已部署）

| 项目 | 值 |
|---|---|
| Python | `D:/workbuddy/2026-11-22-21-40-48/.venv-posterly/Scripts/python.exe`（3.13.14） |
| 仓库 | `D:/workbuddy/2026-11-22-21-40-48/posterly` |
| 依赖 | playwright 1.65.2 + Chromium 159 + pytest 9.2.0 + pypdf 7.1.1 |
| pdfinfo | venv `Scripts/pdfinfo.exe`（pypdf + PyInstaller 打包的兼容 shim，因本机无 poppler） |
| pip 源 | 阿里云源（官方/清华源本机不通） |

换环境时：确保 Python 3.10+，`pip install playwright pytest pypdf`，`playwright install chromium`，并准备可用的 `pdfinfo`（真 poppler 或 shim）。

## 二、五步标准流程

设 `PY = D:/workbuddy/2026-11-22-21-40-48/.venv-posterly/Scripts/python.exe`，工作目录进到海报 html 所在文件夹。

**1. 起模板**
```bash
cp templates/landscape_hero_neutral.html poster.html
```

**2. 改设计令牌 + 填内容**
改 `:root` 设计令牌；把所有 `TODO` 占位替换为真实内容。用脚本批量替换更高效，注意相同占位符 str.replace 会全部替换成同一值——需逐行按索引填不同内容。

**3. 跑校验闸门**
```bash
& $PY ../tools/run_gates.py poster.html --hero
```
结果写入 `GATE_REPORT.json`。硬闸门全 PASS 才算完成。`--hero` 用于 hero 模板；学术栏位海报去掉该参数。

**4. 按报告迭代修排版**
读取 `GATE_REPORT.json` 的 `gates[].summary.tail` 看具体问题。常见修复：
- **style**：禁止任何 `style=` 内联属性，改用 utility class（fs-N / mt-N）。
- **measure spread**：`.column` 的 `padding-bottom` 造成底部错位，调小到 0。
- **卡片间距过大**：增加卡片真实内容量；`justify-content:space-between` 会拉开空隙。
- **到 footer 间距 <30px**：调父 `.poster` 的 `gap`（6u→9u）。
- 改文案会改变区块高度与对齐，每次改完必须重跑闸门。

**5. 渲染 + 校验**
```bash
& $PY ../tools/render_preview.py poster.html
# PowerShell 中先加 PATH 再校验
$env:PATH = "D:\workbuddy\2026-11-22-21-40-48\.venv-posterly\Scripts;" + $env:PATH
& $PY ../tools/poster_check.py verify-final poster_preview.pdf --from-html poster.html
```

## 三、闸门说明

| 闸门 | 检查内容 |
|---|---|
| preflight | 结构、占位符残留、必需区块 |
| style | 零内联样式、设计令牌合规 |
| asset | 图片/图表引用有效 |
| measure | 对齐与间距硬阈值：spread < 5px、卡片间距 ∈[12,50]px、到 footer 间距 ∈[30,50]px |
| polish | 视觉细节警告（非硬失败） |

`run_gates.py` 累积运行全部闸门；`GATE_REPORT.json` 的 `overall` 为 PASS 才算通过。

## 四、已验证结果（2026-11-22）

- 官方 smoke test 全流程 PASS
- pytest 套件：476 passed, 2 skipped
- 真实中文技术海报：60×36in 画布，全闸门 PASS，1 页 4320×2592pt PDF，verify-final PASS

## 五、限制

- 只吃 LaTeX 源码，直接输入 PDF 未经测试。
- 依赖 Chromium + poppler/pdfinfo，环境配置有成本。
- 官方建议模型 effort 不超过 high。
- AGPL-3.0：对外分发衍生品须开源全部源码，商用集成需评估。
