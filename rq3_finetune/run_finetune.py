"""
run_finetune.py — Finetune the pretrained base model on the single target basin,
then evaluate both the base model and the finetuned model and print a comparison.

Usage:
    python run_finetune.py
"""

from pathlib import Path

import pandas as pd

from neuralhydrology.nh_run import finetune, eval_run

HERE = Path(__file__).resolve().parent
RUNS = HERE / "runs"


def latest_run(prefix: str) -> Path:
    candidates = sorted(
        (p for p in RUNS.glob(f"{prefix}*") if p.is_dir()),
        key=lambda p: p.stat().st_mtime,
    )
    if not candidates:
        raise FileNotFoundError(f"No run directory matching '{prefix}*' in {RUNS}")
    return candidates[-1]


def build_finetune_config(base_run_dir: Path) -> Path:
    """Create a derived finetune config that points at the pretrained run."""
    src = (HERE / "finetune.yml").read_text(encoding="utf-8")
    derived = HERE / "finetune_run.yml"
    src += f"\nbase_run_dir: {base_run_dir.as_posix()}\n"
    derived.write_text(src, encoding="utf-8")
    return derived


def metric_for_basin(run_dir: Path, basin: str) -> dict:
    """Read NSE/KGE for `basin` from the latest test evaluation of a run."""
    test_dirs = sorted((run_dir / "test").glob("model_epoch*"))
    csv = test_dirs[-1] / "test_metrics.csv"
    df = pd.read_csv(csv, dtype={"basin": str}).set_index("basin")
    return df.loc[basin].to_dict()


def main() -> None:
    base_run_dir = latest_run("rq3_base_global")
    print(f"Base (pretrained) run: {base_run_dir.name}")

    cfg = build_finetune_config(base_run_dir)
    print(f"Finetuning with: {cfg}")
    finetune(cfg)

    finetuned_run_dir = latest_run("rq3_finetuned")
    print(f"Finetuned run: {finetuned_run_dir.name}")

    # Evaluate both runs on the test period
    print("\nEvaluating base model on test period ...")
    eval_run(base_run_dir, period="test")
    print("Evaluating finetuned model on test period ...")
    eval_run(finetuned_run_dir, period="test")

    target = (HERE / "basins_finetune.txt").read_text().split()[0]
    base_m = metric_for_basin(base_run_dir, target)
    fine_m = metric_for_basin(finetuned_run_dir, target)

    print("\n" + "=" * 56)
    print(f"RESULT — target basin {target}")
    print("=" * 56)
    print(f"{'metric':<8}{'base':>12}{'finetuned':>14}{'delta':>12}")
    for k in ("NSE", "KGE"):
        if k in base_m and k in fine_m:
            b, f = base_m[k], fine_m[k]
            print(f"{k:<8}{b:>12.3f}{f:>14.3f}{f-b:>+12.3f}")


if __name__ == "__main__":
    main()
