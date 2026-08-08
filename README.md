# NeuralHydrology Workspace Guide

This README explains how to use this `NeuralHydrology` folder as a standalone shared project.
It is organized by folder and by workflow:

1. Train models
2. Analyze results
3. Render slides and view charts

## 1. Folder Overview

```text
NeuralHydrology/
  analysis/        # post-training analysis scripts (Python)
  data/            # CAMELS_US dataset used by training configs
  rq3_finetune/    # core RQ3 training/evaluation scripts + yml configs + csv outputs
  slides/          # Quarto slides, chart rendering, html/pdf outputs
  README.md
```

## 2. Environment and Dependency Requirements

### 2.1 Python

Use this interpreter (already verified on this machine):

- Any Python interpreter/environment with `neuralhydrology` installed

Why: `rq3_finetune` scripts import `neuralhydrology.nh_run`.

### 2.2 Node + Quarto + R (for slides)

`slides/render.bat` needs:

1. Node.js (for `pdf.js`)
2. Quarto (for rendering `slides.qmd`)
3. Rscript (for R code chunks in slides)

The batch script auto-detects these tools and prints clear errors if missing.

## 3. data/ Folder: What It Is and How It Is Used

Path used by training configs/scripts:

- `data/CAMELS_US` (relative to this folder)

Expected structure (simplified):

```text
data/CAMELS_US/
  basin_mean_forcing/daymet/01..18/*.txt
  usgs_streamflow/01..18/*.txt
  camels_attributes_v2.0/*.txt
```

Notes:

1. Group folders `01` to `18` are required for group experiments.
2. Missing data files will cause training/evaluation to fail.

## 4. rq3_finetune/ Folder: Training and Evaluation

This is the core experiment folder.

### 4.1 Main files in rq3_finetune/

1. Training entrypoints
   - `run_pretrain_ea.py`
   - `run_folder_group_compare_ea.py`
   - `run_rq3_ea.py` (single-target-basin full pipeline)

2. Evaluation/summary scripts
   - `eval_global_true_by_group.py`
   - `gen_three_way_comparison.py`

3. Config templates
   - `pretrain_ea.yml`, `scratch_ea.yml`, `finetune_ea.yml`
   - and group-specific generated/derived yml files

4. Outputs
   - `results_*.csv`
   - checkpoint state json (e.g., `folder_groups_checkpoint_ea.json`)

### 4.2 How to start training (recommended RQ3 EA-LSTM flow)

Run in PowerShell:

```powershell
cd <path-to-NeuralHydrology>\rq3_finetune
python run_pretrain_ea.py
python run_folder_group_compare_ea.py
```

Resume from a specific group:

```powershell
python run_folder_group_compare_ea.py --start-group 05
```

Force rerun all groups:

```powershell
python run_folder_group_compare_ea.py --force-rerun
```

### 4.3 Where training outputs go

1. Model run directories:
   - Defined by the training scripts/configs (commonly a sibling `runs/` or project-level `runs/`)

2. Group-level csv summaries:
   - `rq3_finetune/results_*.csv`

## 5. analysis/ Folder: Post-Training Analysis Scripts

Scripts in this folder are not required for training.
They analyze csv outputs produced by `rq3_finetune`.

### 5.1 Script list and purpose

1. `check_group01.py`
   - quick check for Group 01 and all-group FT vs Global summary

2. `check_columns.py`
   - inspect csv columns/content sanity

3. `analyze_trend.py`
   - deeper FT vs Local/Global trend summary

4. `deep_analysis.py`
   - basin-level deep dive and group-level diagnostics

5. `check_all_basins_ft_vs_global.py`
   - all-basin merge with per-group global eval and vote stats

6. `compare_basin_ft_vs_global_arch.py`
   - basin-level FT vs Global comparison between EA-LSTM and CudaLSTM

7. `model_comparison.py`
   - grouped architecture comparison metrics and consistency checks

### 5.2 How to run analysis scripts

```powershell
cd <path-to-NeuralHydrology>\analysis
python check_group01.py
python model_comparison.py
```

Notes:

1. These scripts now resolve `rq3_finetune` paths relative to their own location.
2. They assume required `results_*.csv` already exist.

## 6. slides/ Folder: Render and View Charts

This folder is self-contained for slide rendering.

### 6.1 Key files

1. `slides.qmd`
   - main Quarto source

2. `render.bat`
   - one-click render pipeline (HTML + PDF)

3. `book.bib`
   - local bibliography file used by slides

4. `pdf.js`
   - Node script to capture slides and build pdf

5. `output/slides.html` and `output/slides.pdf`
   - rendered outputs

### 6.2 How to render slides

Option A (double click):

1. Open folder `NeuralHydrology/slides`
2. Double-click `render.bat`

Option B (terminal):

```powershell
cd <path-to-NeuralHydrology>\slides
cmd /c render.bat
```

### 6.3 How to view charts in slides

1. Open `output/slides.html` in browser for interactive slides.
2. Open `output/slides.pdf` for static exported version.

Most charts are generated from csv files loaded in `slides.qmd` setup chunk (from `../rq3_finetune/`).

## 7. End-to-End Recommended Workflow

1. Prepare data in `data/CAMELS_US`.
2. Run training in `rq3_finetune/`:
   - `run_pretrain_ea.py`
   - `run_folder_group_compare_ea.py`
3. Run selected scripts in `analysis/` for diagnostics.
4. Render `slides/render.bat` to produce html/pdf charts.

## 8. Troubleshooting

1. `ModuleNotFoundError: neuralhydrology`
   - Activate/select a Python environment where `neuralhydrology` is installed.

2. Training script cannot find data
   - Check `data/CAMELS_US` structure and absolute paths in yml/scripts.

3. slides render fails on Quarto/Node/R
   - Install missing tool reported by `render.bat`.

4. slides render fails on missing csv
   - Run training/evaluation first so `rq3_finetune/results_*.csv` exist.

## 9. Quick Command Cheat Sheet

```powershell
# Training
cd <path-to-NeuralHydrology>\rq3_finetune
python run_pretrain_ea.py
python run_folder_group_compare_ea.py

# Analysis
cd <path-to-NeuralHydrology>\analysis
python check_group01.py

# Slides
cd <path-to-NeuralHydrology>\slides
cmd /c render.bat
```
