import glob
import os
import re
import pandas as pd
from pathlib import Path

base_dir = Path(__file__).resolve().parents[1] / 'rq3_finetune'

# 1) Load local-vs-ft all-basins table
all_df = pd.read_csv(base_dir / 'results_folder_groups_all_basins_ea.csv')
all_df['basin'] = all_df['basin'].astype(int)
all_df['group'] = all_df['group'].astype(int)

# 2) Load per-group global eval files and stack them
all_candidates = sorted(glob.glob(str(base_dir / 'results_folder_*_global_eval_true_ea.csv')))
global_files = [
    fp for fp in all_candidates
    if re.search(r'results_folder_\d{2}_global_eval_true_ea\.csv$', os.path.basename(fp))
]
parts = []
for fp in global_files:
    name = os.path.basename(fp)
    group_str = name.split('_')[2]
    group_id = int(group_str)
    t = pd.read_csv(fp)
    if 'NSE' not in t.columns:
        continue
    t = t[['basin', 'NSE']].copy()
    t['basin'] = t['basin'].astype(int)
    t['group'] = group_id
    t.rename(columns={'NSE': 'global_nse'}, inplace=True)
    parts.append(t)

global_df = pd.concat(parts, ignore_index=True)

# 3) Merge so each basin has local, ft, and global
merged = all_df.merge(global_df, on=['group', 'basin'], how='inner')
merged['ft_minus_global'] = merged['ft_nse'] - merged['global_nse']
merged['ft_minus_local'] = merged['ft_nse'] - merged['local_nse']

n = len(merged)
print('=== ALL BASINS (EA-LSTM, merged with per-group global eval) ===')
print(f'Total basins (merged): {n}')
print(f'FT > Global basins: {(merged["ft_minus_global"] > 0).sum()} / {n}')
print(f'FT == Global basins: {(merged["ft_minus_global"] == 0).sum()} / {n}')
print(f'FT < Global basins: {(merged["ft_minus_global"] < 0).sum()} / {n}')
print()
print(f'Mean(FT-Global): {merged["ft_minus_global"].mean():.4f}')
print(f'Median(FT-Global): {merged["ft_minus_global"].median():.4f}')
print(f'Std(FT-Global): {merged["ft_minus_global"].std():.4f}')
print()
print(f'Mean(FT-Local): {merged["ft_minus_local"].mean():.4f}')
print(f'Median(FT-Local): {merged["ft_minus_local"].median():.4f}')

print('\n=== PER-GROUP BASIN VOTE (FT vs Global) ===')
g = merged.groupby('group')['ft_minus_global'].agg(
    n='count',
    ft_gt_global=lambda x: (x > 0).sum(),
    ft_lt_global=lambda x: (x < 0).sum(),
    mean_delta='mean',
    median_delta='median'
).reset_index().sort_values('group')
g['group'] = g['group'].astype(int).astype(str).str.zfill(2)
print(g.to_string(index=False))
