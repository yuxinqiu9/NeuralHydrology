# -*- coding: utf-8 -*-
"""
run_scratch_ea.py — Train a local model FROM SCRATCH using EA-LSTM.

Usage:
    python run_scratch_ea.py
"""

from pathlib import Path

from neuralhydrology.nh_run import start_run

HERE = Path(__file__).resolve().parent


def main() -> None:
    cfg = HERE / "scratch_ea.yml"
    print(f"Starting scratch training with EA-LSTM: {cfg}")
    start_run(config_file=cfg)
    print("\nScratch training done. Run stored under:", HERE / "runs")


if __name__ == "__main__":
    main()
