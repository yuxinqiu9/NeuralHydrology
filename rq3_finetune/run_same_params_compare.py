from pathlib import Path
import time
import pandas as pd

from neuralhydrology.nh_run import start_run, finetune, eval_run

WORK = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune")
RUNS_ROOT = Path(r"C:/GitHub/climate-change/runs")
TARGET = "01022500"


def newest(prefix: str, root: Path, after: float = 0.0) -> Path:
    cands = sorted(
        [p for p in root.glob(f"{prefix}*") if p.is_dir() and p.stat().st_mtime > after],
        key=lambda p: p.stat().st_mtime,
    )
    if not cands:
        raise FileNotFoundError(f"No runs matching {prefix} in {root}")
    return cands[-1]


def test_metric(run_dir: Path, basin: str):
    test_epochs = sorted((run_dir / "test").glob("model_epoch*"))
    csv = test_epochs[-1] / "test_metrics.csv"
    df = pd.read_csv(csv, dtype={"basin": str}).set_index("basin")
    return float(df.loc[basin, "NSE"]), float(df.loc[basin, "KGE"]), csv


# 1) pick latest global base
base_global = newest("rq3_base_global", RUNS_ROOT)

# 2) local scratch with same params
start_t = time.time()
start_run(WORK / "scratch_same_params.yml")
scratch_run = newest("rq3_scratch_local_same", RUNS_ROOT, after=start_t)

# 3) finetune with same params and same base
cfg_text = (WORK / "finetune_same_params.yml").read_text(encoding="utf-8")
cfg_text += f"\nbase_run_dir: {base_global.as_posix()}\n"
ft_cfg = WORK / "finetune_same_params_run.yml"
ft_cfg.write_text(cfg_text, encoding="utf-8")

start_t = time.time()
finetune(ft_cfg)
finetuned_run = newest("rq3_finetuned_same", WORK / "runs", after=start_t)

# 4) evaluate all
eval_run(base_global, period="test")
eval_run(scratch_run, period="test")
eval_run(finetuned_run, period="test")

nse_g, kge_g, csv_g = test_metric(base_global, TARGET)
nse_s, kge_s, csv_s = test_metric(scratch_run, TARGET)
nse_f, kge_f, csv_f = test_metric(finetuned_run, TARGET)

summary = pd.DataFrame([
    {"model": "global", "NSE": nse_g, "KGE": kge_g, "run_dir": str(base_global), "metrics_csv": str(csv_g)},
    {"model": "pure_local_same_params", "NSE": nse_s, "KGE": kge_s, "run_dir": str(scratch_run), "metrics_csv": str(csv_s)},
    {"model": "global_finetune_same_params", "NSE": nse_f, "KGE": kge_f, "run_dir": str(finetuned_run), "metrics_csv": str(csv_f)},
])

out_csv = WORK / "results_same_params.csv"
summary.to_csv(out_csv, index=False)

print("=== SAME-PARAM RESULTS ===")
print(summary.to_string(index=False))
print("Saved:", out_csv)
print("Delta NSE (finetune - local):", nse_f - nse_s)
