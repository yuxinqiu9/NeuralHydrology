# Data — CAMELS-US

This folder should contain the **CAMELS-US** dataset (or a path to it).

## Download Instructions

### Option A: Direct Download (NCAR)

1. Go to: https://ral.ucar.edu/solutions/products/camels
2. Register and download the full dataset (~2 GB)
3. Extract to this folder:

```
data/
└── CAMELS_US/
    ├── basin_mean_forcing/
    │   ├── daymet/
    │   ├── nldas/
    │   └── maurer/
    ├── usgs_streamflow/
    ├── camels_attributes_v2.0/
    │   ├── camels_clim.txt
    │   ├── camels_geol.txt
    │   ├── camels_hydro.txt
    │   ├── camels_soil.txt
    │   ├── camels_topo.txt
    │   └── camels_vege.txt
    └── basin_set_full_res/
```

4. Update `code/1_basin_demo.yml` → `data_dir:` to the absolute path.

### Option B: NeuralHydrology Tutorial Notebook

Run the prerequisites notebook from the NeuralHydrology examples:

```bash
cd ../../../neuralhydrology/examples/00-Data-Prerequisites
jupyter notebook prerequisites.ipynb
```

### Basin Used in Case Study

| Basin ID | Name | State | Area (km²) | Regime |
|----------|------|-------|------------|--------|
| 01013500 | Fish River near Fort Kent | Maine | 2252 | Snowmelt-dominated |

## Alternative: Use Existing Test Data

The NeuralHydrology library includes a small test dataset at
`neuralhydrology/test/test_data/camels_us/` with 4 basins. This is sufficient
to verify the workflow but not for publication-quality results.

To use it, set in `1_basin_demo.yml`:

```yaml
data_dir: ../../../../neuralhydrology/test/test_data
```

Note: The test data covers only a short time period; NSE values will be lower
than the published benchmarks.
