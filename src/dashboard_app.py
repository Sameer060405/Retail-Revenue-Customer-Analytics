"""Streamlit executive dashboard for retail KPIs."""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "processed" / "orders_clean.csv"

st.set_page_config(
    page_title="Retail Analytics | BA Portfolio",
    page_icon="📊",
    layout="wide",
)

st.title("Retail Revenue & Profitability Dashboard")
st.caption("Business Analyst portfolio — Superstore sample data")


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DATA_PATH.exists():
        st.error("Run `python src/clean_transform.py` after downloading data.")
        st.stop()
    return pd.read_csv(DATA_PATH, parse_dates=["Order Date", "Ship Date"])


df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
regions = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].dropna().unique()),
    default=sorted(df["Region"].dropna().unique()),
)
segments = st.sidebar.multiselect(
    "Customer segment",
    sorted(df["Segment"].dropna().unique()),
    default=sorted(df["Segment"].dropna().unique()),
)
categories = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].dropna().unique()),
    default=sorted(df["Category"].dropna().unique()),
)

mask = (
    df["Region"].isin(regions)
    & df["Segment"].isin(segments)
    & df["Category"].isin(categories)
)
filtered = df.loc[mask]

if filtered.empty:
    st.warning("No data for selected filters.")
    st.stop()

# KPI row
col1, col2, col3, col4, col5 = st.columns(5)
sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
margin = (profit / sales * 100) if sales else 0
loss_pct = filtered["Is_Loss"].mean() * 100

col1.metric("Total sales", f"${sales:,.0f}")
col2.metric("Total profit", f"${profit:,.0f}")
col3.metric("Profit margin", f"{margin:.1f}%")
col4.metric("Orders", f"{filtered['Order ID'].nunique():,}")
col5.metric("Loss line rate", f"{loss_pct:.1f}%")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Sales & profit by region")
    region_df = (
        filtered.groupby("Region", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
        .sort_values("Sales", ascending=False)
    )
    fig_region = px.bar(
        region_df,
        x="Region",
        y=["Sales", "Profit"],
        barmode="group",
        title="Regional performance",
    )
    st.plotly_chart(fig_region, use_container_width=True)

with right:
    st.subheader("Profit by category")
    cat_df = (
        filtered.groupby("Category", as_index=False)["Profit"]
        .sum()
        .sort_values("Profit")
    )
    fig_cat = px.bar(
        cat_df,
        x="Profit",
        y="Category",
        orientation="h",
        title="Category profitability",
        color="Profit",
        color_continuous_scale="RdYlGn",
    )
    st.plotly_chart(fig_cat, use_container_width=True)

st.subheader("Monthly sales trend")
monthly = (
    filtered.assign(Month_Period=filtered["Order Date"].dt.to_period("M").astype(str))
    .groupby("Month_Period", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Month_Period")
)
fig_trend = px.line(
    monthly,
    x="Month_Period",
    y=["Sales", "Profit"],
    markers=True,
    title="Monthly performance",
)
st.plotly_chart(fig_trend, use_container_width=True)

c1, c2 = st.columns(2)

with c1:
    st.subheader("Segment comparison")
    seg_df = (
        filtered.groupby("Segment", as_index=False)
        .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    )
    st.plotly_chart(
        px.scatter(
            seg_df,
            x="Sales",
            y="Profit",
            text="Segment",
            size="Sales",
            title="Sales vs profit by segment",
        ),
        use_container_width=True,
    )

with c2:
    st.subheader("Discount vs profit (binned)")
    filtered = filtered.copy()
    filtered["Discount_Bin"] = pd.cut(
        filtered["Discount"],
        bins=[-0.01, 0, 0.1, 0.2, 0.3, 1.0],
        labels=["0%", "1-10%", "11-20%", "21-30%", "30%+"],
    )
    disc_df = (
        filtered.groupby("Discount_Bin", observed=True)
        .agg(Profit=("Profit", "sum"), Sales=("Sales", "sum"))
        .reset_index()
    )
    st.plotly_chart(
        px.bar(disc_df, x="Discount_Bin", y="Profit", title="Profit by discount level"),
        use_container_width=True,
    )

st.subheader("Loss-making orders (sample)")
loss_sample = (
    filtered.loc[filtered["Is_Loss"]]
    .nlargest(15, "Sales")[["Order Date", "Region", "Sub-Category", "Sales", "Discount", "Profit"]]
)
st.dataframe(loss_sample, use_container_width=True)
