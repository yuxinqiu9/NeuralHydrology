from pathlib import Path

import pandas as pd
from neuralhydrology.nh_run import eval_run


global_dir = Path(r"C:/GitHub/climate-change/runs/rq3_base_global_3006_154109")
scratch_dir = Path(r"C:/GitHub/climate-change/runs/rq3_scratch_local_3006_165552")
fine_dir = Path(r"C:/GitHub/climate-change/NeuralHydrology/rq3_finetune/runs/rq3_finetuned_3006_165930")
target = "01022500"

for d in [global_dir, scratch_dir, fine_dir]:
    eval_run(d, period="test")


def read_metrics(run_dir: Path, basin: str):
    test_epochs = sorted((run_dir / "test").glob("model_epoch*"))
    csv = test_epochs[-1] / "test_metrics.csv"
    df = pd.read_csv(csv, dtype={"basin": str}).set_index("basin")
    return df.loc[basin].to_dict(), csv


s, s_csv = read_metrics(scratch_dir, target)
g, g_csv = read_metrics(global_dir, target)
f, f_csv = read_metrics(fine_dir, target)

print("\n" + "=" * 64)
print(f"RQ3 RESULT — target basin {target}  (GLOBAL=531 basins)")
print("=" * 64)
print(f"{'metric':<8}{'pure-local':>12}{'global':>12}{'global+FT':>12}")
print("-" * 64)
for k in ["NSE", "KGE"]:
    print(f"{k:<8}{s.get(k, float('nan')):>12.3f}{g.get(k, float('nan')):>12.3f}{f.get(k, float('nan')):>12.3f}")
print("-" * 64)
if "NSE" in s and "NSE" in f:
    d = f["NSE"] - s["NSE"]
    verdict = "YES — global+FT beats pure-local" if d > 0 else "NO — pure-local wins"
    print(f"NSE(global+FT) - NSE(pure-local) = {d:+.3f}  ->  {verdict}")

print("\nCSVs:")
print("scratch:", s_csv)
print("global :", g_csv)
print("fine   :", f_csv)
