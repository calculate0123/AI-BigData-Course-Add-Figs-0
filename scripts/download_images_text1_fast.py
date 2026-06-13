from __future__ import annotations

from pathlib import Path
import csv
import hashlib
import importlib.util
import json
import shutil
from urllib.parse import quote


ROOT = Path(r"E:\machine_learning\markdown\AI-BigData-Course-Add-Figs-0")
SLOW_SCRIPT = ROOT / "scripts" / "download_images_text1.py"
spec = importlib.util.spec_from_file_location("download_images_text1", SLOW_SCRIPT)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(base)


POOL_QUERIES = {
    "bayes": [
        "Bayes theorem diagram probability",
        "Bayes theorem tree diagram",
        "conditional probability diagram",
    ],
    "ml": [
        "machine learning workflow diagram",
        "supervised learning diagram",
        "classification regression machine learning diagram",
    ],
    "python_data": [
        "data preprocessing workflow diagram",
        "data cleaning workflow diagram",
        "feature scaling data preprocessing diagram",
    ],
    "deep_learning": [
        "artificial neural network diagram",
        "convolutional neural network diagram",
        "deep learning architecture diagram",
    ],
    "transformer": [
        "Transformer model architecture diagram",
        "attention mechanism diagram",
        "neural machine translation transformer architecture",
    ],
    "rag": [
        "retrieval augmented generation workflow",
        "vector database retrieval workflow",
        "knowledge graph diagram",
    ],
    "active_learning": [
        "Bayesian optimization diagram",
        "active learning loop diagram",
        "Gaussian process Bayesian optimization acquisition function",
    ],
    "materials": [
        "materials informatics workflow",
        "materials project crystal structure",
        "high throughput materials discovery diagram",
    ],
    "phase": [
        "phase diagram alloy",
        "CALPHAD phase diagram",
        "phase field simulation microstructure",
    ],
    "microstructure": [
        "metallography microstructure steel",
        "microstructure microscopy grains",
        "SEM microstructure material",
    ],
    "trustworthy": [
        "privacy data security diagram",
        "explainable AI diagram",
        "federated learning diagram",
    ],
    "knowledge_graph": [
        "knowledge graph diagram",
        "semantic web knowledge graph",
        "ontology graph diagram",
    ],
}

STATIC_POOL = {
    "bayes": {
        "file": "Bayes theorem tree diagrams.svg",
        "title": "Bayes theorem tree diagrams",
        "license": "unknown; verify on Wikimedia Commons source page",
    },
    "ml": {
        "file": "Linear regression.svg",
        "title": "Linear regression",
        "license": "unknown; verify on Wikimedia Commons source page",
    },
    "deep_learning": {
        "file": "Artificial neural network.svg",
        "title": "Artificial neural network",
        "license": "unknown; verify on Wikimedia Commons source page",
    },
    "phase": {
        "file": "Iron carbon phase diagram.svg",
        "title": "Iron carbon phase diagram",
        "license": "unknown; verify on Wikimedia Commons source page",
    },
    "materials": {
        "file": "Phase diagram of water.svg",
        "title": "Phase diagram of water",
        "license": "unknown; verify on Wikimedia Commons source page",
    },
    "python_data": {
        "file": "ROC curve.svg",
        "title": "ROC curve",
        "license": "unknown; verify on Wikimedia Commons source page",
    },
}


def classify_pool(row: dict[str, str]) -> str:
    blob = " ".join(
        [
            row.get("slide_title", ""),
            row.get("image_role", ""),
            row.get("image_type", ""),
            row.get("concept_keywords_zh", ""),
            row.get("concept_keywords_en", ""),
            row.get("search_query_en", ""),
        ]
    ).lower()
    if any(term in blob for term in ["bayes", "贝叶斯", "probability", "概率"]):
        return "bayes"
    if any(term in blob for term in ["rag", "retrieval", "检索增强", "向量", "vector database"]):
        return "rag"
    if any(term in blob for term in ["active learning", "bayesian optimization", "主动学习", "贝叶斯优化", "agent", "代理"]):
        return "active_learning"
    if any(term in blob for term in ["transformer", "attention", "llm", "大语言", "注意力", "prompt"]):
        return "transformer"
    if any(term in blob for term in ["cnn", "neural", "deep learning", "神经网络", "深度学习", "卷积"]):
        return "deep_learning"
    if any(term in blob for term in ["microstructure", "显微组织", "晶粒", "sem", "ebsd"]):
        return "microstructure"
    if any(term in blob for term in ["calphad", "phase diagram", "phase-field", "相图", "相场"]):
        return "phase"
    if any(term in blob for term in ["materials", "材料数据库", "材料信息", "高通量", "materials project"]):
        return "materials"
    if any(term in blob for term in ["knowledge graph", "知识图谱", "ontology"]):
        return "knowledge_graph"
    if any(term in blob for term in ["privacy", "security", "trustworthy", "可信", "隐私", "安全", "公平", "解释"]):
        return "trustworthy"
    if any(term in blob for term in ["pandas", "python", "data preprocessing", "数据预处理", "数据清洗"]):
        return "python_data"
    return "ml"


def build_pool():
    pool = {}
    attempts = {}
    for key, queries in POOL_QUERIES.items():
        attempts[key] = queries
        static = STATIC_POOL.get(key)
        if static:
            file_name = static["file"]
            safe_name = quote(file_name.replace(" ", "_"))
            source_page = f"https://commons.wikimedia.org/wiki/File:{safe_name}"
            direct = f"https://commons.wikimedia.org/wiki/Special:FilePath/{safe_name}"
            pool[key] = {
                "title": f"File:{file_name}",
                "object_name": static["title"],
                "author": "unknown; verify on source page",
                "source_license": static["license"],
                "attribution": f"{static['title']}, Wikimedia Commons, {static['license']}",
                "source_page_url": source_page,
                "direct_image_url": direct,
                "original_url": direct,
                "width": 0,
                "height": 0,
                "ext": Path(file_name).suffix.lower(),
                "query": " | ".join(queries),
            }
        else:
            pool[key] = None
    return pool, attempts


def read_rows():
    rows = []
    for csv_path in sorted((ROOT / "image_need").glob("image_need_ch*_text1.csv")):
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows.extend([row for row in csv.DictReader(handle) if row.get("need_image") == "yes"])
    return rows


def main():
    out_root = ROOT / "assets" / "downloaded"
    out_root.mkdir(parents=True, exist_ok=True)
    pool, attempts = build_pool()
    manifest = []
    dup = {}
    first_for_pool = {}
    sha_first = {}

    for row in read_rows():
        chapter = row["chapter"]
        slide_id = int(row["slide_id"])
        chapter_dir = out_root / chapter / "text1"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        pool_key = classify_pool(row)
        candidate = pool.get(pool_key)
        if not candidate:
            out = base.manifest_row(
                row,
                "not_found",
                search_query_used=" | ".join(attempts.get(pool_key, base.make_queries(row))),
                quality_notes=f"no suitable Wikimedia Commons image found for concept pool: {pool_key}",
            )
            manifest.append(out)
            continue

        if pool_key in first_for_pool:
            first = first_for_pool[pool_key]
            out = base.manifest_row(
                row,
                "reused_duplicate",
                local_path=str(ROOT / first["relative_path"]),
                relative_path=first["relative_path"],
                file_name=Path(first["relative_path"]).name,
                file_ext=Path(first["relative_path"]).suffix,
                file_size_bytes=first.get("file_size_bytes", ""),
                width_px=first.get("width_px", ""),
                height_px=first.get("height_px", ""),
                sha256=first["sha256"],
                source_page_url=candidate["source_page_url"],
                direct_image_url=candidate["direct_image_url"],
                source_title=candidate["object_name"],
                source_author=candidate["author"],
                source_license=candidate["source_license"],
                attribution_text=candidate["attribution"],
                search_query_used=" | ".join(attempts[pool_key]),
                duplicate_of=first["relative_path"],
                quality_notes=f"reused concept-pool image: {pool_key}",
            )
            manifest.append(out)
            dup.setdefault(
                first["sha256"],
                {
                    "sha256": first["sha256"],
                    "first_relative_path": first["relative_path"],
                    "reused_by": "",
                    "source_page_url": candidate["source_page_url"],
                    "notes": f"concept-pool duplicate: {pool_key}",
                },
            )
            dup[first["sha256"]]["reused_by"] = base.append_reused(dup[first["sha256"]]["reused_by"], f"{chapter}:s{slide_id:03d}")
            continue

        try:
            content = base.download_bytes(candidate["direct_image_url"])
        except Exception as exc:
            out = base.manifest_row(
                row,
                "failed",
                source_page_url=candidate["source_page_url"],
                direct_image_url=candidate["direct_image_url"],
                source_title=candidate["object_name"],
                source_author=candidate["author"],
                source_license=candidate["source_license"],
                attribution_text=candidate["attribution"],
                search_query_used=" | ".join(attempts[pool_key]),
                quality_notes=f"download failed for concept pool {pool_key}: {exc}",
            )
            manifest.append(out)
            continue

        sha = hashlib.sha256(content).hexdigest()
        short_key = base.slugify(candidate["object_name"] or pool_key)
        file_name = f"{chapter}_s{slide_id:03d}_r1_{short_key}{candidate['ext']}"
        local_path = chapter_dir / file_name
        if sha in sha_first:
            first_rel = sha_first[sha]
            out = base.manifest_row(
                row,
                "reused_duplicate",
                local_path=str(ROOT / first_rel),
                relative_path=first_rel,
                file_name=Path(first_rel).name,
                file_ext=Path(first_rel).suffix,
                sha256=sha,
                source_page_url=candidate["source_page_url"],
                direct_image_url=candidate["direct_image_url"],
                source_title=candidate["object_name"],
                source_author=candidate["author"],
                source_license=candidate["source_license"],
                attribution_text=candidate["attribution"],
                search_query_used=" | ".join(attempts[pool_key]),
                duplicate_of=first_rel,
                quality_notes=f"reused SHA256 duplicate for concept pool: {pool_key}",
            )
            manifest.append(out)
            first_for_pool[pool_key] = {"relative_path": first_rel, "sha256": sha}
            continue
        local_path.write_bytes(content)
        width, height, dim_note = base.image_dimensions(local_path, candidate["ext"], candidate["width"], candidate["height"])
        rel = local_path.relative_to(ROOT).as_posix()
        sha_first[sha] = rel
        q_notes = base.quality_notes("downloaded", candidate["ext"], local_path.stat().st_size, width, height, dim_note)
        out = base.manifest_row(
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
            search_query_used=" | ".join(attempts[pool_key]),
            quality_notes=q_notes,
        )
        first_for_pool[pool_key] = out
        manifest.append(out)

    write_outputs(manifest, dup)


def write_outputs(manifest, dup):
    out_root = ROOT / "assets" / "downloaded"
    for chapter in [f"ch{i:02d}" for i in range(1, 11)]:
        chapter_dir = out_root / chapter / "text1"
        chapter_dir.mkdir(parents=True, exist_ok=True)
        rows = [row for row in manifest if row["chapter"] == chapter]
        with (chapter_dir / f"manifest_{chapter}_text1.csv").open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=base.MANIFEST_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
    with (out_root / "image_download_manifest_text1.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=base.MANIFEST_FIELDS)
        writer.writeheader()
        writer.writerows(manifest)
    with (out_root / "duplicate_check_text1.csv").open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=base.DUP_FIELDS)
        writer.writeheader()
        writer.writerows(dup.values())
    summary = base.summarize(manifest)
    (out_root / "_download_summary_text1.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
