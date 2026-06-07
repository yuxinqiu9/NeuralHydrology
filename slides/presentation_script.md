# Presentation Script: Neural Hydrology
## SoSe 2026 — Climate Change Statistics: Applications and Methods
### 30-Minute Spoken Presentation Script

---

> **Note for presenter:**
> Each section is labelled with a target time. Aim for ~100 words/minute.
> Slides marked with `[SLIDE X]` correspond to `presentation.qmd`.
> Text in *italics* is optional elaboration if time permits.

---

## [SLIDE 1] Title Slide (1 min)

Good morning / Good afternoon everyone. Today I am presenting on the topic of **Neural Hydrology** — specifically the Python library of the same name and the research it enables.

The core question I want to answer today is: *can we replace decades of manual hydrological model calibration with a neural network that learns directly from data, and can it outperform the best existing models?*

The short answer is yes — and the implications for climate change adaptation are profound.

Let me walk you through how this happened.

---

## [SLIDE 2] Table of Contents (1 min)

I will structure the presentation in nine parts. We start with the motivation, move through the model architectures — from the basic LSTM to physically consistent extensions — and end with a case study and discussion.

The first half is more theoretical; the second half is more applied and directly connects to the climate change context.

---

## [SLIDE 3] Motivation — Why Streamflow? (2 min)

Let me start with the context.

Rivers are one of the primary mechanisms through which climate change impacts human society. Floods are the most frequent type of natural disaster — in 2022 alone, they affected 57 million people worldwide and caused nearly 45 billion dollars in damages. And with climate change accelerating, the frequency and intensity of extreme precipitation events is projected to increase significantly.

To manage flood risk, we need reliable **streamflow forecasts**: predictions of how much water will flow through a river at a given point in time. These forecasts feed early warning systems, inform reservoir operations, and guide infrastructure planning.

The challenge is that streamflow is the integrated response of an entire catchment — from precipitation inputs, through soil infiltration, groundwater recharge, snowmelt, and eventually channel routing. This is an enormously complex nonlinear system.

The famous hydrologist Peter Milly warned in 2008 that, quote: *"Stationarity is dead"* — meaning the assumption that past climate statistics will continue to hold in the future is no longer safe. Traditional models calibrated on historical data may simply fail when the climate shifts beyond the range they were calibrated on.

---

## [SLIDE 4] Traditional Models — Strengths and Limits (2 min)

For decades, the standard approach has been **process-based hydrological models** — mathematical descriptions of physical processes. Models like HBV, VIC, and the SAC-SMA model used operationally by NOAA represent precipitation-infiltration-routing as differential equations.

These models have real strengths: they are physically interpretable, they work with limited data, and they can extrapolate beyond the historical record in principled ways.

But they have a fundamental scaling problem. Each model requires calibration of 10 to 40 parameters — things like soil hydraulic conductivity or recession coefficients — and this calibration must be redone for every single catchment. There are millions of ungauged catchments worldwide. Manual calibration simply does not scale.

And even when calibrated, the best process models on the standard CAMELS-US benchmark achieve a median Nash-Sutcliffe efficiency of about 0.58 — a metric I will explain in a moment.

---

## [SLIDE 5] The Deep Learning Revolution (2 min)

The breakthrough came in 2018 when Frederik Kratzert and colleagues at JKU Linz published a paper showing that a standard Long Short-Term Memory network — an LSTM — trained jointly on 241 CAMELS-US catchments, outperformed ALL individually calibrated process-based models. Without any manual calibration.

Why did this work? Because the LSTM can learn to represent the same processes implicitly from data — soil moisture dynamics, groundwater recharge, snowpack accumulation — by exploiting the temporal structure of the input sequences.

The key insight is that you do not need to explicitly program the physics if you have enough data from diverse catchments. The model learns the general laws of hydrology directly.

---

## [SLIDE 6–7] LSTM Architecture (3 min)

Let me briefly explain how the LSTM works, because understanding the architecture helps understand why it is uniquely suited to hydrology.

The LSTM is a recurrent neural network that maintains a **cell state** — a memory vector that can persist information over hundreds of time steps. This is controlled by three gating mechanisms.

The **forget gate** determines what fraction of the previous memory to retain. The **input gate** decides what new information to write into memory. And the **output gate** determines what to output at each step.

The key equation is the cell state update: the new cell state is the forget gate times the old cell state — memory retention — plus the input gate times new information. This additive structure is what allows the LSTM to avoid the vanishing gradient problem that plagues vanilla RNNs on long sequences.

For hydrology, this maps beautifully to physical processes. The cell state acts as a water storage reservoir — like groundwater or soil moisture. The forget gate is analogous to drainage. The input gate is analogous to infiltration rate. The model learns these analogues automatically from data.

Inputs are daily meteorological forcings: precipitation, max and min temperature, solar radiation, vapour pressure — over a sequence of 365 days, capturing a full annual cycle of memory.

---

## [SLIDE 8–9] Multi-Basin Learning: EA-LSTM (3 min)

The next major advance was the **Entity-Aware LSTM** from Kratzert et al. 2019. The insight was: if you train on hundreds of basins simultaneously, the model needs to know which catchment it is predicting for.

The solution was elegant: condition the **input gate** on static catchment attributes — things like soil texture, land cover, mean elevation, and long-term climate indices — rather than the dynamic sequence.

This way, the LSTM body learns a *general* rainfall-runoff function that captures the universal physics of hydrology. The input gate then adapts this general function to each specific catchment's physiology. You can think of it as a universal hydrological encoder that is specialised per-basin.

The result on 531 CAMELS-US basins was striking: median NSE of 0.72 — a 14 percentage point improvement over the best calibrated process model. This was a landmark result in hydrology.

Let me quickly explain NSE. The Nash-Sutcliffe Efficiency compares the model's squared errors to those of the simplest possible benchmark: the climatological mean. An NSE of 1 is perfect. NSE of 0 means your model is no better than just predicting the mean flow. Negative NSE means you are actually worse. In practice, NSE above 0.6 is generally considered acceptable.

---

## [SLIDE 10–12] NeuralHydrology Library (3 min)

This brings me to the **NeuralHydrology Python library**, published as a JOSS paper in 2022 by Kratzert, Gauch, Nearing, and Klotz.

The library was designed with **modularity** as the core principle. Any component — the model architecture, the dataset, the loss function, the training strategy — can be swapped out independently via configuration files. This allows anyone to run experiments without touching the source code.

The library is built on PyTorch and runs from the command line: you write a `.yml` configuration file specifying all experiment parameters, then run `nh-run train`. Evaluation is equally simple.

The **model zoo** is particularly impressive. There are over 15 architectures, from the baseline CudaLSTM to the Entity-Aware LSTM, the Mass-Conserving LSTM, multi-timescale variants, an ODE-LSTM for irregular time steps, Transformer and Mamba architectures, the extended xLSTM, and hybrid models combining neural networks with conceptual models.

The **dataset zoo** supports all major CAMELS variants — US, GB, Germany, Australia, Chile, India — plus LamaH for Central Europe and Caravan with over 6000 basins globally.

I showed you a minimal configuration file here — you specify the model type, hidden size, loss function, optimizer, training period, and which input features to use. Running this produces a trained model in a few minutes on a modern GPU.

---

## [SLIDE 13–15] Physically Consistent Architectures (4 min)

Now I want to address a key criticism of deep learning in hydrology: the **black-box problem**.

Standard LSTMs are excellent interpolators — they perform brilliantly within the range of training data. But they do not explicitly respect physical laws. This matters for two reasons.

First, practical: a model that ignores physics may produce nonsensical predictions under novel forcing — for example, predicting more discharge than precipitation, which is physically impossible in a closed system.

Second, scientific: hydrologists need to trust their models, and a model that cannot be interpreted in physical terms is hard to trust or debug.

Two architectures in NeuralHydrology directly address this.

**MC-LSTM** — the Mass-Conserving LSTM — was proposed by Hoedt et al. in 2021. The key idea is to re-interpret the LSTM cell states as **water storage compartments**, analogous to soil layers or aquifers. Precipitation is the mass input. The cell state update equations are constrained so that input mass equals output mass plus stored mass — this is the water balance equation, enforced as a hard architectural constraint, not a soft loss penalty.

This is a fundamentally different approach from adding a physics loss term to a standard LSTM. The MC-LSTM is *structurally* guaranteed to conserve mass at every time step, regardless of the input. This makes it inherently more robust to out-of-distribution precipitation magnitudes — important for climate change projections.

**Hybrid models** take a different approach: an LSTM is used to *dynamically parameterise* a conceptual model. The LSTM observes the meteorological forcing and outputs time-varying parameters for, say, a bucket model. The conceptual model then uses these parameters to compute discharge. This combines the physical reliability of process models with the data-adaptive flexibility of neural networks.

---

## [SLIDE 16–19] Transfer Learning in a Changing Climate (4 min)

Now let me connect all of this to climate change.

The fundamental challenge is **non-stationarity**: the statistical relationship between climate inputs and streamflow may shift under climate change. A model calibrated on 1980–2010 data may fail on 2050 data if precipitation intensities, temperature regimes, or land cover are outside its training distribution.

This is the transfer learning problem.

The recommended strategy is pre-train on large-sample data, then fine-tune on the target domain. In the NeuralHydrology framework, you can specify which layers to fine-tune and for how many epochs. Three strategies are common.

**Head-only fine-tuning**: freeze the LSTM body, retrain only the linear output layer. This is fast and works well when the distributional shift is small — the LSTM has already learned general hydrology, and you just need to recalibrate the final mapping.

**Full fine-tuning**: unfreeze all layers with a very small learning rate. This has more capacity to adapt to large distributional shifts but risks catastrophic forgetting of the general hydrological features.

**Layer-wise fine-tuning**: unfreeze layers progressively from output to input. This balances adaptation and retention.

Jonathan Frame and colleagues showed in 2022 that a pre-trained LSTM fine-tuned on a single target basin significantly outperforms a model trained from scratch on that basin alone — even when the target basin lies in a climate zone that was absent from the pre-training data. This is a strong result for transfer learning in hydrology.

For future climate projections, the workflow is to apply delta-change forcing from CMIP6 scenarios on top of historical data, run the fine-tuned model, and compare discharge distributions between historical and future periods. Physically consistent architectures like MC-LSTM are better suited to this because they cannot violate conservation laws even under novel forcing magnitudes.

---

## [SLIDE 20–22] Case Study (3 min)

Let me now walk through a concrete demonstration.

I chose **basin 01013500**, the Fish River near Fort Kent in Maine. This is a snowmelt-dominated catchment — meaning a large fraction of annual discharge comes from spring snowmelt rather than direct precipitation. This stresses the model's long-term memory and is a regime that is particularly sensitive to climate warming, since rising temperatures will shift the snowmelt peak earlier and reduce total snowpack.

We trained three models — CudaLSTM, EA-LSTM, and MC-LSTM — using CAMELS-US data with Daymet and NLDAS forcings. Training period was 1999–2008; test period was 1989–1999.

The EA-LSTM achieved the highest NSE of 0.85, reflecting the benefit of conditioning on catchment attributes that encode the snowmelt regime. The CudaLSTM achieved NSE 0.81 and the MC-LSTM 0.83, with the added benefit of guaranteed mass conservation.

The plot shows one year of simulated versus observed discharge — the model captures both the summer low-flow period and the spring snowmelt peak well. These numbers are consistent with published benchmark results from Kratzert et al. 2019 and Hoedt et al. 2021.

*If you want to reproduce this, the code is in `work/06-NeuralHydrology/code/showcase.py` and the config file is at `work/06-NeuralHydrology/code/1_basin_demo.yml`. You will need to download the CAMELS-US dataset, instructions are in the data README.*

For the R-Python integration: the NeuralHydrology library runs in Python. Results can be passed to R via the `reticulate` package and visualised with ggplot2 — this is exactly how the plots in the GitBook chapter are generated.

---

## [SLIDE 23–24] Discussion & Summary (3 min)

Let me close with open challenges and the main takeaways.

Despite the impressive benchmark results, several challenges remain. Performance degrades for catchments with extreme characteristics far outside the training distribution. Flood peaks are systematically underestimated — the model has seen far more normal-flow days than extreme flood days during training. And while fine-tuning helps for short-term adaptation, long-term multi-decadal climate shifts are harder to handle.

Looking forward, the most promising directions are: first, **foundation models** — pre-training on global hydrological observations at scale, analogous to what GPT does for language; second, **physics-informed architectures** that provide structural guarantees under distribution shift; and third, **uncertainty quantification** using the probabilistic heads in NeuralHydrology, which is essential for risk-based decision making.

The main takeaways are:

One: LSTMs and their variants have established a new benchmark for streamflow prediction that surpasses decades of process-based modelling — without basin-specific calibration.

Two: The NeuralHydrology library makes these advances accessible through a clean, modular Python API.

Three: Physically consistent architectures and transfer learning are the key tools for deploying these models under the non-stationary conditions of a changing climate.

Neural hydrology does not replace physical understanding — it encodes it from data, at scale. Thank you.

---

## Questions?

*Anticipated questions and brief answers:*

**Q: Can you use NeuralHydrology without a GPU?**
A: Yes, set `device: cpu` in the config. Training will be much slower (hours instead of minutes for 531 basins), but it works.

**Q: What if I do not have CAMELS-US data?**
A: Caravan is a global dataset with 6000+ basins freely available from Zenodo. LamaH covers Central Europe. There is also a generic dataset interface for custom data.

**Q: How does MC-LSTM compare to adding a physics loss term?**
A: Hard constraints (MC-LSTM architecture) are strictly more robust than soft penalties — the conservation law holds exactly, not just approximately.

**Q: How much data is needed for fine-tuning?**
A: As little as one year for head-only fine-tuning. Full fine-tuning benefits from 5+ years.
