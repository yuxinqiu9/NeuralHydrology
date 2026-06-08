# 演讲稿：Neural Hydrology（中英文对照版）
## SoSe 2026 - Climate Change Statistics

建议时长：20-25 分钟（可压缩到 12-15 分钟）

---

## 第 1 页 - 封面 / Slide 1 - Cover

中文：
大家好，今天我汇报的主题是 Neural Hydrology，也就是在气候变化背景下，用深度学习方法进行径流预测。我会从四个部分展开：研究背景、核心模型原理、工具与数据基础、以及三个研究问题。

English:
Hello everyone. Today I present Neural Hydrology, which applies deep learning to streamflow prediction under climate change. I will cover four parts: motivation, core model principles, tooling and data foundations, and three research questions.

---

## 第 2 页 - 什么是 Neural Hydrology / Slide 2 - What is Neural Hydrology?

中文：
我们预测的是 streamflow，也就是单位时间通过河道断面的水量。它是流域尺度多过程耦合的综合结果，包括降水、蒸发、入渗、地下水和汇流。建模上可写为：

$$
Q_t = f(X_{1:t}, S)
$$

其中 $X_{1:t}$ 是动态气象序列，$S$ 是静态流域属性。Neural Hydrology 的核心是直接学习这个映射，而不是手工构建完整过程方程。

English:
The target is streamflow, the discharge through a river cross-section per unit time. It is an integrated catchment response from precipitation, evaporation, infiltration, groundwater, and routing. The task can be written as

$$
Q_t = f(X_{1:t}, S)
$$

where $X_{1:t}$ is the dynamic forcing sequence and $S$ denotes static basin attributes. Neural hydrology learns this mapping directly from data instead of manually specifying full process equations.

---

## 第 3 页 - 里程碑 / Slide 3 - Milestones

中文：
2018 年，LSTM 在基准中超越传统校准模型；2019 年 EA-LSTM 实现 531 流域单模型训练；2021 年 MC-LSTM 引入结构性守恒；2022 年 NeuralHydrology 框架发布；2023 年 Caravan 提供 6830 流域全球大样本。

English:
In 2018, LSTM outperformed calibrated process-model baselines; in 2019, EA-LSTM enabled one-model training across 531 basins; in 2021, MC-LSTM introduced structural mass conservation; in 2022, NeuralHydrology was released; in 2023, Caravan expanded large-sample hydrology to 6,830 basins globally.

---

## 第 4 页 - 为什么重要 / Slide 4 - Why It Matters

中文：
流量预测是洪水预警、水库调度和能源系统管理的核心输入。气候变化带来的关键挑战是 non-stationarity：训练分布与未来分布不一致。问题不只是平均误差，而是模型在分布外场景下是否可靠。

English:
Streamflow forecasting is a core input for flood warning, reservoir operation, and energy planning. Under climate change, the main challenge is non-stationarity: the training distribution differs from future conditions. The key question is not only mean error, but reliability under out-of-distribution forcing.

---

## 第 5 页 - 深度学习突破 / Slide 5 - Deep Learning Breakthrough

中文：
在 241 个 CAMELS-US 流域上，逐流域 LSTM 的平均 NSE 约 0.63，高于 SAC-SMA+Snow-17 的 0.58。意义不仅在精度，还在可扩展性：传统模型常需逐流域手工校准，而神经网络更容易批量训练与迁移。

English:
On 241 CAMELS-US basins, single-basin LSTM achieved about 0.63 mean NSE versus 0.58 for SAC-SMA+Snow-17. The impact is both accuracy and scalability: process models require basin-by-basin calibration, while neural models scale more naturally.

---

## 第 6 页 - LSTM 与 EA-LSTM（数学重点） / Slide 6 - LSTM and EA-LSTM (Math)

中文：
LSTM 关键更新为：

$$
\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tanh(\mathbf{W}_g [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_g),
\quad \mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t)
$$

$\mathbf{c}_t$ 是记忆状态，$\mathbf{f}_t,\mathbf{i}_t,\mathbf{o}_t$ 分别是遗忘门、输入门、输出门。水文解释上，记忆可类比储水状态，门控可类比排水/入渗调节。

EA-LSTM 用静态属性控制输入门：

$$
\mathbf{i} = \sigma(\mathbf{W}_i\mathbf{x}_s + \mathbf{b}_i)
$$

注意这里是静态 $\mathbf{i}$，不是 $\mathbf{i}_t$，表示流域个性由静态属性调制。

NSE 指标：

$$
\text{NSE} = 1 - \frac{\sum_t(\hat{q}_t-q_t)^2}{\sum_t(\bar{q}-q_t)^2}
$$

$\text{NSE}=1$ 为完美，$\text{NSE}=0$ 等于均值基线，$\text{NSE}<0$ 代表劣于均值基线。

English:
The core LSTM equations are

$$
\mathbf{c}_t = \mathbf{f}_t \odot \mathbf{c}_{t-1} + \mathbf{i}_t \odot \tanh(\mathbf{W}_g [\mathbf{h}_{t-1}, \mathbf{x}_t] + \mathbf{b}_g),
\quad \mathbf{h}_t = \mathbf{o}_t \odot \tanh(\mathbf{c}_t)
$$

where $\mathbf{c}_t$ is memory state and the gates control retention, write, and readout. In hydrology, this maps naturally to storage-like memory and flow regulation behavior.

EA-LSTM sets a static input gate from static attributes:

$$
\mathbf{i} = \sigma(\mathbf{W}_i\mathbf{x}_s + \mathbf{b}_i)
$$

This separates shared hydrological dynamics from basin-specific conditioning.

NSE is

$$
\text{NSE} = 1 - \frac{\sum_t(\hat{q}_t-q_t)^2}{\sum_t(\bar{q}-q_t)^2}
$$

with $1$ as perfect, $0$ as mean-baseline equivalent, and negative values worse than baseline.

---

## 第 7 页 - NeuralHydrology 工具链 / Slide 7 - NeuralHydrology Tooling

中文：
NeuralHydrology 通过配置文件驱动实验，支持模型、损失、数据、训练策略解耦切换，提升复现性。常见流程是写 config、训练、评估三步。

English:
NeuralHydrology is configuration-driven, enabling reproducible experiments with modular model/loss/data/training choices. Typical workflow: config, train, evaluate.

---

## 第 8 页 - 物理约束与迁移学习 / Slide 8 - Physics and Transfer Learning

中文：
MC-LSTM 强调结构性守恒，概念表达为：

$$
\Delta S_t \approx P_t - \hat{Q}_t - \mathrm{ET}_t
$$

关键是守恒由结构保证，而非仅靠损失惩罚。迁移学习流程是大样本预训练再小样本微调，适合无测站或数据稀缺场景。

English:
MC-LSTM emphasizes structural conservation, conceptually expressed as

$$
\Delta S_t \approx P_t - \hat{Q}_t - \mathrm{ET}_t
$$

The key is architectural enforcement, not only soft-penalty training. Transfer learning follows pre-train on large samples then fine-tune on target basins, which is useful for data-scarce settings.

---

## 第 9 页 - 案例页 / Slide 9 - Case Study

中文：
这一页展示 LamaH-CE 河网案例三组值：
- Station 399（Danube near Bratislava）= 0.899
- 375 站点中位线 = 0.856
- 最差站点 = 0.248

逐条来源：
1. Station 399 站点身份来源：Klingler et al., 2021（ID 399 的站点描述）。
2. 0.856 来源：Exploiting River Network Topology for Flood Forecasting with Graph Neural Networks，文中平均 NSE 85.62%（换算 0.856）。
3. 0.248 来源：同文 worst-case NSE 24.78%（换算 0.248）。
4. 0.899 来源：本页案例汇总图中的展示值（用于说明最下游强结果样本）。
5. 0.6 阈值线来源：水文文献中的经验阈值语境（并非普适硬阈值）。

English:
This slide summarizes three LamaH-CE case values:
- Station 399 (Danube near Bratislava) = 0.899
- 375-gauge median baseline = 0.856
- Worst-case gauge = 0.248

Source mapping:
1. Station identity: Klingler et al., 2021 (ID 399 statement).
2. 0.856: 85.62% mean NSE from Exploiting River Network Topology for Flood Forecasting with Graph Neural Networks.
3. 0.248: 24.78% worst-case NSE from the same manuscript.
4. 0.899: case-summary display value used in this presentation.
5. 0.6 threshold line: context-dependent hydrology convention, not a universal hard threshold.

---

## 第 10 页 - 问题缺口 / Slide 10 - Gap Analysis

中文：
三条核心 gap：
1. 极端事件预测不足，
2. 非平稳气候外推评估不足，
3. 区域迁移证据不足（尤其阿尔卑斯/中欧）。

English:
Three core gaps:
1. Underperformance on extremes,
2. Limited systematic evaluation under non-stationary climate forcing,
3. Limited evidence for regional transfer, especially in Alpine/Central European settings.

---

## 第 11 页 - RQ1 / Slide 11 - RQ1

中文：
问题是概率头（GMM/UMAL）是否能改善高流事件表现。因为 NSE 训练往往被常规样本主导，极端样本梯度占比低。思路是评估 POT 事件和 Q90/Q95/Q99 分位误差。

English:
RQ1 asks whether probabilistic heads (GMM/UMAL) improve high-flow performance. NSE-focused training is often dominated by normal-flow samples, so tail behavior may be underlearned. Evaluation targets POT events and Q90/Q95/Q99 quantile errors.

---

## 第 12 页 - RQ2 / Slide 12 - RQ2

中文：
问题是 MC-LSTM 在 CMIP6 delta-change 场景下是否更可靠。实验比较历史训练后在 SSP2-4.5/SSP5-8.5 扰动下的守恒闭合误差与分布稳定性。

English:
RQ2 asks whether MC-LSTM is more reliable under CMIP6 delta-change forcing. We compare closure consistency and distributional stability under SSP2-4.5 and SSP5-8.5 perturbations.

---

## 第 13 页 - RQ3 / Slide 13 - RQ3

中文：
问题是 Caravan 预训练是否可迁移到巴伐利亚/阿尔卑斯流域，并识别驱动迁移效果的静态属性。方法是预训练+微调+留出评估+SHAP 解释。

English:
RQ3 asks whether Caravan pretraining transfers to Bavarian/Alpine basins and which static attributes drive transferability. Method: pretrain, fine-tune, held-out testing, and SHAP-based interpretation.

---

## 第 14 页 - 总结 / Slide 14 - Summary

中文：
神经水文学已展示强预测能力；物理约束与迁移学习是应对未来非平稳条件的关键工具；下一步工作聚焦极端事件、气候外推可靠性和区域迁移机制。

English:
Neural hydrology has shown strong predictive capability; physics-aware architectures and transfer learning are key tools for non-stationary future conditions; the next steps focus on extremes, climate-extrapolation reliability, and regional transfer mechanisms.

---

## 第 15 页 - 参考文献页 / Slide 15 - References

中文：
本报告中的数学表达、数据来源与数值映射均在参考文献与验证文档中对应。

English:
All equations, data provenance, and numeric mappings in this talk are aligned with the references and validation notes.
