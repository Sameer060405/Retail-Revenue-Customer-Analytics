"""Clean Superstore data and export analysis-ready tables."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "superstore.csv"
PROCESSED_DIR = ROOT / "data" / "processed"


def load_raw() -> pd.DataFrame:
    if not RAW_PATH.exists():
        raise FileNotFoundError(
            f"Missing {RAW_PATH}. Run: python scripts/download_data.py"
        )
    return pd.read_csv(RAW_PATH, encoding="latin-1")


def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [c.strip() for c in df.columns]

    date_cols = ["Order Date", "Ship Date"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    numeric_cols = ["Sales", "Quantity", "Discount", "Profit"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.month
    df["Quarter"] = df["Order Date"].dt.quarter
    df["Month_Name"] = df["Order Date"].dt.month_name()

    df["Profit_Margin_Pct"] = (df["Profit"] / df["Sales"].replace(0, pd.NA)) * 100
    df["Ship_Lag_Days"] = (df["Ship Date"] - df["Order Date"]).dt.days
    df["Is_Loss"] = df["Profit"] < 0
    df["Discounted_Revenue"] = df["Sales"] * (1 - df["Discount"])

    df = df.dropna(subset=["Order ID", "Sales", "Profit", "Order Date"])
    return df


def export(df: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out = PROCESSED_DIR / "orders_clean.csv"
    df.to_csv(out, index=False)
    print(f"Exported {len(df):,} rows -> {out}")


def main() -> None:
    df = load_raw()
    cleaned = clean(df)
    export(cleaned)
    print(
        f"Date range: {cleaned['Order Date'].min().date()} "
        f"to {cleaned['Order Date'].max().date()}"
    )
    print(f"Loss orders: {cleaned['Is_Loss'].sum():,} ({cleaned['Is_Loss'].mean():.1%})")


if __name__ == "__main__":
    main()
