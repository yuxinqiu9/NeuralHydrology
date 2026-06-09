# Presentation Script: Neural Hydrology (English-Led, Bilingual Line-by-Line)
## SoSe 2026 - Climate Change Statistics

Suggested duration: ~8 minutes
Format: English main speech with direct Chinese translation under each paragraph

---

## Slide 1 - Cover

English:
Hello everyone, and thanks for being here. Today I will share my current work on Neural Hydrology. The main question is: under climate change, how can we make streamflow prediction both accurate and reliable?

中文翻译：
大家好，感谢大家来听。今天我分享我目前在 Neural Hydrology 方向的工作。核心问题是：在气候变化背景下，我们怎么把流量预测做得既准确又可靠。

---

## Slide 2 - What is Neural Hydrology?

English:
Here, streamflow means the amount of water passing a river cross-section per unit time. It comes from precipitation, evapotranspiration, infiltration, groundwater, and routing. Neural hydrology learns this relation directly from data, instead of writing a full process equation system by hand.

中文翻译：
在这里，streamflow 指的是单位时间通过河道断面的水量。它主要由降水、蒸散、入渗、地下水和汇流共同决定。神经水文学是直接从数据学习这种关系，而不是手工去写一整套过程方程。

---

## Slide 3 - Milestones

English:
I want to highlight the key stages in how this theory developed. Core LSTM theory was published in 1997, and the big hydrology breakthrough came in 2018 with rainfall-runoff modeling. Then EA-LSTM improved multi-basin learning by using static basin attributes, and MC-LSTM added structural mass conservation, moving from only prediction skill to more physically consistent modeling.

中文翻译：
我想 highlight 一下这个理论发展的关键阶段。LSTM 理论最早发表于 1997 年，而它在水文里的重要突破出现在 2018 年的降雨-径流建模。之后 EA-LSTM 通过加入流域静态属性，提升了多流域联合学习效果，MC-LSTM 又加入了结构性的质量守恒，让模型从“只看预测能力”走向“更符合物理规律”。

---

## Slide 4 - Why It Matters

English:
Streamflow forecasting directly supports flood warning, reservoir operation, and water management. The main challenge is non-stationarity: future climate conditions are different from historical training data. So we care not only about average error, but also about stability under distribution shift.

中文翻译：
流量预测直接服务洪水预警、水库调度和水资源管理。主要挑战是非平稳性，也就是未来气候和历史训练数据分布不一样。所以我们不仅看平均误差，也看模型在分布变化下是否稳定。

---

## Slide 5 - Deep Learning Breakthrough

English:
By 2018, hydrology saw a clear deep-learning breakthrough. Kratzert and colleagues published "Rainfall-Runoff Modelling Using Long Short-Term Memory (LSTM) Based Neural Networks" and showed that LSTM performed better than tuned SAC-SMA on CAMELS-US. In simple words, LSTM is a data-driven sequence model, while SAC-SMA is a physics-based conceptual model with manual calibration. So this was not only a better score, but also a move to more scalable modeling.

中文翻译：
到了 2018 年，水文领域出现了比较明确的 deep learning 突破。Kratzert 团队发表了 "Rainfall-Runoff Modelling Using Long Short-Term Memory (LSTM) Based Neural Networks"，并展示在 CAMELS-US 上，LSTM 表现好于调参后的 SAC-SMA。简单说，LSTM 是数据驱动的时序模型，SAC-SMA 是物理启发、要人工调参的概念模型。所以这不仅是分数更高，也是从手工调参走向可规模化建模。

---

## Slide 6 - LSTM and EA-LSTM

English:
LSTM uses gated memory to decide what to keep, what to add, and what to output over time. EA-LSTM builds on this by adding static basin attributes into the gates. In one sentence: LSTM handles time memory, and EA-LSTM adds basin-specific adaptation.

中文翻译：
LSTM 通过门控记忆来决定保留多少信息、加入多少新信息、以及输出多少状态。EA-LSTM 在此基础上把流域静态属性加入门控过程。用一句话概括：LSTM 主要解决时间记忆，EA-LSTM 额外提供流域特异性适配。

---

## Slide 7 - NeuralHydrology Tooling

English:
A practical advantage of NeuralHydrology is that it is config-driven and workflow-friendly. In practice, I can switch model, head, loss, and dataset settings with very little code change. So this library is good for reproducibility and also great for clean controlled comparisons in my three RQs.

中文翻译：
NeuralHydrology 的一个实际优势是“配置驱动 + 工作流友好”。在操作上，我几乎不用改代码就能切换模型、输出头、损失函数和数据设置。所以这个库既方便复现，也很适合我后面三个 RQ 的控制变量对比。

---

## Slide 8 - Physics and Transfer Learning

English:
Following the tooling slide, this page shows two things we can do in the same NeuralHydrology framework. First, MC-LSTM builds mass conservation into the model structure, not only as a soft loss penalty. Second, transfer learning uses pretrain on large datasets and fine-tune on target basins with limited local data. In short, both reliability and transferability can be done in this library workflow.

中文翻译：
承接上一页工具链，这一页讲的是同一个 NeuralHydrology 框架里可以直接做的两件事。第一，MC-LSTM 把质量守恒直接放进模型结构，不只是加一个损失惩罚。第二，迁移学习用“大样本预训练 + 目标流域小样本微调”。简单说，物理可靠性和迁移能力都能在这个库里实现。

---

## Slide 9 - Case Study

English:
Now let's look at a quick case study. This figure shows three levels in the LamaH-CE river-network setting: a strong case, a median case, and a worst case. The main sources are the 2021 LamaH-CE data paper by Klingler and colleagues for station identity, plus the 2021 river-network GNN work by Kratzert and colleagues and the 2024 ICLR under-review paper "Exploiting River Network Topology for Flood Forecasting with Graph Neural Networks" for benchmark values. The key message is simple: overall performance can look strong, but extreme-tail cases may still fail. Also, to avoid confusion, these case-study values come from river-network GNN studies, not from the earlier single-basin LSTM benchmark.

中文翻译：
下面我们看一个简短的 case study。这个图展示了 LamaH-CE 河网场景下的三个层次：较强样本、中位样本和最差样本。主要来源是 2021 年 Klingler 团队的 LamaH-CE 数据论文（用于站点身份），以及 2021 年 Kratzert 团队的河网 GNN 工作和 2024 年 ICLR 在审稿件 "Exploiting River Network Topology for Flood Forecasting with Graph Neural Networks"（用于性能基准值）。核心结论很简单：整体表现可能很好，但极端尾部样本仍可能失效。还有一点要明确，这一页的 case-study 数值主要来自河网 GNN 研究，不是前面那个单流域 LSTM 基线实验。

---

## Slide 10 - Gap Analysis

English:
At this point, I frame these as my three research interests: better prediction on extreme events, better reliability under climate extrapolation, and better understanding of regional transfer, especially for Alpine and Central European basins.

中文翻译：
到这里我把它归纳成三个研究兴趣方向：提升极端事件预测、提升气候外推下的可靠性，以及更好理解区域迁移机制，特别是在阿尔卑斯和中欧流域场景下。

---

## Slide 11 - RQ1

English:
For my first RQ, I focus on this question: can overall model performance stay strong while still handling extreme-event prediction well? A practical approach is to keep the same LSTM backbone, replace only the prediction head (baseline vs GMM vs UMAL), and evaluate on POT events and high quantiles. The expected contribution is better flood-peak prediction and better tail behavior, because average metrics alone can hide failure cases.

中文翻译：
就此我提出第一个 RQ：我关注的问题是，整体模型预测能不能在极端条件下也表现好。我的可行做法是保持同一个 LSTM 主干不变，只替换输出头（baseline、GMM、UMAL），并在 POT 事件和高分位指标上做对比。这个做完之后的贡献是提升洪峰预测能力和尾部样本表现，因为平均指标可能会掩盖失败样本。

---

## Slide 12 - RQ2

English:
For my second RQ, I focus on how much physical information affects prediction reliability under climate shift. A practical approach is to train MC-LSTM and CudaLSTM on historical data, perturb test forcings with Delta P and Delta T, and compare performance degradation plus closure consistency. The expected contribution is to measure how much physics-aware structure improves stability in extrapolation scenarios.

中文翻译：
第二个 RQ 我关注的是：物理信息对预测结果到底有多大影响。我的可行做法是先用历史数据分别训练 MC-LSTM 和 CudaLSTM，再在测试阶段施加 Delta P 和 Delta T 扰动，比较性能退化和守恒闭合一致性。我的贡献是量化物理约束在气候外推场景下带来的稳定性提升。

---

## Slide 13 - RQ3

English:
For my third RQ, I want to study local basin prediction on top of an existing global model: should we train a local model from scratch, or fine-tune a global pretrained model? A practical approach is to pretrain on Caravan, fine-tune on target basins, evaluate on held-out basins, compare against scratch training, and use SHAP to explain transfer drivers. The expected contribution is practical evidence on when transfer learning is a better choice than local-from-scratch training.

中文翻译：
第三个 RQ 我想研究的是：在已经有全球模型的基础上，针对局部流域问题，到底是直接训练局部模型，还是在全局模型上做 fine-tune 更好。我的可行做法是先在 Caravan 上预训练，再在目标流域微调，在留出流域上评估，并与从零训练做对照，最后用 SHAP 解释迁移驱动因素。我的贡献是给出可落地证据，说明在什么条件下迁移学习比本地从零训练更好。

---

## Slide 14 - Summary

English:
To summarize: neural hydrology already shows strong predictive power; the next step is extremes, climate-extrapolation reliability, and transferability. My three research questions are designed to address these three challenges directly.

中文翻译：
总结来说：神经水文学已经展现出较强的预测能力；下一步重点是极端事件、气候外推可靠性和迁移能力。我的三个研究问题就是围绕这三项挑战直接设计的。

---

## Slide 15 - References

English:
All equations, values, and data sources are traceable in the references and validation notes. Thank you for listening. I am happy to take questions.

中文翻译：
所有公式、数值和数据来源都可以在参考文献和验证文档中追溯。感谢各位聆听，欢迎提问。
