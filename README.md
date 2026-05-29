# Retail Revenue & Customer Analytics — Business Analyst Portfolio

End-to-end business analytics project: define KPIs, clean data with SQL/Python, analyze performance, and present insights in an interactive dashboard. Built for **Business Analyst** and **Analytics** roles.

---


## Where to get data (start here)

### Recommended first dataset (this project)

| Dataset | Why | How to get |
|---------|-----|------------|
| **Tableau Superstore** (~10K orders) | Industry-standard BA practice data; orders, customers, products, profit, regions | Run: `python scripts/download_data.py` |

### Strong alternatives for a 2nd portfolio project

| Project theme | Dataset | Source |
|---------------|---------|--------|
| E-commerce (Brazil) | Olist Brazilian E-Commerce | [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) |
| Telco churn | Telco Customer Churn | [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| HR attrition | IBM HR Analytics Employee Attrition | [Kaggle](https://www.kaggle.com/datasets/pavansubhasht/ibm-hr-analytics-attrition-dataset) |
| Marketing ROI | Marketing Campaign CSV | [Kaggle](https://www.kaggle.com/datasets/rodsaldanha/arketing-campaign) |
| Lending risk | Lending Club (sample) | [Kaggle](https://www.kaggle.com/datasets/wordsforthewise/lending-club) |
| Public / government | Various | [data.gov](https://data.gov), [Google Dataset Search](https://datasetsearch.research.google.com) |

**Rule of thumb:** pick data with **dates**, **customers**, **money** (revenue/cost), and **categories**—so you can do trends, segments, and profitability.

---

## Quick start

```powershell
cd c:\Users\samee\Desktop\Business_Analystics_Project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/download_data.py
python src/clean_transform.py
python src/kpi_analysis.py
streamlit run src/dashboard_app.py
```

---

## Tech stack (what employers expect)

- **SQL** — filtering, GROUP BY, CTEs, rankings
- **Python** — pandas for cleaning & KPIs
- **Visualization** — Streamlit (included); add Tableau/Power BI for extra points
- **Documentation** — business framing + recommendations (not “I made a chart”)

---

## Folder structure

```
├── data/
│   ├── raw/           # downloaded CSV
│   └── processed/     # cleaned for SQL/dashboard
├── sql/
│   └── analysis_queries.sql
├── src/
│   ├── clean_transform.py
│   ├── kpi_analysis.py
│   └── dashboard_app.py
├── scripts/
│   └── download_data.py
└── docs/
    ├── 01_business_problem.md
    └── 02_insights_report.md
```

---

## Next steps for you

1. Run quick start and open the Streamlit dashboard.
2. Build the **Power BI** version: follow `docs/03_power_bi_dashboard_guide.md` (slicers, DAX, drill-through).
3. Fill `docs/02_insights_report.md` with **your** narrative (use output from `kpi_analysis.py`).
4. Record a 2–3 min Loom walkthrough: problem → KPIs → 3 insights → recommendations.
5. Push to GitHub; link repo + Power BI publish link on CV and LinkedIn.
