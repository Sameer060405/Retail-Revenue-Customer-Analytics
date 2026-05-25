# Business problem & analytics plan

## Context

Superstore is a fictional US retailer selling office supplies, furniture, and technology across four regions. Leadership suspects **margin erosion** from discounts and **uneven regional performance**, but lacks a single source of truth for KPIs.

## Stakeholders

| Stakeholder | Need |
|-------------|------|
| Regional managers | Compare sales, profit, and loss rates by region |
| Marketing | Understand segment value and discount impact |
| Product / category leads | Identify sub-categories destroying profit |
| Finance | Track margin % and YoY trends |

## Key questions (hypotheses)

1. Which **regions** contribute most profit—and which underperform on margin?
2. Do **high-discount** orders drive volume but destroy profitability?
3. Which **customer segments** (Consumer, Corporate, Home Office) are most valuable?
4. Which **sub-categories** generate repeated loss orders?
5. How do **sales and profit** trend over time (seasonality)?

## KPI framework

| KPI | Definition | Why it matters |
|-----|------------|----------------|
| Total sales | Sum of order line sales | Top-line health |
| Total profit | Sum of line profit | Bottom-line outcome |
| Profit margin % | Profit ÷ Sales × 100 | Efficiency |
| Loss line rate % | Share of lines where Profit < 0 | Operational leakage |
| Avg discount % | Mean discount on lines | Pricing policy risk |
| Orders / customers | Distinct counts | Scale & reach |

## Success criteria

- Repeatable pipeline from raw CSV → cleaned data → dashboard
- At least **3 actionable recommendations** backed by data
- SQL + Python + visualization skills demonstrated for BA interviews

## Out of scope (for v1)

- Real-time ingestion
- Predictive ML (churn forecast can be **project v2** with Telco/Olist data)
