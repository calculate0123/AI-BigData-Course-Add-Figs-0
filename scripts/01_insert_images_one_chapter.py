# -*- coding: utf-8 -*-
"""
01_insert_images_one_chapter.py

功能：
1. 读取原始 Marp Markdown；
2. 读取 image_catalog_XX.csv；
3. 按 slide_id 将图片插入对应幻灯片；
4. 不修改原始 Markdown，而是输出到 output/；
5. 插入内容带有 FIG_START / FIG_END 标记，脚本可重复运行；
6. 如果用户修改 image_catalog_XX.csv，再次运行本脚本即可自动更新图片。

使用示例：
python scripts/01_insert_images_one_chapter.py ^
  --md slides/第1章_人工智能大数据与材料科学概论_100页_Marp.md ^
  --catalog metadata/image_catalog_01.csv ^
  --out output/第1章_人工智能大数据与材料科学概论_100页_Marp_with_figs.md

  
**似乎效果不好**

"""

import argparse
import csv
import re
from pathlib import Path


FIG_BLOCK_RE = re.compile(
    r"\n?<!-- FIG_START: slide_id=\d+ -->.*?<!-- FIG_END: slide_id=\d+ -->\n?",
    re.DOTALL,
)


def read_catalog(path: Path) -> dict[int, dict]:
    """
    读取 image_catalog_XX.csv。

    返回：
        {slide_id: row}
    """
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))

    catalog = {}
    for row in rows:
        try:
            slide_id = int(str(row.get("slide_id", "")).strip())
        except ValueError:
            continue
        catalog[slide_id] = row

    return catalog


def split_frontmatter(text: str) -> tuple[str, str]:
    """
    将 Markdown 拆分为：
    1. YAML front matter；
    2. 幻灯片正文。

    说明：
    Marp 文件通常以 --- 开始并以第二个 --- 结束 YAML front matter。
    """
    lines = text.splitlines(keepends=True)

    if not lines or lines[0].strip() != "---":
        return "", text

    # 找第二个 ---
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter = "".join(lines[: i + 1])
            body = "".join(lines[i + 1 :])
            return frontmatter, body

    return "", text


def split_slides(body: str) -> list[str]:
    """
    按 Marp 分页符 --- 拆分幻灯片正文。

    注意：
    这里仅识别单独一行的 ---。
    同时用简单 fenced code 检测，避免误拆代码块中的 ---。
    """
    lines = body.splitlines(keepends=True)

    slides = []
    current = []
    in_code_fence = False

    for line in lines:
        stripped = line.strip()

        # 检测 Markdown 代码块
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_fence = not in_code_fence
            current.append(line)
            continue

        # 只有不在代码块中，且一行只有 ---，才作为分页符
        if (not in_code_fence) and stripped == "---":
            slides.append("".join(current).strip("\n"))
            current = []
        else:
            current.append(line)

    slides.append("".join(current).strip("\n"))
    return slides


def to_project_relative_image_path(project_root: Path, output_md: Path, image_path: str) -> str:
    """
    将 catalog 中的项目根目录相对路径转换为相对于输出 Markdown 的路径。

    例如：
        catalog 中：assets/downloaded/ch01/a.png
        输出 md：output/ch01_with_figs.md
        Markdown 中应写：../assets/downloaded/ch01/a.png
    """
    raw = image_path.strip().replace("\\", "/")
    abs_img = (project_root / raw).resolve()
    abs_out_dir = output_md.resolve().parent
    rel = abs_img.relative_to(abs_out_dir) if abs_img.is_relative_to(abs_out_dir) else None

    # Python 3.9 以下没有 Path.is_relative_to；
    # 如果你的环境报错，请使用下面的 fallback 写法。
    return rel.as_posix()


def safe_relpath(project_root: Path, output_md: Path, image_path: str) -> str:
    """
    兼容不同 Python 版本的相对路径计算。
    """
    import os

    raw = image_path.strip().replace("\\", "/")
    abs_img = (project_root / raw).resolve()
    abs_out_dir = output_md.resolve().parent
    return os.path.relpath(abs_img, abs_out_dir).replace("\\", "/")


def build_image_block(slide_id: int, row: dict, project_root: Path, output_md: Path) -> str:
    """
    根据 image_catalog 中的 layout 字段构造插图 Markdown。

    支持三种布局：
    1. right  ：右图左文，使用 Marp 背景分栏语法；
    2. center ：居中大图，使用主题中的 img[alt~="center"] 样式；
    3. bg     ：淡背景图，适合章节过渡页。
    """
    layout = str(row.get("layout", "")).strip().lower()
    image_path = str(row.get("image_path", "")).strip()
    alt = str(row.get("alt", "")).strip() or str(row.get("slide_title", "")).strip()
    width = str(row.get("width", "")).strip() or "720"

    if not image_path:
        return ""

    rel_img = safe_relpath(project_root, output_md, image_path)

    if layout == "right":
        image_md = f"![bg right:38% contain]({rel_img})"

    elif layout == "bg":
        # opacity 用于降低背景干扰；如个别 Marp 环境不识别，可改为 ![bg]。
        image_md = f"![bg opacity:.15]({rel_img})"

    else:
        # center 或其他未知布局均按居中图处理
        image_md = f"![fig center w:{width}]({rel_img})"

    return (
        f"\n<!-- FIG_START: slide_id={slide_id:03d} -->\n"
        f"{image_md}\n"
        f"<!-- FIG_END: slide_id={slide_id:03d} -->\n"
    )


def find_insert_position(slide: str) -> int:
    """
    寻找图片插入位置。

    原则：
    1. 跳过页面开头的 HTML 注释指令，例如 <!-- _class: ... -->；
    2. 优先插入到第一个标题之后；
    3. 如果没有标题，则插入到页面开头。

    这样可以避免图片块插到 Marp 页面指令之前。
    """
    lines = slide.splitlines(keepends=True)

    # 跳过页面开头的 Marp 注释指令和空行
    start = 0
    while start < len(lines):
        s = lines[start].strip()
        if s == "" or s.startswith("<!--"):
            start += 1
        else:
            break

    # 找第一个一级或二级标题
    for i in range(start, len(lines)):
        if re.match(r"^\s{0,3}#{1,2}\s+", lines[i]):
            return sum(len(x) for x in lines[: i + 1])

    return sum(len(x) for x in lines[:start])


def insert_image_into_slide(slide: str, slide_id: int, row: dict, project_root: Path, output_md: Path) -> str:
    """
    对单页幻灯片执行插图。
    """
    # 先删除旧插图块，保证脚本可重复运行
    slide = FIG_BLOCK_RE.sub("\n", slide)

    need_image = str(row.get("need_image", "")).strip().lower()
    enabled = str(row.get("enabled", "")).strip().lower()

    if need_image != "yes" or enabled != "yes":
        return slide.strip("\n")

    block = build_image_block(slide_id, row, project_root, output_md)
    if not block:
        return slide.strip("\n")

    pos = find_insert_position(slide)
    new_slide = slide[:pos] + block + slide[pos:]

    return new_slide.strip("\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", required=True, help="原始 Marp Markdown 文件")
    parser.add_argument("--catalog", required=True, help="metadata/image_catalog_XX.csv")
    parser.add_argument("--out", required=True, help="输出 Markdown 文件")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    md_path = Path(args.md)
    catalog_path = Path(args.catalog)
    output_md = Path(args.out)

    text = md_path.read_text(encoding="utf-8")
    catalog = read_catalog(catalog_path)

    frontmatter, body = split_frontmatter(text)
    slides = split_slides(body)

    new_slides = []
    inserted_count = 0

    for idx, slide in enumerate(slides, start=1):
        row = catalog.get(idx)

        if row is None:
            # catalog 中没有该页，保持原样
            new_slides.append(FIG_BLOCK_RE.sub("\n", slide).strip("\n"))
            continue

        before = slide
        after = insert_image_into_slide(slide, idx, row, project_root, output_md)

        if after != FIG_BLOCK_RE.sub("\n", before).strip("\n"):
            inserted_count += 1

        new_slides.append(after)

    output_md.parent.mkdir(parents=True, exist_ok=True)

    new_text = frontmatter + "\n---\n".join(new_slides) + "\n"
    output_md.write_text(new_text, encoding="utf-8")

    print(f"原始文件：{md_path}")
    print(f"目录文件：{catalog_path}")
    print(f"输出文件：{output_md}")
    print(f"幻灯片页数：{len(slides)}")
    print(f"本次插入或更新图片页数：{inserted_count}")


if __name__ == "__main__":
    main()