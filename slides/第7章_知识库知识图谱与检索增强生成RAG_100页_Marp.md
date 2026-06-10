---
marp: true
size: 4:3
theme: am_green
paginate: true
math: katex
author: Shiyan Pan
class: navbar
header: '**第7章** *知识库* *知识图谱* *向量检索* *RAG流程* *实验室知识* *可靠性*'
footer: '《人工智能与大数据》 | 第7章'
style: |
  /* ============================================================
     第7章局部排版：基于 am_template.scss + am_green.scss。
     目标：4:3 教学课件；避免长 header 溢出；公式、表格、代码可读。
     ============================================================ */
  section { line-height: 1.34; }
  section.course_cover {
    background: linear-gradient(180deg, var(--color-coverbg) 0 58%, #ffffff 58% 100%);
    text-align: center; overflow: hidden;
  }
  section.course_cover h1 {
    position: absolute; left: 5%; right: 5%; top: 10%; width: 90%;
    margin: 0; padding: 0; color: var(--color-title); background: transparent;
    font-size: 42px; line-height: 1.13; letter-spacing: 1px; white-space: normal;
  }
  section.course_cover h6 {
    position: absolute; left: 8%; right: 8%; top: 42%; width: 84%;
    margin: 0; padding: 0; color: var(--color-title); background: transparent;
    font-size: 25px; line-height: 1.20; white-space: normal;
  }
  section.course_cover .cover-meta {
    position: absolute; left: 12%; right: 12%; bottom: 20%;
    margin: 0; padding: 17px 22px; color: var(--color-main);
    background: rgba(255,255,255,0.94); border-radius: 14px;
    box-shadow: 0 8px 24px rgba(32,60,54,0.13);
    font-size: 22px; line-height: 1.52; text-align: left;
  }
  section.course_cover .cover-author {
    position: absolute; left: 0; right: 0; bottom: 8%; color: var(--color-main);
    font-size: 24px; text-align: center;
  }
  section.course_cover header, section.course_cover footer, section.course_cover::after { display: none; }

  section.navbar header {
    height: 42px; padding: 6px 28px 4px 28px; box-sizing: border-box;
    align-items: center; justify-content: space-around; overflow: hidden;
  }
  section.navbar header>em, section.navbar header>strong, section.navbar header>em>strong {
    font-size: 0.78rem; line-height: 1.15; white-space: nowrap;
  }
  section.navbar header>strong { padding: 2px 14px 4px 14px; border-radius: 12px; }

  section.course_toc header {
    font-size: 440%; line-height: 118px; top: 16px; left: 0;
    opacity: 0.12; z-index: 0; pointer-events: none;
  }
  section.course_toc h2, section.course_toc ul, section.course_toc blockquote { position: relative; z-index: 2; }
  section.course_toc h2 { margin-top: 0.25rem; font-size: 40px; }
  section.course_toc ul { margin-top: 20px; }
  section.course_toc li { font-size: 25px; line-height: 1.40; }
  section.course_toc blockquote { margin-top: 24px; font-size: 21px; }

  section.trans h2 { font-size: 42px; }
  section.compact h2 { font-size: 31px; }
  section.compact h3 { font-size: 24px; }
  section.compact p, section.compact li { font-size: 21px; line-height: 1.30; }
  section.compact table { font-size: 17px; line-height: 1.18; }
  section.compact pre { font-size: 17px; line-height: 1.17; }
  section.formula p, section.formula li { font-size: 22px; }
  section.formula .katex-display { font-size: 0.96em; }
  section.codepage pre { font-size: 16px; line-height: 1.15; }
  section.codepage p, section.codepage li { font-size: 21px; }
  section.tight table { font-size: 16px; }
  section.tight li, section.tight p { font-size: 20px; }
  .note { background: rgba(244,250,247,0.95); border-left: 6px solid var(--color-main); padding: 10px 16px; border-radius: 8px; }
  .warn { background: rgba(255,246,238,0.95); border-left: 6px solid #d78634; padding: 10px 16px; border-radius: 8px; }
  .small { font-size: 0.82em; }
  .two { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .three { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; }
---

<!-- _class: course_cover -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
# 第7章 知识库、知识图谱与检索增强生成（RAG）
###### Knowledge Base, Knowledge Graph and Retrieval-Augmented Generation

<div class="cover-meta">
学习路径：知识表示 → 专家系统 → 知识图谱 → 文本嵌入 → 向量数据库 → RAG流程 → 材料文献知识库 → 证据追踪与可靠性评价
</div>

<div class="cover-author">@Shiyan Pan</div>

---

<!-- _class: toc_a fglass course_toc -->
<!-- _header: "CONTENTS" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 目录

- 7.1 知识表示、专家系统与知识工程
- 7.2 知识图谱：实体、关系、属性与推理 △
- 7.3 向量数据库、文本嵌入与相似性检索
- 7.4 RAG基本流程：切分、嵌入、检索、重排、生成 △★
- 7.5 材料文献知识库与实验室知识管理
- 7.6 知识库回答的证据追踪与可靠性评价 ★

> 主线：先把知识组织起来，再让模型在证据约束下回答问题。

---

## 本章学习目标

- 区分数据、信息、知识与知识库。
- 理解专家系统、知识工程与现代知识库的联系。
- 掌握知识图谱中实体、关系、属性、三元组与推理的基本概念。
- 理解文本嵌入、向量数据库与相似性检索的基本数学表达。
- 掌握 RAG 的典型流程：切分、嵌入、检索、重排、生成。
- 能设计材料文献知识库和实验室知识管理的基本方案。
- 能从证据追踪、引用核验和可靠性评价角度审查知识库回答。

---

<!-- _class: compact -->
## 本章知识梯度

| 层级 | 关键问题 | 对应能力 |
|---|---|---|
| 概念 | 什么是知识？ | 区分数据、信息、知识、证据 |
| 表示 | 知识如何让计算机处理？ | 规则、语义网络、三元组 |
| 结构 | 如何描述材料实体关系？ | 知识图谱建模 |
| 检索 | 如何从文献中找相关片段？ | 嵌入、相似度、向量库 |
| 生成 | 如何让 LLM 基于证据回答？ | RAG流水线设计 |
| 可信 | 如何判断回答可靠？ | 溯源、核验、评估 |

---

<!-- _class: compact -->
## 第7章内容安排总览

| 节 | 教学定位 | 由易到难的安排 |
|---|---|---|
| 7.1 | 知识表示与专家系统 | 从规则到知识工程流程 |
| 7.2 | 知识图谱 | 从实体关系到图谱推理 |
| 7.3 | 文本嵌入与向量库 | 从词袋到语义向量检索 |
| 7.4 | RAG基本流程 | 从文档切分到答案生成 |
| 7.5 | 材料知识库 | 从文献管理到实验室知识管理 |
| 7.6 | 可靠性评价 | 从证据追踪到人工审核 |

---

## 为什么第7章安排在第6章之后？

第6章讨论生成式 AI 和大语言模型，核心问题是：

- 大模型可以生成流畅文本；
- 但未必知道课程、实验室和最新文献中的具体事实；
- 也可能生成不存在的引用和错误结论。

第7章给出一种工程化补救路径：

```text
外部知识库 + 检索 + 证据片段 + 大模型生成 + 人类审核
```

<div class="note">RAG不是让模型“更聪明”，而是让模型在回答时接入可追踪证据。</div>

---

<!-- _class: compact -->
## 数据、信息、知识、智慧

| 层级 | 含义 | 材料科学例子 |
|---|---|---|
| 数据 | 原始记录 | 成分、温度、时间、强度值 |
| 信息 | 经过整理的数据 | 某批样品在不同热处理下的强度表 |
| 知识 | 可解释、可复用的规律 | 固溶处理提高元素均匀性 |
| 智慧 | 面向目标的判断 | 针对目标强度选择热处理窗口 |

<div class="warn">知识库建设的关键不是“存得多”，而是“可查、可解释、可验证”。</div>

---

<!-- _class: trans -->
## 7.1 知识表示、专家系统与知识工程

本节从三个问题展开：

1. 知识如何形式化？
2. 专家系统如何利用规则进行推理？
3. 为什么知识工程仍然是 RAG 和知识图谱的基础？

> 学习重点：理解知识表示不是简单保存文本，而是把知识组织成机器可处理的结构。

---

## 7.1 的学习任务

- 认识知识表示的基本目标：表达事实、规则、约束和不确定性。
- 理解产生式规则、框架、语义网络和本体的差异。
- 了解专家系统的组成：知识库、推理机、解释模块、人机接口。
- 理解知识工程流程：获取、表示、验证、维护、更新。

<div class="note">材料领域中的相图规则、工艺规范、失效判据、实验流程均可看作领域知识。</div>

---

## 什么是知识表示？

知识表示是将人类可理解的知识转化为计算机可处理形式的过程。

常见表示对象包括：

- 事实：材料 A 的屈服强度为 850 MPa；
- 关系：时效温度影响析出相尺寸；
- 规则：若碳当量较高，则焊接冷裂纹风险增加；
- 约束：成分含量之和应接近 100%；
- 不确定性：某组织识别结果的置信度为 0.82。

---

<!-- _class: compact -->
## 知识表示的基本要求

| 要求 | 说明 | 材料场景 |
|---|---|---|
| 可表达性 | 能表示领域事实和规则 | 成分—工艺—组织—性能 |
| 可计算性 | 能被算法检索和推理 | 查询合金强度影响因素 |
| 可维护性 | 可更新、可扩展 | 新论文、新实验加入 |
| 可解释性 | 能说明结论来源 | 回答必须给出文献页码 |
| 一致性 | 避免同一术语多种含义 | UTS、抗拉强度统一 |

---

<!-- _class: formula -->
## 产生式规则

产生式规则常写为：

$$
\text{IF condition THEN action}
$$

材料示例：

```text
IF Cr_eq / Ni_eq 较高 AND 冷却速率较大
THEN 焊缝中铁素体倾向增强
```

优点：

- 易理解；
- 易解释；
- 适合专家经验明确的场景。

不足：

- 难以覆盖连续复杂变量；
- 规则冲突和规则维护成本较高。

---

<!-- _class: compact -->
## 框架表示

框架表示把对象看作由属性槽组成的结构。

材料样品框架示例：

| 槽 | 值 |
|---|---|
| 材料 | 316L 不锈钢 |
| 工艺 | 激光选区熔化 |
| 激光功率 | 250 W |
| 扫描速度 | 900 mm/s |
| 组织 | 细胞状枝晶 |
| 性能 | 抗拉强度 620 MPa |

<div class="note">框架表示适合实验记录、样品档案和材料数据库表结构设计。</div>

---

## 语义网络

语义网络用节点和边表示概念及其关系。

```text
316L不锈钢 ──属于── 奥氏体不锈钢
激光功率 ──影响── 熔池温度
熔池温度 ──影响── 冷却速率
冷却速率 ──影响── 枝晶间距
枝晶间距 ──影响── 强度
```

语义网络为知识图谱提供了直观基础。

<div class="warn">如果只画关系图而不定义实体类型、关系语义和数据来源，图谱很难复用。</div>

---

## 本体：概念层面的约束

本体用于规定领域概念、层级和关系约束。

材料领域本体可以规定：

- `Material` 是材料实体；
- `Process` 是加工工艺；
- `Property` 是性能指标；
- `hasComposition` 连接材料与成分；
- `hasProperty` 连接材料与性能；
- `obtainedBy` 连接样品与工艺。

<div class="note">本体解决的是“同一类知识应如何命名、组织和连接”的问题。</div>

---

## 专家系统的基本结构

```text
用户问题
   ↓
人机接口
   ↓
推理机 ←→ 知识库
   ↓
解释模块
   ↓
结论与依据
```

专家系统强调：

- 知识显式存放；
- 推理过程可解释；
- 适合规则明确、领域边界清晰的任务。

---

<!-- _class: compact -->
## 专家系统与机器学习的差异

| 维度 | 专家系统 | 机器学习 |
|---|---|---|
| 知识来源 | 专家规则 | 数据样本 |
| 表达形式 | 规则、逻辑、本体 | 参数、权重、模型 |
| 可解释性 | 通常较强 | 依模型而定 |
| 适用问题 | 规则明确、样本少 | 数据较多、模式复杂 |
| 维护方式 | 修改规则 | 重新训练或微调 |

二者并非对立：现代材料 AI 系统常常同时使用规则、数据库和学习模型。

---

## 知识工程流程

```text
领域问题定义
    ↓
知识获取：文献、专家、标准、实验记录
    ↓
知识建模：实体、属性、关系、规则
    ↓
知识存储：关系库、图数据库、向量库
    ↓
知识验证：一致性、准确性、可追踪性
    ↓
知识维护：版本、更新、权限、审计
```

<div class="note">RAG项目失败的常见原因不是模型太弱，而是知识工程不规范。</div>

---

<!-- _class: compact -->
## 材料知识工程的典型对象

| 对象 | 例子 | 结构化难点 |
|---|---|---|
| 文献 | 论文、综述、专利 | PDF结构复杂、图表信息多 |
| 实验记录 | 样品编号、炉次、参数 | 命名不统一、缺失严重 |
| 计算结果 | DFT、MD、相场、有限元 | 单位、网格、边界条件多样 |
| 图像 | SEM、EBSD、TEM | 标尺、倍率、通道、标签 |
| 谱图 | XRD、EDS、拉曼 | 峰位、背景、噪声、归一化 |

---

## 7.1 小结

- 知识表示解决“知识如何被机器处理”的问题。
- 专家系统体现了早期 AI 的知识驱动思想。
- 知识工程强调知识获取、建模、验证和维护。
- 现代 RAG、知识图谱和实验室知识库仍然离不开知识工程。

> 下一节：把知识表示进一步组织为“实体—关系—属性”的知识图谱。

---

<!-- _class: trans -->
## 7.2 知识图谱：实体、关系、属性与推理 △

知识图谱将知识组织为图结构。

最基本的表达是三元组：

$$
(h, r, t)
$$

其中：

- $h$ 表示头实体；
- $r$ 表示关系；
- $t$ 表示尾实体。

例：`(316L, contains, Cr)`。

---

## 7.2 的学习任务

- 理解实体、关系、属性、三元组的含义。
- 能把材料文本转化为简单图谱结构。
- 理解图谱模式层与实例层的差异。
- 了解图谱查询、路径推理和规则推理。
- 能说明知识图谱与向量检索在 RAG 中的互补作用。

---

<!-- _class: compact -->
## 实体、关系与属性

| 元素 | 含义 | 材料例子 |
|---|---|---|
| 实体 | 可被识别和引用的对象 | 合金、元素、相、工艺、性能 |
| 关系 | 实体之间的语义连接 | contains、improves、causes |
| 属性 | 实体自身的数值或标签 | 熔点、晶格常数、强度 |
| 证据 | 支撑该知识的来源 | 论文、表格、实验记录 |

<div class="note">材料知识图谱不能只存关系，还应存证据来源和单位。</div>

---

<!-- _class: formula -->
## 三元组表示

典型三元组：

$$
\text{Material} \xrightarrow{\text{hasProperty}} \text{Property}
$$

示例：

```text
(316L, hasElement, Cr)
(316L, hasElement, Ni)
(LaserPower, affects, MeltPoolTemperature)
(MeltPoolTemperature, affects, CoolingRate)
(CoolingRate, affects, DendriteArmSpacing)
```

这些三元组可组合为图。

---

<!-- _class: compact -->
## 模式层与实例层

| 层级 | 作用 | 例子 |
|---|---|---|
| 模式层 | 定义类和关系 | Material、Process、Property |
| 实例层 | 存储具体事实 | Sample_001、316L、620 MPa |

模式层示例：

```text
Material --hasComposition--> Composition
Process --hasParameter--> ProcessParameter
Material --hasProperty--> Property
```

实例层示例：

```text
Sample_001 --hasProperty--> UTS_620MPa
```

---

<!-- _class: formula -->
## RDF三元组思想

RDF 的核心思想是用主语、谓语、宾语构成图。

$$
\text{subject} \quad \text{predicate} \quad \text{object}
$$

材料示例：

```text
Sample_001  hasMaterial  316L
Sample_001  processedBy  SLM
SLM         hasParameter LaserPower
LaserPower  hasValue     250W
```

<div class="note">RDF强调语义互联，适合跨数据库、跨文献、跨实验室的知识共享。</div>

---

<!-- _class: compact -->
## 图数据库与关系数据库的差异

| 维度 | 关系数据库 | 图数据库 |
|---|---|---|
| 核心结构 | 表 | 节点与边 |
| 优势 | 规范表格、事务管理 | 关系查询、路径分析 |
| 典型查询 | 筛选、连接、聚合 | 邻居、路径、子图 |
| 材料应用 | 成分—性能表 | 成分—工艺—组织—性能网络 |

二者可以共存：结构化数值表适合关系库，复杂关联知识适合图数据库。

---

## 知识图谱构建流程

```text
确定应用问题
    ↓
设计本体与数据模式
    ↓
抽取实体、关系、属性
    ↓
实体消歧与单位统一
    ↓
图谱入库
    ↓
查询、推理、可视化
    ↓
人工审核与版本更新
```

<div class="warn">图谱构建不是一次性工作，而是持续维护的知识工程过程。</div>

---

<!-- _class: compact -->
## 实体抽取：从文本到结构

原始文本：

> 250 W 激光功率下，316L 不锈钢样品的熔池更深，抗拉强度达到 620 MPa。

可能抽取为：

| 类型 | 实体 |
|---|---|
| 材料 | 316L 不锈钢 |
| 工艺参数 | 激光功率 250 W |
| 组织/几何 | 熔池深度 |
| 性能 | 抗拉强度 620 MPa |

---

## 关系抽取：从句子到边

从同一句话中可以抽取：

```text
(激光功率, affects, 熔池深度)
(316L不锈钢, hasProperty, 抗拉强度)
(样品, hasProcessParameter, 250W)
```

但需要注意：

- “影响”是否为因果关系？
- 是否只在特定条件下成立？
- 是否有对照实验支撑？
- 文献中是否给出误差范围？

<div class="warn">关系抽取不能把相关性直接写成因果性。</div>

---

<!-- _class: compact -->
## 实体对齐与消歧

同一概念可能有多种写法：

| 表达 | 可能统一为 |
|---|---|
| 316L、SS316L、AISI 316L | 316L stainless steel |
| UTS、ultimate tensile strength | 抗拉强度 |
| LPBF、SLM、PBF-LB/M | 激光粉末床熔融 |
| γ 相、奥氏体、austenite | Austenite |

<div class="note">实体对齐是材料知识库质量的基础。</div>

---

<!-- _class: compact -->
## 单位统一与属性规范

材料属性必须记录单位和测试条件。

| 属性 | 不完整写法 | 规范写法 |
|---|---|---|
| 强度 | 620 | 620 MPa，室温拉伸 |
| 温度 | 900 | 900 °C，保温 1 h |
| 成分 | Cr 18 | Cr 18 wt.% |
| 速度 | 900 | 900 mm/s |

<div class="warn">没有单位和条件的数值不能直接进入可靠知识库。</div>

---

## 图谱查询：邻居查询

问题：哪些工艺参数会影响材料强度？

```text
Strength
  ↑ affectedBy
Microstructure
  ↑ affectedBy
CoolingRate
  ↑ affectedBy
LaserPower, ScanSpeed, LayerThickness
```

查询结果不仅给出实体列表，还能给出路径。

这比普通关键词搜索更适合回答“影响链条”类问题。

---

## 图谱推理：路径推理

若图谱中有：

```text
LaserPower affects MeltPoolTemperature
MeltPoolTemperature affects CoolingRate
CoolingRate affects DendriteArmSpacing
DendriteArmSpacing affects Strength
```

则可形成候选推理链：

```text
LaserPower → MeltPoolTemperature → CoolingRate → DendriteArmSpacing → Strength
```

<div class="note">路径推理给出的是候选解释，仍需实验或文献证据验证。</div>

---

<!-- _class: formula -->
## 图谱推理：规则推理

规则示例：

$$
\begin{aligned}
& (x, \text{isA}, \text{AusteniticStainlessSteel}) \\
& (x, \text{contains}, \text{Cr}) \\
& \Rightarrow (x, \text{hasCorrosionResistance}, \text{High})
\end{aligned}
$$

该规则必须限定条件：

- Cr 含量范围；
- 介质环境；
- 热处理状态；
- 是否存在敏化或析出。

---

## 知识图谱在材料科学中的价值

- 整合分散文献、实验记录和数据库。
- 追踪材料设计中的因果链和证据链。
- 支持问答、推荐、溯源和反事实分析。
- 为 RAG 提供结构化检索通道。
- 与机器学习模型结合形成“知识约束 AI”。

<div class="note">知识图谱适合回答“谁与谁有关、关系路径是什么、证据在哪里”。</div>

---

## 知识图谱的局限

- 构建成本较高，需要领域知识和人工审核。
- 文献中的隐含条件难以完整抽取。
- 图谱更新和版本管理复杂。
- 模糊、不确定和矛盾知识难以简单表示。
- 对连续数值模型的表达能力有限。

因此，实际系统常采用：

```text
知识图谱 + 向量检索 + 关系数据库 + 大语言模型
```

---

## 7.2 小结

- 知识图谱以实体、关系、属性构成结构化知识网络。
- 三元组是最基本的图谱表达单元。
- 材料图谱必须重视单位、测试条件、来源和证据。
- 图谱推理可以形成候选解释，但不能替代科学验证。
- 下一节进入向量数据库与文本嵌入，用于处理非结构化文献。

---

<!-- _class: trans -->
## 7.3 向量数据库、文本嵌入与相似性检索

知识图谱适合结构化关系。

但大量材料知识存在于：

- PDF正文；
- 图表说明；
- 实验记录；
- 专利文本；
- 会议报告。

本节讨论如何把文本转化为向量，并进行语义检索。

---

## 7.3 的学习任务

- 理解关键词检索与语义检索的区别。
- 掌握词袋、TF-IDF 和文本嵌入的基本思想。
- 理解余弦相似度、向量索引和近似最近邻检索。
- 能说明向量数据库在 RAG 中的作用。
- 能用 Python 构建一个最小语义检索示例。

---

## 关键词检索的特点

关键词检索关注字面匹配。

优点：

- 实现简单；
- 可解释性强；
- 适合精确术语查询。

局限：

- 同义词难以匹配；
- 语义相近但词不同的文本可能漏检；
- 不容易处理复杂自然语言问题。

材料例子：查询“激光粉末床熔融”时，可能漏掉“LPBF”“PBF-LB/M”“SLM”。

---

<!-- _class: formula -->
## 词袋模型

词袋模型把文本表示为词频向量。

$$
\mathbf{x}_d = [c_1, c_2, \cdots, c_m]
$$

其中：

- $d$ 表示文档；
- $m$ 表示词表大小；
- $c_i$ 表示第 $i$ 个词在文档中出现的次数。

优点是简单，缺点是忽略词序和上下文语义。

---

<!-- _class: formula -->
## TF-IDF 表示

TF-IDF 用于提高“有区分度词语”的权重。

$$
\text{tfidf}(t,d)=\text{tf}(t,d)\cdot \text{idf}(t)
$$

$$
\text{idf}(t)=\log \frac{N}{1+n_t}
$$

其中：

- $N$ 为文档总数；
- $n_t$ 为包含词 $t$ 的文档数。

常见词权重低，特征词权重高。

---

<!-- _class: formula -->
## BM25 的基本思想

BM25 是经典稀疏检索方法。

核心思想：

- 查询词出现越多，相关性越高；
- 但词频收益递减；
- 文档长度需要归一化；
- 稀有词通常更重要。

简化表达：

$$
\text{score}(q,d)=\sum_{t\in q}\text{idf}(t)\cdot f(t,d)
$$

BM25 适合关键词明确的技术文档检索。

---

<!-- _class: formula -->
## 文本嵌入：从词频到语义向量

文本嵌入将文本映射为连续向量：

$$
\mathbf{z}=f_{\theta}(\text{text}) \in \mathbb{R}^{p}
$$

语义相近的文本在向量空间中距离更近。

示例：

```text
“激光粉末床熔融”
“LPBF”
“selective laser melting”
```

这些表达的字面形式不同，但可能具有相近嵌入向量。

---

## 嵌入向量的直观理解

向量空间中的方向可表示语义。

```text
文本 A：316L laser powder bed fusion tensile strength
文本 B：SLM stainless steel mechanical properties
文本 C：XRD peak fitting of alumina powder
```

A 和 B 在语义空间中应更接近。

<div class="note">嵌入模型的质量直接影响 RAG 的检索质量。</div>

---

<!-- _class: formula -->
## 余弦相似度

常用相似度指标为余弦相似度：

$$
\cos(\mathbf{x},\mathbf{y})=
\frac{\mathbf{x}\cdot\mathbf{y}}{\|\mathbf{x}\|_2\|\mathbf{y}\|_2}
$$

取值范围通常为 $[-1,1]$。

- 越接近 1，方向越相似；
- 越接近 0，语义相关性较弱；
- 负值表示方向相反。

---

<!-- _class: compact -->
## 欧氏距离与余弦相似度

| 指标 | 关注点 | 适用情况 |
|---|---|---|
| 欧氏距离 | 向量之间的绝对距离 | 数值尺度有意义时 |
| 余弦相似度 | 向量方向 | 文本嵌入、语义检索 |
| 点积 | 方向与长度共同作用 | 归一化或模型指定时 |

在很多文本检索任务中，向量方向比向量长度更重要。

---

## 向量数据库的作用

向量数据库负责存储和检索嵌入向量。

```text
文档片段 → 嵌入向量 → 向量库
用户问题 → 嵌入向量 → 相似性搜索 → 相关片段
```

它通常提供：

- 向量写入与删除；
- 相似性检索；
- 元数据过滤；
- 近似最近邻索引；
- 批量更新与权限管理。

---

<!-- _class: compact -->
## 元数据为什么重要？

仅有向量不够，还必须保留元数据。

| 元数据 | 作用 |
|---|---|
| 文献题名 | 便于溯源 |
| 作者年份 | 识别来源可靠性 |
| 页码 | 精确定位证据 |
| 材料体系 | 支持过滤 |
| 数据类型 | 文本、表格、图注区分 |
| 可信等级 | 区分论文、笔记、未审核记录 |

<div class="warn">没有元数据的向量库难以做可靠引用核验。</div>

---

## 近似最近邻检索

当向量数量很大时，逐一计算相似度成本较高。

近似最近邻检索目标是快速找到近似最相似的向量。

```text
精确检索：更准，但慢
近似检索：稍有误差，但快
```

常见索引思想包括：

- 聚类划分；
- 图索引；
- 量化压缩；
- 倒排文件。

---

<!-- _class: compact -->
## 稀疏检索与稠密检索

| 类型 | 表示 | 优势 | 风险 |
|---|---|---|---|
| 稀疏检索 | 关键词、TF-IDF、BM25 | 精确术语好 | 同义表达漏检 |
| 稠密检索 | 嵌入向量 | 语义匹配好 | 可能检索到语义近但事实错的内容 |
| 混合检索 | 稀疏 + 稠密 | 兼顾术语与语义 | 系统复杂度高 |

材料术语强、同义表达多，适合使用混合检索。

---

<!-- _class: codepage -->
## Python 示例：TF-IDF 检索

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

texts = [
    "316L stainless steel fabricated by LPBF shows high strength.",
    "Austenite is the dominant phase in 316L steel.",
    "XRD patterns are used for phase identification."
]
query = "LPBF 316L strength"

vec = TfidfVectorizer()
X = vec.fit_transform(texts)
q = vec.transform([query])
score = cosine_similarity(q, X).ravel()
print(score.argsort()[::-1])
```

---

## 检索结果不等于答案

向量检索返回的是“相关片段”，不是最终结论。

需要进一步判断：

- 片段是否真的回答问题？
- 片段是否来自可靠文献？
- 片段是否有单位、条件、实验细节？
- 不同片段之间是否存在矛盾？
- 是否需要人工复核原文？

<div class="warn">RAG 的可靠性首先取决于检索片段的可靠性。</div>

---

## 7.3 小结

- 关键词检索强调字面匹配，语义检索强调向量相似性。
- TF-IDF 和 BM25 是经典稀疏检索方法。
- 文本嵌入把文本转换为连续语义向量。
- 向量数据库提供大规模相似性检索和元数据过滤。
- 下一节将把这些组件组合成 RAG 流程。

---

<!-- _class: trans -->
## 7.4 RAG基本流程：切分、嵌入、检索、重排、生成 △★

RAG 即 Retrieval-Augmented Generation。

基本思想：

```text
先检索外部知识，再让大模型基于检索证据生成回答。
```

它适合解决：

- 模型不知道本地资料；
- 模型知识过时；
- 需要引用依据；
- 需要控制回答范围。

---

## 7.4 的学习任务

- 掌握 RAG 的两阶段结构：入库阶段与问答阶段。
- 理解文档切分、嵌入、索引、检索、重排、生成的作用。
- 能说明 chunk size、overlap、top-k、重排策略对结果的影响。
- 能写出一个最小 RAG 示例程序。
- 能建立材料文献问答中的证据引用格式。

---

<!-- _class: compact -->
## RAG 与微调的区别

| 维度 | RAG | 微调 |
|---|---|---|
| 核心方式 | 检索外部知识作为上下文 | 改变模型参数 |
| 更新成本 | 更新知识库即可 | 通常需要重新训练 |
| 溯源能力 | 较强，可引用片段 | 较弱，知识隐含在参数中 |
| 适合场景 | 文献问答、规程查询 | 风格适配、任务格式学习 |
| 主要风险 | 检索错误、上下文不足 | 遗忘、过拟合、成本高 |

多数课程级知识库优先采用 RAG。

---

## RAG 的入库阶段

```text
原始文档
  ↓ 解析
文本、表格、图注
  ↓ 切分
知识片段 chunks
  ↓ 嵌入
向量表示
  ↓ 入库
向量数据库 + 元数据
```

入库阶段决定“系统知道哪些资料”。

<div class="note">对于材料文献，图表、单位、实验条件和页码元数据尤其重要。</div>

---

## RAG 的问答阶段

```text
用户问题
  ↓ 问题改写或扩展
查询向量
  ↓ 检索 top-k 片段
候选证据
  ↓ 重排
高质量证据
  ↓ 构造提示词
LLM 基于证据回答
  ↓ 引用与核验
最终答案
```

问答阶段决定“系统如何使用资料”。

---

## 文档解析

材料文献 PDF 通常包含：

- 正文段落；
- 表格；
- 图注；
- 公式；
- 参考文献；
- 补充材料链接。

解析难点：

- 双栏排版；
- 化学符号和上下标；
- 图表跨页；
- 表格列名与单位分离。

<div class="warn">PDF解析错误会直接污染知识库。</div>

---

<!-- _class: compact -->
## 切分 chunk 的基本原则

切分目标：让每个片段既足够短，又保留完整语义。

常用策略：

| 策略 | 说明 | 适用场景 |
|---|---|---|
| 固定长度 | 按 token 或字符切分 | 快速原型 |
| 段落切分 | 按自然段 | 文献正文 |
| 标题层级切分 | 按章节结构 | 综述、教材 |
| 表格单元切分 | 保留表头与单位 | 材料性能表 |
| 滑动窗口 | 保留上下文重叠 | 连续叙述文本 |

---

<!-- _class: formula -->
## chunk size 与 overlap

设切分长度为 $L$，重叠长度为 $O$。

```text
chunk 1: token 1     ... token L
chunk 2: token L-O+1 ... token 2L-O
```

影响：

- $L$ 太小：语义不完整；
- $L$ 太大：检索不精确；
- $O$ 太小：跨片段信息丢失；
- $O$ 太大：冗余增加。

材料文献建议根据段落、表格和图注结构切分，而不是只按字数切分。

---

<!-- _class: formula -->
## 嵌入与索引

每个片段 $c_i$ 经过嵌入模型得到向量：

$$
\mathbf{z}_i=f_{\theta}(c_i)
$$

向量库保存：

```text
chunk_id
embedding
source_title
page
section
material_system
data_type
quality_label
```

检索时，问题也被映射为向量：

$$
\mathbf{z}_q=f_{\theta}(q)
$$

---

<!-- _class: formula -->
## top-k 检索

系统选取与问题最相似的前 $k$ 个片段：

$$
\mathcal{C}_k = \operatorname{TopK}_{i}\; s(\mathbf{z}_q,\mathbf{z}_i)
$$

其中 $s$ 可为余弦相似度。

选择 $k$ 时需要平衡：

- $k$ 太小：证据不足；
- $k$ 太大：上下文噪声增加；
- 不同问题可能需要不同 $k$。

---

## 元数据过滤

材料问题常常需要先过滤再检索。

例：只检索 Fe-C 合金、相场模拟、2020 年以后的文献：

```text
material_system = Fe-C
method = phase-field
year >= 2020
```

再进行向量相似性搜索。

<div class="note">元数据过滤可显著降低“语义相近但领域不对”的误检。</div>

---

## 重排 reranking

初检索可能返回较多候选片段。

重排模型进一步判断：

```text
问题 + 候选片段 → 相关性分数
```

重排的作用：

- 提高前几条证据质量；
- 降低无关片段进入上下文的概率；
- 改善复杂问题的回答依据。

缺点：增加计算成本。

---

## 提示词构造

RAG 的提示词通常包含：

```text
系统角色：你是材料科学助教。
任务：只根据给定证据回答问题。
约束：不得编造引用；证据不足时说明不足。
证据：片段1、片段2、片段3。
输出格式：结论、依据、局限、参考来源。
问题：......
```

<div class="warn">提示词必须明确限制模型：不能使用未给出的证据编造结论。</div>

---

## 生成阶段

生成阶段不是自由发挥，而是证据约束生成。

可要求输出：

1. 直接结论；
2. 支撑证据编号；
3. 适用条件；
4. 不确定性或证据不足；
5. 需要人工复核的内容。

示例输出结构：

```text
结论：...
依据：[S1], [S3]
局限：证据未给出热处理时间。
```

---

## RAG 最小闭环

```text
文档集合
  ↓
切分与向量化
  ↓
相似性检索
  ↓
把相关片段放入提示词
  ↓
模型生成回答
  ↓
显示来源
```

这一闭环可以用于：

- 课程教材问答；
- 实验室 SOP 查询；
- 论文阅读助手；
- 材料数据库说明查询。

---

<!-- _class: codepage -->
## Python 示例：最小检索器

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

chunks = [
    "316L LPBF samples often contain cellular substructures.",
    "Cooling rate affects dendrite arm spacing in solidification.",
    "XRD can identify austenite and ferrite phases."
]
query = "How does cooling rate affect dendrite spacing?"

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(chunks)
q = vectorizer.transform([query])
rank = cosine_similarity(q, X).ravel().argsort()[::-1]

for i in rank[:2]:
    print(i, chunks[i])
```

---

<!-- _class: codepage -->
## Python 示例：构造 RAG 提示词

```python
def build_prompt(question, retrieved_chunks):
    evidence = "\n".join(
        f"[S{i+1}] {text}" for i, text in enumerate(retrieved_chunks)
    )
    return f"""
你是材料科学课程助教。只能根据证据回答。
若证据不足，请明确说明不能确定。

证据：
{evidence}

问题：{question}

请按：结论、依据、局限 三部分回答。
"""
```

该函数不调用大模型，但展示了 RAG 的核心提示结构。

---

<!-- _class: compact -->
## RAG 的典型错误类型

| 错误 | 表现 | 可能原因 |
|---|---|---|
| 检索缺失 | 关键证据未进入上下文 | 切分差、嵌入差、top-k太小 |
| 检索污染 | 无关片段被使用 | 向量相似但事实不相关 |
| 引用错配 | 结论引用了不支持的片段 | 生成阶段失控 |
| 条件丢失 | 忽略温度、成分、工艺范围 | chunk不完整 |
| 过度概括 | 把单一论文结论推广到全部材料 | 缺少适用边界 |

---

<!-- _class: compact -->
## RAG 参数调节

| 参数 | 影响 | 调节建议 |
|---|---|---|
| chunk size | 语义完整性与检索粒度 | 从段落级开始 |
| overlap | 跨片段信息保留 | 对长段落适度重叠 |
| top-k | 证据数量 | 问题复杂时增大 |
| embedding model | 语义匹配质量 | 优先选择领域适配模型 |
| reranker | 前排证据质量 | 对高可靠问答建议使用 |
| prompt template | 生成约束 | 明确证据、格式、拒答规则 |

---

## 面向材料文献的 RAG 特别要求

- 保留材料体系、成分、工艺、测试条件。
- 表格数据应保留列名和单位。
- 图注与正文应建立引用关系。
- 相同材料不同状态必须区分。
- 对“提高”“降低”“显著影响”等词应要求原始证据。
- 对强结论应提示证据数量和局限。

<div class="note">材料 RAG 的重点不是“回答流畅”，而是“条件完整、来源清楚、结论克制”。</div>

---

## 7.4 小结

- RAG 由入库阶段和问答阶段组成。
- 入库阶段包括解析、切分、嵌入、索引和元数据管理。
- 问答阶段包括问题嵌入、检索、重排、提示构造和生成。
- RAG 质量取决于文档质量、切分质量、检索质量和生成约束。
- 下一节讨论如何建设材料文献知识库与实验室知识管理系统。

---

<!-- _class: trans -->
## 7.5 材料文献知识库与实验室知识管理

知识库不仅是“文献问答机器人”。

在材料科研中，它还应支持：

- 文献证据管理；
- 实验记录管理；
- 计算数据管理；
- 标准流程管理；
- 课题组知识传承。

---

## 7.5 的学习任务

- 了解材料文献知识库的主要数据来源。
- 能设计文献、实验、计算和图像数据的元数据字段。
- 理解实验室知识管理中的版本、权限和审计。
- 能设计一个面向材料课题组的 RAG 知识库方案。
- 能区分公开知识库、内部知识库和个人知识库。

---

<!-- _class: compact -->
## 材料文献知识库的对象

| 对象 | 内容 | 检索需求 |
|---|---|---|
| 论文正文 | 方法、结果、讨论 | 问答与总结 |
| 表格 | 成分、性能、参数 | 精确查询与比较 |
| 图注 | 图像、谱图解释 | 图文关联 |
| 参考文献 | 证据链 | 追踪源头 |
| 补充材料 | 原始数据 | 复现与核验 |
| 专利 | 合成路线、工艺窗口 | 技术路线分析 |

---

<!-- _class: compact -->
## 材料知识库的元数据字段

| 字段 | 说明 |
|---|---|
| source_id | 文献或记录唯一编号 |
| title | 标题 |
| year | 年份 |
| material_system | 材料体系 |
| process | 加工工艺 |
| property_type | 性能类型 |
| page | 页码 |
| evidence_type | 正文、表格、图注、实验记录 |
| reliability_level | 证据可靠等级 |

<div class="note">元数据设计越规范，后续检索、过滤和核验越容易。</div>

---

## 实验室知识库的数据类型

- 项目申报材料；
- 学生论文与组会报告；
- 实验方案与 SOP；
- 仪器使用记录；
- 原始实验数据；
- 模拟输入文件与结果；
- 代码、脚本和后处理流程；
- 失败实验记录。

<div class="warn">失败实验记录往往最有价值，但最容易丢失。</div>

---

<!-- _class: compact -->
## 实验记录的结构化模板

| 模块 | 字段示例 |
|---|---|
| 样品信息 | 样品编号、材料、批次、制备日期 |
| 工艺参数 | 温度、时间、压力、功率、速度 |
| 测试条件 | 仪器、载荷、温度、环境介质 |
| 结果数据 | 强度、硬度、相分数、图像路径 |
| 异常记录 | 设备异常、样品污染、数据缺失 |
| 负责人 | 操作者、审核人、版本号 |

结构化记录有助于未来机器学习和 RAG 检索。

---

## 计算数据知识库

材料模拟数据应保存：

- 输入文件；
- 软件版本；
- 参数设置；
- 网格或晶胞；
- 边界条件；
- 收敛标准；
- 输出结果；
- 后处理脚本。

<div class="note">没有输入文件和版本信息的模拟结果很难复现。</div>

---

## 面向材料的知识库架构

```text
文献库       实验库       计算库       图像/谱图库
  ↓           ↓           ↓              ↓
解析与清洗 → 元数据标准化 → 向量化与图谱化
  ↓
混合检索层：关键词 + 向量 + 图谱 + 元数据过滤
  ↓
RAG问答层：证据约束生成
  ↓
人工审核、引用核验、版本管理
```

---

<!-- _class: compact -->
## 文献知识库与知识图谱结合

| 问题类型 | 推荐技术 |
|---|---|
| 查找某论文具体结论 | RAG向量检索 |
| 查找某材料的性能表 | 结构化数据库 |
| 查找成分—工艺—性能链条 | 知识图谱 |
| 查找相关论文并总结 | RAG + 元数据过滤 |
| 比较多篇文献结论 | RAG + 表格抽取 + 人工审核 |

实际系统不应只依赖一种检索方法。

---

## 课程案例：焊接高氮钢知识库

目标问题：

```text
高氮钢增材制造过程中，氮含量、冷却速率和相组成之间有什么关系？
```

知识库应包含：

- 高氮钢成分与工艺文献；
- Schaeffler、WRC 或相稳定性判据；
- 热力学计算结果；
- Fluent 熔池模拟结果；
- 显微组织表征结果。

---

## 课程案例：相场模拟知识库

可组织的知识对象：

- 相场方程；
- 自由能函数；
- 边界条件；
- 数值格式；
- 模型参数；
- 典型算例；
- 代码版本；
- 论文图表和讨论结论。

示例问题：

```text
包晶反应相场模型中，如何定义三相点附近的横向位移？
```

---

<!-- _class: compact -->
## 实验室知识管理的权限设计

| 权限层级 | 访问内容 |
|---|---|
| 公开 | 已发表论文、公开课件、公开数据 |
| 课程内部 | 教学资料、作业答案、案例代码 |
| 课题组内部 | 实验记录、组会材料、未发表结果 |
| 项目内部 | 申报书、合同、敏感数据 |
| 管理员 | 用户、版本、日志、备份 |

<div class="warn">知识库必须考虑数据安全和知识产权边界。</div>

---

<!-- _class: compact -->
## 版本管理

知识库中的内容需要版本控制。

| 对象 | 版本需求 |
|---|---|
| 文献条目 | 记录导入时间和解析版本 |
| 实验记录 | 不覆盖原始记录 |
| 数据表 | 记录清洗规则 |
| 代码 | 记录 Git commit |
| RAG提示词 | 记录模板版本 |
| 答案日志 | 记录问题、证据、回答和审核结果 |

<div class="note">可靠知识库必须能够回答：某个结论是何时、由哪些资料、按什么规则生成的。</div>

---

## 数据治理原则

材料知识库需要遵循：

- 原始数据不可随意覆盖；
- 清洗数据应记录处理步骤；
- 机密数据应设置访问权限；
- 训练数据和测试数据应区分；
- 引用他人成果应保留来源；
- AI生成内容应标记为生成或辅助生成。

这部分内容与课程第10章可信 AI 和数据安全直接衔接。

---

## 7.5 小结

- 材料知识库应覆盖文献、实验、计算、图像和谱图。
- 元数据、单位、来源和版本是知识库可靠性的基础。
- 实验室知识管理不仅是检索系统，更是科研流程管理系统。
- 公开知识、内部知识和敏感知识必须分层管理。
- 下一节讨论如何评价知识库回答是否可靠。

---

<!-- _class: trans -->
## 7.6 知识库回答的证据追踪与可靠性评价 ★

RAG 的核心承诺是：

```text
回答应当可以追踪到证据。
```

但“有引用”不等于“引用正确”。

本节讨论如何建立回答可靠性评价流程。

---

## 7.6 的学习任务

- 理解证据追踪、引用核验和回答可靠性的关系。
- 能识别伪引用、错引、过度概括和证据不足。
- 掌握忠实性、相关性、完整性、可复现性的评价指标。
- 能设计材料知识库回答的人工审核表。
- 能说明 RAG 系统在科研场景中的责任边界。

---

## 证据追踪的基本要求

一个可靠回答应至少包含：

1. 结论；
2. 支撑片段编号；
3. 来源文献或记录；
4. 页码或章节；
5. 适用条件；
6. 证据不足说明。

示例：

```text
结论：冷却速率升高通常会减小枝晶间距。
依据：[S2, p.5] 给出一次枝晶间距与冷却速率的关系。
局限：证据仅针对 Al-Cu 合金。
```

---

<!-- _class: compact -->
## 可靠性评价维度

| 维度 | 问题 |
|---|---|
| 相关性 | 检索片段是否与问题相关？ |
| 忠实性 | 回答是否只使用证据支持的内容？ |
| 完整性 | 是否遗漏关键条件或反例？ |
| 可追踪性 | 是否能定位到原始来源？ |
| 一致性 | 多个证据是否互相矛盾？ |
| 可复核性 | 人类能否快速复查原文？ |

---

<!-- _class: formula -->
## 忠实性 faithfulness

忠实性关注回答是否被证据支持。

可形式化理解为：

$$
\text{Faithfulness}=\frac{N_{\text{supported}}}{N_{\text{claims}}}
$$

其中：

- $N_{\text{claims}}$ 为回答中的断言数量；
- $N_{\text{supported}}$ 为可由证据支持的断言数量。

<div class="warn">高流畅度不代表高忠实性。</div>

---

<!-- _class: formula -->
## 相关性 relevance

相关性关注检索片段是否回答用户问题。

$$
\text{Relevance}=\frac{N_{\text{relevant}}}{N_{\text{retrieved}}}
$$

常见问题：

- 片段讨论同一材料但不同性能；
- 片段讨论相似工艺但不同材料；
- 片段只包含背景介绍，没有答案依据。

相关性差会导致生成阶段“看似有证据、实则无依据”。

---

## 完整性 completeness

完整性关注回答是否覆盖关键方面。

材料问题常见遗漏：

- 温度范围；
- 成分范围；
- 热处理状态；
- 试样尺寸；
- 测试方法；
- 误差或置信区间；
- 反例或争议结论。

<div class="note">材料科学结论往往是条件性结论，不能脱离实验条件。</div>

---

<!-- _class: compact -->
## 引用核验

引用核验至少检查：

| 检查项 | 说明 |
|---|---|
| 来源是否存在 | 文献、页码、DOI是否真实 |
| 内容是否对应 | 引用片段是否支持该结论 |
| 术语是否一致 | 材料、相、性能是否对应 |
| 数值是否准确 | 单位、有效数字、误差是否正确 |
| 条件是否保留 | 温度、工艺、测试条件是否完整 |

<div class="warn">最危险的错误不是没有引用，而是引用看似存在但不支持结论。</div>

---

<!-- _class: compact -->
## 伪引用与错引

| 类型 | 表现 |
|---|---|
| 伪引用 | 编造不存在的论文、DOI 或页码 |
| 错引 | 引用真实文献但文献不支持结论 |
| 断章取义 | 忽略作者限定条件 |
| 数据转录错误 | 数值、单位或材料名称错误 |
| 二次传播错误 | 引用综述转述但未查原始文献 |

课堂训练：要求学生随机抽查 2 条引用，回到原文核验。

---

## 人类审核流程

```text
RAG回答
  ↓
自动检查：是否有来源、是否有证据编号
  ↓
人工检查：证据是否支持结论
  ↓
专业判断：条件是否完整、是否过度外推
  ↓
修订答案
  ↓
记录审核结果和版本
```

<div class="note">在科研写作中，AI输出只能作为草稿，不能直接作为最终结论。</div>

---

<!-- _class: compact -->
## 材料知识库回答审核表

| 项目 | 合格标准 | 评分 |
|---|---|---|
| 问题理解 | 回答对象明确 | 0-2 |
| 证据相关 | 引用片段与问题相关 | 0-2 |
| 结论忠实 | 无无证据断言 | 0-2 |
| 条件完整 | 保留材料、工艺、测试条件 | 0-2 |
| 引用准确 | 可定位到原文 | 0-2 |
| 总分 | 满分 10 分 |  |

---

## RAG 系统评估集

构建评估集时应包含：

- 简单事实题；
- 多跳推理题；
- 表格数值题；
- 图注解释题；
- 证据不足题；
- 有冲突证据题；
- 容易混淆材料体系的题。

<div class="note">只有包含“证据不足题”，才能测试系统是否会克制回答。</div>

---

## 证据不足时的合格回答

不合格回答：

```text
该材料一定具有优异耐蚀性。
```

合格回答：

```text
根据给定证据，只能确认该文献报告了室温拉伸性能；
证据中没有腐蚀实验、介质环境和极化曲线，
因此不能判断其耐蚀性。
```

<div class="warn">能拒答，是可信知识库的重要能力。</div>

---

## 可靠 RAG 的设计原则

1. 数据来源明确；
2. 元数据完整；
3. 检索结果可查看；
4. 答案与证据逐条对应；
5. 证据不足时拒答；
6. 敏感内容分级授权；
7. 输出保留人工审核记录。

这些原则可用于课程项目、科研助手和实验室知识平台。

---

## 7.6 小结

- RAG 的目标不是替代判断，而是提供可追踪证据。
- 可靠性评价应关注相关性、忠实性、完整性和可复核性。
- 引用必须回到原文核验，不能只看模型生成的参考文献。
- 材料知识库应保留单位、条件、来源和版本。
- 人类审核是科研场景中不可省略的环节。

---

## 本章综合流程图

```text
领域知识
  ├─ 规则与本体 → 知识图谱
  ├─ 文献与记录 → 文本切分 → 嵌入向量
  ├─ 表格与数据 → 结构化数据库
  ↓
混合检索
  ↓
证据片段 + 元数据
  ↓
大模型生成
  ↓
引用核验 + 人工审核
```

---

<!-- _class: formula -->
## 本章核心公式回顾

TF-IDF：

$$
\text{tfidf}(t,d)=\text{tf}(t,d)\cdot \log\frac{N}{1+n_t}
$$

余弦相似度：

$$
\cos(\mathbf{x},\mathbf{y})=\frac{\mathbf{x}\cdot\mathbf{y}}{\|\mathbf{x}\|_2\|\mathbf{y}\|_2}
$$

Top-k 检索：

$$
\mathcal{C}_k = \operatorname{TopK}_{i}\;s(\mathbf{z}_q,\mathbf{z}_i)
$$

---

<!-- _class: compact -->
## 本章核心概念对照

| 概念 | 解决的问题 |
|---|---|
| 知识表示 | 如何让知识可计算 |
| 专家系统 | 如何用规则推理 |
| 知识图谱 | 如何组织实体关系 |
| 文本嵌入 | 如何表达语义相似性 |
| 向量数据库 | 如何大规模检索相似片段 |
| RAG | 如何让模型基于外部知识回答 |
| 证据追踪 | 如何核验回答可靠性 |

---

## 课堂讨论 1：知识图谱还是向量检索？

问题：

```text
“激光功率如何影响 316L 增材制造件的显微组织和强度？”
```

讨论：

- 哪些部分适合用知识图谱回答？
- 哪些部分适合用 RAG 检索文献？
- 哪些信息必须回到原始实验数据？
- 如何避免把个别论文结论泛化到所有工艺窗口？

---

## 课堂讨论 2：回答是否可靠？

模型回答：

```text
316L在LPBF后一定具有更高强度，因为快速冷却形成细晶组织。
```

需要指出的问题：

- “一定”是否过度绝对？
- 是否给出成分、功率、速度、热处理状态？
- 是否有证据支持“细晶组织”？
- 是否考虑孔隙、残余应力和热处理影响？
- 是否需要原文页码或数据表？

---

<!-- _class: trans -->
## Python 作业：构建一个迷你材料 RAG 检索器

任务目标：

用 Python 构建一个小型材料文献片段检索器。

基本要求：

1. 自拟 8-12 条材料文献片段；
2. 每条片段包含 `source`、`page`、`text`；
3. 使用 `TfidfVectorizer` 建立向量表示；
4. 输入一个材料问题；
5. 输出最相关的 3 条证据片段；
6. 按“结论—依据—局限”格式组织回答草稿。

---

<!-- _class: codepage -->
## 作业代码骨架

```python
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

records = [
    {"source": "Paper A", "page": 3, "text": "..."},
    {"source": "Paper B", "page": 5, "text": "..."},
]

query = "What affects dendrite arm spacing in solidification?"
texts = [r["text"] for r in records]

vec = TfidfVectorizer()
X = vec.fit_transform(texts)
q = vec.transform([query])
scores = cosine_similarity(q, X).ravel()
rank = scores.argsort()[::-1]

for idx in rank[:3]:
    r = records[idx]
    print(scores[idx], r["source"], r["page"], r["text"])
```

---

## 作业扩展要求

可选扩展：

- 加入材料体系过滤字段，例如 `Fe-C`、`Al-Cu`、`316L`。
- 加入数据类型字段，例如 `text`、`table`、`caption`。
- 输出回答时强制引用 `[source, page]`。
- 对证据不足的问题输出“无法根据现有证据判断”。
- 画出一个简单知识图谱：材料—工艺—组织—性能。

评分关注：

- 检索结果是否相关；
- 回答是否忠实于证据；
- 是否保留来源和局限。

---

## 本章结束语

知识库、知识图谱和 RAG 的共同目标不是制造“更会说”的模型，
而是建立一个更可追踪、更可验证、更能服务科研积累的知识系统。

在材料科学中，可靠知识系统应满足：

```text
来源清楚、条件完整、证据可查、结论克制、人工审核
```

下一章将进入 AI 代理、主动学习与贝叶斯优化。

---

<!-- _class: compact -->
## 参考资料与延伸阅读

- RDF 1.1 Concepts and Abstract Syntax，W3C。
- SPARQL Query Language for RDF，W3C。
- OpenAI Embeddings Guide。
- scikit-learn：TF-IDF、cosine similarity 文档。
- Faiss documentation：similarity search and clustering of dense vectors。
- LlamaIndex：Introduction to RAG。
- Materials Project、NOMAD 等材料数据库文档。

> 阅读建议：先理解“知识如何组织”，再学习具体框架和工具。

---

<!-- _class: lastpage -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## Q & A

本章关键词：

- 知识表示
- 专家系统
- 知识图谱
- 文本嵌入
- 向量数据库
- RAG
- 证据追踪
- 引用核验

<div class="note">请在课程项目中优先考虑：你的知识库回答能否被追踪、被核验、被复现？</div>

---

<!-- _class: compact -->
## 附录 A：材料知识库命名规范

建议统一命名：

| 类型 | 命名示例 |
|---|---|
| 样品 | `S_2026_001` |
| 文献 | `PAPER_2024_ActaMater_001` |
| 图像 | `IMG_S_2026_001_SEM_5000X` |
| 谱图 | `XRD_S_2026_001_20260607` |
| 代码 | `SCRIPT_PF_POST_001` |

规范命名可减少后续实体对齐成本。

---

<!-- _class: codepage -->
## 附录 B：知识库最小字段模板

```text
id:
title:
author:
year:
material_system:
process:
property:
page:
text:
evidence_type:
quality_label:
```

这组字段可以作为课程作业的最小数据结构。

---

<!-- _class: codepage -->
## 附录 C：RAG 提示词模板

```text
你是材料科学课程助教。
你只能依据给定证据回答。
若证据不足，请明确说明不能判断。
回答必须包含：结论、依据、局限。
每条依据必须引用证据编号。
```

该模板体现了证据约束、拒答机制和结构化输出。

---

<!-- _class: codepage -->
## 附录 D：知识图谱三元组模板

```text
(entity_1, relation, entity_2, source, page)
```

示例：

```text
(ScanSpeed, affects, CoolingRate, Paper_A, 5)
(CoolingRate, affects, CellSpacing, Paper_A, 6)
```

加入来源与页码后，三元组才具有可核验性。

---

## 附录 E：RAG 答案失败案例

失败表现：

- 回答中没有证据编号；
- 引用片段与结论不对应；
- 把“可能影响”写成“一定导致”；
- 忽略材料体系和工艺范围；
- 使用不存在的文献题名。

改进方向：增强检索、重排、提示约束和人工审核。

---

## 附录 F：课程项目建议

项目题目：构建“材料显微组织文献问答知识库”。

最低要求：

- 10 篇文献；
- 100 个文本片段；
- 每个片段有来源和页码；
- 支持 5 个问题的证据检索；
- 输出回答时给出证据编号。

进阶要求：加入知识图谱或图像图注检索。
