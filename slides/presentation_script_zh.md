# Presentation Script: Neural Hydrology (English-Led, Bilingual Line-by-Line)
## SoSe 2026 - Climate Change Statistics

Suggested duration: ~8 minutes
Format: English main speech with direct Chinese translation under each paragraph

---

## Slide 1 - Cover

English:
Hello everyone, and thank you for joining. Today I will present my interim work on Neural Hydrology. The core question is: under climate change, how can we make streamflow prediction not only accurate, but also reliable?

中文翻译：
大家好，感谢大家参加。今天我汇报的是我在 Neural Hydrology 方向的阶段性工作。核心问题是：在气候变化背景下，我们如何让流量预测不仅准确，而且可靠。

---

## Slide 2 - What is Neural Hydrology?

English:
In this context, streamflow is the amount of water passing a river cross-section per unit time. It is influenced by precipitation, evapotranspiration, infiltration, groundwater, and routing. Neural hydrology learns this mapping directly from data, instead of manually defining a full process-based equation system.

中文翻译：
在这里，streamflow 指的是单位时间通过河道断面的水量。它受到降水、蒸散、入渗、地下水和汇流等过程共同影响。神经水文学的做法是直接从数据学习这种映射关系，而不是手工定义完整的过程型方程系统。

---

## Slide 3 - Milestones

English:
I highlight three milestones. First, the core LSTM theory was published in 1997, and its major hydrology breakthrough came in 2018 with rainfall-runoff modeling. Second, EA-LSTM improved multi-basin learning by conditioning on static basin attributes. Third, MC-LSTM introduced structural mass conservation, moving from pure predictive skill toward physically consistent modeling.

中文翻译：
我重点强调三个里程碑。第一，LSTM 的理论最早发表于 1997 年，而它在水文中的关键突破出现在 2018 年的降雨-径流建模。第二，EA-LSTM 通过引入流域静态属性，提升了多流域联合学习能力。第三，MC-LSTM 引入了结构性质量守恒，让研究从“只追求预测能力”走向“兼顾物理一致性”。

---

## Slide 4 - Why It Matters

English:
Streamflow forecasting directly supports flood warning, reservoir operation, and water resource management. The main challenge is non-stationarity: future climate conditions differ from historical training data. So we care not only about average error, but also about robustness under distribution shift.

中文翻译：
流量预测直接服务于洪水预警、水库调度和水资源管理。主要挑战是非平稳性，也就是未来气候条件与历史训练数据分布不一致。因此我们不仅关注平均误差，还关注模型在分布漂移条件下的稳健性。

---

## Slide 5 - Deep Learning Breakthrough

English:
This slide shows a key comparison: LSTM achieved higher mean NSE than the calibrated SAC-SMA benchmark in CAMELS-US. Conceptually, LSTM is a data-driven deep learning sequence model, while SAC-SMA is a physics-inspired conceptual hydrology model with manual parameter calibration. The importance is not only higher score, but also scalability: we avoid heavy basin-by-basin manual calibration.

中文翻译：
这一页展示了一个关键对比：在 CAMELS-US 上，LSTM 的 mean NSE 高于经过校准的 SAC-SMA 基线。从理论出发，LSTM 是数据驱动的深度学习时序模型，而 SAC-SMA 是物理启发的概念水文模型，并且依赖人工参数校准。其意义不仅是分数更高，还包括更好的可扩展性：我们可以避免逐流域的高成本手工调参。

---

## Slide 6 - LSTM and EA-LSTM

English:
LSTM uses gated memory to decide what to keep, what to write, and what to output over time. EA-LSTM extends this by injecting static basin attributes into gating behavior. In one sentence: LSTM handles temporal memory, and EA-LSTM adds basin-specific adaptation.

中文翻译：
LSTM 通过门控记忆机制来决定保留多少信息、写入多少信息、以及输出多少状态。EA-LSTM 在此基础上进一步将流域静态属性注入门控过程。用一句话概括：LSTM 主要解决时间记忆问题，EA-LSTM 额外提供流域特异性适配能力。

---

## Slide 7 - NeuralHydrology Tooling

English:
A practical advantage of NeuralHydrology is that it is configuration-driven and workflow-oriented. In practice, I can switch model, head, loss, and dataset settings with minimal code changes. So this library is not only convenient for reproducibility, but also ideal for controlled comparisons in my three RQs.

中文翻译：
NeuralHydrology 的一个实践优势是“配置驱动 + 工作流导向”。在实际操作中，我可以在几乎不改代码的情况下切换模型、输出头、损失函数和数据设置。因此这个库不仅有利于复现，也非常适合我后面三个研究问题的控制变量对比。

---

## Slide 8 - Physics and Transfer Learning

English:
Following the tooling slide, this page highlights two capabilities that can be implemented within the same NeuralHydrology framework. First, MC-LSTM enforces mass conservation structurally, not only through a soft penalty in the loss. Second, transfer learning uses pretrain on large datasets and fine-tune on target basins with limited local data. In other words, reliability and transferability are both operational in the library workflow.

中文翻译：
承接上一页工具链，这一页强调的是同一个 NeuralHydrology 框架里可直接落地的两类能力。第一，MC-LSTM 通过模型结构直接约束质量守恒，而不仅仅依赖损失函数软惩罚。第二，迁移学习采用“大样本预训练 + 目标流域小样本微调”的流程。也就是说，物理可靠性与迁移能力都可以在这个库的工作流中实现。

---

## Slide 9 - Case Study

English:
The LamaH-CE case summarizes three levels: a strong example, a median level, and a worst case. The message is important: average performance can look good, while tail cases still fail. This directly motivates the first research question.

中文翻译：
LamaH-CE 案例展示了三个层次：较强样本、中位水平和最差样本。核心信息是：平均表现看起来可以很好，但尾部极端样本仍可能失败。这也是第一个研究问题的直接动机。

---

## Slide 10 - Gap Analysis

English:
I focus on three open gaps: limited performance on extremes, limited reliability under climate extrapolation, and limited evidence for regional transfer, especially in Alpine and Central European settings.

中文翻译：
我聚焦三个尚未解决的缺口：对极端事件的性能不足、在气候外推场景下可靠性不足、以及区域迁移证据不足，特别是在阿尔卑斯和中欧场景中。

---

## Slide 11 - RQ1

English:
RQ1 asks: without changing the LSTM backbone, can probabilistic heads such as GMM and UMAL improve flood-peak prediction? The method is controlled comparison with the same backbone and different heads, then evaluation on POT events and high quantiles. The goal is better tail behavior, not just better average metrics.

中文翻译：
RQ1 的问题是：在不更换 LSTM 主干的前提下，像 GMM 和 UMAL 这样的概率输出头能否改善洪峰预测。方法是保持同一主干、仅替换输出头进行控制变量对比，并在 POT 事件和高分位指标上评估。目标是改善尾部表现，而不只是提高平均指标。

---

## Slide 12 - RQ2

English:
RQ2 asks: under climate perturbation scenarios, which model is more robust, MC-LSTM or CudaLSTM? We train on historical data, perturb test forcings with Delta P and Delta T, then compare performance degradation and closure consistency. The target behavior is responsive but stable.

中文翻译：
RQ2 的问题是：在气候扰动场景下，MC-LSTM 和 CudaLSTM 哪个更稳健。我们先用历史数据训练，再在测试阶段对输入施加 Delta P 和 Delta T 扰动，然后比较性能退化与守恒闭合一致性。理想行为是“有响应，但稳定不过度失真”。

---

## Slide 13 - RQ3

English:
RQ3 asks whether globally pretrained models can transfer effectively to Bavarian and Alpine basins. The workflow is pretrain on Caravan, fine-tune locally, evaluate on held-out basins, and compare against scratch training. SHAP is used to explain which static attributes drive transfer success.

中文翻译：
RQ3 的问题是：全局预训练模型能否有效迁移到巴伐利亚和阿尔卑斯流域。流程是先在 Caravan 上预训练，再在本地微调，并在留出流域上评估，再与从零训练进行对照。最后使用 SHAP 解释哪些静态属性驱动迁移成功。

---

## Slide 14 - Summary

English:
To summarize: neural hydrology already shows strong predictive capability; the next frontier is extremes, climate-extrapolation reliability, and transferability. My three research questions are designed to address these three challenges directly.

中文翻译：
总结来说：神经水文学已经展现出较强的预测能力；下一阶段的前沿是极端事件、气候外推可靠性和迁移能力。我的三个研究问题就是针对这三项挑战直接设计的。

---

## Slide 15 - References

English:
All equations, values, and data sources are traceable in the references and validation notes. Thank you for listening. I am happy to take questions.

中文翻译：
所有公式、数值和数据来源都可以在参考文献和验证文档中追溯。感谢各位聆听，欢迎提问。
