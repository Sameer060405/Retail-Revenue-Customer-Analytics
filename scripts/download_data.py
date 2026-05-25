"""Download Tableau Superstore sample data for the BA portfolio project."""

from pathlib import Path
import sys

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUTPUT = RAW_DIR / "superstore.csv"

# Public mirror of the classic Tableau Superstore dataset
SUPERSTORE_URL = (
    "https://raw.githubusercontent.com/snehangshu2002/"
    "Superstore-Sales-Analysis/main/data/superstore_raw.csv"
)


def download() -> Path:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading from {SUPERSTORE_URL} ...")
    response = requests.get(SUPERSTORE_URL, timeout=120)
    response.raise_for_status()
    OUTPUT.write_bytes(response.content)
    print(f"Saved {len(response.content):,} bytes -> {OUTPUT}")
    return OUTPUT


if __name__ == "__main__":
    try:
        download()
    except requests.RequestException as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        print(
            "\nManual fallback:\n"
            "  1. Go to https://www.kaggle.com/datasets/vizeno/department-store-sales-rfm\n"
            "     OR search Kaggle for 'Superstore Sales Dataset'\n"
            "  2. Save CSV as data/raw/superstore.csv\n",
            file=sys.stderr,
        )
        sys.exit(1)
