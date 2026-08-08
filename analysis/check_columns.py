import pandas as pd
from pathlib import Path


RQ3_DIR = Path(__file__).resolve().parents[1] / 'rq3_finetune'

# 先查看文件结构
g01_local_ft = pd.read_csv(RQ3_DIR / 'results_folder_01_local_vs_finetune_ea.csv')
g01_global = pd.read_csv(RQ3_DIR / 'results_folder_01_global_eval_true_ea.csv')

print("g01_local_ft 列：")
print(g01_local_ft.columns.tolist())
print(g01_local_ft.head(3))
print()
print("g01_global 列：")
print(g01_global.columns.tolist())
print(g01_global.head(3))
