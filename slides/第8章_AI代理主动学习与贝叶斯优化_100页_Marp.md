---
marp: true
size: 4:3
theme: am_green
paginate: true
math: katex
author: Shiyan Pan
class: navbar
header: '**第8章** *AI代理* *工具调用* *主动学习* *贝叶斯优化* *材料优化* *闭环研发*'
footer: '《人工智能与大数据》 | 第8章'
style: |
  /* ============================================================
     第8章局部排版：基于 am_template.scss + am_green.scss。
     目标：4:3 课堂讲授；控制导航栏长度；公式、代码与表格保持可读。
     ============================================================ */
  section { line-height: 1.34; }
  section.course_cover {
    background: linear-gradient(180deg, var(--color-coverbg) 0 58%, #ffffff 58% 100%);
    text-align: center; overflow: hidden;
  }
  section.course_cover h1 {
    position: absolute; left: 5%; right: 5%; top: 10%; width: 90%;
    margin: 0; padding: 0; color: var(--color-title); background: transparent;
    font-size: 43px; line-height: 1.13; letter-spacing: 1px; white-space: normal;
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
    font-size: 420%; line-height: 118px; top: 16px; left: 0;
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
# 第8章 AI代理、主动学习与贝叶斯优化
###### AI Agents, Active Learning and Bayesian Optimization

<div class="cover-meta">
学习路径：AI代理 → 工具调用 → 主动学习 → 贝叶斯优化 → 成分—工艺优化 → 自动化材料研发闭环
</div>

<div class="cover-author">@Shiyan Pan</div>

---
<!-- _class: toc_a fglass course_toc -->
<!-- _header: "CONTENTS" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 目录

- 8.1 AI代理概念：规划、记忆、工具调用与反馈
- 8.2 LLM + 工具调用：代码、数据库、文献检索、绘图
- 8.3 主动学习：样本选择与实验设计 △
- 8.4 贝叶斯优化：代理模型、采集函数、探索—利用平衡 △★
- 8.5 材料成分—工艺参数优化案例
- 8.6 自动化材料研发闭环：计算—实验—模型—反馈 ★

> 主线：让模型不只回答问题，而是能够围绕目标选择下一步实验或计算。

---
## 本章学习目标

- 理解 AI 代理与普通聊天机器人的区别。
- 掌握工具调用、规划、记忆、反馈的基本框架。
- 理解主动学习为何适合材料小样本问题。
- 掌握贝叶斯优化中代理模型、采集函数与探索—利用平衡。
- 能够用 Python 实现一个简化的材料参数优化流程。

---
<!-- _class: compact -->

## 本章知识地图

<div class="note">
本章从“会回答的模型”推进到“会选择下一步行动的系统”。
</div>

```text
问题目标
  ↓
代理规划：把目标分解为若干可执行步骤
  ↓
工具调用：检索、计算、绘图、数据库查询、实验控制
  ↓
主动学习 / 贝叶斯优化：选择最有价值的下一组样本
  ↓
材料研发闭环：计算—实验—模型—反馈
```

---
## 为什么第8章放在这里？

前7章已经建立：

- 数据预处理：把材料数据整理成可建模形式。
- 贝叶斯思想：用概率表达不确定性。
- 机器学习：用数据建立性能预测模型。
- 深度学习与多模态：处理图像、谱图、文本和结构。
- RAG：使模型在证据约束下回答问题。

本章进一步回答：

> 当候选实验很多、预算有限时，下一次应该做哪个计算或实验？

---
## 材料研发中的典型困难

- 候选空间大：成分、热处理、焊接参数、增材制造参数组合极多。
- 单次实验成本高：制样、测试、显微表征、重复验证耗时。
- 数据稀疏：高质量数据通常只有几十到几百条。
- 噪声较强：实验误差、设备差异、批次差异不可避免。
- 目标冲突：强度、塑性、耐蚀性、成本、可焊性往往互相制约。

<div class="warn">
因此，材料 AI 不只是“拟合已有数据”，还要指导下一步最值得获取的数据。
</div>

---
<!-- _class: trans -->

<!-- _footer: "" -->

## 8.1 AI代理概念：从模型到行动系统

<!-- _class: trans -->

## 8.1 AI代理概念：规划、记忆、工具调用与反馈

从“回答问题”到“完成任务”。

---
## 8.1.1 什么是 AI 代理

AI 代理是一个能够围绕目标进行感知、规划、行动和反馈修正的计算系统。

常见组成：

- **目标**：要解决的问题或要优化的指标。
- **状态**：当前已知信息、历史步骤和环境反馈。
- **动作**：检索文献、运行代码、查询数据库、调用实验设备。
- **策略**：决定下一步采取什么动作。
- **反馈**：根据工具返回结果修正计划。

<div class="note">
普通 LLM 主要生成文本；AI 代理强调“文本推理 + 工具执行 + 结果反馈”。
</div>

---
<!-- _class: compact -->

## 8.1.2 代理与聊天机器人的区别

| 对比项 | 普通聊天模型 | AI代理 |
|---|---|---|
| 输入 | 用户问题 | 用户目标、工具环境、历史状态 |
| 输出 | 文本回答 | 文本、代码、检索、实验建议或动作 |
| 记忆 | 通常较弱 | 保留任务状态、阶段结果和偏好 |
| 工具 | 不一定使用 | 主动调用外部工具 |
| 反馈 | 主要依赖用户追问 | 根据工具返回结果自动修正 |
| 风险 | 幻觉、误解 | 幻觉 + 工具误用 + 错误执行 |

结论：代理不是“更会聊天”，而是更接近任务执行系统。

---
<!-- _class: formula -->

## 8.1.3 代理的基本数学抽象

可把代理看作在状态空间中选择动作的系统：

$$
\pi(a_t \mid s_t) = \text{AgentPolicy}(s_t, g, m_t)
$$

其中：

- $s_t$：第 $t$ 步的当前状态。
- $g$：任务目标。
- $m_t$：第 $t$ 步可用记忆。
- $a_t$：代理选择的动作。
- $\pi$：动作选择策略。

执行动作后环境返回：

$$
s_{t+1} = \text{Env}(s_t, a_t)
$$

---
## 8.1.4 规划：把复杂目标拆成步骤

规划是代理区别于一次性问答的重要能力。

以“优化高氮钢电弧增材制造工艺”为例：

1. 明确目标：提高奥氏体稳定性并降低缺陷率。
2. 收集约束：成分范围、热输入范围、实验预算。
3. 检索知识：相图、Schaeffler 图谱、焊接热循环文献。
4. 建立模型：成分—工艺—组织—性能映射。
5. 选择样本：主动学习或贝叶斯优化推荐下一组实验。
6. 更新模型：把新实验数据加入训练集。

---
<!-- _class: compact -->

## 8.1.5 记忆：短期、长期与任务记忆

| 记忆类型 | 作用 | 材料研发示例 |
|---|---|---|
| 短期记忆 | 保留当前对话与推理上下文 | 当前优化目标、最近一次候选参数 |
| 长期记忆 | 保留稳定偏好或长期知识 | 实验室常用材料体系、设备型号 |
| 任务记忆 | 保留项目过程记录 | 第几轮主动学习、哪些样本已测试 |
| 工具记忆 | 保留工具调用结果 | 数据库查询结果、代码运行输出 |

记忆不是简单存储文本，而要能被检索、更新和核验。

---
## 8.1.6 工具调用：让代理连接外部世界

LLM 本身不直接访问实验设备、数据库或计算程序。

工具调用使代理能够：

- 查询数据库：Materials Project、实验室数据表。
- 运行代码：拟合模型、画图、优化采集函数。
- 检索文献：获得带来源的证据。
- 调用仿真：有限元、CALPHAD、相场、分子动力学。
- 输出实验清单：给出可执行的下一批实验方案。

<div class="note">
工具调用的关键不是“能调用”，而是“何时调用、用什么参数调用、如何核验结果”。
</div>

---
## 8.1.7 反馈：闭环系统的核心

反馈用于修正代理行为。

```text
任务目标
  ↓
生成计划
  ↓
调用工具
  ↓
获得结果
  ↓
判断是否满足目标
  ↓
修正计划或输出结论
```

在材料优化中，反馈可能来自：

- 实验测得的硬度、强度、相分数。
- 仿真得到的温度场、应力场、组织形貌。
- 文献检索得到的证据或反例。
- 用户对结果可行性的判断。

---
## 8.1.8 ReAct 思想：推理与行动交替

ReAct 类代理的核心思想：

- Reasoning：分析当前问题和下一步需求。
- Acting：调用工具或执行动作。
- Observation：读取工具返回结果。
- Revision：根据观察结果修正判断。

简化流程：

```text
Thought → Action → Observation → Thought → Action → Observation → Answer
```

<div class="warn">
教学中不要求学生机械模仿“内心思考”，而要理解“计划—执行—观察—修正”的工程逻辑。
</div>

---
<!-- _class: compact -->

## 8.1.9 AI代理在材料领域的作用层级

| 层级 | 能力 | 示例 |
|---|---|---|
| 信息辅助 | 检索、总结、整理 | 自动整理某合金体系文献 |
| 代码辅助 | 生成与调试脚本 | 数据清洗、模型训练、绘图 |
| 建模辅助 | 自动构建候选模型 | 比较 GPR、RF、SVR |
| 决策辅助 | 推荐下一批样本 | 主动学习选择实验点 |
| 闭环执行 | 连接设备与数据库 | 自动化实验平台迭代优化 |

本章重点放在“建模辅助”和“决策辅助”。

---
## 8.1.10 AI代理的风险边界

AI 代理比普通问答系统更有用，也更有风险。

- 错误计划：把目标拆错，导致后续步骤全部偏离。
- 错误工具参数：单位、边界条件、数据列名设置错误。
- 错误解释：把工具输出过度解释为物理因果。
- 错误自动执行：在实验或生产系统中可能造成损失。

<div class="warn">
材料研发代理必须设置人类审核节点，尤其是在实验执行、设备控制、危险工艺与经费决策环节。
</div>

---
<!-- _class: trans -->

<!-- _footer: "" -->

## 8.2 LLM + 工具调用：从文本到可执行任务

<!-- _class: trans -->

## 8.2 LLM + 工具调用

代码、数据库、文献检索、绘图。

---
## 8.2.1 为什么 LLM 需要工具

LLM 的优势：

- 语言理解、任务分解、代码生成、格式转换。

LLM 的不足：

- 对最新资料不一定了解。
- 对数值计算不总是可靠。
- 对数据库内容不能凭空访问。
- 对图表、模型训练、文件处理需要外部执行环境。

因此，工具调用是把 LLM 从“语言模型”扩展为“任务系统”的关键。

---
## 8.2.2 工具调用的基本结构

一次工具调用通常包括：

1. 工具名称：例如 `search_papers`、`run_python`、`query_database`。
2. 参数模式：明确参数名称、类型、单位和约束。
3. 调用请求：由模型根据任务生成。
4. 工具返回：外部系统给出结构化结果。
5. 结果解释：模型把结果转化为用户可理解的回答。

```text
用户目标 → LLM选择工具 → 生成参数 → 工具执行 → 返回结果 → LLM解释
```

---
<!-- _class: codepage -->

## 8.2.3 工具参数模式：为什么要结构化

结构化参数可以降低歧义。

示例：查询高氮钢数据时，不应只写“帮我查一下”。

更合理的参数：

```json
{
  "alloy_system": "Fe-Cr-Mn-N",
  "target_property": "austenite_fraction",
  "temperature_range_K": [300, 1800],
  "process": "arc_additive_manufacturing"
}
```

<div class="note">
结构化工具调用要求把自然语言需求转化为可验证的变量、范围和约束。
</div>

---
<!-- _class: formula -->

## 8.2.4 代码工具：从问题到可运行程序

代码工具适合处理：

- 数据清洗：单位换算、缺失值处理、异常值检测。
- 模型训练：随机森林、GPR、神经网络。
- 数值优化：网格搜索、贝叶斯优化。
- 结果可视化：散点图、等值线图、误差图。

材料案例：

> 给定成分 $x_{\text{Cr}}$、$x_{\text{Ni}}$、$x_{\text{Mo}}$ 和热处理温度 $T$，建立硬度预测模型并推荐下一组测试样本。

---
<!-- _class: codepage -->

## 8.2.5 Python工具调用示意

```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# 读取材料数据：成分、工艺、性能
df = pd.read_csv("materials_data.csv")
features = ["C", "Cr", "Ni", "Mo", "solution_T", "aging_t"]
X = df[features]
y = df["hardness_HV"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)
model = RandomForestRegressor(n_estimators=300, random_state=0)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
```

此类代码可由 LLM 生成，但必须由解释器执行和验证。

---
<!-- _class: compact -->

## 8.2.6 数据库工具：从文本查询到结构化结果

材料数据库工具可以回答：

- 某晶体结构是否已被报道？
- 某材料体系有哪些计算能量、带隙、形成焓？
- 某实验室历史样本中哪些工艺参数接近当前候选点？

工具返回应尽量结构化：

| 字段 | 示例 |
|---|---|
| material_id | `mp-xxxx` 或实验样本编号 |
| composition | `Fe-18Cr-8Ni` |
| property | 硬度、相分数、形成能 |
| provenance | 数据来源、实验者、文献 DOI |
| uncertainty | 测量误差或模型预测标准差 |

---
## 8.2.7 文献检索工具：证据优先

文献检索工具应返回：

- 题名、作者、期刊、年份。
- DOI 或数据库编号。
- 与问题相关的段落或表格位置。
- 检索关键词与筛选规则。
- 与当前结论的支持或冲突关系。

<div class="warn">
文献检索不是“让模型编参考文献”，而是让模型在可追踪证据上组织回答。
</div>

---
## 8.2.8 绘图工具：辅助判断而非装饰

绘图工具适合回答：

- 样本是否覆盖设计空间？
- 预测误差是否随成分或工艺系统变化？
- 不确定性高的区域在哪里？
- 下一批实验点是否集中在合理区域？

常见图形：

- 目标值—预测值散点图。
- 残差分布图。
- 变量相关热图。
- 贝叶斯优化采集函数曲线。
- 主动学习样本选择图。

---
<!-- _class: formula -->

## 8.2.9 工具调用中的单位一致性

材料数据中单位错误极常见。

| 变量 | 常见单位 | 风险 |
|---|---|---|
| 温度 | $^{\circ}\text{C}$、$\text{K}$ | 273.15 偏移被忽略 |
| 时间 | s、min、h | 时效时间尺度混乱 |
| 成分 | wt.%、at.% | 质量分数和原子分数混用 |
| 热输入 | J/mm、kJ/mm | 量级错误 |
| 强度 | MPa、GPa | 数值相差 $10^3$ |

代理调用工具前应显式检查单位。

---
<!-- _class: formula -->

## 8.2.10 工具调用结果的验证

工具返回结果后要做三类检查：

1. **格式检查**：字段是否完整，单位是否明确。
2. **数值检查**：结果是否落在物理合理范围。
3. **逻辑检查**：是否支持当前结论，是否存在反例。

材料例子：

- 不锈钢硬度若预测为 $5000\ \text{HV}$，应触发异常警告。
- 相分数若超过 $1$ 或小于 $0$，说明模型或后处理错误。
- 温度若低于室温却显示完全熔化，说明物理逻辑冲突。

---
## 8.2.11 LLM + 工具调用的小结

- LLM 负责理解任务、组织步骤和解释结果。
- 工具负责检索、计算、绘图和数据访问。
- 工具调用必须结构化、可追踪、可验证。
- 材料研发中尤其要检查单位、边界、数据来源和物理合理性。

<div class="note">
下一节进入主动学习：当实验数据很少时，如何选择最值得补充的样本？
</div>

---
<!-- _class: trans -->

<!-- _footer: "" -->

## 8.3 主动学习：让模型主动选择样本

<!-- _class: trans -->

## 8.3 主动学习：样本选择与实验设计 △

有限预算下，优先获取最有价值的数据。

---
<!-- _class: compact -->

## 8.3.1 被动学习与主动学习

传统监督学习通常假设训练数据已经给定。

主动学习则问：

> 如果只能再测 $k$ 个样本，应选择哪些样本才能最快提升模型？

| 学习方式 | 样本来源 | 适用情形 |
|---|---|---|
| 被动学习 | 随机或历史数据 | 数据量充足，采样成本低 |
| 主动学习 | 模型选择最有价值样本 | 标注或实验成本高 |
| 贝叶斯优化 | 选择最可能改善目标的样本 | 目标函数昂贵、需要优化 |

主动学习更关注“提升模型”，贝叶斯优化更关注“找到最优点”。

---
## 8.3.2 主动学习的基本流程

```text
初始少量样本
  ↓
训练模型
  ↓
在候选池中估计不确定性或信息量
  ↓
选择最值得测试的样本
  ↓
实验或计算获得标签
  ↓
加入训练集并更新模型
  ↓
重复直到预算耗尽或性能满足要求
```

材料场景：

- 从 2000 个候选合金中选择 5 个进行高温拉伸实验。
- 从上万组焊接参数中选择 10 组进行熔池模拟。

---
<!-- _class: formula -->

## 8.3.3 主动学习的数学形式

设已标注数据集为 $\mathcal{D}_L$，未标注候选池为 $\mathcal{D}_U$。

模型在 $\mathcal{D}_L$ 上训练：

$$
\hat{f} = \text{Train}(\mathcal{D}_L)
$$

查询策略从候选池中选择下一个样本：

$$
x^{\ast} = \arg\max_{x \in \mathcal{D}_U} q(x; \hat{f}, \mathcal{D}_L)
$$

其中 $q(x)$ 是样本价值函数，可表示不确定性、代表性或预期信息增益。

---
<!-- _class: formula -->

## 8.3.4 不确定性采样

分类问题中，若模型对某样本最不确定，则该样本可能最有标注价值。

对于类别概率 $p(y=c \mid x)$，分类不确定性可写为：

$$
U(x) = 1 - \max_c p(y=c \mid x)
$$

选择：

$$
x^{\ast} = \arg\max_{x \in \mathcal{D}_U} U(x)
$$

材料例子：

- 显微组织图像分类中，模型无法确定“马氏体/贝氏体/铁素体”的图像优先人工标注。

---
<!-- _class: formula -->

## 8.3.5 边际采样

若最高概率类别与第二高概率类别接近，则模型难以区分。

令 $p_1(x)$ 和 $p_2(x)$ 为前两大类别概率，边际不确定性：

$$
M(x) = p_1(x) - p_2(x)
$$

选择边际最小的样本：

$$
x^{\ast} = \arg\min_{x \in \mathcal{D}_U} M(x)
$$

解释：

- $M(x)$ 越小，模型越难区分前两类。
- 适合材料相组成、缺陷类型、组织类别识别。

---
<!-- _class: formula -->

## 8.3.6 熵采样

信息熵衡量概率分布的不确定性：

$$
H(x) = -\sum_{c=1}^{C} p(y=c \mid x) \log p(y=c \mid x)
$$

选择熵最大的样本：

$$
x^{\ast} = \arg\max_{x \in \mathcal{D}_U} H(x)
$$

若类别概率接近均匀分布，则熵较大，说明模型缺乏判断依据。

---
<!-- _class: formula -->

## 8.3.7 回归问题中的不确定性

材料性能预测多为回归问题，如强度、硬度、热导率。

若模型给出预测均值 $\mu(x)$ 与标准差 $\sigma(x)$：

$$
y(x) \sim \mathcal{N}\left(\mu(x), \sigma^2(x)\right)
$$

可选择预测标准差最大的样本：

$$
x^{\ast} = \arg\max_{x \in \mathcal{D}_U} \sigma(x)
$$

含义：优先测试模型最不确定的材料组合。

---
<!-- _class: formula -->

## 8.3.8 多样性采样：避免扎堆

只按不确定性选点，可能导致样本集中在很小区域。

多样性采样希望候选点之间保持距离：

$$
D(x, \mathcal{S}) = \min_{x_i \in \mathcal{S}} d(x, x_i)
$$

其中 $\mathcal{S}$ 是已选择样本集合。

常见策略：

- K-means 聚类后选每个簇的代表点。
- 最大最小距离采样。
- 不确定性与多样性加权。

---
<!-- _class: formula -->

## 8.3.9 信息增益思想

更严格的主动学习希望最大化新样本带来的信息增益。

可用熵变化表达：

$$
\text{IG}(x) = H(\theta \mid \mathcal{D}_L) - \mathbb{E}_{y \mid x}\left[H(\theta \mid \mathcal{D}_L \cup \{(x,y)\})\right]
$$

其中 $\theta$ 表示模型参数或待估物理量。

直观含义：

> 选择一个样本，使观察它之后模型整体不确定性下降最多。

---
## 8.3.10 主动学习与实验设计

经典实验设计关注：

- 均匀覆盖设计空间。
- 减少参数估计方差。
- 提高统计效率。

主动学习进一步利用模型当前状态：

- 哪里模型最不确定？
- 哪里可能存在分类边界？
- 哪些点能最大改善目标预测？
- 哪些点既有代表性又信息量高？

因此，主动学习可看作“模型驱动的动态实验设计”。

---
<!-- _class: codepage -->

## 8.3.11 主动学习代码示例：候选池选择

```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor

# X_labeled, y_labeled: 已测试样本
# X_pool: 未测试候选样本
models = []
for seed in range(20):
    rf = RandomForestRegressor(n_estimators=100, random_state=seed)
    rf.fit(X_labeled, y_labeled)
    models.append(rf)

# 用模型集成方差估计不确定性
preds = np.vstack([m.predict(X_pool) for m in models])
mu = preds.mean(axis=0)
sigma = preds.std(axis=0)

next_id = np.argmax(sigma)
x_next = X_pool[next_id]
print("下一组建议实验参数:", x_next)
```

---
<!-- _class: formula -->

## 8.3.12 主动学习的材料案例

目标：预测激光增材制造合金的硬度。

特征：

- 成分：$x_{\text{Ni}}, x_{\text{Cr}}, x_{\text{Mo}}, x_{\text{Nb}}$。
- 工艺：激光功率 $P$、扫描速度 $v$、层厚 $h$。
- 组合变量：能量密度 $E = P/(v h)$。

初始数据：20 组实验。

主动学习策略：

- 用模型集成估计硬度预测不确定性。
- 每轮选择 3 组高不确定且分散的候选参数。
- 实验后更新模型。

---
## 8.3.13 主动学习的局限

主动学习并非总是优于随机采样。

常见问题：

- 模型初始阶段很差，不确定性估计不可靠。
- 候选池没有覆盖真实有价值区域。
- 噪声过大，导致模型误判不确定性。
- 只追求不确定性，忽视实验可行性。
- 材料约束复杂，如相稳定性、加工窗口、安全边界。

<div class="warn">
主动学习推荐的点必须经过物理和工艺约束筛选。
</div>

---
<!-- _class: trans -->

<!-- _footer: "" -->

## 8.4 贝叶斯优化：用不确定性指导最优搜索

<!-- _class: trans -->

## 8.4 贝叶斯优化 △★

代理模型、采集函数、探索—利用平衡。

---
<!-- _class: formula -->

## 8.4.1 为什么需要贝叶斯优化

许多材料问题可以写成黑箱优化：

$$
x^{\ast} = \arg\max_{x \in \mathcal{X}} f(x)
$$

其中：

- $x$：成分、工艺或结构参数。
- $f(x)$：实验或仿真返回的性能指标。
- $\mathcal{X}$：满足约束的设计空间。

困难：

- $f(x)$ 不能解析表达。
- 每次评估成本高。
- 数据少且噪声存在。
- 变量之间可能强非线性耦合。

---
## 8.4.2 贝叶斯优化基本思想

贝叶斯优化用一个便宜的代理模型近似昂贵目标函数。

```text
少量初始样本
  ↓
训练代理模型
  ↓
用采集函数评价候选点价值
  ↓
选择下一点做实验或仿真
  ↓
更新代理模型
  ↓
循环迭代
```

核心问题：

- 代理模型如何表达预测均值和不确定性？
- 采集函数如何平衡探索与利用？

---
<!-- _class: compact -->

## 8.4.3 代理模型

代理模型要求：

- 对未知点给出预测均值 $\mu(x)$。
- 对未知点给出不确定性 $\sigma(x)$。
- 能随新数据更新。

常用代理模型：

| 模型 | 优点 | 局限 |
|---|---|---|
| 高斯过程 | 天然给出不确定性 | 高维和大样本较困难 |
| 随机森林 | 鲁棒、适合非线性 | 不确定性需近似估计 |
| 贝叶斯神经网络 | 表达能力强 | 训练复杂 |
| 集成模型 | 易实现 | 不确定性校准需谨慎 |

---
<!-- _class: formula -->

## 8.4.4 高斯过程回归：基本定义

高斯过程可写为：

$$
f(x) \sim \mathcal{GP}\left(m(x), k(x,x')\right)
$$

其中：

- $m(x)$：均值函数。
- $k(x,x')$：核函数，描述样本之间的相似性。

常用核函数之一为径向基核：

$$
k(x,x') = \sigma_f^2 \exp\left(-\frac{\lVert x - x' \rVert^2}{2l^2}\right)
$$

$l$ 为长度尺度，控制函数变化的平滑程度。

---
<!-- _class: formula -->

## 8.4.5 高斯过程预测分布

给定训练数据 $\mathcal{D}=\{X,y\}$，在新点 $x_*$ 处预测：

$$
p(f_* \mid x_*, X, y) = \mathcal{N}\left(\mu_*, \sigma_*^2\right)
$$

其中预测均值和方差为：

$$
\mu_* = k_*^T (K + \sigma_n^2 I)^{-1} y
$$

$$
\sigma_*^2 = k_{**} - k_*^T (K + \sigma_n^2 I)^{-1} k_*
$$

均值用于利用，不确定性用于探索。

---
<!-- _class: compact -->

## 8.4.6 探索与利用

贝叶斯优化的核心矛盾：

- **利用**：选择当前预测性能最好的区域。
- **探索**：选择不确定性大的区域，可能发现更优点。

极端策略的问题：

| 策略 | 问题 |
|---|---|
| 只利用 | 易陷入局部最优 |
| 只探索 | 浪费实验预算 |
| 随机搜索 | 忽视已有知识 |
| 网格搜索 | 高维空间成本指数增长 |

采集函数用于在二者之间折中。

---
<!-- _class: formula -->

## 8.4.7 采集函数：概率改进 PI

设当前最佳观测值为 $f_{\text{best}}$。

概率改进定义为：

$$
\text{PI}(x) = P\left(f(x) \ge f_{\text{best}} + \xi\right)
$$

若 $f(x)$ 的预测服从正态分布，则：

$$
\text{PI}(x) = \Phi\left(\frac{\mu(x)-f_{\text{best}}-\xi}{\sigma(x)}\right)
$$

其中 $\xi$ 控制改进阈值，$\Phi$ 是标准正态分布函数。

---
<!-- _class: formula -->

## 8.4.8 采集函数：期望改进 EI

期望改进不仅考虑改进概率，也考虑改进幅度。

改进量：

$$
I(x) = \max\left(0, f(x)-f_{\text{best}}-\xi\right)
$$

期望改进：

$$
\text{EI}(x) = \mathbb{E}\left[I(x)\right]
$$

若预测为正态分布：

$$
\text{EI}(x) = (\mu - f_{\text{best}} - \xi)\Phi(Z) + \sigma \phi(Z)
$$

$$
Z = \frac{\mu - f_{\text{best}} - \xi}{\sigma}
$$

---
<!-- _class: formula -->

## 8.4.9 采集函数：置信上界 UCB

置信上界采集函数：

$$
\text{UCB}(x) = \mu(x) + \kappa \sigma(x)
$$

其中：

- $\mu(x)$：预测均值，代表利用。
- $\sigma(x)$：预测不确定性，代表探索。
- $\kappa$：探索权重。

当 $\kappa$ 较大时，算法更倾向探索高不确定区域。

当 $\kappa$ 较小时，算法更倾向选择高预测性能区域。

---
<!-- _class: formula -->

## 8.4.10 最小化问题的处理

许多材料问题是最小化：

- 最小化腐蚀速率。
- 最小化裂纹敏感性。
- 最小化残余应力。
- 最小化孔隙率。

可转换为最大化问题：

$$
g(x) = -f(x)
$$

或者使用下置信界：

$$
\text{LCB}(x) = \mu(x) - \kappa \sigma(x)
$$

最小化时选择 $\text{LCB}(x)$ 最小的点。

---
<!-- _class: formula -->

## 8.4.11 约束贝叶斯优化

材料设计通常有约束。

例如：

$$
\max_x f(x)
$$

$$
\text{s.t.}\quad g_j(x) \le 0,\quad j=1,2,\dots,m
$$

约束可能包括：

- 成分总和为 $100\%$。
- 元素含量处于标准范围。
- 工艺参数不超过设备能力。
- 相分数或裂纹倾向满足安全要求。

可用可行概率修正采集函数：

$$
a_c(x) = a(x) P\left(\text{feasible} \mid x\right)
$$

---
<!-- _class: formula -->

## 8.4.12 多目标贝叶斯优化

材料问题常有多个目标：

$$
\max_x \left[f_1(x), f_2(x), \dots, f_m(x)\right]
$$

示例：

- 最大化强度。
- 最大化延伸率。
- 最小化成本。
- 最小化热裂倾向。

不能简单得到唯一最优解，而是得到 Pareto 前沿。

Pareto 最优：不存在另一个解在所有目标上都不差，并至少一个目标更好。

---
<!-- _class: codepage -->

## 8.4.13 贝叶斯优化代码：一维示意

```python
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel

# 已观测点
X = np.array([[0.1], [0.4], [0.8]])
y = np.sin(6 * X).ravel() + X.ravel()

kernel = ConstantKernel(1.0) * RBF(length_scale=0.2)
gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-6, normalize_y=True)
gp.fit(X, y)

X_pool = np.linspace(0, 1, 200).reshape(-1, 1)
mu, std = gp.predict(X_pool, return_std=True)
ucb = mu + 2.0 * std
x_next = X_pool[np.argmax(ucb)]
print("建议下一个点:", x_next)
```

---
<!-- _class: codepage -->

## 8.4.14 EI函数代码示例

```python
import numpy as np
from scipy.stats import norm

def expected_improvement(mu, sigma, y_best, xi=0.01):
    sigma = np.maximum(sigma, 1e-12)
    z = (mu - y_best - xi) / sigma
    ei = (mu - y_best - xi) * norm.cdf(z) + sigma * norm.pdf(z)
    return ei

mu, std = gp.predict(X_pool, return_std=True)
y_best = np.max(y)
ei = expected_improvement(mu, std, y_best)
x_next = X_pool[np.argmax(ei)]
print("EI推荐点:", x_next)
```

注意：最大化目标使用上述形式；最小化问题需调整符号。

---
## 8.4.15 贝叶斯优化适用条件

适合：

- 每次实验或仿真成本高。
- 变量维数中等。
- 可接受序贯迭代。
- 目标函数较平滑或有可学习规律。
- 可以定义明确评价指标。

不适合：

- 变量维数极高且无结构。
- 目标噪声极大且不可重复。
- 候选空间约束不清。
- 每次评估几乎无成本，随机或网格搜索已足够。

---
<!-- _class: compact -->

## 8.4.16 贝叶斯优化与主动学习的区别

| 对比项 | 主动学习 | 贝叶斯优化 |
|---|---|---|
| 主要目的 | 提升模型整体性能 | 尽快找到最优点 |
| 样本选择依据 | 不确定性、代表性、信息增益 | 采集函数、改进概率、置信界 |
| 输出重点 | 更好的模型 | 更好的候选材料或工艺 |
| 典型问题 | 哪些样本最值得标注？ | 下一次实验选哪里更可能提升性能？ |
| 材料例子 | 补充组织图像标注 | 优化热处理温度和时间 |

二者可以结合：先主动学习建立可信模型，再用贝叶斯优化寻找最优区域。

---
<!-- _class: trans -->

<!-- _footer: "" -->

## 8.5 材料成分—工艺参数优化案例

<!-- _class: trans -->

## 8.5 材料成分—工艺参数优化案例

从问题定义到可执行优化流程。

---
<!-- _class: formula -->

## 8.5.1 案例问题：增材制造合金性能优化

目标：在有限实验预算下优化增材制造合金的强度和缺陷率。

设计变量：

- 成分：$x_{\text{Cr}}, x_{\text{Ni}}, x_{\text{Mo}}, x_{\text{N}}$。
- 工艺：激光功率 $P$、扫描速度 $v$、层厚 $h$、预热温度 $T_p$。

性能指标：

- 屈服强度 $\sigma_y$。
- 延伸率 $\delta$。
- 孔隙率 $\phi_p$。
- 奥氏体体积分数 $f_\gamma$。

---
<!-- _class: compact formula -->

## 8.5.2 设计空间定义

设计空间不能随意设定，应来自材料与设备约束。

| 变量 | 范围 | 约束来源 |
|---|---:|---|
| $x_{\text{Cr}}$ | 15–22 wt.% | 不锈钢成分窗口 |
| $x_{\text{Ni}}$ | 6–14 wt.% | 奥氏体稳定性 |
| $x_{\text{N}}$ | 0.05–0.40 wt.% | 高氮钢溶解度与气孔风险 |
| $P$ | 150–350 W | 设备功率 |
| $v$ | 300–1200 mm/s | 熔池稳定性 |
| $h$ | 20–60 μm | 铺粉与成形约束 |

约束越清晰，优化结果越可执行。

---
<!-- _class: formula -->

## 8.5.3 派生特征：体能量密度

增材制造中常用体能量密度：

$$
E = \frac{P}{v h t}
$$

其中：

- $P$：功率。
- $v$：扫描速度。
- $h$：道间距。
- $t$：层厚。

注意：$E$ 是简化描述，并不能完全替代热传导、熔池流动和蒸发行为。

<div class="warn">
不能把能量密度相同的工艺视为物理等价，因为 $P$ 和 $v$ 对熔池形态影响不同。
</div>

---
<!-- _class: formula -->

## 8.5.4 目标函数构造

若只考虑强度最大化：

$$
f(x) = \sigma_y(x)
$$

若同时考虑孔隙率惩罚：

$$
f(x) = \sigma_y(x) - \lambda \phi_p(x)
$$

若考虑强塑积：

$$
f(x) = \sigma_y(x) \cdot \delta(x)
$$

如果指标量纲差异大，应先标准化：

$$
\tilde{y} = \frac{y - \mu_y}{s_y}
$$

---
<!-- _class: formula -->

## 8.5.5 初始实验设计

贝叶斯优化需要初始样本。

常见方式：

- 随机采样：简单，但可能分布不均。
- 拉丁超立方采样：更均匀覆盖各变量范围。
- 正交设计：适合少量离散水平。
- 历史数据：可利用已有实验，但需检查偏差。

建议：

> 初始样本数量可取变量维数的 $2$ 到 $5$ 倍作为教学演示起点。

---
<!-- _class: formula -->

## 8.5.6 代理模型训练

输入矩阵：

$$
X = \begin{bmatrix}
 x_{11} & x_{12} & \cdots & x_{1d} \\
 x_{21} & x_{22} & \cdots & x_{2d} \\
 \vdots & \vdots & \ddots & \vdots \\
 x_{n1} & x_{n2} & \cdots & x_{nd}
\end{bmatrix}
$$

目标向量：

$$
y = \begin{bmatrix} y_1 & y_2 & \cdots & y_n \end{bmatrix}^T
$$

训练代理模型：

$$
\hat{f} = \text{Train}(X,y)
$$

---
<!-- _class: codepage -->

## 8.5.7 候选点生成

候选点必须满足约束。

```python
import numpy as np

rng = np.random.default_rng(0)
N = 5000
X_pool = np.column_stack([
    rng.uniform(15, 22, N),      # Cr wt.%
    rng.uniform(6, 14, N),       # Ni wt.%
    rng.uniform(0.05, 0.40, N),  # N wt.%
    rng.uniform(150, 350, N),    # P W
    rng.uniform(300, 1200, N),   # v mm/s
    rng.uniform(20, 60, N)       # h micrometer
])
```

实际研究中还需加入相图、设备、成形质量等可行性约束。

---
<!-- _class: codepage -->

## 8.5.8 使用 GPR 推荐下一组实验

```python
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, ConstantKernel

kernel = ConstantKernel(1.0) * Matern(length_scale=np.ones(X_train.shape[1]), nu=2.5)
gp = GaussianProcessRegressor(kernel=kernel, alpha=1e-4, normalize_y=True)
gp.fit(X_train, y_train)

mu, std = gp.predict(X_pool, return_std=True)
ucb = mu + 1.96 * std
best_idx = np.argmax(ucb)
print("推荐实验点:", X_pool[best_idx])
print("预测均值:", mu[best_idx], "预测标准差:", std[best_idx])
```

---
<!-- _class: formula -->

## 8.5.9 可行性过滤

优化推荐点不一定可制备。

可行性过滤包括：

- 成分约束：元素总量、杂质上限。
- 相稳定性：避免明显不可接受相区。
- 工艺约束：设备功率、扫描速度范围。
- 成形质量：避免过低或过高能量输入。
- 安全约束：气体、粉末、热源风险。

可写为：

$$
\mathcal{X}_{\text{valid}} = \{x \in \mathcal{X} \mid g_j(x) \le 0, j=1,\dots,m\}
$$

---
<!-- _class: formula -->

## 8.5.10 多目标优化：强度与塑性

若同时优化强度和延伸率：

$$
\max_x \left[\sigma_y(x), \delta(x)\right]
$$

可采用：

- 加权和：$f(x)=w_1\tilde{\sigma}_y(x)+w_2\tilde{\delta}(x)$。
- 约束形式：最大化强度，同时要求延伸率 $\delta \ge 15\%$。
- Pareto 前沿：给出一组互不支配方案。

课堂教学可先使用加权和，再引入 Pareto 思想。

---
<!-- _class: compact -->

## 8.5.11 多保真优化

材料研发中数据来源保真度不同。

| 数据源 | 成本 | 保真度 | 示例 |
|---|---:|---:|---|
| 经验公式 | 低 | 低 | Schaeffler 图谱估计相组成 |
| CALPHAD | 中 | 中 | 平衡相分数、Scheil 凝固 |
| 有限元/相场 | 高 | 中高 | 温度场、组织演化 |
| 实验 | 最高 | 高 | 显微组织、力学性能 |

多保真优化目标：用低成本数据缩小搜索区域，用高保真数据验证关键点。

---
## 8.5.12 案例结果表达

优化结果不应只给一个“最优点”。

建议输出：

- 当前推荐实验点。
- 预测均值和不确定性。
- 推荐理由：高预测性能、高不确定性或二者兼具。
- 与历史最佳样本的差异。
- 可行性检查结果。
- 备选点列表。

<div class="note">
材料实验通常需要一批候选方案，而不是单个唯一答案。
</div>

---
## 8.5.13 常见错误

- 把代理模型预测值当成真实实验结果。
- 忽略数据噪声和实验重复性。
- 采集函数只在训练样本附近搜索。
- 忽略材料成分闭合约束。
- 对小样本使用过复杂模型。
- 不记录失败样本，导致优化偏向“成功案例”。

<div class="warn">
失败样本同样是重要数据，它们定义了不可行区域和风险边界。
</div>

---
<!-- _class: trans -->

<!-- _footer: "" -->

## 8.6 自动化材料研发闭环

<!-- _class: trans -->

## 8.6 自动化材料研发闭环 ★

计算—实验—模型—反馈。

---
## 8.6.1 闭环研发的基本结构

```text
目标定义
  ↓
候选设计生成
  ↓
模型预测与不确定性评估
  ↓
采集函数选择下一批样本
  ↓
自动化计算或实验
  ↓
数据入库与质量控制
  ↓
模型更新
  ↓
下一轮迭代
```

闭环研发的核心不是“自动跑实验”，而是“每轮数据都能改善下一轮决策”。

---
## 8.6.2 计算闭环

计算闭环更容易实现，可作为课程项目起点。

组成：

- 候选结构或成分生成。
- 第一性原理、CALPHAD、分子动力学或有限元计算。
- 自动解析输出文件。
- 数据清洗与入库。
- 机器学习代理模型更新。
- 贝叶斯优化推荐下一批计算。

优势：

- 成本低于实验。
- 可自动化程度较高。
- 便于教学演示。

---
## 8.6.3 实验闭环

实验闭环需要更多工程条件：

- 自动配料、制样或沉积系统。
- 在线传感与数据采集。
- 自动化表征或快速性能测试。
- 样本编号、元数据和原始数据管理。
- 安全联锁和人工审核。

材料实验闭环比纯软件代理更复杂，因为设备、安全、样品制备和误差控制都不可忽略。

---
<!-- _class: compact -->

## 8.6.4 模型在闭环中的位置

模型不是闭环的终点，而是决策部件。

| 环节 | 模型作用 |
|---|---|
| 候选生成 | 过滤明显不可行设计 |
| 性能预测 | 估计目标值 |
| 不确定性评估 | 判断知识盲区 |
| 采集函数 | 选择下一轮样本 |
| 数据质控 | 识别异常结果 |
| 机理解释 | 辅助判断规律是否物理合理 |

模型必须随新数据持续更新。

---
<!-- _class: compact -->

## 8.6.5 数据入库与元数据

闭环系统必须记录元数据。

| 数据类型 | 应记录内容 |
|---|---|
| 成分数据 | nominal composition、measured composition、单位 |
| 工艺数据 | 设备、参数、时间、环境 |
| 表征数据 | 仪器、倍率、区域、图像处理方法 |
| 性能数据 | 测试标准、试样尺寸、重复次数 |
| 模型数据 | 模型版本、训练集、超参数、指标 |
| 优化数据 | 采集函数、候选池、推荐理由 |

没有元数据，闭环结果难以复现。

---
## 8.6.6 人类审核节点

需要人工审核的环节：

- 实验参数是否超出设备安全范围。
- 候选成分是否违反标准或安全规定。
- 模型推荐是否具有基本材料学合理性。
- 文献证据是否真实支持结论。
- 自动生成代码是否正确处理单位和边界。

<div class="warn">
自动化材料研发不是取消专家，而是把专家判断嵌入更高效的闭环流程。
</div>

---
<!-- _class: formula -->

## 8.6.7 闭环停止准则

闭环何时停止？

常见准则：

- 实验预算耗尽。
- 连续若干轮没有显著改进。
- 最优值达到预设阈值。
- 模型不确定性降至可接受范围。
- 推荐点开始重复集中。
- 专家判定已进入工程验证阶段。

可写为：

$$
\Delta f_t = f_{\text{best},t} - f_{\text{best},t-1}
$$

若连续 $r$ 轮满足 $\Delta f_t < \epsilon$，可停止优化。

---
## 8.6.8 闭环系统的可靠性评价

可靠性评价不仅看最终性能，还看过程质量。

- 数据可追溯：每个结论能追到样本和原始记录。
- 模型可复现：代码、版本、随机种子明确。
- 推荐可解释：为什么选择该样本。
- 风险可控制：不让模型直接执行危险操作。
- 失败可学习：失败实验也进入数据库。
- 结论可验证：关键结果必须实验复核。

---
<!-- _class: codepage -->

## 8.6.9 闭环研发 Python 伪代码

```python
for round_id in range(max_rounds):
    # 1. 训练或更新代理模型
    model.fit(X_train, y_train)

    # 2. 在候选池上预测均值和不确定性
    mu, std = model.predict(X_pool, return_std=True)

    # 3. 计算采集函数
    acquisition = mu + kappa * std

    # 4. 可行性过滤
    acquisition[~valid_mask] = -np.inf

    # 5. 选择下一批样本
    selected = np.argsort(acquisition)[-batch_size:]
    X_next = X_pool[selected]

    # 6. 执行实验或计算，并加入数据库
    y_next = run_experiment_or_simulation(X_next)
    X_train, y_train = update_dataset(X_train, y_train, X_next, y_next)
```

---
## 8.6.10 材料科研中的实施路线

可分三阶段推进：

1. **离线闭环**：用历史数据模拟主动学习和贝叶斯优化。
2. **半自动闭环**：模型推荐实验，人类执行并回填数据。
3. **自动闭环**：系统连接计算平台、数据库和实验设备。

建议教学从离线闭环开始：

- 成本低。
- 安全风险低。
- 便于学生理解算法流程。
- 适合用 Python 作业实现。

---
## 8.6.11 本章总结

- AI代理把 LLM 从文本生成扩展到任务执行系统。
- 工具调用连接代码、数据库、文献检索和绘图。
- 主动学习用于在有限预算下选择最有价值样本。
- 贝叶斯优化用于高成本黑箱函数的序贯优化。
- 材料成分—工艺优化必须考虑物理约束和工艺可行性。
- 自动化材料研发闭环需要数据、模型、实验和人类审核共同协同。

---
<!-- _class: compact -->

## 概念辨析：AI代理、主动学习、贝叶斯优化

| 概念 | 核心问题 | 典型输出 |
|---|---|---|
| AI代理 | 下一步该执行什么动作？ | 工具调用、计划、报告 |
| 主动学习 | 下一批标注或实验样本选哪些？ | 最有信息量的样本 |
| 贝叶斯优化 | 下一次评估哪里更可能找到更优解？ | 最有希望改进目标的点 |
| 自动化闭环 | 如何持续迭代改进？ | 计算—实验—模型—反馈流程 |

三者结合后，材料研发从“经验试错”逐步走向“数据驱动的序贯决策”。

---
## 课堂讨论题

1. 对于只有 30 组数据的合金强度预测问题，主动学习是否一定优于随机采样？为什么？
2. 贝叶斯优化推荐的参数组合如果违反工艺经验，应如何处理？
3. 在自动化材料研发闭环中，哪些环节必须保留人工审核？
4. 如果实验数据噪声很大，采集函数应如何调整？
5. 失败实验应不应该进入数据库？如何标注失败原因？

---
<!-- _class: formula -->

## Python编程作业：主动学习 + 贝叶斯优化演示

任务：构造一个简化的“材料性能函数”，模拟有限实验预算下的序贯优化。

要求：

1. 令设计变量为 $x_1$ 和 $x_2$，分别代表成分参数与工艺参数。
2. 构造未知目标函数：

$$
f(x_1,x_2)=\sin(3x_1)+\cos(4x_2)-0.2(x_1-1)^2-0.1(x_2+1)^2
$$

3. 随机选择 5 个初始样本训练高斯过程模型。
4. 用 UCB 或 EI 每轮推荐 1 个新样本。
5. 迭代 15 轮，绘制历史最佳值随轮数变化曲线。
6. 比较随机采样与贝叶斯优化的差异。

---
<!-- _class: codepage -->

## 作业提示：程序结构

```text
1. 生成候选池 X_pool
2. 随机选取初始样本 X_train, y_train
3. for 每一轮:
      训练 GaussianProcessRegressor
      预测候选池的 mu 和 std
      计算 UCB = mu + kappa * std
      选择 UCB 最大的点
      计算真实函数值并加入训练集
      记录当前 best_y
4. 绘制 best_y 与迭代轮数的关系
```

扩展：

- 改变 $\kappa$，观察探索强度对优化结果的影响。
- 加入噪声，观察贝叶斯优化稳定性。

---
<!-- _class: compact -->

## 参考阅读与工具

- OpenAI Function Calling / Tools：理解 LLM 如何连接外部系统。
- OpenAI Agents SDK：理解代理工具、运行状态和工具执行。
- scikit-learn GaussianProcessRegressor：实现高斯过程回归。
- modAL：实现主动学习流程。
- BoTorch：实现更复杂的贝叶斯优化与采集函数。
- scikit-optimize：实现入门级贝叶斯优化。

课堂建议：先用 scikit-learn 写清楚原理，再逐步引入 BoTorch 等工程化工具。

---
<!-- _class: formula -->

## 补充案例1：焊接工艺参数优化

目标：降低孔隙率并提高熔深稳定性。

变量：电流 $I$、电压 $U$、焊接速度 $v$、保护气流量 $Q$。

可构造目标：

$$
f(x)= -\phi_p(x) - \lambda \left|d(x)-d_0\right|
$$

其中 $\phi_p$ 为孔隙率，$d$ 为熔深，$d_0$ 为目标熔深。

推荐流程：先用有限元或 Fluent 结果构建代理模型，再少量实验校正。

---
<!-- _class: formula -->

## 补充案例2：热处理制度优化

目标：获得高硬度且保留足够韧性。

变量：固溶温度、固溶时间、时效温度、时效时间。

可设多目标：

$$
\max_x \left[H(x), K_{IC}(x)\right]
$$

或者约束优化：

$$
\max_x H(x),\quad \text{s.t.}\quad K_{IC}(x) \ge K_0
$$

适合用贝叶斯优化减少热处理实验次数。

---
## 补充案例3：显微组织标注主动学习

目标：减少人工标注显微组织图像成本。

流程：

1. 标注少量图像训练分类模型。
2. 对未标注图像预测类别概率。
3. 选择熵最大的图像给专家标注。
4. 更新模型并重复。

优势：优先标注“模型最困惑”的图像，而不是随机标注大量重复图像。

---
## 补充案例4：CALPHAD + 实验闭环

低保真数据：CALPHAD 预测相分数和相变温度。

高保真数据：实验测得组织和性能。

思路：

- 用 CALPHAD 缩小候选空间。
- 用贝叶斯优化选择实验点。
- 用实验结果校正模型。
- 把失败成分也作为不可行边界记录。

---
## 本章易错点总结

- 把 LLM 输出当作工具执行结果。
- 把不确定性高误解为性能一定好。
- 把贝叶斯优化理解为普通网格搜索。
- 忽略候选空间约束。
- 忽略单位换算与实验噪声。
- 只保存成功实验，不记录失败实验。
- 让自动化系统绕过专家审核。

---
<!-- _class: lastpage -->

<!-- _header: "" -->

<!-- _footer: "" -->

<!-- _paginate: "" -->

## 最后一页

<!-- _class: lastpage -->

# 谢谢

请完成本章 Python 编程作业：主动学习与贝叶斯优化演示。

---
