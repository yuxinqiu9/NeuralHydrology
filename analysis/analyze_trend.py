import pandas as pd
import numpy as np
from pathlib import Path


RQ3_DIR = Path(__file__).resolve().parents[1] / 'rq3_finetune'

# 检查Group 01具体的basin级别情况
g01_local_ft = pd.read_csv(RQ3_DIR / 'results_folder_01_local_vs_finetune_ea.csv')
g01_global = pd.read_csv(RQ3_DIR / 'results_folder_01_global_eval_true_ea.csv')

# 合并数据
merged = g01_local_ft[['basin', 'local_nse', 'ft_nse']].merge(
    g01_global[['basin', 'NSE']], on='basin'
)
merged.rename(columns={'NSE': 'global_nse'}, inplace=True)

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

# 哪些basin在FT vs Global上没有改善或负向
no_improvement = merged[merged['ft_nse'] <= merged['global_nse']]
print(f"【FT ≤ Global 的basin】（没有改善）：{len(no_improvement)} 个 ({100*len(no_improvement)/len(merged):.1f}%)")

print("\n" + "="*80)
print("【关键问题】")
print("="*80)

# 统计所有18个组的情况
df_group = pd.read_csv(RQ3_DIR / 'results_folder_groups_summary_with_global_true_ea.csv')
print("\n各组的FT vs Global情况（按差异从小到大）：")
for idx, row in df_group.sort_values('delta_ft_vs_global_nse').iterrows():
    g = int(row['group'])
    delta = row['delta_ft_vs_global_nse']
    sig = '✓ 显著 (>0.05)' if delta > 0.05 else ('◐ 微小 (0.01-0.05)' if delta > 0.01 else '✗ 极小 (≤0.01)')
    print(f"Group {g:2d}: FT={row['ft_nse_mean']:.4f}, Global={row['global_nse_mean']:.4f}, Δ={delta:.4f} {sig}")

print("\n统计汇总：")
sig_groups = (df_group['delta_ft_vs_global_nse'] > 0.05).sum()
micro_groups = ((df_group['delta_ft_vs_global_nse'] > 0.01) & (df_group['delta_ft_vs_global_nse'] <= 0.05)).sum()
tiny_groups = (df_group['delta_ft_vs_global_nse'] <= 0.01).sum()
print(f"显著改善 (>0.05)：{sig_groups}/18 组")
print(f"微小改善 (0.01-0.05)：{micro_groups}/18 组")
print(f"极小改善 (≤0.01)：{tiny_groups}/18 组")
