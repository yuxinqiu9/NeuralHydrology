from pathlib import Path
import pandas as pd

from neuralhydrology.nh_run import start_run, finetune, eval_run

WORK = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune")
BASE_RUNS_ROOT = Path(r"C:/GitHub/climate-change/runs")
LOCAL_RUNS_ROOT = WORK / "runs"
SEED = 1001


def newest(prefix: str, root: Path) -> Path:
    cands = sorted(
        [p for p in root.glob(f"{prefix}*") if p.is_dir()],
        key=lambda p: p.stat().st_mtime,
    )
    if not cands:
        raise FileNotFoundError(f"No runs matching {prefix} in {root}")
    return cands[-1]


def ensure_region01_basin_file() -> Path:
    src = WORK / "basins_global.txt"
    out = WORK / "basins_local_01.txt"
    basins = [b.strip() for b in src.read_text(encoding="utf-8").splitlines() if b.strip().startswith("01")]
    if not basins:
        raise RuntimeError("No basins starting with '01' found in basins_global.txt")
    out.write_text("\n".join(basins) + "\n", encoding="utf-8")
    print(f"Prepared region basin file: {out} ({len(basins)} basins)")
    return out


def load_metrics(run_dir: Path) -> pd.DataFrame:
    test_epochs = sorted((run_dir / "test").glob("model_epoch*"))
    if not test_epochs:
        raise FileNotFoundError(f"No evaluated test epochs found in {run_dir}")
    csv_path = test_epochs[-1] / "test_metrics.csv"
    df = pd.read_csv(csv_path, dtype={"basin": str})
    return df[["basin", "NSE", "KGE"]].rename(columns={"NSE": "nse", "KGE": "kge"})


ensure_region01_basin_file()

base_global = newest("rq3_base_global", BASE_RUNS_ROOT)
print(f"Using base global run: {base_global}")

start_run(WORK / "scratch_region01_same_params.yml")
local_run = newest("rq3_scratch_region01", LOCAL_RUNS_ROOT)
print(f"Local regional run: {local_run}")

ft_cfg = WORK / "finetune_region01_same_params_run.yml"
cfg_text = (WORK / "finetune_region01_same_params.yml").read_text(encoding="utf-8").rstrip() + "\n"
cfg_text += f"base_run_dir: {base_global.as_posix()}\n"
ft_cfg.write_text(cfg_text, encoding="utf-8")

finetune(ft_cfg)
ft_run = newest("rq3_finetuned_region01", LOCAL_RUNS_ROOT)
print(f"Finetune regional run: {ft_run}")

eval_run(local_run, period="test")
eval_run(ft_run, period="test")

local_df = load_metrics(local_run).rename(columns={"nse": "local_nse", "kge": "local_kge"})
ft_df = load_metrics(ft_run).rename(columns={"nse": "ft_nse", "kge": "ft_kge"})

merged = local_df.merge(ft_df, on="basin", how="inner")
merged["delta_nse_ft_minus_local"] = merged["ft_nse"] - merged["local_nse"]
merged["delta_kge_ft_minus_local"] = merged["ft_kge"] - merged["local_kge"]
merged["seed"] = SEED

summary = pd.DataFrame(
    {
        "metric": ["NSE", "KGE"],
        "local_mean": [merged["local_nse"].mean(), merged["local_kge"].mean()],
        "finetune_mean": [merged["ft_nse"].mean(), merged["ft_kge"].mean()],
        "delta_mean_ft_minus_local": [
            merged["delta_nse_ft_minus_local"].mean(),
            merged["delta_kge_ft_minus_local"].mean(),
        ],
        "n_basins": [len(merged), len(merged)],
        "seed": [SEED, SEED],
    }
)

out_detail = WORK / "results_region01_local_vs_finetune.csv"
out_summary = WORK / "results_region01_local_vs_finetune_summary.csv"

merged.to_csv(out_detail, index=False)
summary.to_csv(out_summary, index=False)

print("\n=== REGION 01 RESULT SUMMARY ===")
print(summary.to_string(index=False))
print(f"Saved detail : {out_detail}")
print(f"Saved summary: {out_summary}")
