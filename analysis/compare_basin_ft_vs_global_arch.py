import glob
import os
import re
import pandas as pd
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / 'rq3_finetune'


def load_arch_data(arch: str):
    if arch == 'ea':
        all_file = BASE / 'results_folder_groups_all_basins_ea.csv'
        pattern = r'results_folder_(\d{2})_global_eval_true_ea\.csv$'
    elif arch == 'cuda':
        all_file = BASE / 'results_folder_groups_all_basins.csv'
        pattern = r'results_folder_(\d{2})_global_eval_true\.csv$'
    else:
        raise ValueError('arch must be ea or cuda')

    all_df = pd.read_csv(all_file)
    all_df['basin'] = all_df['basin'].astype(int)
    all_df['group'] = all_df['group'].astype(int)

    candidates = sorted(glob.glob(str(BASE / 'results_folder_*_global_eval_true*.csv')))
    global_parts = []
    for fp in candidates:
        m = re.search(pattern, os.path.basename(fp))
        if not m:
            continue
        g = int(m.group(1))
        t = pd.read_csv(fp)
        if 'NSE' not in t.columns:
            continue
        t = t[['basin', 'NSE']].copy()
        t['basin'] = t['basin'].astype(int)
        t['group'] = g
        t.rename(columns={'NSE': 'global_nse'}, inplace=True)
        global_parts.append(t)

    global_df = pd.concat(global_parts, ignore_index=True)
    merged = all_df.merge(global_df, on=['group', 'basin'], how='inner')
    merged['ft_minus_global'] = merged['ft_nse'] - merged['global_nse']
    return merged


ea = load_arch_data('ea')
cuda = load_arch_data('cuda')


def summarize(label: str, df: pd.DataFrame):
    n = len(df)
    gt = (df['ft_minus_global'] > 0).sum()
    lt = (df['ft_minus_global'] < 0).sum()
    eq = (df['ft_minus_global'] == 0).sum()
    print(f'=== {label} ===')
    print(f'Total basins: {n}')
    print(f'FT > Global: {gt} / {n} ({gt/n:.2%})')
    print(f'FT = Global: {eq} / {n} ({eq/n:.2%})')
    print(f'FT < Global: {lt} / {n} ({lt/n:.2%})')
    print(f'Mean(FT-Global): {df["ft_minus_global"].mean():.4f}')
    print(f'Median(FT-Global): {df["ft_minus_global"].median():.4f}')
    print(f'Std(FT-Global): {df["ft_minus_global"].std():.4f}')
    print()


summarize('EA-LSTM', ea)
summarize('CudaLSTM', cuda)

# Direct comparison
print('=== DIRECT COMPARISON ===')
ea_rate = (ea['ft_minus_global'] > 0).mean()
cuda_rate = (cuda['ft_minus_global'] > 0).mean()
print(f'Win-rate difference (Cuda - EA): {cuda_rate - ea_rate:+.2%}')
print(f'Mean delta difference (Cuda - EA): {cuda["ft_minus_global"].mean() - ea["ft_minus_global"].mean():+.4f}')
print()

# Per-group basin win rates
print('=== PER-GROUP FT>GLOBAL RATE ===')
ea_g = ea.groupby('group')['ft_minus_global'].apply(lambda x: (x > 0).mean()).reset_index(name='ea_rate')
cuda_g = cuda.groupby('group')['ft_minus_global'].apply(lambda x: (x > 0).mean()).reset_index(name='cuda_rate')
g = ea_g.merge(cuda_g, on='group', how='inner').sort_values('group')
g['diff_cuda_minus_ea'] = g['cuda_rate'] - g['ea_rate']
g['group'] = g['group'].astype(int).astype(str).str.zfill(2)
print(g.to_string(index=False, formatters={
    'ea_rate': lambda x: f'{x:.2%}',
    'cuda_rate': lambda x: f'{x:.2%}',
    'diff_cuda_minus_ea': lambda x: f'{x:+.2%}'
}))

# Count groups where cuda is better in basin-level FT>Global rate
better = (g['diff_cuda_minus_ea'] > 0).sum()
worse = (g['diff_cuda_minus_ea'] < 0).sum()
same = (g['diff_cuda_minus_ea'] == 0).sum()
print()
print(f'Groups where Cuda basin win-rate > EA: {better}')
print(f'Groups where Cuda basin win-rate < EA: {worse}')
print(f'Groups where equal: {same}')
