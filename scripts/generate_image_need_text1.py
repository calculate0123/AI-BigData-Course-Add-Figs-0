from pathlib import Path
import csv
import json
import re


ROOT = Path(r"E:\machine_learning\markdown\AI-BigData-Course-Add-Figs-0")
SLIDES_DIR = ROOT / "slides"
OUT_DIR = ROOT / "image_need"
OUT_DIR.mkdir(exist_ok=True)

HEADERS = [
    "chapter",
    "md_file",
    "slide_id",
    "slide_title",
    "need_image",
    "image_priority",
    "image_role",
    "image_type",
    "concept_keywords_zh",
    "concept_keywords_en",
    "search_query_zh",
    "search_query_en",
    "preferred_source_type",
    "avoid_source_type",
    "license_requirement",
    "suggested_caption_zh",
    "insertion_position",
    "layout_hint",
    "reason",
    "existing_image_detected",
    "notes",
]

PREFERRED = (
    "official documentation; open educational resource; open access paper; "
    "Wikimedia Commons; university course material; government/lab source"
)
AVOID = (
    "AI-generated image; stock photo; watermark image; commercial copyrighted slide; "
    "low-resolution blog image"
)
LICENSE_REQ = "prefer CC BY/CC BY-SA/public domain/official reusable image; record attribution"

CHAPTER_CONTEXT = {
    "ch01": ("人工智能与大数据材料科学概论", "AI big data materials science overview"),
    "ch02": ("Python 数据处理 材料数据预处理", "Python data preprocessing materials dataset workflow"),
    "ch03": ("贝叶斯定理 概率推断", "Bayes theorem probability inference diagram"),
    "ch04": ("机器学习 材料性能预测", "machine learning materials property prediction workflow"),
    "ch05": ("深度学习 多模态AI 显微组织识别", "deep learning microstructure recognition CNN architecture"),
    "ch06": ("生成式AI 大语言模型 提示工程", "large language model Transformer attention mechanism prompt engineering workflow"),
    "ch07": ("知识库 知识图谱 RAG", "knowledge graph retrieval augmented generation workflow vector database"),
    "ch08": ("AI代理 主动学习 贝叶斯优化", "AI agent Bayesian optimization active learning loop"),
    "ch09": ("材料数据库 高通量材料设计", "materials database high-throughput materials design workflow"),
    "ch10": ("可信AI 数据安全 综合应用", "trustworthy AI data security privacy fairness explainability workflow"),
}

PATTERNS = [
    (
        "材料组织",
        "microscopy",
        "材料组织",
        ["显微组织", "晶粒", "组织识别", "microstructure", "SEM", "EBSD", "金相"],
        "materials microstructure recognition microscopy image",
        "材料显微组织识别 图像",
    ),
    (
        "材料应用",
        "simulation",
        "模拟结果",
        ["相场", "CALPHAD", "相图", "分子动力学", "有限元", "高通量", "Materials Project", "材料数据库", "材料基因", "phase-field", "phase diagram", "DFT"],
        "materials informatics CALPHAD phase diagram high-throughput materials design",
        "材料信息学 CALPHAD 相图 高通量材料设计",
    ),
    (
        "算法机理",
        "algorithm_diagram",
        "算法流程",
        ["贝叶斯", "概率分布", "先验", "后验", "似然", "Bayes", "概率", "正态分布", "条件概率"],
        "Bayes theorem diagram probability prior posterior likelihood",
        "贝叶斯定理 先验 后验 概率图示",
    ),
    (
        "机器学习",
        "flowchart",
        "算法流程",
        ["监督学习", "回归", "分类", "聚类", "模型训练", "模型评估", "特征工程", "交叉验证", "过拟合", "欠拟合", "随机森林", "SVM", "KNN"],
        "machine learning workflow feature engineering model training evaluation diagram",
        "机器学习流程 特征工程 模型训练 评估 示意图",
    ),
    (
        "深度学习",
        "algorithm_diagram",
        "算法流程",
        ["神经网络", "CNN", "卷积", "RNN", "Transformer", "注意力", "深度学习", "多模态", "embedding", "编码器", "解码器"],
        "neural network architecture Transformer attention mechanism CNN diagram",
        "神经网络 Transformer 注意力机制 CNN 架构图",
    ),
    (
        "生成式AI",
        "algorithm_diagram",
        "概念示意",
        ["大语言模型", "提示工程", "生成式", "token", "词向量", "幻觉", "LLM", "prompt", "上下文窗口"],
        "large language model Transformer attention mechanism prompt engineering workflow",
        "大语言模型 提示工程 Transformer 注意力机制 示意图",
    ),
    (
        "RAG",
        "flowchart",
        "数据流程",
        ["RAG", "检索增强", "向量数据库", "向量检索", "知识库", "知识图谱", "GraphRAG", "语义检索"],
        "retrieval augmented generation workflow vector database knowledge graph diagram",
        "检索增强生成 RAG 向量数据库 知识图谱 流程图",
    ),
    (
        "主动学习",
        "flowchart",
        "算法流程",
        ["主动学习", "贝叶斯优化", "采集函数", "不确定性", "AI Agent", "代理", "闭环", "优化循环"],
        "Bayesian optimization active learning loop acquisition function AI agent workflow",
        "贝叶斯优化 主动学习 闭环 AI Agent 流程图",
    ),
    (
        "数据流程",
        "flowchart",
        "数据流程",
        ["数据采集", "数据清洗", "数据预处理", "缺失值", "异常值", "数据标准化", "Pandas", "NumPy", "CSV", "数据流"],
        "Python pandas data preprocessing workflow missing values feature scaling diagram",
        "Python Pandas 数据预处理 数据清洗 流程图",
    ),
    (
        "安全合规案例",
        "schematic",
        "安全合规案例",
        ["可信AI", "隐私", "数据安全", "公平性", "可解释", "鲁棒性", "联邦学习", "差分隐私", "合规", "伦理", "水印", "攻击"],
        "trustworthy AI framework data privacy fairness explainability robustness diagram",
        "可信AI 数据安全 隐私 公平性 可解释性 示意图",
    ),
]

BROAD_YES = ["流程", "架构", "机制", "关系", "案例", "应用", "平台", "数据库", "图谱", "模型", "网络", "闭环", "评价", "对比", "示意", "路径", "体系"]
NO_TITLE_TERMS = ["封面", "目录", "本章小结", "小结", "总结", "思考题", "练习", "学习目标", "章节导入", "过渡"]
CODE_MARKERS = ["```", "import ", "def ", "for ", "while ", "class ", "print(", "pd.", "np."]

IMAGE_RE = re.compile(r"(?:!\[[^\]]*\]\([^\)]*\)|<img\b|backgroundImage|_background|\bbackground:\s*url|!\[bg)", re.I)
HEADING_RE = re.compile(r"^\s{0,3}(#{1,3})\s+(.+?)\s*$", re.M)


def target_files():
    candidates = []
    for path in SLIDES_DIR.glob("*_Marp.md"):
        if "_with_figs" in path.name:
            continue
        m = re.search(r"第(\d+)章", path.name)
        if not m:
            continue
        chapter_num = int(m.group(1))
        if 1 <= chapter_num <= 10:
            candidates.append((chapter_num, path))
    candidates.sort(key=lambda item: item[0])
    if len(candidates) != 10:
        raise RuntimeError(f"Expected 10 target Marp files, found {len(candidates)}")
    return [(f"ch{num:02d}", path.name, path) for num, path in candidates]


def split_marp(text):
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    start = 0
    if lines and lines[0].strip() == "---":
        in_fence = False
        for i in range(1, len(lines)):
            stripped = lines[i].strip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
            if not in_fence and stripped == "---":
                start = i + 1
                break

    body_lines = lines[start:]
    slides = []
    buf = []
    in_fence = False
    fence_marker = None
    for line in body_lines:
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            marker = stripped[:3]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
                fence_marker = None
        if not in_fence and stripped == "---":
            slides.append("\n".join(buf).strip("\n"))
            buf = []
        else:
            buf.append(line)
    if buf or body_lines:
        slides.append("\n".join(buf).strip("\n"))
    while slides and not slides[-1].strip():
        slides.pop()
    return slides


def clean_text(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"[`*_{}\[\]()>#]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def get_title(slide, slide_id):
    match = HEADING_RE.search(slide)
    if match:
        title = clean_text(match.group(2))
    else:
        lines = []
        for line in slide.split("\n"):
            stripped = line.strip()
            if not stripped or stripped.startswith("<!--") or stripped.startswith("$") or stripped.startswith("!"):
                continue
            if stripped.startswith(("-", "*")):
                stripped = stripped.lstrip("-* ")
            if stripped.startswith(("class:", "style:", "paginate:", "background")):
                continue
            lines.append(clean_text(stripped))
            if len(lines) >= 2:
                break
        title = " ".join(lines) if lines else f"第{slide_id}页"
    return title[:30] if len(title) > 30 else title


def is_code_heavy(slide):
    code_blocks = len(re.findall(r"```", slide))
    code_hits = sum(slide.count(marker) for marker in CODE_MARKERS)
    return code_blocks >= 1 and code_hits >= 3


def classify(chapter, title, slide, existing_image):
    text = title + "\n" + clean_text(slide)
    lower = text.lower()
    placeholder = bool(re.search(r"placeholder|占位|待插图|figure_placeholder", slide, re.I))
    title_no = any(term in title for term in NO_TITLE_TERMS)
    content_len = len(clean_text(slide))
    bullet_count = len(re.findall(r"^\s*[-*+]\s+", slide, re.M))
    code_heavy = is_code_heavy(slide)

    best = None
    best_hits = []
    for role_name, image_type, image_role, keywords, query_en, query_zh in PATTERNS:
        hits = [kw for kw in keywords if kw.lower() in lower or kw in text]
        if hits and (best is None or len(hits) > len(best_hits)):
            best = (role_name, image_type, image_role, keywords, query_en, query_zh)
            best_hits = hits

    if existing_image and not placeholder:
        need_image, priority, image_role, image_type = "no", "none", "", ""
        insertion_position, layout_hint = "none", "不建议插图"
        reason = "本页已检测到图片语法或背景图，第一阶段不建议重复规划新图。"
        notes = "如原图缺失或不匹配，可人工审核后改为 replace_placeholder。"
    elif title_no and not placeholder:
        need_image, priority, image_role, image_type = "no", "none", "", ""
        insertion_position, layout_hint = "none", "不建议插图"
        reason = "封面、目录、过渡或总结类页面通常以文字结构为主，避免装饰性配图。"
        notes = "可人工判断是否需要主题图。"
    elif code_heavy and best is None:
        need_image, priority, image_role, image_type = "no", "none", "", ""
        insertion_position, layout_hint = "none", "不建议插图"
        reason = "本页以代码阅读或演示为主，插图可能挤压 4:3 板书式排版空间。"
        notes = "若后续需要运行结果截图，可人工补充。"
    elif best is not None:
        role_name, image_type, image_role, keywords, query_en, query_zh = best
        need_image = "yes"
        high_title_terms = ["流程", "机制", "架构", "相图", "显微组织", "RAG", "Transformer", "贝叶斯优化"]
        priority = "high" if len(best_hits) >= 2 or any(term in title for term in high_title_terms) else "medium"
        insertion_position = "replace_placeholder" if placeholder else ("bottom" if image_role in ["算法流程", "数据流程"] or "流程" in title else "right")
        layout_hint = "替换原占位图" if placeholder else ("底部横向流程图" if insertion_position == "bottom" else "右侧 40% 宽度")
        reason = f"本页涉及{role_name}相关概念，配图有助于把抽象关系转化为可视化教学对象。"
        notes = f"关键词命中：{'；'.join(best_hits[:6])}。"
    elif any(term in text for term in BROAD_YES) and content_len < 900 and bullet_count <= 8:
        need_image, priority, image_role, image_type = "yes", "low", "概念示意", "schematic"
        insertion_position, layout_hint = "right", "右侧 35% 宽度"
        reason = "本页包含较抽象的框架、流程或应用关系，可用简洁示意图辅助讲解。"
        notes = "低优先级，建议人工审核是否确有必要。"
    else:
        need_image, priority, image_role, image_type = "no", "none", "", ""
        insertion_position, layout_hint = "none", "不建议插图"
        reason = "本页文字信息已能支撑讲解，或页面内容较密，插图可能降低可读性。"
        notes = ""

    if need_image == "yes":
        if best is not None:
            _, _, _, keywords, query_en, query_zh = best
            zh_keywords = [kw for kw in keywords if not re.search(r"[A-Za-z]", kw)] + [CHAPTER_CONTEXT[chapter][0]]
            en_keywords = [kw for kw in keywords if re.search(r"[A-Za-z]", kw)] + [CHAPTER_CONTEXT[chapter][1]]
            search_query_zh = f"{query_zh} {title}"
            search_query_en = f"{query_en} {CHAPTER_CONTEXT[chapter][1]}"
        else:
            zh_keywords = [title, CHAPTER_CONTEXT[chapter][0]]
            en_keywords = [CHAPTER_CONTEXT[chapter][1], "concept diagram"]
            search_query_zh = f"{CHAPTER_CONTEXT[chapter][0]} {title} 教学示意图"
            search_query_en = f"{CHAPTER_CONTEXT[chapter][1]} {title} concept diagram open educational resource"
        caption = f"{title}的教学示意图"
    else:
        zh_keywords, en_keywords = [], []
        search_query_zh, search_query_en, caption = "", "", ""

    return {
        "need_image": need_image,
        "image_priority": priority,
        "image_role": image_role,
        "image_type": image_type,
        "concept_keywords_zh": "；".join(dict.fromkeys([item for item in zh_keywords if item]))[:300],
        "concept_keywords_en": "; ".join(dict.fromkeys([item for item in en_keywords if item]))[:300],
        "search_query_zh": search_query_zh[:300],
        "search_query_en": search_query_en[:300],
        "suggested_caption_zh": caption[:120],
        "insertion_position": insertion_position,
        "layout_hint": layout_hint,
        "reason": reason,
        "notes": notes,
    }


def build():
    summary = []
    previews = {}
    for chapter, md_file, md_path in target_files():
        slides = split_marp(md_path.read_text(encoding="utf-8-sig"))
        rows = []
        for index, slide in enumerate(slides, 1):
            title = get_title(slide, index)
            existing_image = bool(IMAGE_RE.search(slide))
            info = classify(chapter, title, slide, existing_image)
            row = {
                "chapter": chapter,
                "md_file": md_file,
                "slide_id": index,
                "slide_title": title,
                "need_image": info["need_image"],
                "image_priority": info["image_priority"],
                "image_role": info["image_role"],
                "image_type": info["image_type"],
                "concept_keywords_zh": info["concept_keywords_zh"],
                "concept_keywords_en": info["concept_keywords_en"],
                "search_query_zh": info["search_query_zh"],
                "search_query_en": info["search_query_en"],
                "preferred_source_type": PREFERRED if info["need_image"] == "yes" else "",
                "avoid_source_type": AVOID if info["need_image"] == "yes" else "",
                "license_requirement": LICENSE_REQ if info["need_image"] == "yes" else "",
                "suggested_caption_zh": info["suggested_caption_zh"],
                "insertion_position": info["insertion_position"],
                "layout_hint": info["layout_hint"],
                "reason": info["reason"],
                "existing_image_detected": "yes" if existing_image else "no",
                "notes": info["notes"],
            }
            rows.append(row)

        out_path = OUT_DIR / f"image_need_{chapter}_text1.csv"
        with out_path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=HEADERS)
            writer.writeheader()
            writer.writerows(rows)

        yes_count = sum(1 for row in rows if row["need_image"] == "yes")
        summary.append(
            {
                "chapter": chapter,
                "md_file": md_file,
                "slide_count": len(rows),
                "yes_count": yes_count,
                "no_count": len(rows) - yes_count,
                "csv_path": str(out_path),
            }
        )
        previews[chapter] = rows[:10]

    errors = validate(summary)
    report = {"summary": summary, "errors": errors, "previews": previews}
    (OUT_DIR / "_generation_report_text1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"summary": summary, "errors": errors}, ensure_ascii=False, indent=2))


def validate(summary):
    errors = []
    for item in summary:
        chapter = item["chapter"]
        csv_path = Path(item["csv_path"])
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.DictReader(handle))
        if len(rows) != item["slide_count"]:
            errors.append(f"{chapter}: CSV row count mismatch")
        ids = [int(row["slide_id"]) for row in rows]
        if ids != list(range(1, len(rows) + 1)):
            errors.append(f"{chapter}: slide_id not continuous")
        bad_need = sorted(set(row["need_image"] for row in rows) - {"yes", "no"})
        if bad_need:
            errors.append(f"{chapter}: bad need_image {bad_need}")
        bad_priority = sorted(set(row["image_priority"] for row in rows) - {"high", "medium", "low", "none"})
        if bad_priority:
            errors.append(f"{chapter}: bad image_priority {bad_priority}")
        for row in rows:
            if row["need_image"] == "yes" and (not row["search_query_zh"] or not row["search_query_en"]):
                errors.append(f"{chapter}: missing search query at slide {row['slide_id']}")
                break
    return errors


if __name__ == "__main__":
    build()
