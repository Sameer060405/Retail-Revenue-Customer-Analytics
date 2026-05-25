"""Compute core business KPIs and print executive summary for the insights report."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "orders_clean.csv"


def load() -> pd.DataFrame:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Missing {DATA_PATH}. Run: python src/clean_transform.py"
        )
    return pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date"])


def print_section(title: str) -> None:
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)


def main() -> None:
    df = load()

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    overall_margin = (total_profit / total_sales) * 100
    loss_orders = df.loc[df["Is_Loss"], "Sales"].sum()
    avg_discount = df["Discount"].mean() * 100

    print_section("COMPANY KPIs")
    print(f"Total sales:        ${total_sales:,.2f}")
    print(f"Total profit:       ${total_profit:,.2f}")
    print(f"Profit margin:      {overall_margin:.2f}%")
    print(f"Orders:             {df['Order ID'].nunique():,}")
    print(f"Customers:          {df['Customer ID'].nunique():,}")
    print(f"Avg discount:       {avg_discount:.1f}%")
    print(f"Revenue at loss:    ${loss_orders:,.2f} (loss-making lines)")

    print_section("TOP 5 REGIONS BY PROFIT")
    region = (
        df.groupby("Region", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .assign(Margin_Pct=lambda x: x["Profit"] / x["Sales"] * 100)
        .sort_values("Profit", ascending=False)
    )
    print(region.head().to_string(index=False))

    print_section("BOTTOM 5 SUB-CATEGORIES BY PROFIT")
    subcat = (
        df.groupby(["Category", "Sub-Category"], as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"), Orders=("Order ID", "count"))
        .sort_values("Profit")
    )
    print(subcat.head().to_string(index=False))

    print_section("CUSTOMER SEGMENT PERFORMANCE")
    segment = (
        df.groupby("Segment", as_index=False)
        .agg(
            Customers=("Customer ID", "nunique"),
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Avg_Discount=("Discount", "mean"),
        )
        .assign(Margin_Pct=lambda x: x["Profit"] / x["Sales"] * 100)
        .sort_values("Profit", ascending=False)
    )
    print(segment.to_string(index=False))

    print_section("YEAR-OVER-YEAR SALES & PROFIT")
    yearly = (
        df.groupby("Year", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .sort_values("Year")
    )
    print(yearly.to_string(index=False))

    print_section("HIGH-DISCOUNT ORDERS (Discount >= 20%)")
    high_disc = df[df["Discount"] >= 0.2]
    hd_sales = high_disc["Sales"].sum()
    hd_profit = high_disc["Profit"].sum()
    print(f"Share of orders:    {len(high_disc) / len(df):.1%}")
    print(f"Sales:              ${hd_sales:,.2f}")
    print(f"Profit:             ${hd_profit:,.2f}")
    if hd_sales:
        print(f"Margin on segment:  {hd_profit / hd_sales * 100:.2f}%")

    print("\n-> Use these numbers in docs/02_insights_report.md\n")


if __name__ == "__main__":
    main()
