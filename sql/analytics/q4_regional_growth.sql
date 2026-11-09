WITH selected_period AS (
SELECT
    DATE '2020-06-01' AS start_date,
    DATE '2020-06-30' AS end_date,
    'M' AS selection_type
),
current_period_tmp AS (
SELECT
    selection_type,
    CASE selection_type
        WHEN 'M' THEN DATE_TRUNC('month', start_date) :: DATE
        WHEN 'Q' THEN DATE_TRUNC('quarter', start_date) :: DATE
        WHEN 'Y' THEN DATE_TRUNC('year', start_date) :: DATE
        ELSE start_date
    END AS start_date,
    end_date
FROM selected_period
),
current_period AS (
SELECT
    start_date,
    CASE selection_type
        WHEN 'M' THEN (start_date + INTERVAL '1 month' - INTERVAL '1 day') :: DATE
        WHEN 'Q' THEN (start_date + INTERVAL '4 month' - INTERVAL '1 day') :: DATE
        WHEN 'Y' THEN (start_date + INTERVAL '1 year' - INTERVAL '1 day') :: DATE
        ELSE end_date
    END AS end_date
FROM current_period_tmp
),
comparaison_periods AS (
SELECT
    'current' AS period_type,
    start_date,
    end_date
FROM current_period
UNION ALL
SELECT
    'previous' AS period_type,
    CASE selection_type
        WHEN 'M' THEN (start_date - INTERVAL '1 month') :: DATE
        WHEN 'Q' THEN (start_date - INTERVAL '4 month') :: DATE
        WHEN 'Y' THEN (start_date - INTERVAL '1 year') :: DATE
        ELSE (start_date - (end_date - start_date) - INTERVAL '1 day') :: DATE
    END AS start_date,
    CASE
        WHEN selection_type IN ('M', 'Q', 'Y') THEN (start_date - INTERVAL '1 day') :: DATE
        ELSE (start_date - INTERVAL '1 day') :: DATE
    END AS end_date
FROM selected_period
),
customers_activity AS (
SELECT    
    period_type,
    customer_department AS region,
    dc.customer_id
FROM dw.dim_subscription AS ds
JOIN comparaison_periods AS cp
    ON ds.registration_date <= cp.end_date
        AND (
            termination_date IS NOT NULL
            OR termination_date >= cp.start_date
        )
JOIN dw.dim_customer AS dc ON dc.customer_id = ds.customer_id
),
active_customers AS (
SELECT
    region,
    COUNT(DISTINCT customer_id)
        FILTER(WHERE period_type = 'current') AS current_active_customers,
    COUNT(DISTINCT customer_id)
        FILTER(WHERE period_type = 'previous') AS previous_active_customers    
FROM customers_activity
GROUP BY region
),
purchases AS (
SELECT
    period_type,
    customer_department AS region,
    purchase_id,
    revenue
FROM dw.fact_purchase AS fp
JOIN dw.dim_date AS dd
    ON dd.date_key = fp.date_key
JOIN comparaison_periods AS cp
    ON full_date >= cp.start_date
        AND full_date <= cp.end_date
JOIN dw.dim_customer AS dc
    ON dc.customer_key = fp.customer_key
),
purchase_metrics AS (
SELECT
    region,
    COUNT(purchase_id) FILTER(WHERE period_type = 'current') AS current_purchases,
    COUNT(purchase_id) FILTER(WHERE period_type = 'previous') AS previous_purchases,
    SUM(revenue) FILTER(WHERE period_type = 'current') AS current_revenue,
    SUM(revenue) FILTER(WHERE period_type = 'previous') AS previous_revenue
FROM purchases
GROUP BY region
),
regional_metrics AS (
SELECT
    ac.region,
    current_active_customers,
    previous_active_customers,
    current_purchases,
    previous_purchases,
    current_revenue,
    previous_revenue,
    current_revenue / NULLIF(current_active_customers, 0) AS avg_revenue_per_active_customer
FROM active_customers AS ac
JOIN purchase_metrics AS pm
    ON pm.region = ac.region
),
regional_growth AS (
SELECT
    region,
    current_active_customers,
    previous_active_customers,
    ROUND(
    (current_active_customers - previous_active_customers
    ) * 100.0
    / NULLIF(previous_active_customers, 0),
    2
    ) AS active_customers_growth_rate,

    current_purchases,
    previous_purchases,
    ROUND(
    (current_purchases - previous_purchases
    ) * 100.0
    / NULLIF(previous_purchases, 0),
    2
    ) AS purchases_growth_rate,

    current_revenue,
    previous_revenue,
    ROUND(
    (current_revenue - previous_revenue
    ) * 100.0
    / NULLIF(previous_revenue, 0),
    2
    ) AS revenue_growth_rate,
    avg_revenue_per_active_customer
FROM regional_metrics
)
SELECT * FROM regional_growth
;
