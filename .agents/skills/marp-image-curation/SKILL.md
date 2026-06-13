---

name: marp-image-curation
description: Use this skill when generating image-need CSV files, searching for non-AI-generated teaching images, downloading images, deduplicating images, validating image quality, and preparing attribution manifests for Chinese Marp Markdown course slides.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Marp Image Curation Skill

## Purpose

This skill supports a two-stage workflow for adding appropriate teaching images to Chinese Marp Markdown slides:

1. Stage 1: Generate image-need CSV files only.
2. Stage 2: Download non-AI-generated images according to reviewed CSV files and generate manifests.

This skill is designed for the course:

```text
《人工智能与大数据》
```

Project root:

```text
E:\machine_learning\markdown\AI-BigData-Course-Add-Figs-0
```

## Hard constraints

Always follow these constraints:

1. Do not modify Markdown slide files unless the user explicitly asks for insertion.
2. Do not generate AI images.
3. Do not download AI-generated images.
4. Do not download decorative images with weak teaching value.
5. Do not download duplicate images.
6. Do not fabricate source URLs, licenses, attributions, dimensions, SHA256 hashes, or file paths.
7. Do not skip slides when generating image-need CSV files.
8. Do not treat YAML front matter as slide content.
9. Do not treat `---` inside fenced code blocks as Marp slide delimiters.
10. Use UTF-8 or UTF-8 with BOM for CSV outputs containing Chinese.

## Stage 1: Image-need CSV generation

### Input

Read these files from `slides/`:

```text
第1章_人工智能大数据与材料科学概论_100页_Marp.md
第2章_Python数据处理与材料数据预处理_100页_Marp.md
第3章_贝叶斯定理与概率思维_100页_Marp.md
第4章_机器学习与材料性能预测_100页_Marp.md
第5章_深度学习多模态AI与显微组织识别_100页_Marp.md
第6章_生成式AI大语言模型与提示工程_100页_Marp.md
第7章_知识库知识图谱与检索增强生成RAG_100页_Marp.md
第8章_AI代理主动学习与贝叶斯优化_100页_Marp.md
第9章_大数据平台材料数据库与高通量材料设计_100页_Marp.md
第10章_可信AI数据安全与综合应用_100页_Marp.md
```

### Output

Generate:

```text
image_need/image_need_ch01_text1.csv
image_need/image_need_ch02_text1.csv
image_need/image_need_ch03_text1.csv
image_need/image_need_ch04_text1.csv
image_need/image_need_ch05_text1.csv
image_need/image_need_ch06_text1.csv
image_need/image_need_ch07_text1.csv
image_need/image_need_ch08_text1.csv
image_need/image_need_ch09_text1.csv
image_need/image_need_ch10_text1.csv
```

### CSV schema

Use this exact column order:

```csv
chapter,md_file,slide_id,slide_title,need_image,image_priority,image_role,image_type,concept_keywords_zh,concept_keywords_en,search_query_zh,search_query_en,preferred_source_type,avoid_source_type,license_requirement,suggested_caption_zh,insertion_position,layout_hint,reason,existing_image_detected,notes
```

### Slide parsing method

1. Read the Markdown file as UTF-8.
2. Detect and remove YAML front matter only if the file starts with `---`.
3. Split slides using a line that contains exactly `---`, after excluding fenced code blocks.
4. Assign `slide_id` from 1.
5. Extract the first heading as `slide_title`.
6. Detect existing image references.
7. Generate exactly one CSV row per slide.

### Decision policy

Use `need_image=yes` when:

1. A visual would clarify a difficult concept.
2. A workflow or model architecture is discussed.
3. A mathematical or probabilistic idea benefits from a diagram.
4. The slide concerns materials data, microstructure, phase diagrams, simulation, databases, or high-throughput design.
5. The slide introduces RAG, knowledge graph, AI Agent, active learning, or Bayesian optimization.

Use `need_image=no` when:

1. The slide is a cover, agenda, transition, summary, or assignment page.
2. Existing images are already suitable.
3. The slide is code-heavy and does not require a visual.
4. The slide is too dense for additional figures.
5. The concept is simple enough for text explanation.

### Query design

For `need_image=yes`, provide:

1. Chinese query.
2. English query.
3. Chinese keywords.
4. English keywords.
5. Preferred source type.
6. Avoided source type.
7. Suggested Chinese caption.

Queries must be specific. Avoid generic queries such as:

```text
AI picture
big data image
machine learning image
```

Prefer specific queries such as:

```text
Bayes theorem conditional probability diagram
materials informatics workflow microstructure property prediction
retrieval augmented generation workflow vector database diagram
Bayesian optimization active learning loop surrogate model acquisition function
```

### Stage 1 validation

After writing CSV files:

1. Confirm every CSV exists.
2. Confirm slide IDs are continuous.
3. Confirm row count equals slide count.
4. Confirm `need_image` only contains `yes` or `no`.
5. Confirm `image_priority` only contains `high`, `medium`, `low`, or `none`.
6. Confirm no image files were downloaded.
7. Confirm no Markdown files were modified.
8. Print a chapter-level summary.

## Stage 2: Image download and manifest generation

### Input

Read reviewed CSV files from:

```text
image_need/
```

Only process rows with:

```text
need_image=yes
```

### Output directories

Download images to:

```text
assets/downloaded/ch01/text1/
assets/downloaded/ch02/text1/
assets/downloaded/ch03/text1/
assets/downloaded/ch04/text1/
assets/downloaded/ch05/text1/
assets/downloaded/ch06/text1/
assets/downloaded/ch07/text1/
assets/downloaded/ch08/text1/
assets/downloaded/ch09/text1/
assets/downloaded/ch10/text1/
```

### Manifest outputs

Generate:

```text
assets/downloaded/image_download_manifest_text1.csv
assets/downloaded/duplicate_check_text1.csv
assets/downloaded/ch01/text1/manifest_ch01_text1.csv
assets/downloaded/ch02/text1/manifest_ch02_text1.csv
assets/downloaded/ch03/text1/manifest_ch03_text1.csv
assets/downloaded/ch04/text1/manifest_ch04_text1.csv
assets/downloaded/ch05/text1/manifest_ch05_text1.csv
assets/downloaded/ch06/text1/manifest_ch06_text1.csv
assets/downloaded/ch07/text1/manifest_ch07_text1.csv
assets/downloaded/ch08/text1/manifest_ch08_text1.csv
assets/downloaded/ch09/text1/manifest_ch09_text1.csv
assets/downloaded/ch10/text1/manifest_ch10_text1.csv
```

### Manifest schema

Use this exact column order for `image_download_manifest_text1.csv`:

```csv
chapter,md_file,slide_id,slide_title,need_image,candidate_rank,download_status,local_path,relative_path,file_name,file_ext,file_size_bytes,width_px,height_px,sha256,source_page_url,direct_image_url,source_title,source_author,source_license,attribution_text,search_query_used,image_role,image_type,caption_zh,layout_hint,duplicate_of,quality_notes
```

Allowed `download_status` values:

```text
downloaded
reused_duplicate
not_found
skipped_existing_image
failed
```

### Source preference

Prefer:

1. Official documentation.
2. University open course material.
3. Wikimedia Commons.
4. Government or national laboratory websites.
5. Open-source project documentation.
6. Open-access paper figures with clear licenses.
7. Official database screenshots or documentation.

Avoid:

1. AI-generated image galleries.
2. Stock photo sites.
3. Watermarked commercial images.
4. Paywalled copyrighted paper figures.
5. Unattributed blog reposts.
6. Low-resolution thumbnails.
7. Social media reposts.

### AI-generated image exclusion

Before accepting an image, check whether the source page or image metadata suggests:

```text
AI generated
generated by AI
Midjourney
Stable Diffusion
DALL-E
DALL·E
synthetic image
prompt-generated
text-to-image
```

If any of these indicators appear, reject the image.

### Download quantity

1. Download one primary image per `need_image=yes` row.
2. For complex synthesis slides, a second candidate is allowed.
3. Do not download images for rows marked `need_image=no`.
4. If no appropriate image is found, write a manifest row with `download_status=not_found`.

### File naming

Use:

```text
chXX_sYYY_rR_short-key.ext
```

Examples:

```text
ch03_s012_r1_bayes-theorem-diagram.png
ch05_s034_r1_cnn-microstructure-classification.jpg
ch07_s041_r1_rag-vector-database-workflow.png
ch08_s045_r1_bayesian-optimization-loop.png
ch09_s021_r1_materials-project-database.png
```

### Deduplication

Perform global deduplication across all chapters.

Minimum deduplication requirements:

1. Normalize URLs.
2. Avoid downloading the same direct image URL twice.
3. Compute SHA256 after download.
4. If SHA256 duplicates exist, keep the first file and reuse its relative path.
5. If the same image appears in multiple sizes, keep the higher-resolution version.
6. Record duplicates in `duplicate_check_text1.csv`.

### Image validation

For each downloaded image:

1. Confirm file exists.
2. Confirm file size is greater than 10 KB.
3. Open the image using a local image library or browser-compatible check.
4. Record width and height.
5. Record SHA256.
6. Reject unreadable images.
7. Reject images with obvious watermark.
8. Mark low-resolution images in `quality_notes`.
9. Mark unclear license as `source_license=unknown`.
10. Mark uncertain relevance as `low confidence`.

### Attribution

For each image, record:

1. Source page URL.
2. Direct image URL.
3. Source title.
4. Author or organization.
5. License.
6. Attribution text.

Attribution text should be directly reusable in a slide reference page.

Example attribution format:

```text
Image source: [source title], author/organization, license, source page URL.
```

For Chinese reports, also provide a concise Chinese explanation in `quality_notes` when needed.

## Recommended script structure

When helpful, create temporary utility scripts under:

```text
tools/
```

Recommended scripts:

```text
tools/parse_marp_slides.py
tools/validate_image_need_csv.py
tools/download_images_from_image_need.py
tools/validate_downloaded_images.py
```

Do not create unnecessarily complex frameworks. Keep scripts small, readable, and well-commented.

## Final report requirements

For Stage 1, report:

1. CSV files created.
2. Slide counts per chapter.
3. `need_image=yes` counts per chapter.
4. Validation results.
5. Confirmation that no images were downloaded.
6. Confirmation that Markdown files were not modified.

For Stage 2, report:

1. Downloaded count per chapter.
2. Reused duplicate count per chapter.
3. Not-found count per chapter.
4. Failed count per chapter.
5. Manifest path.
6. Duplicate-check path.
7. Items requiring manual review.
8. Confirmation that Markdown files were not modified.
