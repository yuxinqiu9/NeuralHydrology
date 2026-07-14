# Presentation Script: Neural Hydrology (English-Led, Bilingual)
## SoSe 2026 - Climate Change Statistics

Suggested duration: 30-35 minutes  
Format: English main line + Chinese support line for each slide

---

## Slide 1 - Cover

English:
Hello everyone. Today I will present my final project on neural hydrology under climate change, focusing on whether transfer learning can improve regional streamflow prediction in a robust and practical way.

中文：
大家好。今天我汇报气候变化背景下的神经水文学研究，核心问题是迁移学习能否以稳健、可落地的方式提升区域流量预测。

---

## Slide 2 - Contents

English:
This talk has five parts: fundamentals, research gap, methodology, empirical results, and discussion. I will move from motivation to evidence, then to practical implications.

中文：
本次汇报分为五部分：基础背景、研究缺口、方法设计、实证结果和讨论。我会从动机讲到证据，再落到实践启示。

---

## Slide 3 - What is Neural Hydrology?

English:
On the right figure, we can read the full water pathway from top to bottom. First, rainfall and snowmelt enter the basin. Then one part returns to the atmosphere through evapotranspiration, one part infiltrates into soil and moves as groundwater flow, and another part travels as surface runoff into the river. The streamflow we measure at the outlet is the integrated result of all these processes. Neural hydrology learns this full input-to-streamflow mapping directly from data, across many catchments.

中文：
看右侧这张图，我们可以按从上到下的顺序理解完整水文路径。首先是降雨和融雪进入流域；接着一部分水通过蒸散返回大气，一部分入渗到土壤并形成地下水流，还有一部分作为地表径流汇入河道。我们在流域出口观测到的 streamflow，就是这些过程叠加后的综合结果。神经水文学要做的，就是从数据中直接学习这条“输入到流量”的整体映射，而且是在很多流域上同时学习。

---

## Slide 4 - Why Streamflow Prediction Matters

English:
Reliable streamflow prediction supports flood early warning, reservoir operation, and hydropower scheduling. Under climate change, non-stationarity increases prediction difficulty because future conditions differ from historical patterns.

中文：
可靠的流量预测对洪水预警、水库调度和水电管理非常关键。气候变化导致非平稳性增强，未来条件与历史模式不一致，使预测更困难。

---

## Slide 5 - Milestones in Neural Hydrology

English:
The field evolved quickly: LSTM success in rainfall-runoff modeling, EA-LSTM for multi-basin conditioning, MC-LSTM with mass conservation, and large-sample benchmarks such as Caravan.

中文：
该领域发展迅速：从 LSTM 在降雨径流任务中的突破，到 EA-LSTM 的多流域条件化，再到 MC-LSTM 的质量守恒与 Caravan 大样本基准。

---

## Slide 6 - LSTM and EA-LSTM

English:
LSTM is a sequence model with an explicit memory cell. At each timestep, three gates control information flow: the forget gate decides how much past memory to keep, the input gate decides how much new information to write, and the output gate decides how much internal state to expose. In hydrology, this mechanism is useful because runoff depends on delayed processes such as soil storage and groundwater response. EA-LSTM extends LSTM by injecting static catchment attributes, such as area, slope, soil, and climate indices, into the gating mechanism, especially the input gate. This means the model does not treat all basins as identical; instead, each basin gets a different memory-update preference. So LSTM learns temporal dynamics, while EA-LSTM learns temporal dynamics plus basin-specific behavior, which is why EA-LSTM is better suited for multi-basin transfer learning.

中文：
LSTM 是一种带显式记忆单元的时序模型。每个时间步有三个门控来控制信息流：遗忘门决定保留多少历史记忆，输入门决定写入多少新信息，输出门决定暴露多少内部状态。在水文学中，这个机制很重要，因为径流响应常常具有滞后性，例如土壤蓄水和地下水过程。EA-LSTM 在 LSTM 基础上进一步引入流域静态属性（如面积、坡度、土壤和气候指数）来调制门控，尤其是输入门。这样模型就不会把所有流域当成同一种系统，而是给不同流域不同的记忆更新偏好。可以理解为：LSTM 学习“时间动态”，EA-LSTM 学习“时间动态 + 流域个体差异”，因此更适合多流域迁移学习任务。

---

## Slide 7 - Evaluation Metric I: NSE

English:
NSE is my primary metric. The formula is one minus a ratio. In the numerator, we sum squared errors between prediction and observation over time: \(\sum_{t=1}^{T}(\hat q_t-q_t)^2\). Here, \(\hat q_t\) is predicted streamflow at day \(t\), \(q_t\) is observed streamflow at day \(t\), and \(T\) is the number of timesteps in the evaluation period. In the denominator, \(\sum_{t=1}^{T}(q_t-\bar q)^2\) is the total variance of observed flow, where \(\bar q\) is the mean observed streamflow. Intuitively, NSE asks: is my model error smaller than the natural variability of the river itself? If NSE equals 1, prediction is perfect; if NSE equals 0, it is only as good as predicting the mean every day; if NSE is below 0, it is worse than that mean benchmark.

中文：
NSE 是主评价指标，它的形式是 1 减去一个比值。分子是预测误差平方和：\(\sum_{t=1}^{T}(\hat q_t-q_t)^2\)。其中，\(\hat q_t\) 表示第 \(t\) 天的预测流量，\(q_t\) 表示第 \(t\) 天的观测流量，\(T\) 是评估时段的时间步数量。分母是观测流量相对均值的离差平方和：\(\sum_{t=1}^{T}(q_t-\bar q)^2\)，其中 \(\bar q\) 是观测流量均值。直观上，NSE 在问一个问题：模型误差是否小于河流本身的自然波动？NSE=1 代表完美预测；NSE=0 代表和“每天都预测均值”一样好；NSE<0 代表比这个均值基线还差。

---

## Slide 8 - Evaluation Metric II: KGE

English:
KGE is my complementary metric, defined as \(1-\sqrt{(r-1)^2+(\alpha-1)^2+(\beta-1)^2}\). It contains three components. First, \(r\) is the correlation between predicted and observed flow, describing whether timing and dynamics are synchronized. Second, \(\alpha=\sigma_{\hat q}/\sigma_q\) is the variability ratio, where \(\sigma_{\hat q}\) is the standard deviation of predictions and \(\sigma_q\) is that of observations; it tells us whether peaks and trough amplitudes are over- or under-estimated. Third, \(\beta=\mu_{\hat q}/\mu_q\) is the bias ratio, where \(\mu_{\hat q}\) and \(\mu_q\) are predicted and observed means; it reflects systematic overprediction or underprediction. The optimal value for each component is 1, so KGE is best at 1. Compared with NSE, KGE is more diagnostic because it separates timing, variability, and bias.

中文：
KGE 是补充指标，定义为 \(1-\sqrt{(r-1)^2+(\alpha-1)^2+(\beta-1)^2}\)。它包含三个组成部分。第一，\(r\) 是预测与观测的相关系数，反映过程的时序和动态是否同步。第二，\(\alpha=\sigma_{\hat q}/\sigma_q\) 是变异性比例，其中 \(\sigma_{\hat q}\) 是预测流量标准差，\(\sigma_q\) 是观测流量标准差，用来判断洪峰和低谷的幅度是否被高估或低估。第三，\(\beta=\mu_{\hat q}/\mu_q\) 是偏差比例，其中 \(\mu_{\hat q}\) 和 \(\mu_q\) 分别是预测与观测均值，用于判断系统性高估或低估。三个分量的理想值都是 1，因此 KGE 的最优值也是 1。相比 NSE，KGE 的优势是可诊断性更强，能把“时序问题、振幅问题、偏差问题”拆开看。

---

## Slide 9 - NeuralHydrology: Python Library

English:
I use the NeuralHydrology framework because it is config-driven, reproducible, and supports multiple architectures and datasets. This makes controlled comparison across experiments feasible.

中文：
我使用 NeuralHydrology 框架，因为它配置驱动、可复现，并支持多种模型与数据集，便于开展严格可比的对照实验。

---

## Slide 10 - The Research Gap: Why Transfer Learning?

English:
Global models are strong on average, but regional performance remains heterogeneous. The open question is whether global pretraining plus local fine-tuning can systematically improve weak or data-sparse regions.

中文：
全局模型平均表现较好，但区域间性能仍然不均衡。核心问题是：全局预训练加本地微调，能否系统性改善弱势或数据稀缺区域。

---

## Slide 11 - CAMELS-US Dataset Overview

English:
The study uses CAMELS-US with 531 basins, daily streamflow, Daymet forcings, and rich static attributes. It provides a consistent large-sample setting for transfer-learning analysis.

中文：
本研究使用 CAMELS-US 数据集，包含 531 个流域、日尺度流量、Daymet 气象强迫及丰富静态属性，适合进行统一条件下的大样本迁移学习分析。

---

## Slide 12 - CAMELS-US Basins by Group (Map)

English:
This map shows basin locations colored by 18 geographic groups. It confirms broad spatial coverage and strong heterogeneity, which is important for evaluating transfer robustness.

中文：
这张地图按 18 个地理组展示流域空间分布。它说明样本覆盖广泛且异质性显著，有助于检验迁移学习的鲁棒性。

---

## Slide 13 - Temporal Splits and Distribution Shift

English:
I use non-contiguous temporal splits for training, validation, and testing because I want a realistic generalization test, not an easy interpolation test. If splits are fully contiguous and adjacent, train and test can be too similar. Here, the gap between periods introduces distribution shift on purpose, which is closer to climate-change applications where future regimes may differ from historical regimes. Validation has a specific decision role: it is used for hyperparameter selection, early stopping, and best-checkpoint selection. In other words, training updates model weights, validation chooses the model configuration, and testing is kept untouched for final reporting.

中文：
我采用非连续时间切分进行训练、验证和测试，核心目的是做“真实泛化测试”，而不是“容易的插值测试”。如果时间段完全相邻，训练和测试往往过于相似，结果会偏乐观。这里刻意让时间段拉开，主动引入分布偏移，更接近气候变化场景下“未来分布不同于历史分布”的实际问题。Validation 的作用非常具体：用于超参数选择、early stopping、以及最佳 checkpoint 选择。也就是说，训练集负责更新权重，验证集负责做模型决策，测试集保持不参与调参，只用于最终结果汇报。

---

## Slide 14 - Input Features and Variables

English:
Inputs include daily meteorological forcings and static basin attributes such as area, slope, and elevation. These features jointly represent both dynamic forcing and structural basin differences.

中文：
输入包括日尺度气象强迫和流域静态属性（如面积、坡度、高程），共同刻画动态驱动与流域结构差异。

---

## Slide 15 - Output / Processing

English:
The target is daily streamflow with standardized preprocessing and sequence modeling. This keeps feature scales comparable and stabilizes optimization.

中文：
预测目标是日尺度流量，采用标准化预处理和序列建模，以保证特征尺度可比并稳定训练过程。

---

## Slide 16 - Data Quality and Availability

English:
The evaluation covers 18 groups and 531 basins, with realistic group-size imbalance. Before training, we performed quality checks on basin-file completeness, group coverage consistency, time-split consistency, and metric alignment across runs. The key result is that data quality was already high and no major defects were detected, so no extra corrective processing was required beyond standard preprocessing.

中文：
评估覆盖 18 个地理组和 531 个流域，且组规模不均衡，符合真实数据场景。在训练前，我们先做了质量检查，包括 basin 文件完整性、分组覆盖一致性、时间切分一致性，以及不同实验结果的指标对齐。检查结论是：数据整体质量较高，没有发现需要额外修补的重大问题，因此除了标准预处理之外，没有再做额外的人工修正。

---

## Slide 17 - Testable Predictions

English:
I test two hypotheses: first, fine-tuning outperforms local-from-scratch; second, fine-tuning also outperforms direct global inference. Metrics are NSE and KGE with group-size-weighted aggregation.

中文：
我检验两个假设：第一，微调优于本地从零训练；第二，微调也优于直接全局推理。评估指标为 NSE 和 KGE，并采用按组规模加权汇总。

---

## Slide 18 - Model and Training Setup

English:
The primary architecture is EA-LSTM in a three-arm design: Local, Global, and Fine-tune. This setup isolates adaptation gain from pure local learning and zero-shot transfer.

中文：
主实验架构是 EA-LSTM，采用 Local、Global、Fine-tune 三分支设计，用于区分本地学习能力、零样本迁移能力和适配增益。

---

## Slide 19 - Evaluation Coverage: 18 Groups, 531 Basins

English:
This figure summarizes basin counts per group and confirms complete coverage of all 18 groups in the benchmark.

中文：
该图展示每组流域数量，确认基准中 18 个地理组均被完整覆盖。

---

## Slide 20 - Group Size Distribution

English:
Group sizes vary substantially. Therefore, weighted interpretation is necessary to avoid over-dominance by data-rich groups.

中文：
组规模差异显著，因此需要加权解读，避免大样本组对整体结论形成过度主导。

---

## Slide 21 - Overall Weighted NSE Comparison

English:
At the overall level, Fine-tune achieves the highest weighted NSE, indicating clear aggregate benefit over both Local and Global baselines.

中文：
在总体层面，Fine-tune 的加权 NSE 最高，说明相较 Local 与 Global 基线存在明确整体优势。

---

## Slide 22 - Overall Weighted KGE Comparison

English:
KGE shows the same ranking pattern. This cross-metric consistency strengthens confidence that gains are robust rather than metric-specific.

中文：
KGE 呈现相同排序，这种跨指标一致性增强了结果稳健性，说明收益并非单一指标偶然造成。

---

## Slide 23 - Group-Level NSE: Three-Way Comparison

English:
At group level, Fine-tune consistently leads. This suggests that transfer benefits are broad across regions, not concentrated in only a few groups.

中文：
在组层面，Fine-tune 持续领先，说明迁移收益具有广泛性，而非仅集中在少数组别。

---

## Slide 24 - Group-Level Delta NSE (FT vs Local and FT vs Global)

English:
Most delta bars are above zero for both comparisons, meaning fine-tuning improves over both local training and direct global inference in most groups.

中文：
两类对比中多数增量柱都高于零，表明微调在多数分组中同时优于本地训练和直接全局推理。

---

## Slide 25 - Group-Level Delta KGE (FT vs Local and FT vs Global)

English:
Delta KGE confirms the same improvement direction, reinforcing that transfer gains are stable across different performance aspects.

中文：
Delta KGE 也显示同方向提升，进一步说明迁移收益在不同性能维度上都较稳定。

---

## Slide 26 - Local Baseline vs Fine-Tuned Performance (Group Means)

English:
Points above the diagonal indicate groups where fine-tuning improves over local training. The concentration above the line demonstrates consistent benefit.

中文：
对角线以上的点表示微调优于本地训练。大部分点位于线上方，说明提升具有一致性。

---

## Slide 27 - Basin-Level NSE Distribution

English:
At basin level, the distribution shifts upward after fine-tuning, showing that gains are not limited to a few high-performing groups.

中文：
在流域层面，微调后 NSE 分布整体上移，说明收益并不只来自少数高性能组。

---

## Slide 28 - Basin-Level ECDF of NSE

English:
The fine-tuned ECDF curve dominates across quantiles, indicating distribution-wide improvement from low to high performance basins.

中文：
Fine-tune 的 ECDF 曲线在多个分位上占优，表明从低性能到高性能流域都出现了分布层面的改善。

---

## Slide 29 - Local Baseline Quality vs Transfer Gain

English:
This plot links baseline local quality with transfer gain, helping identify where adaptation contributes most.

中文：
该图刻画本地基线质量与迁移增益的关系，有助于识别适配策略最有效的应用场景。

---

## Slide 30 - Architecture Comparison: EA-LSTM vs CudaLSTM

English:
I run the same three-way logic on two architectures, EA-LSTM and CudaLSTM, under matched settings. The key question is whether transfer gains remain consistent across architectures.

中文：
我在 EA-LSTM 和 CudaLSTM 上使用相同三向实验逻辑与匹配设置，核心是检验迁移收益是否跨架构一致。

---

## Slide 31 - Overall Performance: EA-LSTM vs CudaLSTM

English:
Both architectures show the same transfer pattern: Fine-tune outperforms Local and Global. This supports the generality of the transfer-learning conclusion.

中文：
两种架构都呈现相同迁移模式：Fine-tune 优于 Local 和 Global，说明结论具有跨架构普适性。

---

## Slide 32 - Group 05 Three-Way Snapshot (EA-LSTM)

English:
Group 05 reproduces the full-dataset ranking pattern: Fine-tune > Global > Local. Both mean differences and basin-level win counts support this ordering.

中文：
在 Group 05 中也复现了全数据结论：Fine-tune > Global > Local。无论均值差异还是流域胜场统计都支持这一排序。

---

## Slide 33 - Group 05 Basin-Level Prediction Comparison (EA-LSTM)

English:
Per-basin bars show that gains are broadly distributed across basins in Group 05, not driven by one or two exceptional basins.

中文：
Group 05 的逐流域柱状图显示提升是广泛分布的，并非由个别异常流域拉动。

---

## Slide 34 - EA-LSTM Basin Win Rate: Fine-tune vs Global

English:
At basin level, fine-tuning beats global inference in 443 out of 531 basins, a win rate of about 83.4 percent.

中文：
在流域层面，Fine-tune 在 531 个流域中有 443 个优于 Global，胜率约 83.4%。

---

## Slide 35 - Key Findings: What the Results Demonstrate

English:
Three evidence-based conclusions stand out. First, transfer benefit is universal at group level: in the three-way comparison, Fine-tune consistently outperforms Local, and also outperforms Global across groups in our main NSE comparison. Second, the result is robust across scales: at group level, delta bars are mostly positive; at basin level, both the boxplot and ECDF show an upward distribution shift under Fine-tune, meaning gains are broad rather than driven by a few outliers. Third, gains are not random but structured: the Local-baseline-versus-transfer-gain analysis indicates larger gains in weaker-baseline settings, which supports the practical strategy of prioritizing transfer learning for data-scarce or hard-to-model regions. Finally, the basin win-rate result (443 out of 531) provides an intuitive operational summary that the improvement holds for the majority of basins.

中文：
这里有三点带证据的核心结论。第一，组层面的迁移收益具有普遍性：在三向对比中，Fine-tune 持续优于 Local，在主结果的 NSE 对比中也整体优于 Global。第二，结论在不同尺度上都稳健：组层面的增量柱状图多数为正；流域层面的箱线图和 ECDF 都显示 Fine-tune 分布整体上移，说明提升是“广泛发生”的，而不是少数异常点拉出来的。第三，收益具有结构性而非随机性：从“Local 基线质量 vs 迁移增益”的关系图可以看到，基线较弱的场景通常获得更大增益，这支持在数据稀缺或建模困难区域优先采用迁移学习。最后，流域胜率结果（531 个流域中有 443 个提升）提供了直观的落地总结：改进发生在大多数流域上。

---

## Slide 36 - Practical Implementation & Limitations

English:
For practice, start from global pretraining and always fine-tune locally. Current limitations include single seed, CAMELS-US-only scope, and reliance on NSE/KGE; future work should extend to larger global datasets and richer diagnostics.

中文：
实践建议是先全局预训练、再本地微调。当前局限包括单随机种子、仅 CAMELS-US、指标主要为 NSE/KGE；未来应扩展全球数据和更丰富诊断。

---

## Slide 37 - Conclusion

English:
Across 18 groups and 531 basins, global pretraining plus fine-tuning is a robust default strategy for regional streamflow prediction under data constraints.

中文：
在 18 个组、531 个流域上的结果表明：在数据受限条件下，全局预训练加本地微调是区域流量预测的稳健默认策略。

---

## Slide 38 - References

English:
All equations, datasets, and claims are traceable in the reference section. Thank you for listening, and I welcome your questions.

中文：
所有公式、数据来源和结论都可在参考文献中追溯。感谢聆听，欢迎提问。
