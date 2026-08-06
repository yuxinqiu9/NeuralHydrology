"""
run_rq3.py — Full RQ3 experiment:

    Does "global pretrain + finetune" beat "local training from scratch"
    on a held-out target basin?

Pipeline (all on the SAME target basin, which is NOT in the pretrain set):
    1. Pretrain a global base model on the pretrain basins.
    2. Train a local model FROM SCRATCH on the target basin only.
    3. Finetune the global base on the target basin.
    4. Evaluate all three on the target basin's test period and compare.

Usage:
    python run_rq3.py
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
    src = (HERE / "finetune.yml").read_text(encoding="utf-8")
    src += f"\nbase_run_dir: {base_run_dir.as_posix()}\n"
    out = HERE / "finetune_run.yml"
    out.write_text(src, encoding="utf-8")
    return out


def test_metrics(run_dir: Path, basin: str) -> dict:
    epochs = sorted((run_dir / "test").glob("model_epoch*"))
    df = pd.read_csv(epochs[-1] / "test_metrics.csv", dtype={"basin": str})
    return df.set_index("basin").loc[basin].to_dict()


def main() -> None:
    target = (HERE / "basins_finetune.txt").read_text().split()[0]
    print(f"Target basin: {target} (diluted inside the global training set)\n")

    # 1) Global model: trained on ALL basins (target included, diluted) ------
    print("=" * 60)
    print("[1/3] Training GLOBAL model on all basins (target diluted) ...")
    print("=" * 60)
    start_run(config_file=HERE / "pretrain.yml")
    base_dir = latest_run("rq3_base_global")

    # 2) Local from scratch -------------------------------------------------
    print("\n" + "=" * 60)
    print("[2/3] Training LOCAL model from scratch on target ...")
    print("=" * 60)
    start_run(config_file=HERE / "scratch.yml")
    scratch_dir = latest_run("rq3_scratch_local")

    # 3) Finetune global base on target -------------------------------------
    print("\n" + "=" * 60)
    print("[3/3] Finetuning global base on target ...")
    print("=" * 60)
    finetune(build_finetune_config(base_dir))
    fine_dir = latest_run("rq3_finetuned")

    # Evaluate all three on the test period ---------------------------------
    print("\nEvaluating all three models on test period ...")
    eval_run(base_dir, period="test")
    eval_run(scratch_dir, period="test")
    eval_run(fine_dir, period="test")

    base_m = test_metrics(base_dir, target)
    scratch_m = test_metrics(scratch_dir, target)
    fine_m = test_metrics(fine_dir, target)

    print("\n" + "=" * 64)
    print(f"RQ3 RESULT — target basin {target}")
    print("=" * 64)
    header = f"{'metric':<8}{'pure-local':>12}{'global':>12}{'global+FT':>12}"
    print(header)
    print("-" * 64)
    for k in ("NSE", "KGE"):
        if all(k in m for m in (scratch_m, base_m, fine_m)):
            print(f"{k:<8}{scratch_m[k]:>12.3f}{base_m[k]:>12.3f}{fine_m[k]:>12.3f}")

    print("-" * 64)
    if "NSE" in scratch_m and "NSE" in fine_m:
        d = fine_m["NSE"] - scratch_m["NSE"]
        verdict = ("YES — global+finetune beats pure-local"
                   if d > 0 else "NO — pure-local wins")
        print(f"NSE(global+FT) - NSE(pure-local) = {d:+.3f}  ->  {verdict}")


if __name__ == "__main__":
    main()
