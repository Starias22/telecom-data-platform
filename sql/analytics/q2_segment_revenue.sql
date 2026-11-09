WITH selected_period AS (
SELECT
    DATE '2020-06-01' AS start_date,
    DATE '2020-06-30' AS end_date
),
x AS (
SELECT
    customer_segment,
    SUM(revenue) AS total_revenue
FROM dw.fact_purchase AS fp
JOIN dw.dim_customer AS dc
    ON dc.customer_key = fp.customer_key
JOIN dw.dim_date AS dd
    ON dd.date_key = fp.date_key
JOIN selected_period AS sp
    ON full_date >= sp.start_date -- Period start
        AND full_date <= sp.end_date -- Period end
GROUP BY customer_segment
),
y AS (
SELECT SUM(total_revenue) AS global_telecom_revenue FROM x
),
active_customers_count_by_segment AS (
SELECT
    customer_segment,
    COUNT(DISTINCT dc.customer_id) AS active_customers_count
FROM dw.dim_customer AS dc
JOIN dw.dim_subscription AS ds ON ds.customer_id = dc.customer_id

JOIN selected_period AS sp
    ON ds.registration_date <= sp.end_date -- Period end
        AND (
            ds.termination_date IS NULL
            OR ds.termination_date >= sp.start_date -- Period start
        )
GROUP BY customer_segment
)
SELECT
    x.customer_segment,
    global_telecom_revenue,
    total_revenue,
    ROUND(
        100.0 * total_revenue / global_telecom_revenue,
        2
    ) AS contribution_to_revenue
    ,
    ROUND(
        total_revenue / active_customers_count,
        2
    ) AS avg_revenue_per_active_customer
FROM x
CROSS JOIN y
JOIN active_customers_count_by_segment AS accbs
    ON accbs.customer_segment = x.customer_segment
ORDER BY customer_segment
;
