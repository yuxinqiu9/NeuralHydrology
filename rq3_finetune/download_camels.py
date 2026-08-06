"""
download_camels.py — Fetch the minimal CAMELS-US subset for the RQ3 finetune demo.

Downloads from the official Zenodo record (10.5065/D6MW2F4D):
  * 7 catchment-attribute .txt files  (~0.7 MB total)
  * basin_timeseries_v1p2_metForcing_obsFlow.zip  (3.4 GB)

To save time/disk, only the *daymet* forcing and *usgs_streamflow* folders are
extracted (maurer/nldas are skipped). Final layout (what NeuralHydrology expects):

    NeuralHydrology/data/CAMELS_US/
        basin_mean_forcing/daymet/<HUC>/<gauge>_..._forcing_leap.txt
        usgs_streamflow/<HUC>/<gauge>_streamflow_qc.txt
        camels_attributes_v2.0/camels_*.txt
"""

from __future__ import annotations

import subprocess
import sys
import zipfile
from pathlib import Path

ZENODO = "https://zenodo.org/records/15529996/files"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "CAMELS_US"
ATTR_DIR = DATA_DIR / "camels_attributes_v2.0"
ZIP_NAME = "basin_timeseries_v1p2_metForcing_obsFlow.zip"
ZIP_PATH = DATA_DIR / ZIP_NAME

ATTR_FILES = [
    "camels_clim.txt",
    "camels_geol.txt",
    "camels_hydro.txt",
    "camels_name.txt",
    "camels_soil.txt",
    "camels_topo.txt",
    "camels_vege.txt",
]

# Inside the zip, only members under these (after the top-level folder) are kept.
KEEP_PREFIXES = ("basin_mean_forcing/daymet/", "usgs_streamflow/")


def _download(url: str, dest: Path, *, resume: bool = True) -> None:
    """Download via curl.exe (robust on Windows; Zenodo blocks urllib's UA)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "curl.exe", "-L", "--fail", "--retry", "5", "--retry-delay", "5",
        "-A", "Mozilla/5.0",
        "-o", str(dest), url,
    ]
    if resume:
        cmd.insert(1, "-C")
        cmd.insert(2, "-")
    subprocess.run(cmd, check=True)


def download_attributes() -> None:
    print("[1/3] Catchment attributes ...")
    ATTR_DIR.mkdir(parents=True, exist_ok=True)
    for name in ATTR_FILES:
        dest = ATTR_DIR / name
        if dest.exists() and dest.stat().st_size > 0:
            print(f"  [skip] {name}")
            continue
        _download(f"{ZENODO}/{name}?download=1", dest, resume=False)


def download_timeseries() -> None:
    print(f"[2/3] Time series zip ({ZIP_NAME}, ~3.4 GB) ...")
    # Skip if the zip is already present and looks complete (>3 GB).
    if ZIP_PATH.exists() and ZIP_PATH.stat().st_size > 3_000_000_000:
        print(f"  [skip] {ZIP_NAME} already present "
              f"({ZIP_PATH.stat().st_size/1e9:.2f} GB)")
        return
    _download(f"{ZENODO}/{ZIP_NAME}?download=1", ZIP_PATH)


def _needed_basins() -> set[str]:
    here = Path(__file__).resolve().parent
    ids: set[str] = set()
    for name in ("basins_global.txt", "basins_pretrain.txt", "basins_finetune.txt"):
        p = here / name
        if p.exists():
            ids.update(p.read_text().split())
    return ids


def extract_subset() -> None:
    needed = _needed_basins()
    print(f"[3/3] Extracting daymet + streamflow for {len(needed)} basins "
          f"(skipping maurer/nldas) ...")
    n = 0
    with zipfile.ZipFile(ZIP_PATH) as zf:
        for member in zf.namelist():
            if member.endswith("/"):
                continue
            # strip leading top-level folder, e.g. "basin_dataset_public_v1p2/"
            parts = member.split("/", 1)
            rel = parts[1] if len(parts) == 2 else parts[0]
            if not rel.startswith(KEEP_PREFIXES):
                continue
            base = rel.rsplit("/", 1)[-1]
            gauge = base.split("_", 1)[0]
            if needed and gauge not in needed:
                continue
            out = DATA_DIR / rel
            if out.exists() and out.stat().st_size > 0:
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(member) as src, open(out, "wb") as dst:
                dst.write(src.read())
            n += 1
    print(f"  extracted {n} files. Done.")


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    download_attributes()
    download_timeseries()
    extract_subset()
    print("\nCAMELS-US minimal subset ready at:")
    print(f"  {DATA_DIR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
