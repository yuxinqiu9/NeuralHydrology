"""
salvage_rq3.py — Finish the RQ3 three-way comparison using the already-trained
531-basin GLOBAL model (recovered after a cwd/runs path mix-up).

Reuses:
  * GLOBAL  = newest rq3_base_global_* in C:/GitHub/climate-change/runs (531 basins)
  * SCRATCH = newest rq3_scratch_local_* in the same folder (pure-local)
Then finetunes the GLOBAL on the target basin, evaluates all three on the target
test period, and prints the comparison.

Run from anywhere:
    python salvage_rq3.py
"""

from pathlib import Path

import pandas as pd

from neuralhydrology.nh_run import finetune, eval_run

FT_DIR = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune")
RUNS = Path(r"C:/GitHub/climate-change/runs")  # where the new runs actually live


def newest(prefix: str, *, after: float = 0.0) -> Path:
    cands = sorted(
        (p for p in RUNS.glob(f"{prefix}*")
         if p.is_dir() and p.stat().st_mtime > after),
        key=lambda p: p.stat().st_mtime,
    )
    if not cands:
        raise FileNotFoundError(f"No '{prefix}*' in {RUNS} (after={after})")
    return cands[-1]


def test_metrics(run_dir: Path, basin: str) -> dict:
    epochs = sorted((run_dir / "test").glob("model_epoch*"))
    df = pd.read_csv(epochs[-1] / "test_metrics.csv", dtype={"basin": str})
    return df.set_index("basin").loc[basin].to_dict()


def main() -> None:
    target = (FT_DIR / "basins_finetune.txt").read_text().split()[0]
    global_dir = newest("rq3_base_global")
    scratch_dir = newest("rq3_scratch_local")
    print(f"Target basin : {target}")
    print(f"GLOBAL (531) : {global_dir.name}")
    print(f"SCRATCH      : {scratch_dir.name}")

    # Finetune the 531-basin global on the target basin
    cfg_src = (FT_DIR / "finetune.yml").read_text(encoding="utf-8")
    cfg_src += f"\nbase_run_dir: {global_dir.as_posix()}\n"
    cfg = FT_DIR / "finetune_run.yml"
    cfg.write_text(cfg_src, encoding="utf-8")

    import time
    t0 = time.time()
    print("\nFinetuning the 531-global on target ...")
    finetune(cfg)
    fine_dir = newest("rq3_finetuned", after=t0)
    print(f"FINETUNED    : {fine_dir.name}")

    # Evaluate all three on the target test period
    print("\nEvaluating all three on test period ...")
    eval_run(global_dir, period="test")
    eval_run(scratch_dir, period="test")
    eval_run(fine_dir, period="test")

    s = test_metrics(scratch_dir, target)
    g = test_metrics(global_dir, target)
    f = test_metrics(fine_dir, target)

    print("\n" + "=" * 64)
    print(f"RQ3 RESULT — target basin {target}  (GLOBAL = 531 basins)")
    print("=" * 64)
    print(f"{'metric':<8}{'pure-local':>12}{'global':>12}{'global+FT':>12}")
    print("-" * 64)
    for k in ("NSE", "KGE"):
        if all(k in m for m in (s, g, f)):
            print(f"{k:<8}{s[k]:>12.3f}{g[k]:>12.3f}{f[k]:>12.3f}")
    print("-" * 64)
    if "NSE" in s and "NSE" in f:
        d = f["NSE"] - s["NSE"]
        verdict = ("YES — global+finetune beats pure-local"
                   if d > 0 else "NO — pure-local wins")
        print(f"NSE(global+FT) - NSE(pure-local) = {d:+.3f}  ->  {verdict}")


if __name__ == "__main__":
    main()
