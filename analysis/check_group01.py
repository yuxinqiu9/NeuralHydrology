import pandas as pd
from pathlib import Path

RQ3_DIR = Path(__file__).resolve().parents[1] / 'rq3_finetune'

df = pd.read_csv(RQ3_DIR / 'results_folder_groups_summary_with_global_true_ea.csv')
print('Group 01 数据：')
g01 = df[df['group'] == 1]
print(g01[['group', 'local_nse_mean', 'global_nse_mean', 'ft_nse_mean', 'delta_ft_vs_global_nse', 'delta_ft_vs_local_nse']].to_string())
print()
print('FT - Global 手动计算：', f"{g01['ft_nse_mean'].values[0]:.4f} - {g01['global_nse_mean'].values[0]:.4f} = {g01['ft_nse_mean'].values[0] - g01['global_nse_mean'].values[0]:.4f}")
print('FT - Local 手动计算：', f"{g01['ft_nse_mean'].values[0]:.4f} - {g01['local_nse_mean'].values[0]:.4f} = {g01['ft_nse_mean'].values[0] - g01['local_nse_mean'].values[0]:.4f}")
print()
print('所有组的 FT vs Global 对比（从小到大排序）：')
comp = df[['group', 'ft_nse_mean', 'global_nse_mean', 'delta_ft_vs_global_nse']].sort_values('delta_ft_vs_global_nse')
comp['group'] = comp['group'].astype(int).astype(str).str.zfill(2)
print(comp.to_string(index=False))

print("\n" + "="*80)
print("分析：")
print("="*80)
print(f"FT > Global 的组数：{(df['delta_ft_vs_global_nse'] > 0).sum()} / 18")
print(f"FT 平均比 Global 提升：{df['delta_ft_vs_global_nse'].mean():.4f}")
print(f"FT vs Global 最小提升：{df['delta_ft_vs_global_nse'].min():.4f} (Group {df.loc[df['delta_ft_vs_global_nse'].idxmin(), 'group']:.0f})")
print(f"FT vs Global 最大提升：{df['delta_ft_vs_global_nse'].max():.4f} (Group {df.loc[df['delta_ft_vs_global_nse'].idxmax(), 'group']:.0f})")
