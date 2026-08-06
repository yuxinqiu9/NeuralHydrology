"""
run_pretrain.py — Train the small "global" base model on the pretrain basins.

Usage:
    python run_pretrain.py
"""

from pathlib import Path

from neuralhydrology.nh_run import start_run

HERE = Path(__file__).resolve().parent


def main() -> None:
    cfg = HERE / "pretrain.yml"
    print(f"Starting pretraining with: {cfg}")
    start_run(config_file=cfg)
    print("\nPretraining done. Base run stored under:", HERE / "runs")


if __name__ == "__main__":
    main()
