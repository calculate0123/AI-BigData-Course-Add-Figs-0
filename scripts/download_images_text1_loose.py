from __future__ import annotations

from pathlib import Path
from urllib.parse import quote_plus, urlparse
from urllib.request import Request, urlopen
import csv
import hashlib
import html
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
MANIFEST_PATH = DOWNLOAD_ROOT / "image_download_manifest_text1_loose.csv"
DUPLICATE_PATH = DOWNLOAD_ROOT / "duplicate_check_text1_loose.csv"
SUMMARY_PATH = DOWNLOAD_ROOT / "_download_summary_text1_loose.json"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/125.0 Safari/537.36"
)

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

ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif"}


def request_text(url: str, timeout: int = 20) -> str:
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def request_bytes(url: str, timeout: int = 30) -> bytes:
    req = Request(url, headers={"User-Agent": USER_AGENT, "Referer": "https://duckduckgo.com/"})
    with urlopen(req, timeout=timeout) as resp:
        return resp.read()


def normalize_ext(url: str, content: bytes) -> str:
    ext = Path(urlparse(url).path).suffix.lower()
    if ext in ALLOWED_EXTS:
        return ".jpg" if ext == ".jpeg" else ext
    head = content[:32].lower()
    if head.startswith(b"\x89png"):
        return ".png"
    if head.startswith(b"\xff\xd8"):
        return ".jpg"
    if head.startswith(b"riff") and b"webp" in head:
        return ".webp"
    if b"<svg" in content[:500].lower():
        return ".svg"
    if head.startswith(b"gif"):
        return ".gif"
    return ".jpg"


def slugify(text: str, fallback: str = "image") -> str:
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower())
    text = re.sub(r"-+", "-", text).strip("-")
    return (text or fallback)[:44].strip("-") or fallback


def make_queries(row: dict[str, str]) -> list[str]:
    queries = []
    for key in ["search_query_en", "search_query_zh"]:
        value = (row.get(key) or "").strip()
        if value:
            queries.append(value)
    en_keywords = [x.strip() for x in (row.get("concept_keywords_en") or "").split(";") if x.strip()]
    zh_keywords = [x.strip() for x in re.split(r"[;；]", row.get("concept_keywords_zh") or "") if x.strip()]
    if en_keywords:
        queries.append(" ".join(en_keywords[:5]) + " diagram")
    if zh_keywords:
        queries.append(" ".join(zh_keywords[:5]) + " 示意图")
    cleaned = []
    for q in queries:
        q = re.sub(r"\s+", " ", q).strip()
        if q and q not in cleaned:
            cleaned.append(q)
    return cleaned[:3]


def search_images(query: str, max_results: int = 30) -> list[dict[str, str]]:
    search_url = "https://www.bing.com/images/search?q=" + quote_plus(query) + "&form=HDRSC2&first=1"
    html = request_text(search_url)
    results = []
    seen = set()
    for match in re.finditer(r'class="iusc"[^>]*?m="([^"]+)"', html):
        raw = html_module_unescape(match.group(1))
        try:
            data = json.loads(raw)
        except Exception:
            continue
        image = data.get("murl") or data.get("turl")
        if not image or image in seen:
            continue
        seen.add(image)
        results.append(
            {
                "image": image,
                "url": data.get("purl") or "",
                "title": data.get("t") or "",
                "source": data.get("s") or "",
            }
        )
        if len(results) >= max_results:
            break
    if results:
        return results

    # Fallback parser for alternate Bing markup with escaped JSON attributes.
    entity_matches = re.findall(r"&quot;murl&quot;:&quot;(.*?)&quot;", html)
    page_matches = re.findall(r"&quot;purl&quot;:&quot;(.*?)&quot;", html)
    title_matches = re.findall(r"&quot;t&quot;:&quot;(.*?)&quot;", html)
    for idx, image in enumerate(entity_matches):
        page = page_matches[idx] if idx < len(page_matches) else ""
        title = title_matches[idx] if idx < len(title_matches) else ""
        image = image.replace("\\/", "/").replace("&amp;", "&")
        page = page.replace("\\/", "/").replace("&amp;", "&")
        title = title.replace("&amp;", "&")
        if image and image not in seen:
            seen.add(image)
            results.append({"image": image, "url": page, "title": title, "source": ""})
        if len(results) >= max_results:
            break
    return results


COMMONS_CACHE: dict[str, list[dict[str, str]]] = {}
BING_CACHE: dict[str, list[dict[str, str]]] = {}


def commons_loose_images(query: str, max_results: int = 20) -> list[dict[str, str]]:
    if query in COMMONS_CACHE:
        return COMMONS_CACHE[query]
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": query,
        "gsrlimit": str(max_results),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": "1600",
        "redirects": "1",
    }
    api_url = "https://commons.wikimedia.org/w/api.php?" + "&".join(f"{k}={quote_plus(v)}" for k, v in params.items())
    try:
        data = json.loads(request_text(api_url))
    except Exception:
        COMMONS_CACHE[query] = []
        return []
    results = []
    pages = data.get("query", {}).get("pages", {})
    for page in sorted(pages.values(), key=lambda item: item.get("index", 9999)):
        info_items = page.get("imageinfo") or []
        if not info_items:
            continue
        info = info_items[0]
        direct = info.get("thumburl") or info.get("url")
        if not direct:
            continue
        title = page.get("title") or ""
        source_page = "https://commons.wikimedia.org/wiki/" + title.replace(" ", "_")
        meta = info.get("extmetadata") or {}
        license_short = ((meta.get("LicenseShortName") or {}).get("value") or "").replace("<span class=\"licensetpl_short\">", "").replace("</span>", "")
        author = re.sub(r"<[^>]+>", "", ((meta.get("Artist") or {}).get("value") or "unknown"))
        results.append(
            {
                "image": direct,
                "url": source_page,
                "title": title,
                "source": "Wikimedia Commons",
                "license": license_short or "unknown; copyright risk not checked",
                "author": author,
            }
        )
    COMMONS_CACHE[query] = results
    time.sleep(0.2)
    return results


def relevant_candidate(query: str, candidate: dict[str, str]) -> bool:
    blob = " ".join([candidate.get("title", ""), candidate.get("url", ""), candidate.get("image", ""), candidate.get("source", "")]).lower()
    terms = []
    for term in re.split(r"[^A-Za-z0-9\u4e00-\u9fff]+", query.lower()):
        if len(term) >= 4 or re.search(r"[\u4e00-\u9fff]", term):
            terms.append(term)
    stop = {"diagram", "image", "workflow", "concept", "open", "resource", "materials", "science", "overview"}
    useful = [term for term in terms if term not in stop]
    if not useful:
        return True
    return any(term in blob for term in useful[:8])


def bing_thumbnail_candidate(query: str, row: dict[str, str]) -> dict[str, str]:
    enriched_query = (query + " " + row.get("slide_title", "")).strip()
    direct = "https://tse1.mm.bing.net/th?q=" + quote_plus(enriched_query) + "&w=1600&h=900&c=7&rs=1&p=0"
    return {
        "image": direct,
        "url": "https://www.bing.com/images/search?q=" + quote_plus(enriched_query),
        "title": enriched_query,
        "source": "Bing thumbnail fallback",
        "license": "unknown; copyright risk not checked",
        "author": "unknown",
    }


def html_module_unescape(value: str) -> str:
    return html.unescape(value)


def dims(path: Path, ext: str) -> tuple[int, int, str]:
    if ext == ".svg":
        text = path.read_text(encoding="utf-8", errors="ignore")[:5000]
        width = height = 0
        m_w = re.search(r'\bwidth=["\']?([0-9.]+)', text)
        m_h = re.search(r'\bheight=["\']?([0-9.]+)', text)
        if m_w and m_h:
            width, height = int(float(m_w.group(1))), int(float(m_h.group(1)))
        if not width or not height:
            m = re.search(r'\bviewBox=["\'][^"\']*?\s([0-9.]+)\s+([0-9.]+)', text)
            if m:
                width, height = int(float(m.group(1))), int(float(m.group(2)))
        return width, height, "svg parsed"
    if Image is None:
        return 0, 0, "Pillow unavailable"
    try:
        with Image.open(path) as img:
            img.verify()
        with Image.open(path) as img:
            return int(img.width), int(img.height), "opened successfully"
    except Exception as exc:
        return 0, 0, f"image open failed: {exc}"


def manifest_row(row: dict[str, str], status: str, **kwargs) -> dict[str, str]:
    out = {field: "" for field in MANIFEST_FIELDS}
    out.update(
        {
            "chapter": row.get("chapter", ""),
            "md_file": row.get("md_file", ""),
            "slide_id": row.get("slide_id", ""),
            "slide_title": row.get("slide_title", ""),
            "need_image": row.get("need_image", ""),
            "candidate_rank": "1",
            "download_status": status,
            "source_license": "unknown; copyright risk not checked",
            "source_author": "unknown",
            "attribution_text": "来源不明或版权未核验，需人工复核后再用于正式课件。",
            "image_role": row.get("image_role", ""),
            "image_type": row.get("image_type", ""),
            "caption_zh": row.get("suggested_caption_zh", ""),
            "layout_hint": row.get("layout_hint", ""),
        }
    )
    for key, value in kwargs.items():
        out[key] = "" if value is None else str(value)
    return out


def read_need_rows() -> list[dict[str, str]]:
    rows = []
    for path in sorted(IMAGE_NEED_DIR.glob("image_need_ch*_text1.csv")):
        with path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows.extend([row for row in csv.DictReader(handle) if row.get("need_image") == "yes"])
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def choose_and_download(row: dict[str, str], seen_sha: dict[str, str], used_urls: set[str]) -> dict[str, str]:
    chapter = row["chapter"]
    slide_id = int(row["slide_id"])
    out_dir = DOWNLOAD_ROOT / chapter / "text1_loose"
    out_dir.mkdir(parents=True, exist_ok=True)
    attempted_queries = []

    for query in make_queries(row):
        attempted_queries.append(query)
        try:
            candidates = [bing_thumbnail_candidate(query, row)]
        except Exception as exc:
            last_error = f"search failed: {exc}"
            time.sleep(0.5)
            continue
        for rank, cand in enumerate(candidates, 1):
            if not relevant_candidate(query, cand):
                continue
            image_url = cand["image"]
            if image_url in used_urls:
                continue
            try:
                content = request_bytes(image_url)
            except Exception:
                continue
            if len(content) < 1024:
                continue
            ext = normalize_ext(image_url, content)
            sha = hashlib.sha256(content).hexdigest()
            if sha in seen_sha:
                first = seen_sha[sha]
                used_urls.add(image_url)
                return manifest_row(
                    row,
                    "reused_duplicate",
                    candidate_rank=rank,
                    local_path=str(ROOT / first),
                    relative_path=first,
                    file_name=Path(first).name,
                    file_ext=Path(first).suffix,
                    file_size_bytes=len(content),
                    sha256=sha,
                    source_page_url=cand.get("url", ""),
                    direct_image_url=image_url,
                    source_title=cand.get("title", ""),
                    source_author=cand.get("author", "unknown"),
                    source_license=cand.get("license", "unknown; copyright risk not checked"),
                    search_query_used=query,
                    duplicate_of=first,
                    quality_notes="loose mode; duplicate by SHA256; source and copyright not verified",
                )
            key = slugify(cand.get("title") or row.get("slide_title") or query)
            file_name = f"{chapter}_s{slide_id:03d}_r1_{key}{ext}"
            local_path = out_dir / file_name
            local_path.write_bytes(content)
            width, height, note = dims(local_path, ext)
            rel = local_path.relative_to(ROOT).as_posix()
            seen_sha[sha] = rel
            used_urls.add(image_url)
            qnotes = ["loose mode; source and copyright not verified", note]
            if width and width < 400:
                qnotes.append("low resolution")
            return manifest_row(
                row,
                "downloaded",
                candidate_rank=rank,
                local_path=str(local_path),
                relative_path=rel,
                file_name=file_name,
                file_ext=ext,
                file_size_bytes=local_path.stat().st_size,
                width_px=width,
                height_px=height,
                sha256=sha,
                source_page_url=cand.get("url", ""),
                direct_image_url=image_url,
                source_title=cand.get("title", ""),
                source_author=cand.get("author", "unknown"),
                source_license=cand.get("license", "unknown; copyright risk not checked"),
                search_query_used=query,
                quality_notes="; ".join([x for x in qnotes if x]),
            )
        time.sleep(0.2)

    return manifest_row(
        row,
        "not_found",
        search_query_used=" | ".join(attempted_queries),
        quality_notes="loose mode still found no downloadable image; " + locals().get("last_error", ""),
    )


def summarize(rows: list[dict[str, str]]) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for row in rows:
        ch = row["chapter"]
        summary.setdefault(ch, {"downloaded": 0, "reused_duplicate": 0, "not_found": 0, "failed": 0, "skipped_existing_image": 0, "total": 0})
        summary[ch]["total"] += 1
        summary[ch][row["download_status"]] = summary[ch].get(row["download_status"], 0) + 1
    return summary


def main():
    DOWNLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    rows = read_need_rows()
    manifest = []
    seen_sha: dict[str, str] = {}
    used_urls: set[str] = set()
    for idx, row in enumerate(rows, 1):
        try:
            manifest.append(choose_and_download(row, seen_sha, used_urls))
        except Exception as exc:
            manifest.append(manifest_row(row, "failed", quality_notes=f"unexpected failure: {exc}"))
        if idx % 25 == 0:
            print(f"processed {idx}/{len(rows)}", flush=True)

    write_csv(MANIFEST_PATH, manifest, MANIFEST_FIELDS)
    for ch in [f"ch{i:02d}" for i in range(1, 11)]:
        write_csv(DOWNLOAD_ROOT / ch / "text1_loose" / f"manifest_{ch}_text1_loose.csv", [r for r in manifest if r["chapter"] == ch], MANIFEST_FIELDS)

    dup = {}
    for row in manifest:
        if row["download_status"] == "reused_duplicate" and row["sha256"]:
            rec = dup.setdefault(row["sha256"], {"sha256": row["sha256"], "first_relative_path": row["duplicate_of"], "reused_by": "", "source_page_url": row["source_page_url"], "notes": "loose duplicate"})
            rec["reused_by"] = (rec["reused_by"] + ";" if rec["reused_by"] else "") + f"{row['chapter']}:s{int(row['slide_id']):03d}"
    write_csv(DUPLICATE_PATH, list(dup.values()), DUP_FIELDS)
    summary = summarize(manifest)
    SUMMARY_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
