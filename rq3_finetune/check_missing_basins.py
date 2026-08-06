# 读取全局basin和每个group的basin
import os

# 读全局basin
with open('basins_global.txt') as f:
    global_basins = set(line.strip() for line in f if line.strip())

# 读所有group的basin
group_basins = set()
for i in range(1, 19):
    gfile = f'basin_lists_by_folder/basins_{i:02d}.txt'
    if os.path.exists(gfile):
        with open(gfile) as f:
            for line in f:
                group_basins.add(line.strip())

# 找缺失的basin
missing = global_basins - group_basins

print(f"全局basin总数: {len(global_basins)}")
print(f"Group分配的basin总数: {len(group_basins)}")
print(f"缺失basin数: {len(missing)}")
print(f"\n缺失的basin列表 (前30个):")
for i, b in enumerate(sorted(missing)):
    if i < 30:
        print(f"  {b}")
    if i == 29 and len(missing) > 30:
        print(f"  ... 还有 {len(missing)-30} 个")
        break
