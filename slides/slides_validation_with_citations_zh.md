# Slides 校验报告（详细版，逐页逐条）

本文件是对 slides.qmd 的详细事实核验记录，目标是把“每页说了什么、是否可靠、证据来自哪里、哪里仍有风险、建议怎么改”写清楚。

适用范围：
- 文件：NeuralHydrology/slides/slides.qmd
- 结论依据：已抓取到的论文正文/官方文档/报告页面内容 + 当前书目条目

状态定义：
- VALID：有可直接引用的来源文本，且与幻灯片表述一致或近似一致。
- PARTIAL：主方向正确，但措辞、数字、公式形式或结论强度需要收敛。
- UNVERIFIED：当前工具链下未能拿到可直接支撑该句的原文证据。

---

## 1) 页码与标题索引

按 slides.qmd 的页面顺序（含封面）：
1. Cover
2. What is Neural Hydrology?
3. Milestones in Neural Hydrology
4. Why Streamflow Prediction Matters
5. The Deep Learning Breakthrough
6. LSTM and EA-LSTM
7. NeuralHydrology: Python Library
8. Physics and Transfer Learning
9. Case Study: River-Network Forecasting on LamaH-CE
10. Gap Analysis: What Remains Unsolved
11. RQ 1 — Probabilistic Losses for Flood-Peak Prediction
12. RQ 2 — Physics Constraints under Climate Forcing
13. RQ 3 — Transfer Learning to Alpine Basins
14. Summary
15. References

---

## 2) 逐页详细核验

## 第 1 页（Cover）
- 页面性质：封面页
- 事实性技术 claim：无
- 结论：不需要事实核验

## 第 2 页（What is Neural Hydrology?）
### 2.1 本页关键表述
- Streamflow 定义为河道某点单位时间水量，常见单位 mm/day 或 m3/s，并作为流域综合输出。
- Rainfall-runoff 是核心水文问题。
- Neural Hydrology 用深度学习学习输入到流量的映射。

### 2.2 对应 claim 与状态
- Claim B（降雨-径流建模是关键挑战）-> VALID
- Claim A（CAMELS 是属性+气象大样本集）
  - 说明：该页没有直接陈述 CAMELS 定义句，但引用链对后续相关内容有支撑。

### 2.3 证据与理由
- 证据：Kratzert et al. (2018) 正文明确写到：
  - "Rainfall-runoff modelling is one of the key challenges in the field of hydrology."
- 结论：该页“核心问题”表述成立。

### 2.4 建议
- 可保持当前写法。
- 若要更严格，可在本页增加一句“本文采用 CAMELS 语境下的数据驱动建模框架”的显式过渡。

来源：
- https://hess.copernicus.org/articles/22/6005/2018/

## 第 3 页（Milestones in Neural Hydrology）
### 3.1 本页关键表述
- 2018 LSTM 里程碑（优于 SAC-SMA+Snow-17）
- 2019 EA-LSTM（531 basins）
- 2021 MC-LSTM（质量守恒）
- 2022 NeuralHydrology（开源统一框架）
- 2023 Caravan（6830 basins）

### 3.2 对应 claim 与状态
- Claim C -> VALID
- Claim D -> VALID
- Claim F -> VALID
- Claim G -> VALID
- Claim I -> VALID
- Claim J -> VALID

### 3.3 证据与理由
- C（241 basins, 0.63 vs 0.58）：Kratzert 2018 文中直接给出。
- D（531 basins）：Kratzert 2019 摘要与方法部分可直接对应。
- F（MC-LSTM mass-conserving）：Hoedt 2021 标题与模型定义明确。
- G（NeuralHydrology 开源库）：JOSS 论文题目与官方文档一致。
- I/J（Caravan 数据集与 6830）：Scientific Data + Zenodo 版本日志可支撑。

### 3.4 风险
- 无实质风险；该页时间线与证据一致。

来源：
- https://hess.copernicus.org/articles/22/6005/2018/
- https://hess.copernicus.org/articles/23/5089/2019/
- https://arxiv.org/abs/2101.05186
- https://doi.org/10.21105/joss.04050
- https://doi.org/10.1038/s41597-023-01975-w
- https://zenodo.org/records/7944025

## 第 4 页（Why Streamflow Prediction Matters）
### 4.1 本页关键表述
- 洪灾高频且影响大。
- 气候变化下，极端降水增强、季节性改变、雪融过程变化。
- 非平稳性（non-stationarity）是模型挑战。

### 4.2 对应 claim 与状态
- Claim K（水循环广泛变化）-> VALID
- Claim L（变暖改变降水特征）-> VALID
- Claim M（Milly 2008 归属）-> PARTIAL
- Claim N（2022 年 5700 万）-> UNVERIFIED（此数字已从 slides 主文案移除）

### 4.3 证据与理由
- K/L：IPCC AR6 WGI Ch.8 可直接支持。
  - "widespread, non-uniform human-caused alterations of the water cycle"
  - "precipitation intensity, duration and intermittence ... altered as the climate warms"
- M：题名和 DOI 可确认，但 Science 全文抓取 403，无法在本工具里做逐字上下文核验。
- N：CRED 2022 PDF 当前抽取失败，不能在本流程下确认“5700万”这句原文；因此已降级处理并修改 slide 文案。

### 4.4 建议
- 保留 IPCC 句子作为核心支撑。
- Milly 句子建议按“文献框架化表达”使用，不做未经全文核验的强直引。

来源：
- https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-8/
- https://doi.org/10.1126/science.1151915
- https://cred.be/sites/default/files/2022_EMDAT_report.pdf

## 第 5 页（The Deep Learning Breakthrough）
### 5.1 本页关键表述
- 图和正文给出 LSTM 与 SAC-SMA 对比（241 basins: 0.63 vs 0.58）。

### 5.2 对应 claim 与状态
- Claim C -> VALID

### 5.3 证据与理由
- 文献可直接对应均值结果与实验设置。

### 5.4 风险
- 无。

来源：
- https://hess.copernicus.org/articles/22/6005/2018/

## 第 6 页（LSTM and EA-LSTM）
### 6.1 本页关键表述
- 标准 LSTM 状态更新式。
- EA-LSTM 静态输入门。
- NSE 公式、范围与解释。

### 6.2 对应 claim 与状态
- Claim D -> VALID
- Claim E -> VALID
- Claim O -> PARTIAL（主要是阈值语义）
- Math M1（LSTM方程）-> VALID
- Math M2（EA-LSTM静态门写法）-> PARTIAL（如果写 i_t 会引起歧义）
- Math M3（NSE）-> VALID（公式与范围），PARTIAL（阈值表述）

### 6.3 证据与理由
- LSTM 方程：Hochreiter 1997 + Kratzert 2019 方法节。
- EA-LSTM：Kratzert 2019 指出 i 为静态门（不随时间变）。
- NSE：Nash-Sutcliffe 原始定义可直接支持范围；“>0.6可接受”只在特定论文语境下成立，不应普适化。

### 6.4 建议
- 公式符号统一为静态 i。
- 阈值句子使用“context dependent”限定语（已在 slide 中处理）。

来源：
- https://doi.org/10.1162/neco.1997.9.8.1735
- https://hess.copernicus.org/articles/23/5089/2019/
- https://doi.org/10.1016/0022-1694(70)90255-6
- https://essd.copernicus.org/articles/13/4529/2021/

## 第 7 页（NeuralHydrology: Python Library）
### 7.1 本页关键表述
- 开源 PyTorch 库
- config 驱动
- model zoo / probabilistic heads / evaluation tools

### 7.2 对应 claim 与状态
- Claim G -> VALID
- Claim H -> VALID

### 7.3 证据与理由
- JOSS + 官方 docs 相互印证。

### 7.4 风险
- 无。

来源：
- https://doi.org/10.21105/joss.04050
- https://neuralhydrology.readthedocs.io/en/latest/
- https://neuralhydrology.readthedocs.io/en/latest/usage/config.html
- https://neuralhydrology.readthedocs.io/en/latest/usage/models.html

## 第 8 页（Physics and Transfer Learning）
### 8.1 本页关键表述
- MC-LSTM 是结构性守恒。
- 迁移学习工作流（pre-train + fine-tune）。

### 8.2 对应 claim 与状态
- Claim F -> VALID
- Claim R -> PARTIAL（工具链 VALID，效果“总是提升”不成立）
- Math M4（MC-LSTM 守恒表达）-> PARTIAL

### 8.3 证据与理由
- MC-LSTM 架构守恒：可直接支持。
- 迁移学习：文档有流程，但收益依赖任务/数据，不可写成必然改善。
- 守恒公式：幻灯片中的水量平衡写法可作为概念解释，但不是论文逐字标准公式。

### 8.4 建议
- 保留“结构性守恒”表述。
- 迁移学习句子保持概率性措辞（can/often）。

来源：
- https://arxiv.org/abs/2101.05186
- https://neuralhydrology.readthedocs.io/en/latest/usage/models.html
- https://neuralhydrology.readthedocs.io/en/latest/usage/config.html

## 第 9 页（Case Study: River-Network Forecasting on LamaH-CE）
### 9.1 本页关键表述
- LamaH-CE 河网建模案例。
- 375 个站点平均 NSE=0.856，最困难站点 NSE=0.248。

### 9.2 对应 claim 与状态
- Claim P（本地参考论文中的性能结论）-> VALID [LOCAL-REF]

### 9.3 证据与理由
- EGU21 报告给出 LamaH-CE 大规模河网建模背景。
- 后续稿件条目给出本页使用的指标口径（375 站点平均 NSE 与最差站点 NSE）。
- 这两条证据均来自你本地 reference 文件夹，并已在书目中映射为 `@kratzert2021gnn`、`@anon2024gnn`。

### 9.4 建议
- 当前页面维持“本地论文可追溯 benchmark”写法。
- 若后续用于正式论文，可补充本地 PDF 的表号/页码定位信息。
- 当前版本采用“来源分离”写法：`ID 399` 的站点身份来自 Klingler et al. (2021)，而性能数值来自两篇河网建模文献。

来源：
- 本地文件：reference/EGU21-13375_presentation.pdf（bib key: @kratzert2021gnn）
- 本地文件：reference/1991_Exploiting_River_Network_.pdf（bib key: @anon2024gnn）

## 第 10 页（Gap Analysis）
### 10.1 本页关键表述
- 极端事件、非平稳性、区域迁移三大未解问题。

### 10.2 对应 claim 与状态
- Claim Q -> VALID（极端洪峰问题）

### 10.3 证据与理由
- Frame 2022 可支持“极端事件表现退化”的研究动机。

来源：
- https://doi.org/10.5194/hess-26-3377-2022

## 第 11 页（RQ1）
### 11.1 本页关键表述
- 用概率头改进极端高流表现。

### 11.2 对应 claim 与状态
- Claim Q -> VALID

### 11.3 证据与理由
- RQ1 与 frame2022 的动机一致。

来源：
- https://doi.org/10.5194/hess-26-3377-2022

## 第 12 页（RQ2）
### 12.1 本页关键表述
- 比较 MC-LSTM 与 CudaLSTM 在气候扰动下的可靠性。

### 12.2 对应 claim 与状态
- 该页主要是研究问题，不是既成事实声明。
- 状态：不判定 VALID/PARTIAL（问题设定页）

### 12.3 背景支撑
- 守恒架构背景：Hoedt 2021
- 气候水循环变化背景：IPCC Ch.8

来源：
- https://arxiv.org/abs/2101.05186
- https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-8/

## 第 13 页（RQ3）
### 13.1 本页关键表述
- 预训练 Caravan，再迁移到巴伐利亚场景。

### 13.2 对应 claim 与状态
- Claim R（工具链可用性）-> VALID
- Claim R（效果必然提升）-> PARTIAL

### 13.3 证据与理由
- 文档支持 fine-tune 流程。
- Caravan 作为大样本预训练基础成立。
- 性能提升幅度需要实验验证，不能先验保证。

来源：
- https://neuralhydrology.readthedocs.io/en/latest/usage/config.html
- https://zenodo.org/records/7944025

## 第 14 页（Summary）
### 14.1 本页关键表述
- 汇总 LSTM 对比结果、EA-LSTM 多流域训练、NeuralHydrology 基础设施。

### 14.2 对应 claim 与状态
- Claim C -> VALID
- Claim D -> VALID
- Claim G -> VALID
- Claim H -> VALID

### 14.3 证据与理由
- 与前述页面一致，均有直接来源支撑。

来源：
- https://hess.copernicus.org/articles/22/6005/2018/
- https://hess.copernicus.org/articles/23/5089/2019/
- https://doi.org/10.21105/joss.04050
- https://neuralhydrology.readthedocs.io/en/latest/

## 第 15 页（References）
- 页面性质：参考文献页
- claim：无
- 状态：无
- 说明：不承载新增事实结论

---

## 3) Claim 总览（便于快速检索）

- A：CAMELS 数据集定义 -> VALID（未单独映射到某页主句）
- B：降雨-径流是关键问题 -> VALID
- C：241 流域 0.63 vs 0.58 -> VALID
- D：EA-LSTM 531 basins -> VALID
- E：EA-LSTM 静态门机制 -> VALID
- F：MC-LSTM 守恒架构 -> VALID
- G：NeuralHydrology 开源库 -> VALID
- H：配置驱动/模型与概率头能力 -> VALID
- I：Caravan 全球大样本 -> VALID
- J：Caravan 达到 6830 basins（版本日志）-> VALID
- K：广泛水循环变化 -> VALID
- L：变暖改变降水特征 -> VALID
- M：Stationarity is dead 归属 -> PARTIAL
- N：2022 年 5700 万受影响 -> UNVERIFIED
- O：NSE 公式与解释 -> PARTIAL（阈值语义）
- P：LamaH-CE 河网案例（375 站点，平均 NSE 0.856，最差 0.248）-> VALID [LOCAL-REF]
- Q：极端洪峰短板动机 -> VALID
- R：迁移学习工具链可用 -> VALID；效果保证 -> PARTIAL

---

## 4) 当前残余风险与可执行动作

### 4.1 残余风险
- Science 全文（milly2008）受限，无法在本工具链下逐段核验。
- CRED 2022 PDF 文本抽取失败，无法机器化复核具体数字句。

### 4.2 可执行动作（建议）
1. 人工下载并检查 CRED 2022 PDF 原文，若有明确数字再恢复硬数字表述。
2. 若需要直引 Milly 2008 全文，请通过机构访问后做人工逐字核对并补页码。
3. 保持当前 slides 中“保守且可溯源”的写法，优先保证答辩时可追溯性。

---

## 5) 本地 reference 文件夹来源标记（显式）

以下 VALID 条目来自本地 reference 文件夹中的论文：

- 第 9 页 / Claim P -> VALID [LOCAL-REF]
  - bib key：`@kratzert2021gnn`
  - 本地文件：`reference/EGU21-13375_presentation.pdf`
  - bib key：`@anon2024gnn`
  - 本地文件：`reference/1991_Exploiting_River_Network_.pdf`
