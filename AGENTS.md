# AGENTS.md

## Project

This repository is a Marp Markdown slide project for the course:

```text
《人工智能与大数据》
```

The current task family is:

```text
Generate image-need CSV files, curate teaching images, download non-AI-generated images, and prepare image manifests for later manual or scripted insertion into Marp Markdown slides.
```

Repository root on Windows:

```text
E:\machine_learning\markdown\AI-BigData-Course-Add-Figs-0
```

## Important directories

```text
AI-BigData-Course-Add-Figs-0/
├─ slides/
│  ├─ 第1章_人工智能大数据与材料科学概论_100页_Marp.md
│  ├─ 第2章_Python数据处理与材料数据预处理_100页_Marp.md
│  ├─ 第3章_贝叶斯定理与概率思维_100页_Marp.md
│  ├─ 第4章_机器学习与材料性能预测_100页_Marp.md
│  ├─ 第5章_深度学习多模态AI与显微组织识别_100页_Marp.md
│  ├─ 第6章_生成式AI大语言模型与提示工程_100页_Marp.md
│  ├─ 第7章_知识库知识图谱与检索增强生成RAG_100页_Marp.md
│  ├─ 第8章_AI代理主动学习与贝叶斯优化_100页_Marp.md
│  ├─ 第9章_大数据平台材料数据库与高通量材料设计_100页_Marp.md
│  └─ 第10章_可信AI数据安全与综合应用_100页_Marp.md
├─ image_need/
│  ├─ image_need_ch01_text1.csv
│  ├─ image_need_ch02_text1.csv
│  ├─ image_need_ch03_text1.csv
│  ├─ image_need_ch04_text1.csv
│  ├─ image_need_ch05_text1.csv
│  ├─ image_need_ch06_text1.csv
│  ├─ image_need_ch07_text1.csv
│  ├─ image_need_ch08_text1.csv
│  ├─ image_need_ch09_text1.csv
│  └─ image_need_ch10_text1.csv
├─ assets/
│  └─ downloaded/
│     ├─ ch01/text1/
│     ├─ ch02/text1/
│     ├─ ch03/text1/
│     ├─ ch04/text1/
│     ├─ ch05/text1/
│     ├─ ch06/text1/
│     ├─ ch07/text1/
│     ├─ ch08/text1/
│     ├─ ch09/text1/
│     └─ ch10/text1/
├─ am_template.scss
├─ am_green.scss
└─ .agents/
   └─ skills/
      └─ marp-image-curation/
         └─ SKILL.md
```

## Course chapter mapping

Use this exact chapter mapping:

```text
ch01 = 第1章_人工智能大数据与材料科学概论_100页_Marp.md
ch02 = 第2章_Python数据处理与材料数据预处理_100页_Marp.md
ch03 = 第3章_贝叶斯定理与概率思维_100页_Marp.md
ch04 = 第4章_机器学习与材料性能预测_100页_Marp.md
ch05 = 第5章_深度学习多模态AI与显微组织识别_100页_Marp.md
ch06 = 第6章_生成式AI大语言模型与提示工程_100页_Marp.md
ch07 = 第7章_知识库知识图谱与检索增强生成RAG_100页_Marp.md
ch08 = 第8章_AI代理主动学习与贝叶斯优化_100页_Marp.md
ch09 = 第9章_大数据平台材料数据库与高通量材料设计_100页_Marp.md
ch10 = 第10章_可信AI数据安全与综合应用_100页_Marp.md
```

## General working rules

1. Use Chinese for explanations, reports, CSV captions, and teaching notes.
2. Preserve all original Markdown slide files unless the user explicitly requests Markdown modification.
3. Do not modify files in `slides/` during image-need planning or image downloading.
4. Do not generate AI images.
5. Do not use AI-generated pictures from the web.
6. Do not download decorative images with weak teaching relevance.
7. Prefer authoritative and reusable sources.
8. Record source, license, attribution, and local path for every downloaded image.
9. Use deterministic scripts for parsing, validation, and manifest generation when possible.
10. Use UTF-8 or UTF-8 with BOM for CSV files so that Chinese text opens correctly in Excel on Windows.
11. Never fabricate downloaded file paths, image sources, licenses, or validation results.
12. If a source cannot be verified, mark the relevant field as `unknown` and include a review note.

## Marp parsing rules

When parsing Marp Markdown files:

1. The YAML front matter at the beginning of the file is not a slide.
2. A slide starts after the YAML front matter and is separated by a line containing only `---`.
3. Do not treat `---` inside fenced code blocks as slide separators.
4. `slide_id` starts from 1.
5. Every slide must be represented in the image-need CSV.
6. Extract the slide title from the first Markdown heading in the slide:

   * Prefer `#`
   * Then `##`
   * Then `###`
7. If no heading exists, infer a concise Chinese title from the slide content.
8. Detect existing images by checking:

   * Markdown image syntax: `![](...)`
   * HTML image tags: `<img ...>`
   * Marp background syntax: `![bg ...](...)`
   * local image references in HTML or Markdown

## Image planning policy

Mark `need_image=yes` only when an image materially improves instruction.

Good reasons for `need_image=yes`:

1. The slide introduces an abstract concept that benefits from visual explanation.
2. The slide describes a workflow, algorithm, model architecture, or data pipeline.
3. The slide discusses materials science, microstructure, phase diagrams, databases, or high-throughput design.
4. The slide would benefit from a real experimental, simulation, or software interface example.
5. The slide has too much abstract text and a compact visual can reduce cognitive load.

Good reasons for `need_image=no`:

1. Cover, agenda, transition, summary, or assignment page.
2. Existing image is already appropriate.
3. Slide is code-heavy and does not need a visual.
4. Slide is dense and adding an image would damage the 4:3 board-style layout.
5. Slide is a simple definition that can be explained verbally.

## Image source policy

Allowed image categories:

1. Conceptual schematic diagrams.
2. Algorithm workflow diagrams.
3. Experimental results.
4. Simulation results.
5. Materials microstructure images.
6. Database or software interface screenshots from official sources.
7. Open educational resources.
8. Open-access paper figures with clear license.
9. Wikimedia Commons images with license metadata.
10. Government, national laboratory, university, or official documentation images.

Forbidden image categories:

1. AI-generated images.
2. Midjourney, Stable Diffusion, DALL-E, or similar generated images.
3. Commercial stock images.
4. Watermarked images.
5. Images with unclear source.
6. Images with obvious copyright restrictions.
7. Low-resolution or visually ambiguous images.
8. Decorative images that do not improve teaching.
9. Duplicates across slides or chapters.

## Preferred sources

Prefer:

```text
official documentation
open-source project documentation
university open course material
government or national laboratory sources
Wikimedia Commons
open access journals with clear license
Materials Project
AFLOW
NOMAD
Matminer
Scikit-learn
PyTorch
TensorFlow
Hugging Face
Apache project documentation
Python scientific-computing documentation
```

Avoid:

```text
AI image galleries
stock photo sites
paywalled paper screenshots
commercial slide decks
Pinterest-style reposts
unattributed blog images
low-resolution thumbnails
images with watermarks
```

## File naming

Downloaded image names must follow:

```text
chXX_sYYY_rR_short-key.ext
```

Examples:

```text
ch03_s012_r1_bayes-theorem-diagram.png
ch05_s034_r1_cnn-microstructure-classification.jpg
ch08_s045_r1_bayesian-optimization-loop.png
ch09_s021_r1_materials-project-database.png
```

## CSV validation

For every CSV created or modified:

1. Validate column names and column order.
2. Validate row count.
3. Validate continuous `slide_id`.
4. Validate no empty required fields for `need_image=yes`.
5. Validate `need_image` values are only `yes` or `no`.
6. Validate `image_priority` values are only `high`, `medium`, `low`, or `none`.
7. Produce a summary report.

## Download validation

For every downloaded image:

1. Confirm the file exists.
2. Confirm file size is greater than 10 KB.
3. Confirm the image opens successfully.
4. Record width and height.
5. Compute SHA256.
6. Check for duplicates.
7. Check for obvious watermark.
8. Check for source and license.
9. Record source page URL and direct image URL.
10. If the image fails validation, delete it or mark it as failed.

## Completion criteria

A task is complete only when:

1. The requested output files exist.
2. The output paths match the project structure.
3. Validation results are reported.
4. No prohibited Markdown files were modified.
5. No AI-generated images were downloaded.
6. Downloaded image metadata and attribution are recorded.
7. Any uncertain license or image-quality problem is explicitly listed for manual review.

## Reporting style

Final responses should be concise but complete. Include:

1. What was created.
2. Where it was saved.
3. What was not changed.
4. Validation summary.
5. Items requiring manual review.

Use Chinese in final reports.
