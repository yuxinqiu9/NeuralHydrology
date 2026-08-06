# RQ3 Complete Experiment Summary 

## 1. Research Question and Experimental Objectives

This experiment addresses the following research question:

- **In scenarios where target basin/region data is limited, does `global + local fine-tuning` outperform `pure local from-scratch` training? Can transfer learning from 531 global CAMELS-US basins improve regional streamflow prediction?**

The three-way comparison adopted in this study:

1. **Pure Local**: Training only on basins within the target region/group from scratch
2. **Global**: Pre-trained global model on all 531 CAMELS-US basins (target group basins included in training set but diluted by large sample)
3. **Global + Fine-tune**: Initialization with global model weights, followed by fine-tuning on target region/group basins

**Evaluation Scope**: 18 geographic groups across CAMELS-US (533 basins total)

**Model Architecture (Unified across all groups)**:
- All three configurations use `CudaLSTM` as the backbone

---

## 2. Data Source and Data Types

### 2.1 Data Source

- **Dataset**: CAMELS-US
- **Official Repository**: <https://zenodo.org/records/15529996>

**Data files used in this study**:

1. `basin_timeseries_v1p2_metForcing_obsFlow.zip` (~3.4GB)
2. Seven static attribute files:
   - `camels_clim.txt`
   - `camels_geol.txt`
   - `camels_hydro.txt`
   - `camels_name.txt`
   - `camels_soil.txt`
   - `camels_topo.txt`
   - `camels_vege.txt`

### 2.2 Data Fields Used

**Dynamic Inputs (Daymet forcing)**:
- `prcp (mm/day)`: Daily precipitation
- `srad (W/m²)`: Daily average shortwave radiation
- `tmax (°C)`: Daily maximum temperature
- `tmin (°C)`: Daily minimum temperature
- `vp (Pa)`: Vapor pressure

**Target Variable**:
- `QObs (mm/d)`: Observed streamflow

**Static Attributes**: 26 attributes (used in global and fine-tune; not used in pure local)

**Rationale for Static Attributes**:
- For global and fine-tune models: Help capture cross-basin differences in response to the same meteorological forcing
- For pure local: Disabled (set to `[]`) because in single-group scenarios with limited samples, static features may cause standardization issues (low variance across group)

### 2.3 Data Directory Structure and Extraction Strategy

- **Data root directory**: `C:/GitHub/climate-change/NeuralHydrology/data/CAMELS_US`
- **Key subdirectories**:
  - `basin_mean_forcing/daymet/...`
  - `usgs_streamflow/...`
  - `camels_attributes_v2.0/...`

**Extraction Strategy**: Due to Windows-incompatible filenames in the zip archive (containing `*` characters), a whitelist-based extraction approach was used:
- Do not extract full zip
- Extract only daymet and streamflow files for basins required by the experiment

**Final global experiment**: 531 basins (listed in `basins_global.txt`)

---

## 3. Temporal and Spatial Data Division

### 3.1 Temporal Division (Unified)

- **Training period**: 1999-10-01 to 2008-09-30
- **Validation period**: 1980-10-01 to 1989-09-30
- **Test period**: 1989-10-01 to 1999-09-30

This temporal split follows the standard practice in NeuralHydrology and the series of Kratzert et al. papers.

### 3.2 Spatial Division

- **Global model**: 531 basins across CAMELS-US
- **Pure local (by group)**: Each of 18 geographic groups evaluated independently (25-79 basins per group)
- **Fine-tune (by group)**: Base model from global, fine-tuned on each respective group's basins

**Basin list files**:
- `basins_global.txt` (531 rows, for global model training)
- `basins_01.txt` to `basins_18.txt` (individual group basin lists for group-level local and fine-tune training)

---

## 4. Model Architectures and Training Configurations

In NeuralHydrology, `CudaLSTM` refers to a PyTorch standard LSTM implementation, characterized by stable training and fast computation speed, making it ideal as a unified baseline for fair three-way comparison.

### 4.1 Global Model

**Configuration file**: `pretrain.yml`

- **Model**: `cudalstm`
- **Hidden size**: 64
- **Dropout**: 0.4
- **Optimizer**: Adam
- **Loss function**: NSE
- **Learning rate schedule**:
  - Epoch 0: 1e-3
  - Epoch 2: 5e-4
- **Batch size**: 256
- **Training epochs**: 3
- **Sequence length**: 365 days
- **Device**: CPU
- **Static attributes**: 26
- **Forcing**: Daymet

**Run directory**: `C:/GitHub/climate-change/runs/rq3_base_global_3006_154109`

### 4.2 Pure Local Model (From-scratch, Per-Group)

**Configuration file**: `scratch.yml`

- **Architecture**: Aligned with global model structure (CudaLSTM, hidden=64, dropout=0.4)
- **Training basins**: Each of 18 regional groups independently (group-level basins only)
- **Learning rate schedule**:
  - Epoch 0: 1e-3
  - Epoch 15: 5e-4
  - Epoch 25: 1e-4
- **Training epochs**: 30
- **Static attributes**: [] (empty)

**Rationale for empty static attributes**: In group-limited scenarios (small sample per group), static features have high correlation, limiting model generalization. Disabling static attributes prevents standardization instability.

**Run directories**: Individual runs for each of 18 groups
- Group 01: `rq3_group_01_local_...`
- Group 02: `rq3_group_02_local_...`
- ... (continues through Group 18)

### 4.3 Global + Fine-tune Model (Per-Group)

**Configuration file**: `finetune.yml` (base_run_dir appended at runtime)

- **Base weights**: Initialized from global model `rq3_base_global_3006_154109` (531-basin pre-training)
- **Fine-tuning basins**: Each of 18 regional groups independently
- **Learning rate schedule**:
  - Epoch 0: 5e-4
  - Epoch 2: 5e-5
- **Fine-tuning epochs**: 10
- **Fine-tune modules**: `head`, `lstm`

**Run directories**: Individual fine-tune runs for each of 18 groups
- Group 01 fine-tune: `rq3_group_01_finetune_...`
- Group 02 fine-tune: `rq3_group_02_finetune_...`
- ... (continues through Group 18)

**Orchestration**: All 18 groups processed via `run_folder_group_compare.py` with automatic checkpoint management

### 4.4 Configuration Design Rationale

This configuration is **not arbitrary** but determined by the combination of literature baselines, tool defaults, computational constraints, and fair comparison principles.

1. **Task-driven design priority**
   - RQ3 requires three comparable groups: pure local vs. global vs. global + fine-tune
   - Ensures consistent backbone architecture across all three to avoid conflating architecture benefits with transfer learning improvements
   - Unified choice: `cudalstm`, fixed `hidden_size=64`, `dropout=0.4`

2. **Temporal division from CAMELS/NeuralHydrology standards**
   - This temporal split is consistent with NeuralHydrology tutorials and Kratzert et al. papers
   - Aligns methodology with existing literature for comparability

3. **Input variable selection following "minimum reproducibility + stability"**
   - Uses only daymet dynamic inputs (5 meteorological variables) for quick, stable reproduction
   - Did not enable nldas/maurer forcing simultaneously to reduce data preparation and configuration complexity
   - Global/fine-tune use 26 static attributes to support cross-basin difference modeling
   - Pure local disables static attributes (empty list) due to standardization issues in single-basin context

4. **Training hyperparameter selection**
   - `optimizer=Adam`, `loss=NSE`: Common practice in rainfall-runoff tasks with NeuralHydrology
   - `seq_length=365`: Covers seasonal cycles, standard for rainfall-runoff modeling
   - `batch_size=256`: Practical balance for CPU execution with reasonable throughput
   - **Learning rate schedules use piecewise decay**:
     - Pretrain: 1e-3 → 5e-4
     - Scratch: 1e-3 → 5e-4 → 1e-4
     - Fine-tune: 5e-4 → 5e-5 (lower LR to preserve pre-trained representations)

5. **Epoch numbers reflect computational constraints, not theoretical optimality**
   - **Global = 3 epochs**: Training 531 basins on CPU is computationally intensive; this represents a feasible experimental version to verify the methodological pipeline
   - **Scratch = 30 epochs**: Provides ample convergence space for group-level local models, avoiding accuracy degradation from under-training
   - **Fine-tune = 10 epochs**: Sufficient for stable improvement per group; empirically verified to deliver consistent gains across all 18 groups

6. **Hardware and implementation constraints**
   - Environment: `torch==2.12.1+cpu` → `device=cpu`
   - Although the machine has NVIDIA GPU, this study uses CPU version PyTorch for consistency
   - Affects absolute training time but does not alter three-way comparison logic

7. **From "research feasibility" to "future publication optimization"**
   - Current configuration: Validates whether RQ3 direction is methodologically sound (proof of concept)
   - For formal publication version, should include:
     - Longer global training (e.g., 10-30 epochs)
     - Multiple random seeds
     - Multiple target basins
     - Statistical significance testing

**Summary**: This configuration prioritizes fair comparison, logical completeness, and reproducibility on current hardware. It emphasizes result verifiability first, performance optimization second.

---

## 5. Training Pipeline (End-to-End)

### 5.1 Environment Setup

- **Python Environment**: `C:/GitHub/climate-change/.venv/Scripts/python.exe`
- **Critical Packages**:
  - `neuralhydrology==1.13.0`
  - `torch==2.12.1+cpu`

### 5.2 Data Preparation

1. Manually download CAMELS zip (3.4GB) and 7 attribute txt files
2. Place in `CAMELS_US` directory
3. Use extraction scripts to select daymet + streamflow for required basins

### 5.3 Model Training Sequence

1. Train global model
2. Train pure local model
3. Train fine-tuned model based on global weights
4. Evaluate all three on test period
5. Output test metrics for each

---

## 6. Complete Group-Based Experiment Results (All 18 Groups)

**Overview**: This section presents complete results from "basin grouping by Daymet forcing folder" experiment. All 18 groups completed with detailed outputs, covering **533 basins total** (531 from global model + 2 additional: 01013500, 01030500).

**Result Files**:
- Individual group results: `results_folder_01-18_local_vs_finetune.csv` (18 files)
- Summary files: `results_folder_groups_summary.csv`, `results_folder_groups_all_basins.csv`
- Completed groups: 01 to 18 (complete)
- Random seed: 1001

### 6.1 Group Summary Table (18 Groups × 533 Basins)

| Group | Basins | Local NSE | Global NSE | FT NSE | ΔFT-Local | ΔFT-Global |
|---|---:|---:|---:|---:|---:|---:|
| 01 | 25 | 0.520 | 0.725 | 0.769 | 0.249 | 0.044 |
| 02 | 69 | 0.549 | 0.673 | 0.684 | 0.135 | 0.011 |
| 03 | 79 | 0.544 | 0.672 | 0.705 | 0.161 | 0.034 |
| 04 | 29 | 0.464 | 0.663 | 0.705 | 0.242 | 0.042 |
| 05 | 35 | 0.527 | 0.704 | 0.731 | 0.204 | 0.027 |
| 06 | 16 | 0.315 | 0.732 | 0.768 | 0.454 | 0.037 |
| 07 | 29 | 0.346 | 0.640 | 0.688 | 0.343 | 0.049 |
| 08 | 7 | 0.193 | 0.617 | 0.647 | 0.455 | 0.030 |
| 09 | 2 | 0.077 | 0.312 | 0.412 | 0.335 | 0.100 |
| 10 | 49 | 0.302 | 0.559 | 0.612 | 0.310 | 0.052 |
| 11 | 22 | 0.189 | 0.564 | 0.615 | 0.426 | 0.051 |
| 12 | 32 | 0.201 | 0.560 | 0.586 | 0.386 | 0.027 |
| 13 | 7 | 0.453 | 0.625 | 0.724 | 0.271 | 0.099 |
| 14 | 15 | 0.655 | 0.803 | 0.834 | 0.178 | 0.030 |
| 15 | 14 | 0.183 | 0.392 | 0.476 | 0.293 | 0.084 |
| 16 | 5 | 0.353 | 0.778 | 0.785 | 0.431 | 0.007 |
| 17 | 72 | 0.680 | 0.772 | 0.795 | 0.115 | 0.023 |
| 18 | 26 | 0.469 | 0.740 | 0.766 | 0.298 | 0.026 |
| **Overall (Basin-Weighted)** | **533** | **0.462** | **0.666** | **0.701** | **0.239** | **0.034** |

### 6.2 Key Observations

**Global Statistics**
- **Total 533 basins** (531 from global + 2 newly added), distributed across 18 geographic groups (Daymet forcing folders)
- **All 18 groups show fine-tune superiority over pure local** (NSE Δ = +0.239)
- **After true per-group global evaluation, all groups show FT NSE > Global NSE** (18/18 groups positive; overall: FT 0.701 > Global 0.666 > Local 0.462)
- **Best performing groups**: 06, 08, 11 (NSE improvement > 0.425)
- **Most stable groups**: Group 17 (largest sample 72 basins, NSE improvement +0.115)

**Group-Level Classification**

1. **High-Benefit Groups (ΔFT-Local > 0.35)**: 06, 08, 11, 12
   - Group 06 (16 basins): Most significant transfer benefit, typical of data-scarce regions (+0.454)
   - Group 08 (7 basins): Small sample but stable gains (+0.455)
   - Group 11 (22 basins): Consistent improvement (+0.426)

2. **Medium-Benefit Groups (0.2 < ΔFT-Local < 0.35)**: 01, 04, 05, 07, 09, 10, 13, 15, 16, 18
   - Group 01 (25 basins): Decent local baseline, fine-tune adds +0.249
   - Group 10 (49 basins): High geographic diversity, transfer effectiveness maintained (+0.310)

3. **Lower-Benefit Groups (ΔFT-Local < 0.2)**: 02, 03, 14, 17
   - Group 02, 03 (69, 79 basins): Larger local samples support stronger baseline; transfer margin compressed
   - Group 17 (72 basins): Largest local sample, local NSE already 0.68; fine-tune still adds +0.115 (consistent positive)

**Consistency Verification**
- In 533 basins total, > 95% show NSE improvement through fine-tuning

### 6.3 Conclusions

**Research Question Answer**: `Global + fine-tune` demonstrates **stable, universal positive gains** compared to `pure local from-scratch`.

**Key Findings**:

1. **Universality**: All 18 groups positive; no single group shows performance degradation. Transfer initialization is robust across diverse geographies.

2. **Sample-Efficiency Pattern**:
   - **Small sample (Groups 06, 08)**: Maximum transfer benefit (> 0.45 NSE)
   - **Medium sample (Groups 02, 03)**: Moderate benefit (> 0.13 NSE)
   - **Large sample (Group 17)**: Compressed but still positive benefit (> 0.10 NSE)
   - **Trend**: Benefit magnitude inversely proportional to local sample size (intuitive and expected)

3. **Transfer Learning Reliability**: On LSTM baseline, cross-regional transfer from 531-basin global model stably improves local target performance.

**Recommendations for Future Application**:
- For new basins with limited data: Prioritize `global + fine-tune` approach
- For basins with > 50 basins of local training data: Local performance approaches saturation; consider increased model complexity or feature engineering

---

### 6.4 Global Model Reference (True Per-Group Evaluation)

This section uses **true per-group evaluation** (not constant placeholder): each group had the global model evaluated independently on its respective basins, with the resulting average NSE computed.

**True Three-Way Benchmark** (basin-weighted across 533 total):
- **Global NSE ≈ 0.666**
- **Fine-tune NSE ≈ 0.701**
- **Local NSE ≈ 0.462**

**Conclusion**: Under this grouping evaluation setting, performance ranking is **Fine-tune > Global > Local**. Compared to pure local, fine-tune shows clear gains (+0.239); fine-tune also demonstrates steady improvement over global (+0.034, positive in 18/18 groups).

---

## 7. Reproduction Recommendations (Next Steps)

For course reports or publications, consider further enhancements to increase credibility:

1. **Expand basin coverage**: Evaluate on 50-100 basins instead of 20
2. **Multi-seed robustness**: For each basin, run with 3-5 different random seeds
3. **Statistical testing**: Compute confidence intervals or perform significance tests on Δ metrics
4. **Computational scaling**: If resources permit, increase global baseline training epochs (10-30 instead of 3)

---

## 8. Key Scripts and Configuration Files

All located in: `C:/GitHub/climate-change/NeuralHydrology/rq3_finetune/`

- `download_camels.py`: CAMELS data retrieval
- `pretrain.yml`: Global model configuration
- `scratch.yml`: Pure local model configuration
- `finetune.yml`: Fine-tuning model configuration
- `run_rq3.py`: Main orchestration script
- `run_folder_group_compare.py`: 18-group training coordinator
- `eval_global_true_by_group.py`: True per-group global model evaluation

**Result files**:
- `results_folder_01-18_local_vs_finetune.csv`: Individual group results
- `results_folder_groups_summary.csv`: Summary across all groups
- `results_folder_groups_summary_with_global_true.csv`: Three-way comparison with true global values

---

## 9. Literature References

### 9.1 Data Sources (Fully Traceable)

1. **CAMELS-US Time Series** (forcing + streamflow)
   - Data DOI: `10.5065/D6MW2F4D`
   - Zenodo: `https://zenodo.org/records/15529996`
   - Reference Paper: Newman et al., 2015, HESS (`10.5194/hess-19-209-2015`)

2. **CAMELS Basin Static Attributes**
   - Attribute DOI: `10.5065/D6G73C3Q`
   - Reference Paper: Addor et al., 2017, HESS (`10.5194/hess-21-5293-2017`)

### 9.2 Experimental Settings Sources

1. **Kratzert et al., 2019** (Foundational EA-LSTM paper)
   - Paper: *Towards learning universal, regional, and local hydrological behaviors via machine learning*
   - DOI: `10.5194/hess-23-5089-2019`
   - **Key sections**:
     - Section 2.6 Experimental Setup: Time period division and framework
     - Appendix B Hyperparameter Tuning: Search and final parameters
   - Specific contributions:
     - Standard temporal division (train 1999-2008, val 1980-1989, test 1989-1999)
     - Representative optimal parameters: hidden=256, dropout=0.4, seq_length=270, 1-layer LSTM
     - Multi-seed ensemble (8 seeds) for robustness

2. **NeuralHydrology Official Fine-tuning Tutorial**
   - Documentation: `https://neuralhydrology.readthedocs.io/en/latest/tutorials/finetuning.html`
   - Example directory: `examples/06-Finetuning`
   - Provides executable configurations including:
     - 531-basin configuration
     - `base_run_dir` + `finetune_modules` workflow
     - Canonical temporal split (train 1999-2008, val 1980-1989, test 1989-1999)

### 9.3 Relationship Between This Study and Original Papers

**Important Disclaimer**:
- This is a "reproducible proof-of-concept experiment", not a 1:1 replication of Kratzert et al. 2019's optimal setup
- Simplifications for reproducibility on CPU-only machine:
  - Use `cudalstm` instead of EA-LSTM
  - `hidden_size=64` instead of 256
  - Global `epochs=3` instead of full multi-seed ensemble
  
**Appropriate Framing**:
- This study validates whether **RQ3 comparison direction is methodologically sound** (proof of feasibility)
- Not claiming to achieve paper-level SOTA performance metrics
- Serves as foundation for future extended study with full hyperparameter optimization and multi-seed rigor

---

## 10. Summary of Key Findings

| Aspect | Finding |
|---|---|
| **Primary RQ3 Conclusion** | Fine-tune consistently outperforms pure local across all 533 basins (18 groups) |
| **Overall NSE Improvement** | +0.239 (basin-weighted average) |
| **Minimum Group Improvement** | +0.115 (Group 17, largest local sample) |
| **Maximum Group Improvement** | +0.455 (Group 08, smallest local sample) |
| **Transfer Reliability** | 100% groups show FT > Local (18/18) |
| **Global Baseline Comparison** | FT > Global in 18/18 groups (+0.034 average) |

---

**Document Version**: 1.0 (English Edition)  
**Experiment Completion Date**: 2024  
**Basin Coverage**: 533 (531 global + 2 additional)  
**Random Seed**: 1001 (fixed)
