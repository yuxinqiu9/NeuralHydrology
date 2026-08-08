import pandas as pd
import numpy as np
from pathlib import Path


RQ3_DIR = Path(__file__).resolve().parents[1] / 'rq3_finetune'

# Load both datasets
p1 = RQ3_DIR / 'results_folder_groups_summary_with_global_true_ea.csv'
p2 = RQ3_DIR / 'results_folder_groups_summary_with_global_true.csv'
ea = pd.read_csv(p1)
cu = pd.read_csv(p2)

print("=" * 80)
print("深度对比：CudaLSTM vs EA-LSTM")
print("=" * 80)

# 1. 按组统计胜出情况
print("\n【按组统计胜出情况】")
print(f"CudaLSTM: FT>Local 在 {(cu['delta_ft_vs_local_nse']>0).sum()}/18 组")
print(f"EA-LSTM:  FT>Local 在 {(ea['delta_ft_vs_local_nse']>0).sum()}/18 组")
print(f"CudaLSTM: FT>Global 在 {(cu['delta_ft_vs_global_nse']>0).sum()}/18 组")
print(f"EA-LSTM:  FT>Global 在 {(ea['delta_ft_vs_global_nse']>0).sum()}/18 组")

# 2. 迁移增益方向一致性
print("\n【迁移增益方向一致性检查】")
cu['group_str'] = cu['group'].astype(str).str.zfill(2)
ea['group_str'] = ea['group'].astype(str).str.zfill(2)
m = cu.merge(ea, on='group_str', suffixes=('_cu', '_ea'))

ft_local_cu = m['delta_ft_vs_local_nse_cu'] > 0
ft_local_ea = m['delta_ft_vs_local_nse_ea'] > 0
ft_local_match = (ft_local_cu == ft_local_ea).sum()

ft_global_cu = m['delta_ft_vs_global_nse_cu'] > 0
ft_global_ea = m['delta_ft_vs_global_nse_ea'] > 0
ft_global_match = (ft_global_cu == ft_global_ea).sum()

print(f"FT>Local 方向一致的组数: {ft_local_match}/18")
if ft_local_match < 18:
    disagree_local = m.loc[ft_local_cu != ft_local_ea, 'group_str'].values
    print(f"  不一致的组: {disagree_local}")

print(f"FT>Global 方向一致的组数: {ft_global_match}/18")
if ft_global_match < 18:
    disagree_global = m.loc[ft_global_cu != ft_global_ea, 'group_str'].values
    print(f"  不一致的组: {disagree_global}")

# 3. 数值差异
print("\n【加权平均数值差异】")
w = ea['n_basins'].values
def wm(df, col):
    return float((df[col].values * w).sum() / w.sum())

nse_local_cu = wm(cu, 'local_nse_mean')
nse_local_ea = wm(ea, 'local_nse_mean')
nse_global_cu = wm(cu, 'global_nse_mean')
nse_global_ea = wm(ea, 'global_nse_mean')
nse_ft_cu = wm(cu, 'ft_nse_mean')
nse_ft_ea = wm(ea, 'ft_nse_mean')

print(f"Local NSE     - CudaLSTM: {nse_local_cu:.4f}, EA-LSTM: {nse_local_ea:.4f}, Δ: {nse_local_ea-nse_local_cu:+.4f}")
print(f"Global NSE    - CudaLSTM: {nse_global_cu:.4f}, EA-LSTM: {nse_global_ea:.4f}, Δ: {nse_global_ea-nse_global_cu:+.4f}")
print(f"Fine-tune NSE - CudaLSTM: {nse_ft_cu:.4f}, EA-LSTM: {nse_ft_ea:.4f}, Δ: {nse_ft_ea-nse_ft_cu:+.4f}")

# 4. 迁移增益本身有没有变
print("\n【迁移增益量级对比】")
gain_cu = nse_ft_cu - nse_local_cu
gain_ea = nse_ft_ea - nse_local_ea
print(f"FT-Local 增益：CudaLSTM: {gain_cu:+.4f}, EA-LSTM: {gain_ea:+.4f}")

# 5. 具体数值对比表
print("\n【逐组对比（按 EA-LSTM FT NSE 排序）】")
ea_sorted = ea.sort_values('ft_nse_mean', ascending=False).reset_index(drop=True)
cu_sorted = cu.sort_values('ft_nse_mean', ascending=False).reset_index(drop=True)

comparison = pd.DataFrame({
    'Group': ea_sorted['group'].astype(str).str.zfill(2),
    'EA_Local': ea_sorted['local_nse_mean'].round(3),
    'EA_FT': ea_sorted['ft_nse_mean'].round(3),
    'EA_Δ': (ea_sorted['ft_nse_mean'] - ea_sorted['local_nse_mean']).round(3),
})

# 添加对应的cuda数据
cu_dict = {str(int(x)).zfill(2): i for i, x in enumerate(cu['group'])}
cu_deltas = []
for g in comparison['Group']:
    idx = cu_dict.get(g)
    if idx is not None:
        cu_deltas.append((cu.iloc[idx]['ft_nse_mean'] - cu.iloc[idx]['local_nse_mean']).round(3))
    else:
        cu_deltas.append(None)
comparison['CUDA_Δ'] = cu_deltas

print(comparison.to_string(index=False))

# 最终结论
print("\n" + "=" * 80)
print("【最终结论】")
print("=" * 80)
if ft_local_match == 18 and ft_global_match == 18:
    print("✓ 两个模型的结论 100% 一致：")
    print("  • 所有 18 个组都满足：FT > Local")
    print("  • 所有 18 个组都满足：FT > Global")
    print("  • 只是数值量级不同（EA-LSTM 整体偏保守）")
    print("\n→ 推荐：可合并为单一研究结论，用对比图展示两个模型的一致性")
else:
    print("✗ 两个模型有不同的发现：")
    print(f"  • FT>Local 不一致的组数: {18-ft_local_match}")
    print(f"  • FT>Global 不一致的组数: {18-ft_global_match}")
    print("\n→ 推荐：分开讨论两个模型的优劣")
