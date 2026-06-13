from __future__ import annotations

from pathlib import Path
from urllib.parse import quote, urlencode, urlparse, urlunparse
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
MANIFEST_PATH = DOWNLOAD_ROOT / "image_download_manifest_text1.csv"
DUPLICATE_PATH = DOWNLOAD_ROOT / "duplicate_check_text1.csv"

COMMONS_API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "AI-BigData-Course-ImagePlanner/1.0 (educational material preparation)"

MANIFEST_FIELDS = [
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

ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg"}
BAD_TITLE_TERMS = [
    "logo",
    "icon",
    "portrait",
    "selfie",
    "flag",
    "map",
    "coat of arms",
    "seal",
    "stamp",
    "cover",
    "poster",
]
AI_TERMS = ["midjourney", "stable diffusion", "dall-e", "dalle", "ai-generated", "ai generated"]


def normalize_url(url: str) -> str:
    parsed = urlparse(url)
    filtered_query = []
    for part in parsed.query.split("&"):
        if not part:
            continue
        key = part.split("=", 1)[0].lower()
        if key.startswith("utm_") or key in {"fbclid", "gclid", "mc_cid", "mc_eid"}:
            continue
        filtered_query.append(part)
    return urlunparse(parsed._replace(query="&".join(filtered_query), fragment=""))


def slugify(text: str, fallback: str = "image") -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    if not text:
        text = fallback
    return text[:42].strip("-") or fallback


def make_queries(row: dict[str, str]) -> list[str]:
    queries = []
    for key in ["search_query_en", "search_query_zh"]:
        value = (row.get(key) or "").strip()
        if value:
            queries.append(value)

    en_keywords = [part.strip() for part in (row.get("concept_keywords_en") or "").split(";") if part.strip()]
    zh_keywords = [part.strip() for part in re.split(r"[;；]", row.get("concept_keywords_zh") or "") if part.strip()]
    if en_keywords:
        queries.append(" ".join(en_keywords[:5]) + " diagram")
    if zh_keywords:
        queries.append(" ".join(zh_keywords[:5]) + " 示意图")

    cleaned = []
    for query in queries:
        query = re.sub(r"\b(AI generated|Midjourney|Stable Diffusion|DALL-E)\b", "", query, flags=re.I)
        query = re.sub(r"\s+", " ", query).strip()
        if query and query not in cleaned:
            cleaned.append(query)
    return cleaned[:3]


def commons_search(query: str, limit: int = 8) -> list[str]:
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": "1400",
        "redirects": "1",
    }
    url = COMMONS_API + "?" + urlencode(params)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=20) as response:
        data = json.loads(response.read().decode("utf-8"))
    pages = data.get("query", {}).get("pages", {})
    return sorted(pages.values(), key=lambda p: p.get("index", 9999))


def strip_html(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value or "")
    return re.sub(r"\s+", " ", value).strip()


def candidate_from_page(page: dict, query: str) -> dict | None:
    title = page.get("title") or ""
    if any(term in title.lower() for term in BAD_TITLE_TERMS):
        return None
    info_items = page.get("imageinfo") or []
    if not info_items:
        return None
    info = info_items[0]
    original_url = normalize_url(info.get("url") or "")
    if not original_url:
        return None
    ext = Path(urlparse(original_url).path).suffix.lower()
    if ext not in ALLOWED_EXTS:
        return None
    direct_url = normalize_url(original_url if ext == ".svg" else (info.get("thumburl") or info.get("url") or ""))
    if not direct_url:
        return None
    meta = info.get("extmetadata") or {}
    author = strip_html((meta.get("Artist") or {}).get("value", ""))
    license_short = strip_html((meta.get("LicenseShortName") or {}).get("value", ""))
    credit = strip_html((meta.get("Credit") or {}).get("value", ""))
    object_name = strip_html((meta.get("ObjectName") or {}).get("value", "")) or title
    usage_terms = strip_html((meta.get("UsageTerms") or {}).get("value", ""))
    lower_blob = " ".join([title, author, credit, license_short, usage_terms, direct_url]).lower()
    if any(term in lower_blob for term in AI_TERMS):
        return None
    width = int(info.get("thumbwidth") or info.get("width") or 0)
    height = int(info.get("thumbheight") or info.get("height") or 0)
    original_width = int(info.get("width") or width or 0)
    original_height = int(info.get("height") or height or 0)
    if ext != ".svg" and (original_width < 600 or original_height < 250):
        return None
    page_url = f"https://commons.wikimedia.org/wiki/{quote(title.replace(' ', '_'), safe=':/_')}"
    source_license = license_short or usage_terms or "unknown"
    attribution = f"{object_name}, {author or 'unknown author'}, Wikimedia Commons, {source_license}"
    return {
        "title": title,
        "object_name": object_name,
        "author": author,
        "source_license": source_license,
        "attribution": attribution,
        "source_page_url": page_url,
        "direct_image_url": direct_url,
        "original_url": original_url,
        "width": width,
        "height": height,
        "ext": ext,
        "query": query,
    }


def choose_candidate(row: dict[str, str]) -> dict | None:
    for query in make_queries(row):
        try:
            pages = commons_search(query)
        except Exception:
            time.sleep(0.5)
            continue
        for page in pages:
            candidate = candidate_from_page(page, query)
            if candidate:
                return candidate
        time.sleep(0.15)
    return None


def download_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read()


def image_dimensions(path: Path, ext: str, fallback_width: int, fallback_height: int) -> tuple[int, int, str]:
    notes = []
    if ext == ".svg":
        text = path.read_text(encoding="utf-8", errors="ignore")[:4000]
        width_match = re.search(r'\bwidth="([0-9.]+)', text)
        height_match = re.search(r'\bheight="([0-9.]+)', text)
        width = int(float(width_match.group(1))) if width_match else fallback_width
        height = int(float(height_match.group(1))) if height_match else fallback_height
        if not width or not height:
            viewbox = re.search(r'\bviewBox="[^"]*?\s([0-9.]+)\s+([0-9.]+)"', text)
            if viewbox:
                width = int(float(viewbox.group(1)))
                height = int(float(viewbox.group(2)))
        return width or fallback_width, height or fallback_height, "svg checked"
    if Image is None:
        return fallback_width, fallback_height, "Pillow unavailable; dimensions from source metadata"
    try:
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            return int(img.width), int(img.height), "opened successfully"
    except Exception as exc:
        notes.append(f"image open failed: {exc}")
        return fallback_width, fallback_height, "; ".join(notes)


def quality_notes(status: str, ext: str, file_size: int, width: int, height: int, extra: str) -> str:
    notes = []
    if extra:
        notes.append(extra)
    if status == "downloaded":
        if file_size <= 10_240:
            notes.append("file smaller than 10KB")
        if ext != ".svg" and width < 600:
            notes.append("resolution below recommended width")
        if ext != ".svg" and width < 900:
            notes.append("flowchart may be below preferred 900px width")
    return "; ".join(dict.fromkeys(notes))


def manifest_row(row: dict[str, str], status: str, rank: int = 1, **kwargs) -> dict[str, str]:
    output = {field: "" for field in MANIFEST_FIELDS}
    output.update(
        {
            "chapter": row.get("chapter", ""),
            "md_file": row.get("md_file", ""),
            "slide_id": row.get("slide_id", ""),
            "slide_title": row.get("slide_title", ""),
            "need_image": row.get("need_image", ""),
            "candidate_rank": str(rank),
            "download_status": status,
            "image_role": row.get("image_role", ""),
            "image_type": row.get("image_type", ""),
            "caption_zh": row.get("suggested_caption_zh", ""),
            "layout_hint": row.get("layout_hint", ""),
        }
    )
    for key, value in kwargs.items():
        output[key] = str(value) if value is not None else ""
    return output


def process():
    DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    rows_out = []
    sha_to_first: dict[str, str] = {}
    dup_rows: dict[str, dict[str, str]] = {}
    url_to_first: dict[str, tuple[str, str]] = {}

    csv_paths = sorted(IMAGE_NEED_DIR.glob("image_need_ch*_text1.csv"))
    for csv_path in csv_paths:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        chapter_rows = []
        for row in rows:
            if row.get("need_image") != "yes":
                continue
            chapter = row["chapter"]
            slide_id = int(row["slide_id"])
            chapter_dir = DOWNLOAD_ROOT / chapter / "text1"
            chapter_dir.mkdir(parents=True, exist_ok=True)
            candidate = choose_candidate(row)
            if not candidate:
                out = manifest_row(
                    row,
                    "not_found",
                    search_query_used=" | ".join(make_queries(row)),
                    quality_notes="no suitable Wikimedia Commons image found after 3 query attempts",
                )
                rows_out.append(out)
                chapter_rows.append(out)
                continue

            norm_direct = candidate["direct_image_url"]
            if norm_direct in url_to_first:
                first_rel, first_sha = url_to_first[norm_direct]
                out = manifest_row(
                    row,
                    "reused_duplicate",
                    local_path=str(ROOT / first_rel),
                    relative_path=first_rel,
                    file_name=Path(first_rel).name,
                    file_ext=Path(first_rel).suffix,
                    sha256=first_sha,
                    source_page_url=candidate["source_page_url"],
                    direct_image_url=candidate["direct_image_url"],
                    source_title=candidate["object_name"],
                    source_author=candidate["author"],
                    source_license=candidate["source_license"],
                    attribution_text=candidate["attribution"],
                    search_query_used=candidate["query"],
                    duplicate_of=first_rel,
                    quality_notes="reused by normalized URL duplicate",
                )
                rows_out.append(out)
                chapter_rows.append(out)
                dup_rows.setdefault(first_sha, {"sha256": first_sha, "first_relative_path": first_rel, "reused_by": "", "source_page_url": candidate["source_page_url"], "notes": "duplicate reused"})
                dup_rows[first_sha]["reused_by"] = append_reused(dup_rows[first_sha]["reused_by"], f"{chapter}:s{slide_id:03d}")
                continue

            try:
                content = download_bytes(candidate["direct_image_url"])
            except Exception as exc:
                out = manifest_row(
                    row,
                    "failed",
                    source_page_url=candidate["source_page_url"],
                    direct_image_url=candidate["direct_image_url"],
                    source_title=candidate["object_name"],
                    source_author=candidate["author"],
                    source_license=candidate["source_license"],
                    attribution_text=candidate["attribution"],
                    search_query_used=candidate["query"],
                    quality_notes=f"download failed: {exc}",
                )
                rows_out.append(out)
                chapter_rows.append(out)
                continue

            sha = hashlib.sha256(content).hexdigest()
            if sha in sha_to_first:
                first_rel = sha_to_first[sha]
                out = manifest_row(
                    row,
                    "reused_duplicate",
                    local_path=str(ROOT / first_rel),
                    relative_path=first_rel,
                    file_name=Path(first_rel).name,
                    file_ext=Path(first_rel).suffix,
                    file_size_bytes=len(content),
                    sha256=sha,
                    source_page_url=candidate["source_page_url"],
                    direct_image_url=candidate["direct_image_url"],
                    source_title=candidate["object_name"],
                    source_author=candidate["author"],
                    source_license=candidate["source_license"],
                    attribution_text=candidate["attribution"],
                    search_query_used=candidate["query"],
                    duplicate_of=first_rel,
                    quality_notes="reused by SHA256 duplicate",
                )
                rows_out.append(out)
                chapter_rows.append(out)
                dup_rows.setdefault(sha, {"sha256": sha, "first_relative_path": first_rel, "reused_by": "", "source_page_url": candidate["source_page_url"], "notes": "duplicate reused"})
                dup_rows[sha]["reused_by"] = append_reused(dup_rows[sha]["reused_by"], f"{chapter}:s{slide_id:03d}")
                continue

            short_key_source = candidate["object_name"] or row.get("slide_title", "") or row.get("image_type", "")
            file_name = f"{chapter}_s{slide_id:03d}_r1_{slugify(short_key_source)}{candidate['ext']}"
            local_path = chapter_dir / file_name
            local_path.write_bytes(content)
            width, height, dim_note = image_dimensions(local_path, candidate["ext"], candidate["width"], candidate["height"])
            rel = local_path.relative_to(ROOT).as_posix()
            sha_to_first[sha] = rel
            url_to_first[norm_direct] = (rel, sha)
            q_notes = quality_notes("downloaded", candidate["ext"], local_path.stat().st_size, width, height, dim_note)
            out = manifest_row(
                row,
                "downloaded",
                local_path=str(local_path),
                relative_path=rel,
                file_name=file_name,
                file_ext=candidate["ext"],
                file_size_bytes=local_path.stat().st_size,
                width_px=width,
                height_px=height,
                sha256=sha,
                source_page_url=candidate["source_page_url"],
                direct_image_url=candidate["direct_image_url"],
                source_title=candidate["object_name"],
                source_author=candidate["author"],
                source_license=candidate["source_license"],
                attribution_text=candidate["attribution"],
                search_query_used=candidate["query"],
                quality_notes=q_notes,
            )
            rows_out.append(out)
            chapter_rows.append(out)

        chapter = csv_path.stem.split("_")[2]
        manifest_ch = DOWNLOAD_ROOT / chapter / "text1" / f"manifest_{chapter}_text1.csv"
        with manifest_ch.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
            writer.writeheader()
            writer.writerows(chapter_rows)

    with MANIFEST_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(rows_out)

    with DUPLICATE_PATH.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=DUP_FIELDS)
        writer.writeheader()
        writer.writerows(dup_rows.values())

    summary = summarize(rows_out)
    (DOWNLOAD_ROOT / "_download_summary_text1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def append_reused(existing: str, value: str) -> str:
    items = [item for item in existing.split(";") if item]
    if value not in items:
        items.append(value)
    return ";".join(items)


def summarize(rows: list[dict[str, str]]) -> dict:
    result = {}
    for row in rows:
        chapter = row["chapter"]
        result.setdefault(chapter, {"downloaded": 0, "reused_duplicate": 0, "not_found": 0, "skipped_existing_image": 0, "failed": 0, "total": 0})
        status = row["download_status"]
        result[chapter]["total"] += 1
        result[chapter][status] = result[chapter].get(status, 0) + 1
    return result


if __name__ == "__main__":
    process()
