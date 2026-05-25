-- Business Analyst portfolio: SQL analysis on orders_clean.csv
-- Import data/processed/orders_clean.csv into SQLite, DuckDB, or PostgreSQL.

-- 1) Executive KPIs
SELECT
    COUNT(DISTINCT "Order ID") AS total_orders,
    COUNT(DISTINCT "Customer ID") AS total_customers,
    ROUND(SUM("Sales"), 2) AS total_sales,
    ROUND(SUM("Profit"), 2) AS total_profit,
    ROUND(SUM("Profit") * 100.0 / NULLIF(SUM("Sales"), 0), 2) AS profit_margin_pct,
    ROUND(AVG("Discount") * 100, 2) AS avg_discount_pct
FROM orders_clean;

-- 2) Regional ranking
SELECT
    "Region",
    ROUND(SUM("Sales"), 2) AS sales,
    ROUND(SUM("Profit"), 2) AS profit,
    ROUND(SUM("Profit") * 100.0 / NULLIF(SUM("Sales"), 0), 2) AS margin_pct
FROM orders_clean
GROUP BY "Region"
ORDER BY profit DESC;

-- 3) Sub-category profitability (bottom performers)
SELECT
    "Category",
    "Sub-Category",
    COUNT(*) AS line_items,
    ROUND(SUM("Sales"), 2) AS sales,
    ROUND(SUM("Profit"), 2) AS profit
FROM orders_clean
GROUP BY "Category", "Sub-Category"
ORDER BY profit ASC
LIMIT 10;

-- 4) Customer segment deep dive
SELECT
    "Segment",
    COUNT(DISTINCT "Customer ID") AS customers,
    ROUND(SUM("Sales"), 2) AS sales,
    ROUND(SUM("Profit"), 2) AS profit,
    ROUND(AVG("Discount") * 100, 2) AS avg_discount_pct
FROM orders_clean
GROUP BY "Segment"
ORDER BY profit DESC;

-- 5) Year-over-year (requires Year column from ETL)
SELECT
    "Year",
    ROUND(SUM("Sales"), 2) AS sales,
    ROUND(SUM("Profit"), 2) AS profit
FROM orders_clean
GROUP BY "Year"
ORDER BY "Year";

-- 6) High-discount impact
SELECT
    CASE
        WHEN "Discount" >= 0.2 THEN 'High (20%+)'
        WHEN "Discount" >= 0.1 THEN 'Medium (10-19%)'
        ELSE 'Low (<10%)'
    END AS discount_band,
    COUNT(*) AS orders,
    ROUND(SUM("Sales"), 2) AS sales,
    ROUND(SUM("Profit"), 2) AS profit
FROM orders_clean
GROUP BY 1
ORDER BY profit DESC;

-- 7) Top customers by profit (RFM-style value)
SELECT
    "Customer ID",
    "Customer Name",
    COUNT(DISTINCT "Order ID") AS order_count,
    ROUND(SUM("Sales"), 2) AS total_sales,
    ROUND(SUM("Profit"), 2) AS total_profit
FROM orders_clean
GROUP BY "Customer ID", "Customer Name"
ORDER BY total_profit DESC
LIMIT 20;

-- 8) Window: running total sales by month
SELECT
    strftime('%Y-%m', "Order Date") AS order_month,
    ROUND(SUM("Sales"), 2) AS monthly_sales,
    ROUND(
        SUM(SUM("Sales")) OVER (ORDER BY strftime('%Y-%m', "Order Date")),
        2
    ) AS running_sales
FROM orders_clean
GROUP BY order_month
ORDER BY order_month;
