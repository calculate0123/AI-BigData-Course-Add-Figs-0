# -*- coding: utf-8 -*-
"""
01_insert_images_one_chapter_optimized.py

功能：
1. 读取原始 Marp Markdown；
2. 读取 image_catalog_XX.csv；
3. 按 slide_id 将图片插入对应幻灯片；
4. 不修改原始 Markdown，而是输出到 output/；
5. 插入内容带有 FIG_START / FIG_END 标记，脚本可重复运行；
6. 重新写出 Markdown 时，使每个“幻灯片分页符 ---”前后各空一行；
7. 保留 YAML front matter 的第一个 --- 位于文件首行，避免破坏 Marp 对 front matter 的识别。

推荐运行方式：
python scripts/01_insert_images_one_chapter_optimized.py ^
  --md slides/第1章_人工智能大数据与材料科学概论_100页_Marp.md ^
  --catalog metadata/image_catalog_01.csv ^
  --out output/第1章_人工智能大数据与材料科学概论_100页_Marp_with_figs.md

说明：
- 默认从当前工作目录推断 project_root。因此请在项目根目录运行本脚本。
- 若需要显式指定项目根目录，可增加：--project-root E:/machine_learning/markdown/AI-BigData-Course-Add-Figs-0
"""

from __future__ import annotations

import argparse
import csv
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple


# 旧插图块识别：用于重复运行时先删除旧块，再写入新块。
FIG_BLOCK_RE = re.compile(
    r"\n?<!--\s*FIG_START:\s*slide_id=\d+\s*-->.*?<!--\s*FIG_END:\s*slide_id=\d+\s*-->\n?",
    re.DOTALL,
)

# 单独一行的 Marp/Markdown 分隔符。
HR_RE = re.compile(r"^\s*---\s*$")

# Markdown fenced code 起止行。
FENCE_RE = re.compile(r"^\s*(```|~~~)")


TRUE_VALUES = {"yes", "y", "true", "1", "on"}
FALSE_VALUES = {"no", "n", "false", "0", "off", ""}


def normalize_bool(value: object, default: bool = False) -> bool:
    """将 CSV 中的 yes/no、true/false、1/0 等值统一转为布尔值。"""
    s = str(value if value is not None else "").strip().lower()
    if s in TRUE_VALUES:
        return True
    if s in FALSE_VALUES:
        return False
    return default


def read_catalog(path: Path) -> Dict[int, dict]:
    """
    读取 image_catalog_XX.csv。

    返回：
        {slide_id: row}
    """
    if not path.exists():
        raise FileNotFoundError(f"找不到 image catalog 文件：{path}")

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    catalog: Dict[int, dict] = {}
    for row in rows:
        try:
            slide_id = int(str(row.get("slide_id", "")).strip())
        except ValueError:
            continue
        catalog[slide_id] = row

    return catalog


def split_frontmatter(text: str) -> Tuple[str, str]:
    """
    将 Markdown 拆分为 YAML front matter 与正文。

    Marp 文件通常以第一行 --- 开始，并以第二个 --- 结束 YAML front matter。
    注意：第一个 --- 必须保留在文件首行，不应在它前面人为增加空行。
    """
    # 统一换行符，避免 Windows/Unix 换行混用导致判断不稳定。
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.splitlines(keepends=True)

    if not lines or lines[0].strip() != "---":
        return "", text

    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter = "".join(lines[: i + 1]).strip("\n")
            body = "".join(lines[i + 1 :]).strip("\n")
            return frontmatter, body

    return "", text.strip("\n")


def split_slides(body: str) -> List[str]:
    """
    按单独一行的 --- 拆分幻灯片正文。

    保护规则：
    - 代码块中的 --- 不作为分页符；
    - YAML front matter 已在 split_frontmatter() 中剥离，不参与本函数处理。
    """
    if not body.strip():
        return []

    lines = body.splitlines(keepends=True)
    slides: List[str] = []
    current: List[str] = []
    in_code_fence = False

    for line in lines:
        stripped = line.strip()

        if FENCE_RE.match(stripped):
            in_code_fence = not in_code_fence
            current.append(line)
            continue

        if (not in_code_fence) and HR_RE.match(stripped):
            slides.append("".join(current).strip("\n"))
            current = []
        else:
            current.append(line)

    slides.append("".join(current).strip("\n"))

    # 避免极端情况下产生纯空白幻灯片。
    return [s for s in slides if s.strip()]


def make_markdown_image_path(project_root: Path, output_md: Path, image_path: str) -> str:
    """
    将 catalog 中的图片路径转换为相对于输出 Markdown 文件的路径。

    支持：
    1. 项目根目录相对路径：assets/downloaded/ch01/a.png；
    2. 绝对路径：E:/xxx/a.png；
    3. Windows 反斜杠路径。
    """
    raw = str(image_path).strip().replace("\\", "/")
    if not raw:
        return ""

    raw_path = Path(raw)
    if raw_path.is_absolute():
        abs_img = raw_path.resolve()
    else:
        abs_img = (project_root / raw).resolve()

    abs_out_dir = output_md.resolve().parent
    return os.path.relpath(abs_img, abs_out_dir).replace("\\", "/")


def clean_alt_text(text: str) -> str:
    """
    清理 Markdown 图片 alt 文本，避免换行、方括号等字符破坏图片语法。
    """
    s = str(text or "").strip()
    s = re.sub(r"[\r\n]+", " ", s)
    s = s.replace("[", "").replace("]", "")
    return s


def get_width(row: dict, default: str = "720") -> str:
    """
    读取图片宽度。

    对 center 布局：width 建议为 560、640、720 等数值。
    对 right 布局：若 width 写成 36% 这类百分比，则可作为右侧区域比例。
    """
    width = str(row.get("width", "")).strip()
    return width if width else default


def build_image_block(slide_id: int, row: dict, project_root: Path, output_md: Path) -> str:
    """
    根据 image_catalog 中的 layout 字段构造插图 Markdown。

    支持三种布局：
    - right  ：右图左文，使用 Marp 背景分栏语法；
    - center ：居中大图，兼容 am_template.scss 中常见的 #c 居中约定；
    - bg     ：淡背景图，适合章节过渡页或概念引入页。
    """
    layout = str(row.get("layout", "")).strip().lower()
    image_path = str(row.get("image_path", "")).strip()
    slide_title = str(row.get("slide_title", "")).strip()
    alt = clean_alt_text(row.get("alt", "") or slide_title or f"slide {slide_id} figure")
    caption = str(row.get("caption", "")).strip()
    width = get_width(row)

    if not image_path:
        return ""

    rel_img = make_markdown_image_path(project_root, output_md, image_path)

    if layout == "right":
        # 对右图左文，优先使用 right_width 字段；若没有，则根据 width 是否为百分比判断。
        right_width = str(row.get("right_width", "")).strip()
        if not right_width:
            right_width = width if width.endswith("%") else "36%"
        image_md = f"![bg right:{right_width} contain]({rel_img})"

    elif layout == "bg":
        opacity = str(row.get("opacity", "")).strip() or ".15"
        image_md = f"![bg opacity:{opacity}]({rel_img})"

    else:
        # #c 可配合 AwesomeMarp / am_template 中常见的居中图片规则；
        # w:720 是 Marp/Marpit 的扩展图片尺寸写法。
        image_md = f"![#c autofig center w:{width} {alt}]({rel_img})"

    lines = [
        f"<!-- FIG_START: slide_id={slide_id:03d} -->",
        image_md,
    ]

    # 仅居中图默认加 caption；右侧背景图和背景图不加，避免遮挡正文。
    if caption and layout not in {"right", "bg"}:
        lines.append(f'<div class="fig-caption">{caption}</div>')

    lines.append(f"<!-- FIG_END: slide_id={slide_id:03d} -->")

    # 图块自身前后不强行塞多余空行；由插入函数统一控制。
    return "\n".join(lines)


def find_insert_position(slide: str) -> int:
    """
    寻找图片插入位置。

    插入原则：
    1. 跳过页面开头的 HTML 注释指令，例如 <!-- _class: ... -->；
    2. 优先插入到第一个一级或二级标题之后；
    3. 如果没有标题，则插入到页面开头指令之后。
    """
    lines = slide.splitlines(keepends=True)

    start = 0
    while start < len(lines):
        s = lines[start].strip()
        if s == "" or s.startswith("<!--"):
            start += 1
        else:
            break

    for i in range(start, len(lines)):
        if re.match(r"^\s{0,3}#{1,2}\s+", lines[i]):
            return sum(len(x) for x in lines[: i + 1])

    return sum(len(x) for x in lines[:start])


def insert_image_into_slide(slide: str, slide_id: int, row: dict, project_root: Path, output_md: Path) -> Tuple[str, bool]:
    """
    对单页幻灯片执行插图。

    返回：
        (new_slide, inserted_or_updated)
    """
    slide_without_old_block = FIG_BLOCK_RE.sub("\n", slide).strip("\n")

    need_image = normalize_bool(row.get("need_image", ""), default=False)
    enabled = normalize_bool(row.get("enabled", ""), default=need_image)

    if not need_image or not enabled:
        return slide_without_old_block, False

    block = build_image_block(slide_id, row, project_root, output_md)
    if not block:
        return slide_without_old_block, False

    pos = find_insert_position(slide_without_old_block)
    new_slide = (
        slide_without_old_block[:pos].rstrip("\n")
        + "\n\n"
        + block
        + "\n\n"
        + slide_without_old_block[pos:].lstrip("\n")
    ).strip("\n")

    return new_slide, True


def join_frontmatter_and_slides(frontmatter: str, slides: List[str]) -> str:
    """
    重新组合 Markdown。

    核心要求：
    - 每个“幻灯片分页符 ---”前后各空一行；
    - YAML front matter 的第一个 --- 必须仍在文件首行；
    - front matter 结束后空一行再进入第一页。

    输出形态：
        ---
        yaml...
        ---

        slide 1

        ---

        slide 2
    """
    clean_slides = [s.strip("\n") for s in slides if s.strip()]
    body = "\n\n---\n\n".join(clean_slides)

    if frontmatter.strip():
        return frontmatter.strip("\n") + "\n\n" + body + "\n"

    return body + "\n"


def count_slide_separators_with_spacing(text: str) -> Tuple[int, int]:
    """
    统计正文分页符数量，并检查其前后是否各有空行。

    说明：
    - 不检查文件首行的 YAML front matter 起始符；
    - 对 front matter 结束符只要求其后有空行，不强制其前有空行；
    - 对正文中的分页符要求前后各空一行。
    """
    lines = text.splitlines()
    separator_indices = [i for i, line in enumerate(lines) if line.strip() == "---"]

    if len(separator_indices) <= 2:
        return 0, 0

    body_separator_indices = separator_indices[2:]
    ok_count = 0

    for i in body_separator_indices:
        prev_blank = i > 0 and lines[i - 1].strip() == ""
        next_blank = i + 1 < len(lines) and lines[i + 1].strip() == ""
        if prev_blank and next_blank:
            ok_count += 1

    return len(body_separator_indices), ok_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="按 image_catalog_XX.csv 自动向 Marp Markdown 插入图片。")
    parser.add_argument("--md", required=True, help="原始 Marp Markdown 文件")
    parser.add_argument("--catalog", required=True, help="metadata/image_catalog_XX.csv")
    parser.add_argument("--out", required=True, help="输出 Markdown 文件")
    parser.add_argument(
        "--project-root",
        default=".",
        help="项目根目录。默认当前工作目录；建议在项目根目录运行脚本。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    project_root = Path(args.project_root).resolve()
    md_path = Path(args.md)
    catalog_path = Path(args.catalog)
    output_md = Path(args.out)

    if not md_path.exists():
        raise FileNotFoundError(f"找不到 Markdown 文件：{md_path}")
    if not catalog_path.exists():
        raise FileNotFoundError(f"找不到 image catalog 文件：{catalog_path}")

    text = md_path.read_text(encoding="utf-8")
    catalog = read_catalog(catalog_path)

    frontmatter, body = split_frontmatter(text)
    slides = split_slides(body)

    new_slides: List[str] = []
    inserted_count = 0

    for idx, slide in enumerate(slides, start=1):
        row = catalog.get(idx)

        if row is None:
            # catalog 中没有该页：仅删除旧 FIG_BLOCK，保持正文原样。
            new_slides.append(FIG_BLOCK_RE.sub("\n", slide).strip("\n"))
            continue

        new_slide, changed = insert_image_into_slide(slide, idx, row, project_root, output_md)
        new_slides.append(new_slide)
        if changed:
            inserted_count += 1

    new_text = join_frontmatter_and_slides(frontmatter, new_slides)

    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_md.write_text(new_text, encoding="utf-8")

    sep_total, sep_ok = count_slide_separators_with_spacing(new_text)

    print(f"原始文件：{md_path}")
    print(f"目录文件：{catalog_path}")
    print(f"输出文件：{output_md}")
    print(f"幻灯片页数：{len(slides)}")
    print(f"本次插入或更新图片页数：{inserted_count}")
    print(f"正文分页符检查：{sep_ok}/{sep_total} 个 --- 已满足前后各空一行")
    if sep_total != sep_ok:
        print("警告：仍有正文分页符未满足空行要求，请检查输出文件。")


if __name__ == "__main__":
    main()
