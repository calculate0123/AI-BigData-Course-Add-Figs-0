from __future__ import annotations

from pathlib import Path
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
import csv
import hashlib
import json
import re
import time

try:
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


ROOT = Path(r"E:\machine_learning\markdown\AI-BigData-Course-Add-Figs-0")
IMAGE_NEED_DIR = ROOT / "image_need"
DOWNLOAD_ROOT = ROOT / "assets" / "downloaded"
OUT_TAG = "text1_expanded"
MANIFEST_PATH = DOWNLOAD_ROOT / "image_download_manifest_text1_expanded.csv"
DUPLICATE_PATH = DOWNLOAD_ROOT / "duplicate_check_text1_expanded.csv"
SUMMARY_PATH = DOWNLOAD_ROOT / "_download_summary_text1_expanded.json"

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0 Safari/537.36"

FIELDS = [
    "chapter",
    "md_file",
    "slide_id",
    "slide_title",
    "need_image",
    "candidate_rank",
    "download_status",
    "local_path",
    "relative_path",
    "file_name",
    "file_ext",
    "file_size_bytes",
    "width_px",
    "height_px",
    "sha256",
    "source_page_url",
    "direct_image_url",
    "source_title",
    "source_author",
    "source_license",
    "attribution_text",
    "search_query_used",
    "image_role",
    "image_type",
    "caption_zh",
    "layout_hint",
    "duplicate_of",
    "quality_notes",
]

DUP_FIELDS = ["sha256", "first_relative_path", "reused_by", "source_page_url", "notes"]

CHAPTER_TERMS = {
    "ch01": "artificial intelligence big data materials science",
    "ch02": "python pandas data preprocessing materials dataset",
    "ch03": "Bayesian statistics probability inference",
    "ch04": "machine learning materials property prediction",
    "ch05": "deep learning microstructure recognition microscopy",
    "ch06": "large language model transformer prompt engineering",
    "ch07": "knowledge graph RAG vector database retrieval augmented generation",
    "ch08": "AI agent active learning Bayesian optimization loop",
    "ch09": "materials database high throughput materials discovery",
    "ch10": "trustworthy AI data security privacy explainable AI",
}

ROLE_TERMS = {
    "概念示意": "concept illustration diagram",
    "算法流程": "algorithm workflow diagram",
    "数据流程": "data pipeline workflow",
    "实验结果": "experimental result figure",
    "模拟结果": "simulation result figure",
    "软件界面": "software interface screenshot",
    "材料组织": "materials microstructure microscopy",
    "安全合规案例": "data security privacy compliance diagram",
}


def read_rows() -> list[dict[str, str]]:
    rows = []
    for path in sorted(IMAGE_NEED_DIR.glob("image_need_ch*_text1.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows.extend([row for row in csv.DictReader(handle) if row.get("need_image") == "yes"])
    return rows


def ascii_words(text: str) -> str:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+-]{2,}", text or "")
    stop = {"diagram", "image", "workflow", "concept", "open", "educational", "resource", "materials", "science"}
    kept = []
    for word in words:
        lw = word.lower()
        if lw not in stop and lw not in [x.lower() for x in kept]:
            kept.append(word)
    return " ".join(kept[:10])


def short_title(row: dict[str, str]) -> str:
    title = row.get("slide_title", "")
    title = re.sub(r"第\d+章", "", title)
    title = re.sub(r"[^\w\u4e00-\u9fff ]+", " ", title)
    title = re.sub(r"\s+", " ", title).strip()
    return title[:60]


def query_variants(row: dict[str, str]) -> list[str]:
    title = short_title(row)
    chapter = CHAPTER_TERMS.get(row["chapter"], "")
    role = ROLE_TERMS.get(row.get("image_role", ""), row.get("image_role", ""))
    image_type = row.get("image_type", "")
    en = row.get("search_query_en", "")
    zh = row.get("search_query_zh", "")
    en_kw = ascii_words(row.get("concept_keywords_en", ""))
    title_kw = ascii_words(title)
    variants = [
        f"{en} {title}",
        f"{title_kw} {chapter} {role}",
        f"{en_kw} {chapter} {image_type} diagram",
        f"{chapter} {title} infographic",
        f"{chapter} {role} {title} education",
        f"{zh} {title}",
        f"{title} {role}",
        f"{en_kw} scientific visualization",
        f"{chapter} schematic illustration",
        f"{title_kw} technical diagram",
        f"{row['chapter']} slide {int(row['slide_id']):03d} {chapter} {title_kw}",
        f"{en} {row['chapter']} {int(row['slide_id']):03d}",
    ]
    cleaned = []
    for item in variants:
        item = re.sub(r"\b(AI generated|Midjourney|Stable Diffusion|DALL-E)\b", "", item, flags=re.I)
        item = re.sub(r"\s+", " ", item).strip()
        if item and item not in cleaned:
            cleaned.append(item)
    return cleaned[:12]


def bing_thumb_url(query: str, variant_index: int) -> str:
    widths = [1600, 1400, 1200, 1000]
    heights = [900, 900, 800, 700]
    w = widths[variant_index % len(widths)]
    h = heights[variant_index % len(heights)]
    # The thumbnail service returns one image per query; varying text is the useful diversity lever.
    return "https://tse1.mm.bing.net/th?q=" + quote_plus(query) + f"&w={w}&h={h}&c=7&rs=1&p=0"


def download(url: str) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Referer": "https://www.bing.com/images/search"})
    with urlopen(req, timeout=30) as response:
        return response.read()


def ext_from_bytes(data: bytes) -> str:
    head = data[:32].lower()
    if head.startswith(b"\x89png"):
        return ".png"
    if head.startswith(b"\xff\xd8"):
        return ".jpg"
    if head.startswith(b"riff") and b"webp" in head:
        return ".webp"
    if head.startswith(b"gif"):
        return ".gif"
    if b"<svg" in data[:500].lower():
        return ".svg"
    return ".jpg"


def dimensions(path: Path, ext: str) -> tuple[int, int, str]:
    if ext == ".svg":
        return 0, 0, "svg not raster-verified"
    if Image is None:
        return 0, 0, "Pillow unavailable"
    try:
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            return int(img.width), int(img.height), "opened successfully"
    except Exception as exc:
        return 0, 0, f"image open failed: {exc}"


def slugify(text: str, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text.lower())
    text = re.sub(r"-+", "-", text).strip("-")
    return (text or fallback)[:44].strip("-") or fallback


def make_row(row: dict[str, str], status: str, **kwargs) -> dict[str, str]:
    output = {field: "" for field in FIELDS}
    output.update(
        {
            "chapter": row["chapter"],
            "md_file": row["md_file"],
            "slide_id": row["slide_id"],
            "slide_title": row["slide_title"],
            "need_image": row["need_image"],
            "candidate_rank": "1",
            "download_status": status,
            "source_author": "unknown",
            "source_license": "unknown; copyright risk not checked",
            "attribution_text": "Bing thumbnail fallback; 来源和版权未核验，需人工复核后再用于正式课件。",
            "image_role": row.get("image_role", ""),
            "image_type": row.get("image_type", ""),
            "caption_zh": row.get("suggested_caption_zh", ""),
            "layout_hint": row.get("layout_hint", ""),
        }
    )
    for key, value in kwargs.items():
        output[key] = "" if value is None else str(value)
    return output


def process_one(row: dict[str, str], seen_sha: dict[str, str]) -> dict[str, str]:
    chapter = row["chapter"]
    slide_id = int(row["slide_id"])
    out_dir = DOWNLOAD_ROOT / chapter / OUT_TAG
    out_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(out_dir.glob(f"{chapter}_s{slide_id:03d}_r1_*"))
    if existing:
        path = existing[0]
        data = path.read_bytes()
        sha = hashlib.sha256(data).hexdigest()
        rel = path.relative_to(ROOT).as_posix()
        seen_sha.setdefault(sha, rel)
        width, height, note = dimensions(path, path.suffix.lower())
        query = query_variants(row)[0]
        return make_row(
            row,
            "downloaded",
            local_path=str(path),
            relative_path=rel,
            file_name=path.name,
            file_ext=path.suffix.lower(),
            file_size_bytes=path.stat().st_size,
            width_px=width,
            height_px=height,
            sha256=sha,
            source_page_url="https://www.bing.com/images/search?q=" + quote_plus(query),
            direct_image_url=bing_thumb_url(query, 1),
            source_title=query,
            search_query_used=query,
            quality_notes=f"expanded loose mode; resumed existing file; {note}",
        )
    duplicate_candidate = None
    tried = []
    variants = query_variants(row)
    for index, query in enumerate(variants, 1):
        tried.append(query)
        url = bing_thumb_url(query, index)
        try:
            data = download(url)
        except Exception:
            continue
        if len(data) < 1024:
            continue
        sha = hashlib.sha256(data).hexdigest()
        if sha in seen_sha:
            duplicate_candidate = (sha, seen_sha[sha], query, url)
            continue
        ext = ext_from_bytes(data)
        key = slugify(ascii_words(query) or row.get("image_type", ""), f"slide-{slide_id:03d}")
        file_name = f"{chapter}_s{slide_id:03d}_r1_{key}{ext}"
        path = out_dir / file_name
        path.write_bytes(data)
        width, height, note = dimensions(path, ext)
        rel = path.relative_to(ROOT).as_posix()
        seen_sha[sha] = rel
        qnotes = ["expanded loose mode; source and copyright not verified", note]
        if width and width < 600:
            qnotes.append("low resolution")
        return make_row(
            row,
            "downloaded",
            candidate_rank=index,
            local_path=str(path),
            relative_path=rel,
            file_name=file_name,
            file_ext=ext,
            file_size_bytes=path.stat().st_size,
            width_px=width,
            height_px=height,
            sha256=sha,
            source_page_url="https://www.bing.com/images/search?q=" + quote_plus(query),
            direct_image_url=url,
            source_title=query,
            search_query_used=query,
            quality_notes="; ".join([x for x in qnotes if x]),
        )
        time.sleep(0.05)

    if duplicate_candidate:
        sha, rel, query, url = duplicate_candidate
        return make_row(
            row,
            "reused_duplicate",
            local_path=str(ROOT / rel),
            relative_path=rel,
            file_name=Path(rel).name,
            file_ext=Path(rel).suffix,
            sha256=sha,
            source_page_url="https://www.bing.com/images/search?q=" + quote_plus(query),
            direct_image_url=url,
            source_title=query,
            search_query_used=query,
            duplicate_of=rel,
            quality_notes="expanded loose mode; duplicate reused after 12 query variants",
        )
    return make_row(row, "not_found", search_query_used=" | ".join(tried), quality_notes="no downloadable thumbnail after 12 query variants")


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def summarize(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    result: dict[str, dict[str, int]] = {}
    for row in rows:
        chapter = row["chapter"]
        result.setdefault(chapter, {"downloaded": 0, "reused_duplicate": 0, "not_found": 0, "failed": 0, "skipped_existing_image": 0, "total": 0})
        result[chapter]["total"] += 1
        result[chapter][row["download_status"]] = result[chapter].get(row["download_status"], 0) + 1
    return result


def main() -> None:
    rows = read_rows()
    manifest = []
    seen_sha: dict[str, str] = {}
    for idx, row in enumerate(rows, 1):
        try:
            manifest.append(process_one(row, seen_sha))
        except Exception as exc:
            manifest.append(make_row(row, "failed", quality_notes=f"unexpected failure: {exc}"))
        if idx % 25 == 0:
            print(f"processed {idx}/{len(rows)}", flush=True)

    write_csv(MANIFEST_PATH, manifest, FIELDS)
    for chapter in [f"ch{i:02d}" for i in range(1, 11)]:
        write_csv(DOWNLOAD_ROOT / chapter / OUT_TAG / f"manifest_{chapter}_{OUT_TAG}.csv", [row for row in manifest if row["chapter"] == chapter], FIELDS)

    dup: dict[str, dict[str, str]] = {}
    for row in manifest:
        if row["download_status"] == "reused_duplicate" and row["sha256"]:
            rec = dup.setdefault(row["sha256"], {"sha256": row["sha256"], "first_relative_path": row["duplicate_of"], "reused_by": "", "source_page_url": row["source_page_url"], "notes": "expanded loose duplicate"})
            rec["reused_by"] = (rec["reused_by"] + ";" if rec["reused_by"] else "") + f"{row['chapter']}:s{int(row['slide_id']):03d}"
    write_csv(DUPLICATE_PATH, list(dup.values()), DUP_FIELDS)
    summary = summarize(manifest)
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
