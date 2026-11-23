# -*- coding: utf-8 -*-
"""商业海报 HTML 构建脚本：把主视觉图片转 base64 注入 HTML 骨架。

作用：读取一个含 {{IMAGE_DATA}} 占位符的 HTML 骨架，把主视觉图片转为
data URI 内嵌进去，输出最终 poster.html。base64 内嵌可确保 Playwright
渲染的 PDF 中图片一定被嵌入（相对路径在 file:// 下常失败）。

用法：
  python build.py --image 主视觉.png --template build_skeleton.html --out poster.html

参数：
  --image      主视觉图片路径（png/jpg/webp）
  --template   HTML 骨架，默认同目录 build_skeleton.html
  --out        输出 HTML 路径，默认 ./poster.html

也可在 Python 中调用：
  from build import build_html
  build_html(image="图.png", out="poster.html")
"""
import argparse
import base64
import mimetypes
from pathlib import Path

HERE = Path(__file__).parent
PLACEHOLDER = "{{IMAGE_DATA}}"


def img_to_data_uri(image_path: str) -> str:
    """把图片文件转为 data URI。"""
    p = Path(image_path)
    if not p.exists():
        raise FileNotFoundError(f"找不到图片：{image_path}")
    mime, _ = mimetypes.guess_type(p.name)
    if not mime or not mime.startswith("image/"):
        mime = "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_html(image: str, template: str = None, out: str = "poster.html") -> Path:
    """构建最终海报 HTML，返回输出路径。"""
    tpl_path = Path(template) if template else HERE / "build_skeleton.html"
    if not tpl_path.exists():
        raise FileNotFoundError(f"找不到 HTML 骨架：{tpl_path}")

    html = tpl_path.read_text(encoding="utf-8")
    if PLACEHOLDER not in html:
        raise ValueError(f"HTML 骨架中缺少占位符 {PLACEHOLDER}，请检查模板")

    data_uri = img_to_data_uri(image)
    html = html.replace(PLACEHOLDER, data_uri)

    out_path = Path(out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")
    print(f"OK: {out_path}  ({out_path.stat().st_size/1024:.1f} KB, image embedded)")
    return out_path


def main():
    ap = argparse.ArgumentParser(description="构建含内嵌主视觉的海报 HTML")
    ap.add_argument("--image", required=True, help="主视觉图片路径")
    ap.add_argument("--template", default=None, help="HTML 骨架路径（默认 build_skeleton.html）")
    ap.add_argument("--out", default="poster.html", help="输出 HTML 路径")
    args = ap.parse_args()
    build_html(args.image, args.template, args.out)


if __name__ == "__main__":
    main()
