from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd
from neuralhydrology.nh_run import eval_run, finetune, start_run

WORK = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune")
GLOBAL_RUNS_ROOT = Path(r"C:/GitHub/climate-change/runs")
LOCAL_RUNS_ROOT = WORK / "runs"

PRETRAIN_TEMPLATE = WORK / "pretrain.yml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run leave-one-group-out (LOGO) comparison for one target group."
    )
    parser.add_argument("--group", required=True, help="Target group id, e.g. 01")
    parser.add_argument("--epochs-global", type=int, default=1)
    parser.add_argument("--epochs-local", type=int, default=1)
    parser.add_argument("--epochs-ft", type=int, default=1)
    parser.add_argument("--seed", type=int, default=1001)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only generate config/list files and print plan.",
    )
    return parser.parse_args()


def read_basins(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_basins(path: Path, basins: list[str]) -> None:
    path.write_text("\n".join(sorted(set(basins))) + "\n", encoding="utf-8")


def write_cfg_with_updates(base_cfg: Path, out_cfg: Path, updates: dict[str, str]) -> None:
    lines = base_cfg.read_text(encoding="utf-8").splitlines()
    written = {k: False for k in updates}
    out_lines: list[str] = []

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


def newest(prefix: str, roots: list[Path]) -> Path:
    cands: list[Path] = []
    for root in roots:
        if root.exists():
            cands.extend([p for p in root.glob(f"{prefix}*") if p.is_dir()])
    if not cands:
        raise FileNotFoundError(f"No run found with prefix '{prefix}' in {roots}")
    cands.sort(key=lambda p: p.stat().st_mtime)
    return cands[-1]


def read_test_metrics(run_dir: Path) -> pd.DataFrame:
    epochs = sorted((run_dir / "test").glob("model_epoch*"))
    if not epochs:
        raise FileNotFoundError(f"No evaluated epochs in {run_dir / 'test'}")
    metrics_csv = epochs[-1] / "test_metrics.csv"
    return pd.read_csv(metrics_csv, dtype={"basin": str})[["basin", "NSE", "KGE"]]


def main() -> None:
    args = parse_args()
    group = args.group.zfill(2)

    group_file = WORK / "basin_lists_by_folder" / f"basins_{group}.txt"
    if not group_file.exists():
        raise FileNotFoundError(f"Missing group basin list: {group_file}")

    global_all_file = WORK / "basins_global.txt"
    if not global_all_file.exists():
        raise FileNotFoundError(f"Missing global basin list: {global_all_file}")

    target_basins = set(read_basins(group_file))
    global_all = read_basins(global_all_file)
    global_excluded = [b for b in global_all if b not in target_basins]

    if not global_excluded:
        raise RuntimeError("Excluded global basin list is empty.")

    logo_global_file = WORK / f"basins_global_excluding_{group}.txt"
    write_basins(logo_global_file, global_excluded)

    local_template = WORK / f"scratch_folder_{group}.yml"
    ft_template = WORK / f"finetune_folder_{group}.yml"
    if not local_template.exists() or not ft_template.exists():
        raise FileNotFoundError(
            f"Missing templates for group {group}: {local_template}, {ft_template}"
        )

    logo_pretrain_cfg = WORK / f"logo_pretrain_group_{group}.yml"
    logo_local_cfg = WORK / f"logo_scratch_group_{group}.yml"
    logo_ft_cfg = WORK / f"logo_finetune_group_{group}.yml"

    write_cfg_with_updates(
        PRETRAIN_TEMPLATE,
        logo_pretrain_cfg,
        {
            "experiment_name": f"rq3_logo_base_group_{group}",
            "train_basin_file": logo_global_file.as_posix(),
            "validation_basin_file": logo_global_file.as_posix(),
            "test_basin_file": group_file.as_posix(),
            "epochs": str(args.epochs_global),
            "seed": str(args.seed),
        },
    )

    write_cfg_with_updates(
        local_template,
        logo_local_cfg,
        {
            "experiment_name": f"rq3_logo_scratch_group_{group}",
            "epochs": str(args.epochs_local),
            "seed": str(args.seed),
        },
    )

    # base_run_dir is filled after global run finishes
    write_cfg_with_updates(
        ft_template,
        logo_ft_cfg,
        {
            "experiment_name": f"rq3_logo_finetuned_group_{group}",
            "epochs": str(args.epochs_ft),
            "seed": str(args.seed),
        },
    )

    print(f"Prepared LOGO files for group {group}:")
    print(f"  global basin list : {logo_global_file}")
    print(f"  pretrain config   : {logo_pretrain_cfg}")
    print(f"  local config      : {logo_local_cfg}")
    print(f"  finetune config   : {logo_ft_cfg}")
    print(f"  excluded basins   : {len(target_basins)}")
    print(f"  global train size : {len(global_excluded)}")

    if args.dry_run:
        print("Dry run mode: stop before training.")
        return

    print("\n[1/6] Train LOGO global model...")
    start_run(logo_pretrain_cfg)
    logo_base_run = newest(
        f"rq3_logo_base_group_{group}",
        [GLOBAL_RUNS_ROOT, LOCAL_RUNS_ROOT],
    )
    print(f"  base run: {logo_base_run}")

    print("[2/6] Evaluate LOGO global model...")
    eval_run(logo_base_run, period="test")

    print("[3/6] Train local-from-scratch model...")
    start_run(logo_local_cfg)
    logo_local_run = newest(
        f"rq3_logo_scratch_group_{group}",
        [LOCAL_RUNS_ROOT, GLOBAL_RUNS_ROOT],
    )
    print(f"  local run: {logo_local_run}")

    print("[4/6] Evaluate local-from-scratch model...")
    eval_run(logo_local_run, period="test")

    print("[5/6] Train fine-tuned model from LOGO global base...")
    write_cfg_with_updates(
        logo_ft_cfg,
        logo_ft_cfg,
        {"base_run_dir": logo_base_run.as_posix()},
    )
    finetune(logo_ft_cfg)
    logo_ft_run = newest(
        f"rq3_logo_finetuned_group_{group}",
        [LOCAL_RUNS_ROOT, GLOBAL_RUNS_ROOT],
    )
    print(f"  finetune run: {logo_ft_run}")

    print("[6/6] Evaluate fine-tuned model and summarize...")
    eval_run(logo_ft_run, period="test")

    g = read_test_metrics(logo_base_run).rename(columns={"NSE": "global_nse", "KGE": "global_kge"})
    l = read_test_metrics(logo_local_run).rename(columns={"NSE": "local_nse", "KGE": "local_kge"})
    f = read_test_metrics(logo_ft_run).rename(columns={"NSE": "ft_nse", "KGE": "ft_kge"})

    merged = l.merge(g, on="basin", how="inner").merge(f, on="basin", how="inner")
    merged["group"] = group
    merged["seed"] = args.seed
    merged["delta_ft_minus_local_nse"] = merged["ft_nse"] - merged["local_nse"]
    merged["delta_ft_minus_global_nse"] = merged["ft_nse"] - merged["global_nse"]

    out_csv = WORK / f"results_logo_group_{group}.csv"
    merged.to_csv(out_csv, index=False)

    print("\n=== LOGO quick summary ===")
    print(f"Group: {group} | Basins: {len(merged)}")
    print(f"Mean Local NSE:  {merged['local_nse'].mean():.3f}")
    print(f"Mean Global NSE: {merged['global_nse'].mean():.3f}")
    print(f"Mean FT NSE:     {merged['ft_nse'].mean():.3f}")
    print(f"FT-Local mean:   {merged['delta_ft_minus_local_nse'].mean():+.3f}")
    print(f"FT-Global mean:  {merged['delta_ft_minus_global_nse'].mean():+.3f}")
    print(f"Saved: {out_csv}")


if __name__ == "__main__":
    main()
