from pathlib import Path
import time
import pandas as pd

from neuralhydrology.nh_run import start_run, finetune, eval_run

WORK = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune")
BASE_RUNS_ROOT = Path(r"C:/GitHub/climate-change/runs")
LOCAL_RUNS_ROOT = WORK / "runs"
BASIN_SOURCE = WORK / "basins_global.txt"
FIXED_SEED = 1001
ADDITIONAL_BASINS = 10


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
    if not test_epochs:
        raise FileNotFoundError(f"No evaluated test epochs found in {run_dir}")
    csv = test_epochs[-1] / "test_metrics.csv"
    df = pd.read_csv(csv, dtype={"basin": str}).set_index("basin")
    return float(df.loc[basin, "NSE"]), float(df.loc[basin, "KGE"]), csv


def write_cfg_with_updates(base_cfg: Path, out_cfg: Path, updates: dict):
    lines = base_cfg.read_text(encoding="utf-8").splitlines()
    written = {k: False for k in updates}
    out_lines = []

    for line in lines:
        replaced = False
        for key, value in updates.items():
            if line.startswith(f"{key}:"):
                out_lines.append(f"{key}: {value}")
                written[key] = True
                replaced = True
                break
        if not replaced:
            out_lines.append(line)

    for key, value in updates.items():
        if not written[key]:
            out_lines.append(f"{key}: {value}")

    out_cfg.write_text("\n".join(out_lines).rstrip() + "\n", encoding="utf-8")


all_basins = [b.strip() for b in BASIN_SOURCE.read_text(encoding="utf-8").splitlines() if b.strip()]
existing_csv = WORK / "results_multibasin_seed1001_10basins.csv"

if existing_csv.exists():
    existing = pd.read_csv(existing_csv, dtype={"basin": str})
    done_basins = set(existing["basin"].astype(str).tolist())
else:
    existing = pd.DataFrame()
    done_basins = set()

remaining = [b for b in all_basins if b not in done_basins]
run_basins = remaining[:ADDITIONAL_BASINS]

if not run_basins:
    raise RuntimeError("No remaining basins to run. Consider increasing source basins or checking existing CSV.")

base_global = newest("rq3_base_global", BASE_RUNS_ROOT)
print(f"Using global base: {base_global}")
print(f"Already done basins: {len(done_basins)}")
print(f"Running additional basins: {len(run_basins)}")
print("Basins:", ", ".join(run_basins))

basin_dir = WORK / "basin_lists_multibasin"
basin_dir.mkdir(exist_ok=True)

rows = []

for idx, basin in enumerate(run_basins, start=1):
    print(f"\n=== NEW BASIN {idx}/{len(run_basins)} | {basin} ===")

    basin_file = basin_dir / f"basin_{basin}.txt"
    basin_file.write_text(f"{basin}\n", encoding="utf-8")

    local_cfg = WORK / f"scratch_same_params_basin_{basin}.yml"
    ft_cfg = WORK / f"finetune_same_params_basin_{basin}.yml"

    write_cfg_with_updates(
        WORK / "scratch_same_params.yml",
        local_cfg,
        {
            "experiment_name": f"rq3_scratch_basin_{basin}",
            "seed": FIXED_SEED,
            "train_basin_file": basin_file.as_posix(),
            "validation_basin_file": basin_file.as_posix(),
            "test_basin_file": basin_file.as_posix(),
        },
    )

    write_cfg_with_updates(
        WORK / "finetune_same_params.yml",
        ft_cfg,
        {
            "experiment_name": f"rq3_finetuned_basin_{basin}",
            "seed": FIXED_SEED,
            "train_basin_file": basin_file.as_posix(),
            "validation_basin_file": basin_file.as_posix(),
            "test_basin_file": basin_file.as_posix(),
            "base_run_dir": base_global.as_posix(),
        },
    )

    t0 = time.time()
    start_run(local_cfg)
    local_run = newest(f"rq3_scratch_basin_{basin}", LOCAL_RUNS_ROOT, after=t0)

    t1 = time.time()
    finetune(ft_cfg)
    finetune_run = newest(f"rq3_finetuned_basin_{basin}", LOCAL_RUNS_ROOT, after=t1)

    eval_run(local_run, period="test")
    eval_run(finetune_run, period="test")

    nse_l, kge_l, csv_l = test_metric(local_run, basin)
    nse_f, kge_f, csv_f = test_metric(finetune_run, basin)

    rows.append(
        {
            "basin": basin,
            "seed": FIXED_SEED,
            "local_run_dir": str(local_run),
            "local_NSE": nse_l,
            "local_KGE": kge_l,
            "local_metrics_csv": str(csv_l),
            "finetune_run_dir": str(finetune_run),
            "finetune_NSE": nse_f,
            "finetune_KGE": kge_f,
            "finetune_metrics_csv": str(csv_f),
            "delta_NSE_ft_minus_local": nse_f - nse_l,
            "delta_KGE_ft_minus_local": kge_f - kge_l,
        }
    )

    print(
        f"Basin {basin} done | local NSE={nse_l:.6f}, ft NSE={nse_f:.6f}, "
        f"delta={nse_f - nse_l:.6f}"
    )

new_df = pd.DataFrame(rows)
out_additional = WORK / "results_multibasin_seed1001_additional.csv"
new_df.to_csv(out_additional, index=False)

if not existing.empty:
    combined = pd.concat([existing, new_df], ignore_index=True)
else:
    combined = new_df.copy()

combined = combined.drop_duplicates(subset=["basin"], keep="last").reset_index(drop=True)
n_basins = len(combined)
out_combined = WORK / f"results_multibasin_seed1001_{n_basins}basins.csv"
combined.to_csv(out_combined, index=False)

summary = pd.DataFrame(
    {
        "metric": ["NSE", "KGE"],
        "local_mean": [combined["local_NSE"].mean(), combined["local_KGE"].mean()],
        "finetune_mean": [combined["finetune_NSE"].mean(), combined["finetune_KGE"].mean()],
        "delta_mean_ft_minus_local": [
            combined["delta_NSE_ft_minus_local"].mean(),
            combined["delta_KGE_ft_minus_local"].mean(),
        ],
        "n_basins": [n_basins, n_basins],
        "seed": [FIXED_SEED, FIXED_SEED],
    }
)

out_summary = WORK / f"results_multibasin_seed1001_{n_basins}basins_summary.csv"
summary.to_csv(out_summary, index=False)

print("\n=== ADDITIONAL MULTI-BASIN RESULTS SAVED ===")
print(new_df[["basin", "local_NSE", "finetune_NSE", "delta_NSE_ft_minus_local"]].to_string(index=False))
print("\n=== COMBINED SUMMARY ===")
print(summary.to_string(index=False))
print(f"Saved additional: {out_additional}")
print(f"Saved combined  : {out_combined}")
print(f"Saved summary   : {out_summary}")
