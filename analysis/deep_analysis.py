import pandas as pd
import numpy as np
from pathlib import Path


RQ3_DIR = Path(__file__).resolve().parents[1] / 'rq3_finetune'

# 检查Group 01具体的basin级别情况
g01_data = pd.read_csv(RQ3_DIR / 'results_folder_01_local_vs_finetune_ea.csv')
g01_global = pd.read_csv(RQ3_DIR / 'results_folder_01_global_eval_true_ea.csv')

# 合并数据
merged = g01_data.merge(g01_global[['basin', 'NSE']], on='basin', suffixes=('_local_ft', '_global'))
merged.columns = ['basin', 'local_nse', 'ft_nse', 'global_nse']

print("=== Group 01 深度分析 ===\n")
print(f"总basin数：{len(merged)}")
print(f"FT > Local 的basin数：{(merged['ft_nse'] > merged['local_nse']).sum()}")
print(f"FT > Global 的basin数：{(merged['ft_nse'] > merged['global_nse']).sum()}")
print()

# 按FT-Global的差异排序
merged['ft_minus_global'] = merged['ft_nse'] - merged['global_nse']
merged['ft_minus_local'] = merged['ft_nse'] - merged['local_nse']

print("【FT vs Global 的差异分布】")
print(f"均值：{merged['ft_minus_global'].mean():.4f}")
print(f"中位数：{merged['ft_minus_global'].median():.4f}")
print(f"标准差：{merged['ft_minus_global'].std():.4f}")
print(f"最小值：{merged['ft_minus_global'].min():.4f}")
print(f"最大值：{merged['ft_minus_global'].max():.4f}")
print()

print("【FT vs Local 的差异分布】")
print(f"均值：{merged['ft_minus_local'].mean():.4f}")
print(f"中位数：{merged['ft_minus_local'].median():.4f}")
print(f"标准差：{merged['ft_minus_local'].std():.4f}")
print()

# 哪些basin在FT vs Global上没有改善
no_improvement = merged[merged['ft_nse'] <= merged['global_nse']]
print(f"【FT ≤ Global 的basin】（没有改善）：{len(no_improvement)} 个 ({100*len(no_improvement)/len(merged):.1f}%)")
if len(no_improvement) > 0:
    print(no_improvement[['basin', 'local_nse', 'global_nse', 'ft_nse', 'ft_minus_global']].to_string(index=False))

print("\n" + "="*80)
print("【关键问题】")
print("="*80)

# 统计所有18个组的情况
df_group = pd.read_csv(RQ3_DIR / 'results_folder_groups_summary_with_global_true_ea.csv')
print("\n各组的FT vs Global情况：")
for idx, row in df_group.iterrows():
    g = int(row['group'])
    print(f"Group {g:2d}: FT={row['ft_nse_mean']:.4f}, Global={row['global_nse_mean']:.4f}, Δ={row['delta_ft_vs_global_nse']:.4f} {'✓ 显著' if row['delta_ft_vs_global_nse'] > 0.05 else '✗ 微小'}")
