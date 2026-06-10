# -*- coding: utf-8 -*-
"""
01_make_image_catalog_one_chapter.py

功能：
1. 读取大语言模型生成的 image_need_XX.csv；
2. 生成或更新 image_catalog_XX.csv；
3. 如果 image_catalog_XX.csv 已经存在，则尽量保留人工修改过的 image_path、caption、license 等字段；
4. 默认给 need_image=yes 的页面填入统一占位图路径；
5. 后续用户只需修改 image_catalog_XX.csv，再重新运行插图脚本。

使用示例：
python scripts/01_make_image_catalog_one_chapter.py --need metadata/image_need_01.csv --catalog metadata/image_catalog_01.csv


(ai-bigdata-figs) E:\machine_learning\markdown\AI-BigData-Course-Add-Figs-0>python scripts/01_make_image_catalog_one_chapter.py  --need metadata/image_need_01.csv  --catalog metadata/image_catalog_01.csv
已生成或更新：metadata\image_catalog_01.csv
总行数：20
后续请人工修改 image_path、caption、license、enabled 等字段。
"""

import argparse
import csv
from pathlib import Path


CATALOG_FIELDS = [
    "md_file",
    "slide_id",
    "slide_title",
    "need_image",
    "image_type",
    "layout",
    "image_path",
    "alt",
    "caption",
    "width",
    "enabled",
    "source",
    "license",
    "notes",
]


def read_csv(path: Path) -> list[dict]:
    """读取 CSV 文件，返回字典列表。"""
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    """写入 CSV 文件，统一使用 UTF-8 with BOM，便于 Excel 正确识别中文。"""
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CATALOG_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--need", required=True, help="metadata/image_need_XX.csv")
    parser.add_argument("--catalog", required=True, help="metadata/image_catalog_XX.csv")
    parser.add_argument(
        "--placeholder",
        default="assets/placeholders/figure_placeholder.svg",
        help="默认占位图路径，按项目根目录相对路径填写",
    )
    args = parser.parse_args()

    need_path = Path(args.need)
    catalog_path = Path(args.catalog)

    need_rows = read_csv(need_path)
    old_catalog_rows = read_csv(catalog_path)

    # 用 slide_id 作为主键，保留旧 catalog 中的人工修改内容
    old_by_slide_id = {
        str(row.get("slide_id", "")).strip(): row
        for row in old_catalog_rows
        if str(row.get("slide_id", "")).strip()
    }

    new_rows: list[dict] = []

    for need in need_rows:
        slide_id = str(need.get("slide_id", "")).strip()
        old = old_by_slide_id.get(slide_id, {})

        need_image = str(need.get("need_image", "")).strip().lower()
        layout = str(need.get("layout", "")).strip() if need_image == "yes" else ""

        # 若旧 catalog 已有人为指定图片，则保留；否则使用占位图
        old_image_path = str(old.get("image_path", "")).strip()
        image_path = old_image_path if old_image_path else (
            args.placeholder if need_image == "yes" else ""
        )

        row = {
            "md_file": need.get("md_file", ""),
            "slide_id": slide_id,
            "slide_title": need.get("slide_title", ""),
            "need_image": need_image,
            "image_type": need.get("image_type", "") if need_image == "yes" else "",
            "layout": layout,
            "image_path": image_path,
            "alt": old.get("alt", "") or need.get("query_cn", "") or need.get("slide_title", ""),
            "caption": old.get("caption", ""),
            "width": old.get("width", "") or "720",
            "enabled": old.get("enabled", "") or ("yes" if need_image == "yes" else "no"),
            "source": old.get("source", ""),
            "license": old.get("license", ""),
            "notes": old.get("notes", ""),
        }

        new_rows.append(row)

    write_csv(catalog_path, new_rows)

    print(f"已生成或更新：{catalog_path}")
    print(f"总行数：{len(new_rows)}")
    print("后续请人工修改 image_path、caption、license、enabled 等字段。")


if __name__ == "__main__":
    main()