# -*- coding: utf-8 -*-
"""
run_rq3_ea.py — Full RQ3 experiment with EA-LSTM:

    Does "global pretrain + finetune" beat "local training from scratch"
    on a held-out target basin?

Pipeline (all on the SAME target basin, which is NOT in the pretrain set):
    1. Pretrain a global base model on the pretrain basins (EA-LSTM).
    2. Train a local model FROM SCRATCH on the target basin only (EA-LSTM).
    3. Finetune the global base on the target basin (EA-LSTM).
    4. Evaluate all three on the target basin's test period and compare.

Usage:
    python run_rq3_ea.py
"""

from pathlib import Path

import pandas as pd

from neuralhydrology.nh_run import start_run, finetune, eval_run

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"


def latest_run(prefix: str) -> Path:
    cands = sorted(
        (p for p in RUNS.glob(f"{prefix}*") if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
    )
    if not cands:
        raise FileNotFoundError(f"No run matching '{prefix}*' in {RUNS}")
    return cands[-1]


def build_finetune_config(base_run_dir: Path) -> Path:
    src = (HERE / "finetune_ea.yml").read_text(encoding="utf-8")
    src += f"\nbase_run_dir: {base_run_dir.as_posix()}\n"
    out = HERE / "finetune_ea_run.yml"
    out.write_text(src, encoding="utf-8")
    return out


def test_metrics(run_dir: Path, basin: str) -> dict:
    epochs = sorted((run_dir / "test").glob("model_epoch*"))
    df = pd.read_csv(epochs[-1] / "test_metrics.csv", dtype={"basin": str})
    return df.set_index("basin").loc[basin].to_dict()


def main() -> None:
    # Step 1: Pretrain global base model with EA-LSTM
    print("=" * 80)
    print("STEP 1: Pretraining global base model (EA-LSTM)")
    print("=" * 80)
    pretrain_cfg = HERE / "pretrain_ea.yml"
    start_run(config_file=pretrain_cfg)
    base_run = latest_run("rq3_base_global_ea")
    print(f"\n✓ Base run completed: {base_run}")

    # Step 2: Train local model from scratch with EA-LSTM
    print("\n" + "=" * 80)
    print("STEP 2: Training local model from scratch (EA-LSTM)")
    print("=" * 80)
    scratch_cfg = HERE / "scratch_ea.yml"
    start_run(config_file=scratch_cfg)
    scratch_run = latest_run("rq3_scratch_local_ea")
    print(f"\n✓ Scratch run completed: {scratch_run}")

    # Step 3: Finetune on target basin with EA-LSTM
    print("\n" + "=" * 80)
    print("STEP 3: Finetuning base model on target basin (EA-LSTM)")
    print("=" * 80)
    finetune_cfg = build_finetune_config(base_run)
    finetune(config_file=finetune_cfg, run_dir=base_run)
    finetune_run = latest_run("rq3_finetuned_ea")
    print(f"\n✓ Finetune run completed: {finetune_run}")

    # Step 4: Compare results
    print("\n" + "=" * 80)
    print("STEP 4: Three-way comparison on target basin")
    print("=" * 80)
    
    # Evaluate all three runs on the test set
    for run_path, label in [
        (base_run, "Base (global pretrain)"),
        (scratch_run, "Scratch (local from zero)"),
        (finetune_run, "Finetuned (finetune)"),
    ]:
        print(f"\nEvaluating {label}: {run_path.name}")
        eval_run(run_dir=run_path)

    # Read test results from target basin
    basin = "01022500"  # Adjust to your target basin if needed
    print(f"\nTest metrics for target basin {basin}:")
    print("-" * 80)
    
    for run_label, run_path in [
        ("Base (Global Pretrain)", base_run),
        ("Scratch (Local From Zero)", scratch_run),
        ("Finetuned", finetune_run),
    ]:
        try:
            metrics = test_metrics(run_path, basin)
            print(f"\n{run_label}:")
            for key, val in sorted(metrics.items()):
                if isinstance(val, (int, float)):
                    print(f"  {key:20s}: {val:8.4f}")
        except Exception as e:
            print(f"\n{run_label}: Error reading metrics - {e}")


if __name__ == "__main__":
    main()
