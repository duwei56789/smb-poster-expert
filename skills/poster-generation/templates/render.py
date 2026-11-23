# -*- coding: utf-8 -*-
"""通用商业海报渲染脚本：HTML -> 印刷级 PDF + PNG 预览。

用法：
  1. 先准备好 poster.html（画布尺寸用 mm，见 design-playbook.md）
  2. 修改下方 SIZE_MM / NAME，或直接命令行传参
  3. python render.py [poster.html] [输出名] [宽mm] [高mm]

依赖：playwright + chromium（pip install playwright && playwright install chromium）。
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
HTML = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "poster.html"
NAME = sys.argv[2] if len(sys.argv) > 2 else "poster"
W_MM = float(sys.argv[3]) if len(sys.argv) > 3 else 420.0   # 默认 A2 宽
H_MM = float(sys.argv[4]) if len(sys.argv) > 4 else 594.0   # 默认 A2 高

PDF = HTML.parent / f"{NAME}.pdf"
PNG = HTML.parent / f"{NAME}.png"

PX_PER_MM = 96 / 25.4
W = round(W_MM * PX_PER_MM)
H = round(H_MM * PX_PER_MM)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=2)
    page.goto(HTML.resolve().as_uri(), wait_until="networkidle")
    page.emulate_media(media="print")
    page.pdf(
        path=str(PDF),
        width=f"{W_MM}mm", height=f"{H_MM}mm",
        print_background=True,
        margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        prefer_css_page_size=False,
    )
    # 优先截 .poster 元素；没有则整页截图
    loc = page.locator(".poster")
    if loc.count():
        loc.screenshot(path=str(PNG))
    else:
        page.screenshot(path=str(PNG), full_page=True)
    browser.close()

print(f"PDF -> {PDF}  ({PDF.stat().st_size/1024:.1f} KB)")
print(f"PNG -> {PNG}  ({PNG.stat().st_size/1024:.1f} KB)")
print(f"Size -> {W_MM}x{H_MM}mm  ({W}x{H}px @96dpi)")
