---
marp: true
size: 4:3
theme: am_green
paginate: true
math: katex
author: Shiyan Pan
class: navbar
header: '**第2章** *Python环境* *NumPy/Pandas* *材料数据* *数据清洗* *统计可视化* *可靠性*'
footer: '《人工智能与大数据》 | 第2章'
style: |
  /* ============================================================
     第2章局部排版修正：使用 am_template + am_green 的导航栏、
     目录、分栏、Callout 与过渡页工具，并补充面向课堂讲授的
     代码页、公式页、表格页和案例页样式。
     ============================================================ */
  section {
    line-height: 1.34;
  }
  section.course_cover {
    background: linear-gradient(180deg, var(--color-coverbg) 0 58%, #ffffff 58% 100%);
    text-align: center;
    overflow: hidden;
  }
  section.course_cover h1 {
    position: absolute;
    left: 6%;
    right: 6%;
    top: 13%;
    width: 88%;
    margin: 0;
    padding: 0;
    color: var(--color-title);
    background: transparent;
    font-size: 46px;
    line-height: 1.18;
    letter-spacing: 1px;
    transform: none;
    white-space: normal;
  }
  section.course_cover h6 {
    position: absolute;
    left: 8%;
    right: 8%;
    top: 42%;
    width: 84%;
    margin: 0;
    padding: 0;
    color: var(--color-title);
    background: transparent;
    font-size: 28px;
    line-height: 1.18;
    transform: none;
    white-space: normal;
  }
  section.course_cover .cover-meta {
    position: absolute;
    left: 12%;
    right: 12%;
    bottom: 21%;
    margin: 0;
    padding: 17px 22px;
    color: var(--color-main);
    background: rgba(255,255,255,0.94);
    border-radius: 14px;
    box-shadow: 0 8px 24px rgba(32,60,54,0.13);
    font-size: 23px;
    line-height: 1.52;
    text-align: left;
    transform: none;
  }
  section.course_cover .cover-author {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 8%;
    color: var(--color-main);
    font-size: 24px;
    text-align: center;
  }
  section.course_cover header,
  section.course_cover footer,
  section.course_cover::after {
    display: none;
  }
  section.course_toc h2 { margin-top: 0.30rem; font-size: 40px; }
  section.course_toc ul { margin-top: 22px; }
  section.course_toc li { font-size: 24px; line-height: 1.44; margin: 0.20rem 0; }
  section.course_toc blockquote { margin: 18px 32px 0 32px; font-size: 21px; }
  section.section_start h2 { font-size: 42px; line-height: 1.22; }
  section.section_start ul, section.section_start ol, section.section_start p { font-size: 26px; }
  section.formula_page p, section.formula_page li { font-size: 24px; }
  section.code_page pre { font-size: 18px; line-height: 1.25; }
  section.code_page p, section.code_page li { font-size: 22px; }
  section.table_page table { font-size: 0.70rem; }
  section.table_page th, section.table_page td { padding: 4px 6px; }
  section.case_page blockquote { font-size: 22px; }
  section.compact_text p, section.compact_text li { font-size: 22px; line-height: 1.28; }
  section.compact_text h2 { font-size: 32px; }
  .tag {
    display: inline-block;
    padding: 2px 9px;
    border-radius: 999px;
    background: rgba(39,132,106,0.12);
    color: var(--color-main);
    font-size: 0.72em;
    margin-right: 4px;
  }
  .card {
    background: rgba(255,255,255,0.92);
    border-left: 6px solid var(--color-coverbg);
    border-radius: 12px;
    padding: 12px 16px;
    box-shadow: 0 5px 16px rgba(32,60,54,0.08);
    margin: 8px 0;
  }
  .small { font-size: 0.75em; }
  .tiny { font-size: 0.64em; }
  .centerbox {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
  }
---

<!-- _class: course_cover -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
# 第2章<br>Python数据处理与材料数据预处理

###### Python Data Processing and Materials Data Preprocessing

<div class="cover-meta">
课程定位：从 Python 科学计算工具进入材料数据分析<br>
学习路径：环境 → 数组 → 表格 → 材料数据 → 清洗 → 可视化 → 可靠性<br>
本章目标：把原始材料数据整理为可建模、可解释、可复现的数据集
</div>

<div class="cover-author">@Shiyan Pan</div>

---

## 本章学习目标

完成本章学习后，应能够：

1. 说明 Python 科学计算环境中 Jupyter、NumPy、Pandas、Matplotlib 的角色。
2. 使用数组和表格结构表达材料成分、工艺、组织和性能数据。
3. 识别材料数据中的缺失值、异常值、重复值、单位不一致和数据泄漏问题。
4. 选择合适的清洗、插补、标准化和异常值处理方法。
5. 使用统计量和图形描述材料数据的分布、相关性和不确定性。
6. 从数据质量和数据偏差角度判断模型结果是否可靠。

---

## 本章知识主线

本章不是单纯的 Python 语法课，而是**材料数据进入 AI 模型前的准备课**。

- 第一层：Python 科学计算环境如何组织数据分析流程？
- 第二层：NumPy、Pandas、Matplotlib 分别解决什么问题？
- 第三层：材料数据有哪些类型、尺度和结构？
- 第四层：为什么清洗和预处理比建模本身更重要？
- 第五层：如何判断数据是否足以支持可信模型？

---

<!-- _class: bq-green case_page -->
## 课堂导入：为什么先讲数据预处理？

材料 AI 建模的常见问题不是“模型太简单”，而是：

- 成分单位混乱：wt.%、at.%、mass fraction 混用
- 工艺参数缺失：温度、时间、冷却速率记录不完整
- 性能数据来源不同：测试标准、试样尺寸、热处理状态不同
- 显微组织标签主观性强：晶粒、相区、缺陷边界不一致
- 数据量小但维度高：几十个样本对应数十个变量

> 数据预处理的目标：把“实验记录”转化为“机器可学习的数据表”。

---

<!-- _class: formula_page -->
## 从材料数据到机器学习样本

材料机器学习通常将每个样本写成：

$$
\left(\mathbf{x}_i, y_i
\right), \quad i=1,2,\ldots,n
$$

其中：

- $\mathbf{x}_i$：第 $i$ 个样本的输入特征
- $y_i$：第 $i$ 个样本的目标性能或类别标签
- $n$：样本数量

材料场景中的 $\mathbf{x}_i$ 往往包含：

$$
\mathbf{x}_i = [\mathbf{c}_i,\mathbf{p}_i,\mathbf{m}_i,\mathbf{s}_i]
$$

- $\mathbf{c}_i$：成分特征；$\mathbf{p}_i$：工艺特征
- $\mathbf{m}_i$：组织特征；$\mathbf{s}_i$：谱图、图像或结构特征

---

<!-- _class: toc_a fglass course_toc -->
<!-- _header: "CONTENTS" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 目录

- 2.1 Python科学计算环境简介
- 2.2 NumPy、Pandas与Matplotlib基础
- 2.3 材料数据类型：成分、工艺、组织、性能、图像、谱图
- 2.4 数据清洗、缺失值处理、异常值识别
- 2.5 材料数据可视化与统计描述
- 2.6 数据质量、数据偏差与模型可靠性

> 先建立数据结构，再处理数据问题，最后讨论可靠性。

---

<!-- _class: trans section_start -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 2.1 Python科学计算环境简介

---

## 2.1 的学习任务

本节回答三个问题：

1. 为什么材料数据分析常用 Python？
2. 一个可复现的科学计算环境应包含哪些要素？
3. Jupyter、脚本、虚拟环境和包管理分别适合什么场景？

学习重点：

- Python 解释器与包管理
- Jupyter Notebook / Lab 的交互式分析
- NumPy、Pandas、Matplotlib 的工具链定位
- 数据文件、代码文件和结果文件的组织方式

---

<!-- _class: bq-blue -->
## Python在科学计算中的定位

Python 适合材料数据分析，核心原因不是“语法简单”，而是生态完整。

- 数值计算：NumPy、SciPy
- 表格处理：Pandas
- 图形绘制：Matplotlib、Plotly
- 机器学习：Scikit-learn、PyTorch、TensorFlow
- 材料专用工具：pymatgen、ASE、matminer、pycalphad
- 交互式分析：Jupyter Notebook / JupyterLab

> Python 是材料数据工作流的“胶水语言”：连接实验数据、模拟结果、数据库和机器学习模型。

---

<!-- _class: table_page -->
## 科学计算环境的基本组成

一个最小可用的 Python 科学计算环境包括：

| 组成 | 作用 | 材料数据场景 |
|---|---|---|
| Python解释器 | 执行代码 | 运行数据处理脚本 |
| 包管理器 | 安装依赖 | numpy、pandas、matplotlib |
| 虚拟环境 | 隔离项目 | 避免版本冲突 |
| 编辑器 | 编写代码 | VS Code、PyCharm |
| Notebook | 交互分析 | 边计算边看图 |
| 文件结构 | 管理数据与结果 | data、src、figures、outputs |

---

<!-- _class: formula_page -->
## 解释器、包和环境

Python 程序运行时依赖三类对象：

- 解释器：决定 Python 版本，例如 Python 3.11
- 包：扩展功能，例如 `numpy`、`pandas`
- 环境：解释器与包的组合

推荐理解为：

$$
\text{项目环境}=\text{Python版本}+\text{依赖包版本}+\text{配置文件}
$$

环境不稳定会导致：

- 同一代码在不同电脑上结果不同
- 包版本升级后接口变化
- 图形或表格输出格式不一致

---

<!-- _class: code_page -->
## Conda与pip的角色

- `conda`：更适合管理完整科学计算环境
  - 可管理 Python 版本
  - 可安装含底层依赖的科学计算包
  - 适合 Windows 科研环境

- `pip`：更接近 Python 官方包安装方式
  - 适合安装纯 Python 包
  - 与 PyPI 包生态连接紧密
  - 常用于补充 conda 中没有的包

建议做法：

```bash
conda create -n ai-bigdata python=3.11
conda activate ai-bigdata
conda install numpy pandas matplotlib scikit-learn jupyter
```

---

<!-- _class: bq-purple -->
## Jupyter Notebook适合做什么？

Jupyter 的优势是交互式探索：

- 逐步读取数据
- 立即查看表格和图像
- 记录分析过程
- 适合课堂演示和初步探索

但 Jupyter 也有风险：

- 单元格执行顺序不清楚
- 中间变量残留
- 不便于大型项目维护
- 不适合作为最终自动化流程

> 建议：探索用 Notebook，稳定流程转化为 `.py` 脚本。

---

<!-- _class: code_page -->
## 脚本文件适合做什么？

`.py` 脚本适合固定、可重复执行的流程：

```text
project/
├── data/
│   ├── raw/              原始数据
│   └── processed/        清洗后数据
├── src/
│   ├── clean_data.py     数据清洗
│   ├── features.py       特征构造
│   └── plot_data.py      绘图
├── figures/              输出图像
├── outputs/              模型结果
└── README.md             项目说明
```

科学研究中的关键要求：

- 原始数据不可覆盖
- 清洗步骤可追踪
- 图表可由代码重新生成

---

<!-- _class: table_page -->
## 材料数据项目的最小目录结构

建议每个材料数据分析项目采用固定结构：

| 文件夹 | 内容 | 注意事项 |
|---|---|---|
| `data/raw` | 原始实验或模拟数据 | 只读，不手工修改 |
| `data/interim` | 中间处理文件 | 可重新生成 |
| `data/processed` | 建模数据集 | 记录字段含义 |
| `notebooks` | 探索性分析 | 文件名加序号 |
| `src` | 可复用函数 | 清洗、绘图、特征工程 |
| `figures` | 图片输出 | 与论文图关联 |
| `reports` | 表格和报告 | 保留生成时间 |

---

<!-- _class: code_page -->
## 第一个可运行示例

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 构造一个简单的材料性能数据表
data = pd.DataFrame({
    "C_wt": [0.05, 0.10, 0.20, 0.40],
    "Mn_wt": [0.5, 0.8, 1.0, 1.2],
    "cooling_rate": [5, 10, 20, 50],
    "hardness_HV": [160, 185, 230, 310]
})

print(data)
data.plot(x="cooling_rate", y="hardness_HV", marker="o")
plt.xlabel("Cooling rate / K s$^{-1}$")
plt.ylabel("Hardness / HV")
plt.show()
```

---

## 科学计算环境小结

本节形成的基本认识：

- Python 是材料数据分析的统一工作平台
- Conda / pip 负责环境和依赖管理
- Jupyter 适合探索，脚本适合复现
- 数据目录结构决定结果能否追踪
- 第2章后续内容都建立在 NumPy、Pandas、Matplotlib 三个基础工具之上

> 下一步：把材料数据放入数组、表格和图形中。

---

<!-- _class: trans section_start -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 2.2 NumPy、Pandas与Matplotlib基础

---

<!-- _class: table_page formula_page -->
## 2.2 的学习任务

本节的核心目标：理解三类基础数据工具的分工。

| 工具 | 核心对象 | 主要用途 |
|---|---|---|
| NumPy | `ndarray` | 数值数组、矩阵运算、向量化计算 |
| Pandas | `Series`、`DataFrame` | 表格数据、索引、分组、缺失值 |
| Matplotlib | `Figure`、`Axes` | 绘制散点图、折线图、直方图等 |

三者关系：

$$
\text{NumPy数组} 
\rightarrow \text{Pandas表格} 
\rightarrow \text{Matplotlib图形}
$$

---

<!-- _class: code_page -->
## NumPy：从列表到数组

Python 列表可以存数据，但不适合大规模数值计算。

```python
# Python列表
c_list = [0.05, 0.10, 0.20, 0.40]

# NumPy数组
import numpy as np
c_array = np.array(c_list)

print(c_array)
print(c_array * 100)
```

NumPy 数组的优点：

- 计算速度快
- 支持向量化运算
- 支持矩阵和张量
- 与科学计算库高度兼容

---

<!-- _class: table_page formula_page -->
## 数组维度：标量、向量、矩阵、张量

材料数据可用不同维度表示：

| 对象 | 数学形式 | Python形状 | 材料示例 |
|---|---|---|---|
| 标量 | $x$ | `()` | 单个硬度值 |
| 向量 | $\mathbf{x}$ | `(d,)` | 一个样本的成分向量 |
| 矩阵 | $\mathbf{X}$ | `(n,d)` | 多个样本的特征表 |
| 张量 | $\mathcal{X}$ | `(n,h,w,c)` | 多张显微组织图像 |

其中 $n$ 为样本数，$d$ 为特征数。

---

<!-- _class: formula_page code_page -->
## 材料成分向量示例

以 Fe-C-Mn-Si 合金为例，成分向量可写为：

$$
\mathbf{c}=[c_{\mathrm{Fe}},c_{\mathrm{C}},c_{\mathrm{Mn}},c_{\mathrm{Si}}]
$$

若使用质量分数，通常满足：

$$
\sum_{j=1}^{d} c_j = 1
$$

Python 表示：

```python
import numpy as np
c = np.array([0.982, 0.004, 0.010, 0.004])
print(c.sum())
```

---

<!-- _class: formula_page code_page -->
## NumPy向量化计算

向量化是 NumPy 的核心思想：一次操作整个数组。

```python
import numpy as np

C = np.array([0.05, 0.10, 0.20, 0.40])
Mn = np.array([0.5, 0.8, 1.0, 1.2])

# 简化的经验硬度估计式，仅用于教学演示
HV = 120 + 300 * C + 20 * Mn
print(HV)
```

数学表达为：

$$
\mathbf{y}=120+300\mathbf{C}+20\mathbf{Mn}
$$

优点：少写循环，表达更接近数学公式。

---

<!-- _class: code_page bq-blue -->
## 广播机制：数组形状自动匹配

NumPy 广播用于处理不同形状数组的运算。

```python
import numpy as np

X = np.array([[0.05, 0.5],
              [0.10, 0.8],
              [0.20, 1.0]])

coef = np.array([300, 20])
y = 120 + X * coef
print(y)
```

广播的意义：

- 将一个系数向量应用到多行样本
- 避免显式循环
- 提高计算效率

> 广播前必须检查数组形状，否则容易产生隐蔽错误。

---

<!-- _class: formula_page code_page -->
## NumPy常用统计函数

```python
import numpy as np

hardness = np.array([160, 185, 230, 310, 295])

print(np.mean(hardness))     # 均值
print(np.std(hardness))      # 标准差
print(np.min(hardness))      # 最小值
print(np.max(hardness))      # 最大值
print(np.percentile(hardness, [25, 50, 75]))
```

对应统计量：

$$
\bar{x}=\frac{1}{n}\sum_{i=1}^{n}x_i
$$

$$
s=\sqrt{\frac{1}{n-1}\sum_{i=1}^{n}(x_i-\bar{x})^2}
$$

---

<!-- _class: code_page -->
## Pandas：表格数据的核心工具

材料数据多数不是单纯数组，而是带列名、单位和样本编号的表格。

```python
import pandas as pd

df = pd.DataFrame({
    "alloy": ["A", "B", "C"],
    "C_wt": [0.05, 0.10, 0.20],
    "Mn_wt": [0.5, 0.8, 1.0],
    "hardness_HV": [160, 185, 230]
})

print(df.head())
print(df.info())
print(df.describe())
```

Pandas 的核心优势：列名、索引、缺失值处理、分组统计。

---

<!-- _class: table_page bq-green -->
## DataFrame的结构

一个 `DataFrame` 可以理解为带标签的二维数据表。

| 组成 | 含义 | 示例 |
|---|---|---|
| 行索引 | 样本编号 | alloy_001 |
| 列名 | 变量名 | C_wt、HV |
| 值 | 具体数据 | 0.12、260 |
| 数据类型 | int、float、object | 数值、字符串 |
| 元数据 | 单位、来源 | wt.%、K、HV |

材料数据表的第一原则：

> 一行一个样本，一列一个变量，一个单元格一个值。

---

<!-- _class: code_page -->
## 读取CSV和Excel数据

```python
import pandas as pd

# 读取CSV文件
df_csv = pd.read_csv("data/raw/alloy_data.csv")

# 读取Excel文件
df_xlsx = pd.read_excel("data/raw/alloy_data.xlsx", sheet_name="Sheet1")

# 查看数据结构
print(df_csv.shape)
print(df_csv.columns)
print(df_csv.head())
```

读取后必须先检查：

- 行数和列数是否符合预期
- 列名是否有空格和乱码
- 数值列是否被读成字符串
- 单位是否写入列名或数据说明文档

---

<!-- _class: code_page formula_page -->
## 选择行、列与条件筛选

```python
# 选择单列
carbon = df["C_wt"]

# 选择多列
features = df[["C_wt", "Mn_wt", "hardness_HV"]]

# 条件筛选：选取碳含量大于0.1 wt.%的样本
high_c = df[df["C_wt"] > 0.10]

# 多条件筛选
selected = df[(df["C_wt"] > 0.10) & (df["hardness_HV"] > 200)]
```

筛选的本质是构造布尔掩码：

$$
\mathbf{m}=[m_1,m_2,\ldots,m_n], \quad m_i\in\{\text{True},\text{False}\}
$$

---

<!-- _class: code_page -->
## 新增列：从原始变量到派生特征

材料数据预处理经常需要构造派生特征。

```python
# 简化碳当量公式，仅用于教学示例
df["CE"] = df["C_wt"] + df["Mn_wt"] / 6

# 工艺复合变量
df["heat_input"] = df["power_W"] / df["scan_speed_mm_s"]

# 取对数变换，处理跨度大的变量
import numpy as np
df["log_cooling_rate"] = np.log10(df["cooling_rate"])
```

派生特征应有物理含义，不能只追求数量。

---

<!-- _class: code_page -->
## 分组统计：按材料类别或工艺分组

```python
# 按热处理状态分组，计算平均硬度和标准差
summary = df.groupby("heat_treatment")["hardness_HV"].agg(["mean", "std", "count"])
print(summary)

# 按合金体系和工艺路线双重分组
summary2 = df.groupby(["alloy_system", "process"])["strength_MPa"].mean()
```

材料场景：

- 按合金体系统计性能
- 按热处理状态比较强度
- 按打印参数区间分析缺陷率
- 按测试温度统计蠕变寿命

---

<!-- _class: code_page -->
## Matplotlib：从数据到图形

Matplotlib 是 Python 基础绘图库。

```python
import matplotlib.pyplot as plt

plt.figure(figsize=(5, 4))
plt.scatter(df["C_wt"], df["hardness_HV"])
plt.xlabel("C / wt.%")
plt.ylabel("Hardness / HV")
plt.title("Effect of carbon on hardness")
plt.tight_layout()
plt.show()
```

图形不是装饰，而是数据诊断工具：

- 看趋势
- 看离群点
- 看分布
- 看数据是否支持建模假设

---

<!-- _class: code_page -->
## Figure与Axes的概念

Matplotlib 图形由两层组成：

- `Figure`：整张画布
- `Axes`：具体绘图区

```python
fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(df["C_wt"], df["hardness_HV"])
ax.set_xlabel("C / wt.%")
ax.set_ylabel("Hardness / HV")
ax.set_title("C-Hardness relation")
plt.show()
```

推荐使用 `fig, ax = plt.subplots()`，便于后续精细控制。

---

<!-- _class: code_page -->
## 三个工具如何协同？

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Pandas读取数据
df = pd.read_csv("alloy_data.csv")

# NumPy进行数值变换
x = df["cooling_rate"].to_numpy()
df["log_rate"] = np.log10(x)

# Matplotlib绘图
fig, ax = plt.subplots()
ax.scatter(df["log_rate"], df["hardness_HV"])
ax.set_xlabel("log10(cooling rate)")
ax.set_ylabel("Hardness / HV")
plt.show()
```

工作流：读取 → 变换 → 可视化 → 诊断。

---

<!-- _class: formula_page -->
## 2.2 小结

本节应形成三个基本能力：

1. 用 NumPy 表达向量、矩阵和数值计算。
2. 用 Pandas 管理带列名和样本编号的材料数据表。
3. 用 Matplotlib 观察数据分布、趋势和异常。

三者分工：

$$
\text{数值计算} 
\rightarrow \text{表格管理} 
\rightarrow \text{图形诊断}
$$

下一节进入材料数据类型：材料数据为什么比普通表格数据更复杂？

---

<!-- _class: trans section_start -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 2.3 材料数据类型

---

<!-- _class: bq-blue -->
## 2.3 的学习任务

材料数据不是单一类型的数据，而是多源、多尺度、多模态数据。

本节将材料数据分为六类：

1. 成分数据
2. 工艺数据
3. 组织数据
4. 性能数据
5. 图像数据
6. 谱图数据

核心问题：

> 如何把不同来源、不同尺度、不同格式的材料信息组织成可分析的数据结构？

---

<!-- _class: formula_page -->
## 材料数据的“结构—工艺—性能”框架

材料科学常用关系链：

$$
\text{成分} + \text{工艺} 
\rightarrow \text{组织结构} 
\rightarrow \text{性能}
$$

进一步可写为：

$$
\mathbf{y}=f(\mathbf{c},\mathbf{p},\mathbf{m})
$$

其中：

- $\mathbf{c}$：成分向量
- $\mathbf{p}$：工艺参数向量
- $\mathbf{m}$：组织结构描述符
- $\mathbf{y}$：性能向量

AI 的任务是从数据中近似未知映射 $f$。

---

## 成分数据：材料最基本的输入

成分数据通常包括：

- 元素种类：Fe、C、Mn、Si、Ni、Cr 等
- 含量单位：wt.%、at.%、mass fraction
- 主元素与微量元素
- 杂质元素：O、N、S、P 等

成分数据的常见问题：

- 单位混用
- 元素缺失被误认为 0
- 总和不为 100%
- 检测下限以下数据未注明

> 成分数据看似简单，但最容易产生单位和归一化错误。

---

<!-- _class: table_page -->
## 成分数据表的推荐格式

| sample_id | Fe_wt | C_wt | Mn_wt | Si_wt | Cr_wt | Ni_wt |
|---|---:|---:|---:|---:|---:|---:|
| S001 | 98.20 | 0.20 | 1.10 | 0.30 | 0.10 | 0.10 |
| S002 | 97.80 | 0.35 | 1.20 | 0.40 | 0.15 | 0.10 |
| S003 | 96.50 | 0.10 | 0.80 | 0.20 | 1.50 | 0.90 |

推荐规则：

- 列名中写清单位
- 不同单位不要放在同一列
- 未检测与真实为 0 要区分
- 保留原始报告文件或检测仪器信息

---

<!-- _class: formula_page code_page -->
## 成分归一化

若成分总和不是 1 或 100%，常需要归一化：

$$
\tilde{c}_j=\frac{c_j}{\sum_{k=1}^{d}c_k}
$$

Python 示例：

```python
import pandas as pd

cols = ["Fe_wt", "C_wt", "Mn_wt", "Si_wt"]
row_sum = df[cols].sum(axis=1)
df_norm = df[cols].div(row_sum, axis=0)
```

注意：归一化前应判断是否需要保留杂质、空位或未测元素。

---

<!-- _class: formula_page -->
## wt.% 与 at.% 的转换思想

质量分数到原子分数的基本关系：

$$
x_j=\frac{w_j/M_j}{\sum_{k=1}^{d} w_k/M_k}
$$

其中：

- $x_j$：元素 $j$ 的原子分数
- $w_j$：元素 $j$ 的质量分数
- $M_j$：元素 $j$ 的摩尔质量

该转换在相图计算、热力学建模和第一性原理数据整合中很常见。

---

<!-- _class: code_page -->
## wt.% 到 at.% 的Python示例

```python
import pandas as pd

comp_wt = pd.Series({"Fe": 98.0, "C": 0.2, "Mn": 1.5, "Si": 0.3})
M = pd.Series({"Fe": 55.845, "C": 12.011, "Mn": 54.938, "Si": 28.085})

moles = comp_wt / M
comp_at = moles / moles.sum()

print(comp_at * 100)
```

结果解释：

- 轻元素 C 的 at.% 往往显著高于 wt.%
- 单位转换会改变模型输入分布
- 建模前必须明确使用何种成分尺度

---

## 工艺数据：过程决定组织

工艺数据描述材料如何被制备或加工：

- 铸造：浇注温度、冷却速率、过冷度
- 热处理：固溶温度、保温时间、时效温度
- 焊接：电流、电压、焊速、保护气体
- 增材制造：激光功率、扫描速度、层厚、道间距
- 轧制/锻造：变形量、应变速率、温度

工艺数据通常是材料数据中最不规范的一类。

---

<!-- _class: formula_page -->
## 工艺参数的派生特征

在增材制造中，常用体积能量密度作为简化工艺指标：

$$
E=\frac{P}{v h t}
$$

其中：

- $P$：激光功率
- $v$：扫描速度
- $h$：道间距
- $t$：层厚

注意：$E$ 是简化指标，不等价于真实热输入场。真实组织演化还受热传导、熔池流动和重复热循环影响。

---

<!-- _class: code_page -->
## 工艺派生特征代码示例

```python
# P: W, v: mm/s, h: mm, t: mm
# E: J/mm^3
df["energy_density"] = (
    df["laser_power_W"] /
    (df["scan_speed_mm_s"] * df["hatch_spacing_mm"] * df["layer_thickness_mm"])
)

# 焊接线能量，单位 J/mm
df["line_energy"] = df["voltage_V"] * df["current_A"] / df["welding_speed_mm_s"]
```

派生特征必须记录公式和单位，否则难以复现。

---

## 组织数据：连接工艺与性能的桥梁

显微组织数据可以来自：

- 光学显微镜图像
- SEM / TEM 图像
- EBSD 晶粒与取向数据
- XRD 相组成数据
- 相场、元胞自动机、分子动力学模拟结果

组织描述符示例：

- 晶粒尺寸
- 第二相体积分数
- 枝晶臂间距
- 孔隙率
- 织构强度
- 相界面密度

---

<!-- _class: table_page -->
## 组织描述符的数据表

| sample_id | grain_size_um | phase_alpha_frac | porosity_pct | texture_index |
|---|---:|---:|---:|---:|
| S001 | 12.5 | 0.32 | 0.20 | 1.8 |
| S002 | 8.4 | 0.45 | 0.35 | 2.3 |
| S003 | 20.1 | 0.18 | 0.10 | 1.2 |

组织数据的主要难点：

- 图像区域是否有代表性
- 阈值分割是否稳定
- 人工标注是否一致
- 尺度从纳米到毫米跨越很大

---

## 性能数据：模型预测目标

性能数据可以是标量，也可以是曲线或多目标。

常见性能：

- 力学性能：屈服强度、抗拉强度、硬度、延伸率
- 热学性能：热导率、热膨胀系数
- 电学性能：电导率、电阻率
- 化学性能：腐蚀电流密度、氧化增重
- 服役性能：疲劳寿命、蠕变寿命、磨损率

关键问题：性能不是材料固有常数，往往依赖测试条件。

---

<!-- _class: table_page -->
## 性能数据必须记录测试条件

同一材料的性能数据应同时记录：

| 性能 | 必要条件 | 说明 |
|---|---|---|
| 硬度 | 载荷、保载时间、测试位置 | HV0.2 与 HV10 不可混用 |
| 拉伸强度 | 试样尺寸、应变速率、温度 | 室温与高温不可直接合并 |
| 疲劳寿命 | 应力比、频率、环境 | 寿命常需对数处理 |
| 腐蚀性能 | 溶液、温度、扫描速率 | 测试体系决定结果 |

缺少测试条件的性能数据不适合直接作为高可信标签。

---

<!-- _class: formula_page -->
## 图像数据：从像素到特征

显微组织图像可表示为张量：

$$
\mathcal{I}\in\mathbb{R}^{H\times W\times C}
$$

其中：

- $H$：图像高度
- $W$：图像宽度
- $C$：通道数，灰度图为 1，彩色图为 3

图像数据处理要点：

- 像素尺寸标定
- 亮度和对比度一致化
- 裁剪区域代表性
- 标签定义一致
- 避免同一原图切片同时进入训练集和测试集

---

<!-- _class: table_page -->
## 图像文件与标签表

图像数据不宜直接塞进 Excel，应采用“文件路径 + 标签表”的方式：

| image_id | file_path | alloy | process | label |
|---|---|---|---|---|
| I001 | images/S001_01.png | Fe-C | casting | dendrite |
| I002 | images/S001_02.png | Fe-C | casting | dendrite |
| I003 | images/S002_01.png | Ti alloy | AM | pore |

优点：

- 图像文件单独存储
- 标签和元数据可检索
- 便于批量读取和训练

---

<!-- _class: formula_page -->
## 谱图数据：曲线型材料数据

谱图数据包括：

- XRD：衍射强度随 $2\theta$ 变化
- Raman：强度随波数变化
- FTIR：吸收强度随波数变化
- XPS：强度随结合能变化
- EDS：强度随能量变化

谱图可视为一维信号：

$$
\mathbf{s}=[I(x_1),I(x_2),\ldots,I(x_m)]
$$

其中 $x$ 可以是角度、能量或波数。

---

## 谱图数据处理的基本步骤

谱图进入机器学习前通常需要：

1. 横坐标统一：插值到同一网格
2. 背景扣除：去除基线漂移
3. 平滑去噪：降低测量噪声
4. 强度归一化：消除总体强度差异
5. 峰位和峰面积提取：构造物理特征

注意：过度平滑可能抹掉真实峰信息；背景扣除方法应固定并记录。

---

<!-- _class: code_page -->
## 多源材料数据整合

多源数据整合的关键是样本主键：

```text
sample_id
  ├── composition.csv
  ├── process.csv
  ├── microstructure.csv
  ├── property.csv
  ├── images/*.png
  └── spectra/*.csv
```

推荐原则：

- 每个样本有唯一 `sample_id`
- 不同数据表通过 `sample_id` 合并
- 原始数据与处理数据分离
- 记录数据来源、测试条件和处理步骤

---

<!-- _class: code_page -->
## Pandas合并多张材料数据表

```python
comp = pd.read_csv("composition.csv")
proc = pd.read_csv("process.csv")
prop = pd.read_csv("property.csv")

# 按 sample_id 合并
alloy_data = comp.merge(proc, on="sample_id", how="inner")
alloy_data = alloy_data.merge(prop, on="sample_id", how="inner")

print(alloy_data.shape)
print(alloy_data.head())
```

合并前必须检查：

- `sample_id` 是否唯一
- 是否存在重复样本
- `inner`、`left`、`outer` 合并方式是否合理

---

## 2.3 小结

材料数据的复杂性来自：

- 多源：实验、模拟、文献、数据库
- 多尺度：电子、原子、晶粒、构件
- 多模态：表格、图像、谱图、文本
- 多单位：质量分数、原子分数、温度、时间、能量密度
- 强物理约束：成分守恒、相变路径、测试条件依赖

> 下一节讨论：这些数据进入模型前必须如何清洗。

---

<!-- _class: trans section_start -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 2.4 数据清洗、缺失值处理、异常值识别

---

<!-- _class: bq-blue -->
## 2.4 的学习任务

数据清洗是材料 AI 建模前最关键的环节。

本节重点：

1. 数据清洗的基本流程
2. 重复值、单位错误和类型错误处理
3. 缺失值识别与插补
4. 异常值识别：统计方法与物理判断
5. 标准化、归一化与特征尺度处理
6. 数据泄漏与预处理顺序

核心观点：

> 清洗不是“美化数据”，而是把数据问题显式化、可追踪化。

---

<!-- _class: table_page -->
## 原始数据常见问题清单

| 问题 | 表现 | 后果 |
|---|---|---|
| 缺失值 | 空白、NA、--、未检出 | 模型无法训练或产生偏差 |
| 重复值 | 同一样本重复录入 | 过度代表某类样本 |
| 单位混乱 | mm/s 与 m/s 混用 | 数值量级错误 |
| 类型错误 | 数值读成字符串 | 统计计算失败 |
| 异常值 | 远离总体分布 | 扭曲模型参数 |
| 数据泄漏 | 测试集信息进入训练 | 评估结果虚高 |

材料数据清洗必须同时依赖统计判断和材料知识。

---

<!-- _class: code_page -->
## 数据清洗的基本流程

推荐流程：

```text
读取原始数据
  ↓
检查行列、字段、单位和数据类型
  ↓
处理重复样本和明显录入错误
  ↓
识别缺失值并分析缺失机制
  ↓
识别异常值并区分错误与真实极端样本
  ↓
标准化、编码和特征构造
  ↓
保存处理后数据并记录处理日志
```

注意：处理顺序应固定，并能由代码重新运行。

---

<!-- _class: code_page -->
## 读取后第一步：快速体检

```python
import pandas as pd

df = pd.read_csv("data/raw/alloy_data.csv")

print(df.shape)
print(df.columns)
print(df.head())
print(df.info())
print(df.describe(include="all"))
```

重点观察：

- 样本数是否符合预期
- 列名是否有空格、中文括号和特殊符号
- 数值列是否存在字符串
- 类别列是否有拼写不一致
- 最大值和最小值是否物理合理

---

<!-- _class: code_page -->
## 列名规范化

不规范列名会导致代码难以维护。

```python
# 原始列名可能为："C (wt%)", "Cooling Rate/Ks-1"
df.columns = (
    df.columns
      .str.strip()
      .str.replace(" ", "_")
      .str.replace("(", "", regex=False)
      .str.replace(")", "", regex=False)
      .str.lower()
)

print(df.columns)
```

推荐列名：

- `c_wt`
- `mn_wt`
- `cooling_rate_k_s`
- `hardness_hv`

---

<!-- _class: code_page -->
## 数据类型检查与转换

```python
# 查看每列类型
print(df.dtypes)

# 将字符串数值转为浮点数，错误值转为 NaN
df["c_wt"] = pd.to_numeric(df["c_wt"], errors="coerce")

# 类别变量统一为字符串
df["process"] = df["process"].astype("string")
```

常见问题：

- `"0.25"` 被读成字符串
- `"<0.01"` 无法直接转数值
- `"未测"`、`"--"`、`"N/A"` 含义不同
- 数字中的中文单位未剥离

---

<!-- _class: code_page -->
## 重复值检查

```python
# 检查完全重复行
print(df.duplicated().sum())

# 根据 sample_id 检查重复样本
print(df["sample_id"].duplicated().sum())

# 查看重复记录
duplicates = df[df["sample_id"].duplicated(keep=False)]
print(duplicates)
```

处理原则：

- 完全重复：通常可删除
- 同一样本多次测试：应保留并记录为重复测量
- 同一编号对应不同数据：需回查原始记录

---

<!-- _class: code_page -->
## 单位一致化

单位错误是材料数据中最严重的问题之一。

示例：扫描速度统一为 `mm/s`。

```python
# 若原始数据有速度值和单位两列
def convert_speed(row):
    if row["speed_unit"] == "m/s":
        return row["speed"] * 1000
    elif row["speed_unit"] == "mm/s":
        return row["speed"]
    else:
        return None

df["scan_speed_mm_s"] = df.apply(convert_speed, axis=1)
```

原则：单位转换必须写入代码，不建议手工改 Excel。

---

<!-- _class: formula_page code_page -->
## 缺失值的基本识别

```python
# 每列缺失值数量
missing_count = df.isna().sum()

# 每列缺失率
missing_ratio = df.isna().mean()

summary = pd.DataFrame({
    "missing_count": missing_count,
    "missing_ratio": missing_ratio
})
print(summary.sort_values("missing_ratio", ascending=False))
```

缺失率定义：

$$
r_j=\frac{n_{\mathrm{missing},j}}{n}
$$

其中 $r_j$ 为第 $j$ 列的缺失比例。

---

<!-- _class: table_page -->
## 缺失值不是一种情况

缺失机制影响处理方法：

| 缺失机制 | 含义 | 示例 | 处理思路 |
|---|---|---|---|
| 完全随机缺失 | 与变量无关 | 仪器偶然故障 | 删除或插补 |
| 随机缺失 | 与观测变量有关 | 高温样本更易漏记 | 建模插补 |
| 非随机缺失 | 与缺失值自身有关 | 低于检测限未报告 | 不能简单插补 |

材料数据中“未检出”不等于 0，也不等于普通缺失。

---

<!-- _class: code_page -->
## 缺失值处理策略一：删除

删除适合缺失少且不影响样本代表性的情况。

```python
# 删除目标值缺失的样本
df1 = df.dropna(subset=["hardness_hv"])

# 删除缺失率过高的列
threshold = 0.5
cols_keep = df.columns[df.isna().mean() < threshold]
df2 = df[cols_keep]
```

风险：

- 小样本材料数据删除后样本更少
- 若缺失与工艺或性能相关，会产生选择偏差
- 删除前应报告删除比例和原因

---

<!-- _class: formula_page code_page -->
## 缺失值处理策略二：简单插补

常见插补方法：

$$
\tilde{x}_{ij}=\begin{cases}
x_{ij}, & \text{若观测到} \\
\mu_j, & \text{若缺失且采用均值插补}
\end{cases}
$$

Python 示例：

```python
from sklearn.impute import SimpleImputer

num_cols = ["c_wt", "mn_wt", "cooling_rate_k_s"]
imputer = SimpleImputer(strategy="median")
X_imp = imputer.fit_transform(df[num_cols])
```

中位数插补比均值插补对异常值更稳健。

---

<!-- _class: code_page -->
## 缺失值处理策略三：分组插补

若不同合金体系分布差异很大，应考虑分组插补。

```python
# 按合金体系用组内中位数插补硬度
med = df.groupby("alloy_system")["hardness_hv"].transform("median")
df["hardness_hv_filled"] = df["hardness_hv"].fillna(med)
```

适用场景：

- 不同材料体系的性能水平差异明显
- 不同工艺路线的数据分布不同
- 样本量允许在组内估计统计量

注意：不能使用目标变量未来信息进行插补。

---

<!-- _class: formula_page code_page -->
## 缺失指示变量

缺失本身可能包含信息。例如“某元素未检出”可能代表含量低。

```python
# 创建缺失指示变量
df["o_missing"] = df["o_wt"].isna().astype(int)

# 再对原始列插补
df["o_wt"] = df["o_wt"].fillna(0.0)
```

数学表示：

$$
m_{ij}=\begin{cases}
1, & \text{若 }x_{ij}\text{ 缺失} \\
0, & \text{若 }x_{ij}\text{ 被观测}
\end{cases}
$$

缺失指示变量可帮助模型识别“未测”和“真实为零”的差异。

---

<!-- _class: bq-red -->
## 异常值：错误还是重要样本？

异常值有两种完全不同的含义：

1. 数据错误
   - 小数点录错
   - 单位转换错误
   - 仪器故障
   - 样本编号错配

2. 真实极端样本
   - 特殊工艺导致超高强度
   - 相变路径不同
   - 缺陷导致性能异常降低

> 材料数据中不能只靠统计规则删除异常值，必须结合物理和实验记录判断。

---

<!-- _class: formula_page code_page -->
## 单变量异常值：Z-score方法

Z-score 定义为：

$$
z_i=\frac{x_i-\mu}{\sigma}
$$

常用规则：

$$
|z_i|>3 \Rightarrow \text{可能为异常值}
$$

Python 示例：

```python
x = df["hardness_hv"]
z = (x - x.mean()) / x.std()
outliers = df[z.abs() > 3]
print(outliers)
```

缺点：均值和标准差本身会受异常值影响。

---

<!-- _class: formula_page code_page -->
## 单变量异常值：IQR方法

四分位距：

$$
\mathrm{IQR}=Q_3-Q_1
$$

异常值判据：

$$
x<Q_1-1.5\mathrm{IQR}\quad \text{或}\quad x>Q_3+1.5\mathrm{IQR}
$$

Python 示例：

```python
x = df["hardness_hv"]
q1 = x.quantile(0.25)
q3 = x.quantile(0.75)
iqr = q3 - q1
mask = (x < q1 - 1.5 * iqr) | (x > q3 + 1.5 * iqr)
print(df[mask])
```

---

<!-- _class: formula_page -->
## 多变量异常值：马氏距离

多变量异常值不一定在单个变量上极端。

马氏距离：

$$
D_M^2=(\mathbf{x}-\boldsymbol{\mu})^{\mathrm{T}}\mathbf{\Sigma}^{-1}(\mathbf{x}-\boldsymbol{\mu})
$$

其中：

- $\boldsymbol{\mu}$：均值向量
- $\mathbf{\Sigma}$：协方差矩阵

意义：考虑变量相关性后的距离。

材料场景：某个样本的 C 和 Mn 单独看正常，但组合关系不符合合金设计规律。

---

<!-- _class: code_page -->
## 多变量异常值代码示例

```python
import numpy as np

cols = ["c_wt", "mn_wt", "si_wt", "hardness_hv"]
X = df[cols].dropna().to_numpy()

mu = X.mean(axis=0)
Sigma = np.cov(X, rowvar=False)
Sigma_inv = np.linalg.pinv(Sigma)

diff = X - mu
D2 = np.sum(diff @ Sigma_inv * diff, axis=1)

print(D2)
```

注意：样本量很小时协方差矩阵估计不稳定。

---

<!-- _class: table_page -->
## 异常值处理的四种方式

| 方式 | 适用情况 | 风险 |
|---|---|---|
| 回查更正 | 明确录入或单位错误 | 需要原始记录 |
| 删除 | 明确为错误数据 | 可能删除真实机制 |
| 截尾/Winsorize | 极端值影响统计量 | 改变真实分布 |
| 保留并标注 | 可能是真实极端样本 | 模型可能受影响 |

推荐实践：

- 不要静默删除异常值
- 记录异常判断依据
- 报告处理前后样本数和分布变化

---

<!-- _class: formula_page -->
## 标准化：让变量具有可比尺度

标准化公式：

$$
x'_{ij}=\frac{x_{ij}-\mu_j}{\sigma_j}
$$

其中：

- $\mu_j$：第 $j$ 个特征的均值
- $\sigma_j$：第 $j$ 个特征的标准差

适用场景：

- 线性模型
- 支持向量机
- KNN
- 神经网络
- 主成分分析

随机森林等树模型通常对尺度不敏感。

---

<!-- _class: formula_page code_page -->
## 归一化：压缩到固定范围

Min-Max 归一化：

$$
x'_{ij}=\frac{x_{ij}-x_{j,\min}}{x_{j,\max}-x_{j,\min}}
$$

Python 示例：

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

cols = ["c_wt", "mn_wt", "cooling_rate_k_s"]

scaler = StandardScaler()
X_std = scaler.fit_transform(df[cols])

minmax = MinMaxScaler()
X_mm = minmax.fit_transform(df[cols])
```

注意：`fit` 只能在训练集上进行，不能在全数据上进行。

---

<!-- _class: bq-red -->
## 数据泄漏：最容易忽略的错误

数据泄漏指测试集信息以某种方式进入训练过程。

典型错误：

- 先对全数据标准化，再划分训练集和测试集
- 先对全数据插补，再划分训练集和测试集
- 同一显微组织原图裁剪出的子图同时出现在训练集和测试集
- 用包含目标信息的派生变量作为输入特征

正确原则：

> 任何需要“学习参数”的预处理步骤，只能在训练集上 `fit`。

---

<!-- _class: code_page -->
## 正确的预处理顺序

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

X = df[["c_wt", "mn_wt", "cooling_rate_k_s"]]
y = df["hardness_hv"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=0
)

pipe = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

X_train_p = pipe.fit_transform(X_train)
X_test_p = pipe.transform(X_test)
```

---

## 2.4 小结

数据清洗应形成可复现流程：

1. 检查结构：行列、类型、列名、单位
2. 处理错误：重复、明显录入错误、单位不一致
3. 处理缺失：识别机制、选择删除或插补
4. 处理异常：统计判断 + 物理判断
5. 特征尺度：标准化、归一化、编码
6. 避免泄漏：训练集拟合，测试集只变换

> 下一节：用统计图形检查清洗后的材料数据。

---

<!-- _class: trans section_start -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 2.5 材料数据可视化与统计描述

---

## 2.5 的学习任务

可视化与统计描述用于回答：

- 数据分布是什么样？
- 是否存在离群点或分组差异？
- 输入变量和目标性能是否相关？
- 数据是否足以支持后续机器学习？

本节重点：

1. 基本统计量
2. 直方图、箱线图、散点图
3. 相关系数与热图
4. 多变量图形
5. 材料图像和谱图的可视化

---

<!-- _class: table_page formula_page -->
## 描述性统计量

常用统计量：

| 统计量 | 公式或含义 | 用途 |
|---|---|---|
| 均值 | $\bar{x}$ | 集中趋势 |
| 中位数 | $Q_2$ | 抗异常值 |
| 标准差 | $s$ | 离散程度 |
| 四分位数 | $Q_1,Q_3$ | 分布范围 |
| 偏度 | 分布不对称性 | 判断长尾 |
| 相关系数 | $r$ | 变量关系 |

描述统计不是结论，而是建模前的数据诊断。

---

<!-- _class: code_page -->
## Pandas描述统计

```python
# 数值列统计
print(df.describe())

# 指定列统计
cols = ["c_wt", "mn_wt", "cooling_rate_k_s", "hardness_hv"]
print(df[cols].describe())

# 类别列频数
print(df["process"].value_counts())
```

观察重点：

- `count` 是否一致
- `min` 和 `max` 是否物理合理
- `mean` 与 `50%` 差异是否很大
- 某些类别样本是否过少

---

<!-- _class: code_page -->
## 直方图：看单变量分布

```python
fig, ax = plt.subplots(figsize=(5, 4))
ax.hist(df["hardness_hv"].dropna(), bins=15, edgecolor="black")
ax.set_xlabel("Hardness / HV")
ax.set_ylabel("Count")
ax.set_title("Distribution of hardness")
plt.tight_layout()
plt.show()
```

直方图用于检查：

- 是否近似正态分布
- 是否长尾
- 是否多峰
- 是否有明显异常值

---

<!-- _class: code_page -->
## 箱线图：看离群点和分组差异

```python
fig, ax = plt.subplots(figsize=(5, 4))
df.boxplot(column="hardness_hv", by="process", ax=ax)
ax.set_xlabel("Process")
ax.set_ylabel("Hardness / HV")
plt.suptitle("")
plt.tight_layout()
plt.show()
```

箱线图包含：

- 中位数
- 上下四分位数
- 四分位距
- 可能离群点

适合比较不同工艺路线的性能分布。

---

<!-- _class: code_page -->
## 散点图：看变量关系

```python
fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(df["cooling_rate_k_s"], df["hardness_hv"])
ax.set_xscale("log")
ax.set_xlabel("Cooling rate / K s$^{-1}$")
ax.set_ylabel("Hardness / HV")
plt.tight_layout()
plt.show()
```

散点图可以判断：

- 是否近似线性
- 是否存在阈值效应
- 是否存在不同分组
- 是否存在高杠杆点

---

<!-- _class: formula_page -->
## 相关系数

Pearson 相关系数：

$$
r_{xy}=\frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i-\bar{x})^2}\sqrt{\sum_{i=1}^{n}(y_i-\bar{y})^2}}
$$

取值范围：

$$
-1\le r_{xy}\le 1
$$

解释：

- $r>0$：正相关
- $r<0$：负相关
- $r\approx0$：线性相关弱，但不代表无非线性关系

---

<!-- _class: code_page -->
## 相关矩阵计算

```python
cols = ["c_wt", "mn_wt", "si_wt", "cooling_rate_k_s", "hardness_hv"]
corr = df[cols].corr(method="pearson")
print(corr)

fig, ax = plt.subplots(figsize=(5, 4))
im = ax.imshow(corr, vmin=-1, vmax=1)
ax.set_xticks(range(len(cols)), labels=cols, rotation=45, ha="right")
ax.set_yticks(range(len(cols)), labels=cols)
fig.colorbar(im, ax=ax)
plt.tight_layout()
plt.show()
```

相关性不能直接解释为因果关系。

---

<!-- _class: formula_page code_page -->
## 分组均值与误差棒

```python
summary = df.groupby("process")["hardness_hv"].agg(["mean", "std", "count"])
summary["sem"] = summary["std"] / summary["count"]**0.5

fig, ax = plt.subplots(figsize=(5, 4))
ax.errorbar(summary.index, summary["mean"], yerr=summary["sem"], fmt="o")
ax.set_xlabel("Process")
ax.set_ylabel("Hardness / HV")
plt.tight_layout()
plt.show()
```

标准误：

$$
\mathrm{SEM}=\frac{s}{\sqrt{n}}
$$

---

<!-- _class: formula_page code_page -->
## 成分三元图的思想

对于三元合金 A-B-C：

$$
c_A+c_B+c_C=1
$$

三元图用于展示成分空间中的性能分布。

课堂中可先用二维投影近似理解：

```python
fig, ax = plt.subplots(figsize=(5, 4))
sc = ax.scatter(df["cr_wt"], df["ni_wt"], c=df["hardness_hv"])
ax.set_xlabel("Cr / wt.%")
ax.set_ylabel("Ni / wt.%")
fig.colorbar(sc, ax=ax, label="Hardness / HV")
plt.show()
```

颜色表示目标性能或相组成。

---

<!-- _class: code_page -->
## 工艺窗口图

增材制造中常用二维工艺图观察质量区间：

```python
fig, ax = plt.subplots(figsize=(5, 4))
sc = ax.scatter(
    df["laser_power_W"],
    df["scan_speed_mm_s"],
    c=df["relative_density_pct"]
)
ax.set_xlabel("Laser power / W")
ax.set_ylabel("Scan speed / mm s$^{-1}$")
fig.colorbar(sc, ax=ax, label="Relative density / %")
plt.show()
```

可用于识别：

- 未熔合区
- 稳定成形区
- 过热或匙孔区

---

<!-- _class: code_page -->
## 显微组织图像可视化

```python
import matplotlib.pyplot as plt
from matplotlib.image import imread

img = imread("images/microstructure_001.png")

fig, ax = plt.subplots(figsize=(5, 4))
ax.imshow(img, cmap="gray")
ax.axis("off")
ax.set_title("Microstructure image")
plt.show()
```

图像可视化注意事项：

- 是否有比例尺
- 是否裁剪了关键区域
- 是否改变了灰度范围
- 是否保留原始图像文件

---

<!-- _class: code_page -->
## 谱图可视化

```python
spec = pd.read_csv("spectra/xrd_s001.csv")

fig, ax = plt.subplots(figsize=(5, 4))
ax.plot(spec["two_theta"], spec["intensity"])
ax.set_xlabel(r"$2\theta$ / degree")
ax.set_ylabel("Intensity")
ax.set_title("XRD pattern")
plt.tight_layout()
plt.show()
```

谱图诊断重点：

- 峰位是否偏移
- 背景是否漂移
- 峰宽是否异常
- 多个样本横坐标是否一致

---

<!-- _class: bq-green -->
## 可视化的科研规范

材料论文和报告中的图形应满足：

- 坐标轴有物理量和单位
- 图例说明分组含义
- 不使用误导性坐标范围
- 不随意删除离群点
- 图形可由代码重新生成
- 文件命名与样本编号一致

> 图形是证据链的一部分，而不是最后的装饰。

---

## 2.5 小结

可视化与统计描述的目标：

1. 发现数据问题
2. 理解变量分布
3. 识别分组差异
4. 判断相关关系
5. 为后续模型选择提供依据

常用图形：

- 直方图：分布
- 箱线图：离群点和分组差异
- 散点图：变量关系
- 热图：相关矩阵
- 图像/谱图：多模态数据诊断

下一节：数据看起来合理，是否就意味着模型可靠？

---

<!-- _class: trans section_start -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 2.6 数据质量、数据偏差与模型可靠性

---

<!-- _class: bq-blue -->
## 2.6 的学习任务

本节讨论更高层次的问题：

- 数据质量如何影响模型可靠性？
- 数据偏差为什么会导致错误结论？
- 小样本材料数据如何避免过度解释？
- 如何建立可复现的数据处理记录？

核心观点：

> 模型预测能力的上限，往往由数据质量决定，而不是由算法名称决定。

---

<!-- _class: table_page -->
## 数据质量的六个维度

| 维度 | 含义 | 材料数据示例 |
|---|---|---|
| 准确性 | 数值是否正确 | 成分检测误差 |
| 完整性 | 关键字段是否缺失 | 热处理时间缺失 |
| 一致性 | 单位和标准是否统一 | HV与HRC混用 |
| 代表性 | 样本是否覆盖目标空间 | 只包含高性能样本 |
| 可追溯性 | 来源是否清楚 | 文献数据缺少测试条件 |
| 可复现性 | 能否重复生成数据集 | 清洗步骤无代码 |

数据质量应在建模前评估，而不是模型失败后补救。

---

## 数据偏差一：选择偏差

选择偏差指样本不是目标总体的代表。

材料案例：

- 文献通常更倾向发表性能较好的材料
- 失败实验和低性能样本较少进入数据库
- 某些合金体系研究较多，其他体系样本稀疏
- 工艺参数集中在少数可成形区域

后果：

- 模型会高估平均性能
- 模型在低性能或失败区域外推能力差
- 优化算法可能给出不可制造方案

---

## 数据偏差二：测量偏差

测量偏差来自仪器、方法或标准差异。

示例：

- 不同硬度载荷得到不同数值
- 不同腐蚀溶液下的腐蚀电流不可直接比较
- 不同显微镜放大倍数影响组织统计
- 不同实验室的热处理炉温标定不同

处理方式：

- 保留测试标准和条件
- 引入实验室或仪器作为元数据
- 对不同来源数据进行分层分析
- 必要时只整合同一标准下的数据

---

## 数据偏差三：标签偏差

标签偏差指目标值或类别标签存在系统性偏差。

显微组织识别中的常见问题：

- 不同标注者对晶界、孔洞、第二相边界理解不同
- 图像标签来自样本整体，但图像局部并不代表整体
- “缺陷”标签可能混合孔洞、裂纹、未熔合等不同机制
- 分类标签过粗，掩盖连续组织演化

建议：

- 制定标注准则
- 多人标注并评估一致性
- 保存原始标签和修订标签
- 不确定样本单独标记

---

<!-- _class: formula_page -->
## 小样本与高维特征

材料数据常见状态：

$$
n \ll d
$$

其中：

- $n$：样本数量
- $d$：特征数量

问题：

- 模型容易记住训练样本
- 交叉验证波动大
- 特征重要性不稳定
- 高精度可能是假象

解决思路：

- 减少无物理意义特征
- 使用正则化
- 引入先验知识
- 报告不确定性而非单一指标

---

<!-- _class: formula_page -->
## 外推风险

模型通常只在训练数据覆盖范围内可靠。

若训练数据满足：

$$
\mathbf{x}\in\Omega_{\mathrm{train}}
$$

而预测点位于：

$$
\mathbf{x}^{*}
otin\Omega_{\mathrm{train}}
$$

则属于外推预测。

材料案例：

- 用低碳钢数据预测高碳钢
- 用铸造数据预测增材制造数据
- 用室温性能数据预测高温性能
- 用低冷却速率数据预测极快凝固过程

---

<!-- _class: code_page -->
## 可靠性检查：训练集覆盖范围

```python
features = ["c_wt", "mn_wt", "cooling_rate_k_s"]

for col in features:
    print(col, df[col].min(), df[col].max())

# 检查一个新样本是否超出训练范围
new_sample = {"c_wt": 0.8, "mn_wt": 1.0, "cooling_rate_k_s": 1000}
for col, value in new_sample.items():
    low, high = df[col].min(), df[col].max()
    print(col, low <= value <= high)
```

超出范围不代表不能预测，但必须标注为低可信外推。

---

## 数据划分与重复样本问题

材料数据划分不能只随机切分。

高风险情形：

- 同一材料多次测试数据同时进入训练集和测试集
- 同一显微图像切成多个 patch 后随机划分
- 同一文献中的相近样本同时出现在训练和测试中
- 同一模拟参数微扰样本被分散到不同集合

建议：

- 按样本编号分组划分
- 按文献来源分组验证
- 按合金体系外推验证
- 按工艺路线外推验证

---

<!-- _class: code_page -->
## 分组划分示例

```python
from sklearn.model_selection import GroupShuffleSplit

X = df[["c_wt", "mn_wt", "cooling_rate_k_s"]]
y = df["hardness_hv"]
groups = df["sample_id"]

splitter = GroupShuffleSplit(test_size=0.2, random_state=0)
train_idx, test_idx = next(splitter.split(X, y, groups=groups))

X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
```

分组划分可以降低重复样本造成的虚高评估。

---

<!-- _class: formula_page -->
## 模型评估指标与数据质量

常用回归误差：

$$
\mathrm{MAE}=\frac{1}{n}\sum_{i=1}^{n}|y_i-\hat{y}_i|
$$

$$
\mathrm{RMSE}=\sqrt{\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2}
$$

如果标签测量误差本身约为 $\pm 20\,\mathrm{HV}$，则模型 MAE 为 $5\,\mathrm{HV}$ 可能不可信。

> 模型误差不能脱离实验误差解释。

---

<!-- _class: table_page -->
## 数据处理日志

建议为每个数据集建立处理日志：

| 项目 | 内容 |
|---|---|
| 数据来源 | 实验、模拟、文献、数据库 |
| 原始文件 | 文件名、版本、日期 |
| 清洗规则 | 删除哪些样本，为什么删除 |
| 单位转换 | 转换公式和目标单位 |
| 缺失处理 | 插补方法和缺失比例 |
| 异常处理 | 异常判据和处理结果 |
| 输出文件 | 文件名、生成脚本、生成日期 |

处理日志是数据可靠性的证据。

---

<!-- _class: code_page -->
## 可复现的数据预处理函数

```python
def preprocess_alloy_data(df):
    """清洗材料数据表，返回处理后的DataFrame。"""
    df = df.copy()

    # 1. 统一列名
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # 2. 数值列转换
    num_cols = ["c_wt", "mn_wt", "cooling_rate_k_s", "hardness_hv"]
    for col in num_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 3. 删除目标值缺失样本
    df = df.dropna(subset=["hardness_hv"])

    # 4. 构造派生特征
    df["ce"] = df["c_wt"] + df["mn_wt"] / 6
    return df
```

---

<!-- _class: bq-green -->
## 数据质量检查清单

建模前建议逐项检查：

- 是否存在重复样本？
- 是否所有列都有明确单位？
- 成分总和是否合理？
- 目标值是否有测试标准？
- 缺失值比例是否报告？
- 异常值是否回查原始记录？
- 训练集和测试集是否存在泄漏？
- 新预测样本是否落在训练数据范围内？
- 数据处理代码是否可以重新运行？

> 通过清单化方式降低人为遗漏。

---

## 2.6 小结

模型可靠性来自三方面：

1. 数据可靠
   - 单位、来源、测试条件清楚
   - 缺失和异常处理可追踪

2. 划分可靠
   - 避免重复样本泄漏
   - 评估外推能力

3. 解释可靠
   - 不把相关性误认为因果
   - 不夸大小样本模型精度
   - 将模型误差与实验误差共同讨论

下一步：进行本章综合案例与编程作业。

---

<!-- _class: trans section_start -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
## 综合案例：合金硬度数据预处理流程

---

## 案例背景

假设已有一份合金硬度数据，字段包括：

- `sample_id`：样本编号
- `C_wt`、`Mn_wt`、`Si_wt`：成分
- `cooling_rate`：冷却速率
- `process`：制备工艺
- `hardness_HV`：硬度

目标：

> 将原始数据清洗为可用于机器学习建模的数据表，并输出基本统计图。

---

<!-- _class: code_page -->
## 第一步：读取与检查

```python
import pandas as pd

raw_path = "data/raw/alloy_hardness.csv"
df = pd.read_csv(raw_path)

print("shape:", df.shape)
print("columns:", df.columns.tolist())
print(df.head())
print(df.info())
print(df.isna().mean().sort_values(ascending=False))
```

检查目的：

- 确认数据规模
- 识别缺失字段
- 检查列名和数据类型
- 判断是否需要单位转换

---

<!-- _class: code_page -->
## 第二步：统一列名和类型

```python
df.columns = (
    df.columns
      .str.strip()
      .str.replace(" ", "_")
      .str.lower()
)

num_cols = ["c_wt", "mn_wt", "si_wt", "cooling_rate", "hardness_hv"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 类别变量规范化
df["process"] = df["process"].str.strip().str.lower()
```

该步骤使后续代码不依赖原始表格中的偶然格式。

---

<!-- _class: formula_page code_page -->
## 第三步：成分合理性检查

```python
comp_cols = ["c_wt", "mn_wt", "si_wt"]

# 检查负值
for col in comp_cols:
    print(col, (df[col] < 0).sum())

# 简化检查：合金元素总量不应超过100 wt.%
df["known_sum_wt"] = df[comp_cols].sum(axis=1)
print(df[df["known_sum_wt"] > 100])
```

若包含所有元素，可进一步检查：

$$
\sum_j c_j \approx 100\%
$$

---

<!-- _class: code_page -->
## 第四步：缺失值处理

```python
# 删除目标值缺失样本
df = df.dropna(subset=["hardness_hv"])

# 数值特征用中位数插补
features = ["c_wt", "mn_wt", "si_wt", "cooling_rate"]
for col in features:
    df[col + "_missing"] = df[col].isna().astype(int)
    df[col] = df[col].fillna(df[col].median())
```

保留缺失指示变量可以记录原始缺失信息。

---

<!-- _class: code_page -->
## 第五步：异常值识别

```python
x = df["hardness_hv"]
q1 = x.quantile(0.25)
q3 = x.quantile(0.75)
iqr = q3 - q1

low = q1 - 1.5 * iqr
high = q3 + 1.5 * iqr

outlier_mask = (x < low) | (x > high)
print(df.loc[outlier_mask, ["sample_id", "hardness_hv", "process"]])
```

输出后应回查原始实验记录，而不是直接删除。

---

<!-- _class: code_page -->
## 第六步：派生特征与保存

```python
import numpy as np

# 碳当量教学示例
df["ce"] = df["c_wt"] + df["mn_wt"] / 6

# 冷却速率跨度大，取对数
df["log_cooling_rate"] = np.log10(df["cooling_rate"])

# 保存处理后数据
df.to_csv("data/processed/alloy_hardness_clean.csv", index=False)
```

保存时建议同时保存处理脚本和数据说明文件。

---

<!-- _class: code_page -->
## 第七步：输出诊断图

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(5, 4))
ax.scatter(df["log_cooling_rate"], df["hardness_hv"])
ax.set_xlabel("log10(cooling rate)")
ax.set_ylabel("Hardness / HV")
ax.set_title("Hardness vs cooling rate")
plt.tight_layout()
plt.savefig("figures/hardness_vs_cooling_rate.png", dpi=300)
plt.show()
```

图像文件应可由代码重复生成。

---

<!-- _class: code_page -->
## 本章知识结构回顾

本章形成完整的数据预处理链条：

```text
Python环境
  ↓
NumPy数组、Pandas表格、Matplotlib图形
  ↓
材料数据类型识别
  ↓
缺失值、异常值、单位和类型处理
  ↓
统计描述与可视化诊断
  ↓
数据质量、偏差和模型可靠性评估
```

核心能力：把材料数据从“能看懂”变成“能建模”。

---

<!-- _class: compact_text -->
## 本章关键概念速记

- `ndarray`：高效数值数组
- `DataFrame`：带列名和索引的二维数据表
- 缺失值：缺失机制决定处理方法
- 异常值：统计异常不一定是物理错误
- 标准化：使变量具有可比尺度
- 数据泄漏：测试集信息进入训练流程
- 数据偏差：样本或标签不能代表真实目标空间
- 可复现性：数据处理过程可由代码重新生成

---

<!-- _class: bq-purple -->
## 课堂讨论题

1. 对材料文献中整理出的数据，哪些字段最容易缺失？
2. 如果某个样本硬度远高于其他样本，应该删除还是保留？
3. 显微组织图像裁剪后随机划分训练集和测试集，为什么可能导致数据泄漏？
4. 以增材制造为例，体积能量密度是否足以代表工艺过程？
5. 小样本材料数据中，为什么“高 $R^2$”不一定说明模型可靠？

---

## 本章简单Python编程作业

题目：合金硬度数据预处理与可视化

请自行构造或整理一个至少包含 20 个样本的数据表，字段包括：

- `sample_id`
- 至少 3 个成分变量，例如 `c_wt`、`mn_wt`、`si_wt`
- 至少 2 个工艺变量，例如 `cooling_rate`、`heat_treatment_temp`
- 1 个性能变量，例如 `hardness_hv`

要求：完成缺失值检查、异常值识别、派生特征构造和至少 3 张图。

---

## 作业具体要求

提交内容：

1. 原始数据文件：`raw_data.csv`
2. 数据处理代码：`preprocess_homework.py` 或 Notebook
3. 清洗后数据：`clean_data.csv`
4. 图形文件：至少 3 张 PNG
5. 简短说明文档：300 字以内

必须包含：

- 缺失值比例统计
- 至少一种异常值识别方法
- 至少一个材料相关派生特征
- 至少一个散点图和一个直方图
- 对数据质量和模型可靠性的简要评价

---

<!-- _class: code_page -->
## 作业参考代码框架

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取数据
df = pd.read_csv("raw_data.csv")

# 2. 检查缺失值
print(df.isna().mean())

# 3. 数值列转换与插补
num_cols = ["c_wt", "mn_wt", "si_wt", "cooling_rate", "hardness_hv"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")
    df[col] = df[col].fillna(df[col].median())

# 4. 构造派生特征
df["ce"] = df["c_wt"] + df["mn_wt"] / 6

# 5. 保存结果
df.to_csv("clean_data.csv", index=False)
```

---

<!-- _class: table_page -->
## 作业评价标准

| 项目 | 分值 | 要求 |
|---|---:|---|
| 数据结构 | 20 | 字段清晰，单位明确，一行一个样本 |
| 缺失与异常处理 | 25 | 有统计、有方法、有说明 |
| 派生特征 | 15 | 具有材料意义，不是机械堆砌 |
| 可视化 | 20 | 图形清楚，坐标轴和单位完整 |
| 可靠性讨论 | 20 | 能指出数据偏差、样本量或外推风险 |

重点不是代码复杂，而是数据处理逻辑清楚。

---

<!-- _class: lastpage -->
<!-- _header: "" -->
<!-- _footer: "" -->
<!-- _paginate: "" -->
###### 第2章结束

<div class="icons">

- **下一章：贝叶斯定理与概率思维**
  - 从确定性判断转向概率更新
  - 理解先验、似然、后验和不确定性
  - 为小样本材料建模和贝叶斯优化做准备

</div>
