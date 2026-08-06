from pathlib import Path
import time
import pandas as pd

from neuralhydrology.nh_run import start_run, finetune, eval_run

WORK = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune")
BASE_RUNS_ROOT = Path(r"C:/GitHub/climate-change/runs")
LOCAL_RUNS_ROOT = WORK / "runs"
TARGET = "01022500"
N_GROUPS = 10
SEEDS = [1001 + i for i in range(N_GROUPS)]


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


base_global = newest("rq3_base_global", BASE_RUNS_ROOT)
rows = []

print(f"Using global base: {base_global}")

for idx, seed in enumerate(SEEDS, start=1):
    print(f"\n=== GROUP {idx}/{N_GROUPS} | seed={seed} ===")

    local_cfg = WORK / f"scratch_same_params_g{idx:02d}.yml"
    ft_cfg = WORK / f"finetune_same_params_g{idx:02d}.yml"

    write_cfg_with_updates(
        WORK / "scratch_same_params.yml",
        local_cfg,
        {
            "experiment_name": f"rq3_scratch_local_same_g{idx:02d}",
            "seed": seed,
        },
    )

    write_cfg_with_updates(
        WORK / "finetune_same_params.yml",
        ft_cfg,
        {
            "experiment_name": f"rq3_finetuned_same_g{idx:02d}",
            "seed": seed,
            "base_run_dir": base_global.as_posix(),
        },
    )

    t0 = time.time()
    start_run(local_cfg)
    local_run = newest(f"rq3_scratch_local_same_g{idx:02d}", LOCAL_RUNS_ROOT, after=t0)

    t1 = time.time()
    finetune(ft_cfg)
    finetune_run = newest(f"rq3_finetuned_same_g{idx:02d}", LOCAL_RUNS_ROOT, after=t1)

    eval_run(local_run, period="test")
    eval_run(finetune_run, period="test")

    nse_l, kge_l, csv_l = test_metric(local_run, TARGET)
    nse_f, kge_f, csv_f = test_metric(finetune_run, TARGET)

    rows.append(
        {
            "group": idx,
            "seed": seed,
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
        f"Group {idx} done | local NSE={nse_l:.6f}, ft NSE={nse_f:.6f}, "
        f"delta={nse_f - nse_l:.6f}"
    )

result_df = pd.DataFrame(rows)
out_csv = WORK / "results_same_params_10groups.csv"
result_df.to_csv(out_csv, index=False)

summary = pd.DataFrame(
    {
        "metric": ["NSE", "KGE"],
        "local_mean": [result_df["local_NSE"].mean(), result_df["local_KGE"].mean()],
        "finetune_mean": [result_df["finetune_NSE"].mean(), result_df["finetune_KGE"].mean()],
        "delta_mean_ft_minus_local": [
            result_df["delta_NSE_ft_minus_local"].mean(),
            result_df["delta_KGE_ft_minus_local"].mean(),
        ],
    }
)

summary_csv = WORK / "results_same_params_10groups_summary.csv"
summary.to_csv(summary_csv, index=False)

print("\n=== 10-GROUP RESULTS SAVED ===")
print(result_df.to_string(index=False))
print("\n=== MEAN SUMMARY ===")
print(summary.to_string(index=False))
print(f"Saved detailed: {out_csv}")
print(f"Saved summary : {summary_csv}")
