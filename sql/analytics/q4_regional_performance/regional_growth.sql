WITH x AS (
SELECT
    customer_department,
    dc.customer_id,
    ds.registration_date AS subsciption_registration_date,
    ds.termination_date AS subsciption_termination_date,
    purchase_id,
    revenue
FROM dw.fact_purchase AS fp
JOIN dw.dim_customer AS dc
    ON dc.customer_key = fp.customer_key
JOIN dw.dim_subscription AS ds ON ds.customer_id = dc.customer_id
),
actual_period_purchases_count_by_by_department AS (
SELECT
    customer_department,
    COUNT(DISTINCT customer_id) AS active_customers_count_actual_period,
    COUNT(purchase_id) AS purchases_count_actual_period,
    SUM(revenue) AS total_revenue_actual_period
FROM x
WHERE subsciption_registration_date <=  '2020-06-30' -- Actual Period end
    AND (
        subsciption_termination_date IS NULL
        OR subsciption_termination_date >= '2020-06-01' -- Actual period start
    )
GROUP BY customer_department
),
previous_period_purchases_count_by_by_department AS (
SELECT
    customer_department,
    COUNT(DISTINCT customer_id) AS active_customers_count_previous_period,
    COUNT(purchase_id) AS purchases_count_previous_period,
    SUM(revenue) AS total_revenue_previous_period
FROM x
WHERE subsciption_registration_date <=  '2020-05-31' -- Previous Period end
    AND (
        subsciption_termination_date IS NULL
        OR subsciption_termination_date >= '2020-05-31' -- Previous period start
    )
GROUP BY customer_department
)
SELECT
    a_purchases_count.customer_department,
    
    -- Customers growth by region
    active_customers_count_previous_period,
    active_customers_count_actual_period,
    ROUND(
    (active_customers_count_actual_period - 
    active_customers_count_previous_period
    ) * 100.0
    / active_customers_count_previous_period,
    2
    ) AS active_customers_count_growth_rate,


    -- Purchases growth by region
    purchases_count_previous_period,
    purchases_count_actual_period,
    ROUND(
    (purchases_count_actual_period - 
    purchases_count_previous_period
    ) * 100.0
    / purchases_count_previous_period,
    2
    ) AS purchases_count_growth_rate,


    -- Revenue growth by region
    total_revenue_previous_period,
    total_revenue_actual_period,
    ROUND(
    (total_revenue_actual_period - 
    total_revenue_previous_period
    ) * 100.0
    / total_revenue_previous_period,
    2
    ) AS total_revenue_growth_rate,

    -- Average revenue by region by active customer
    total_revenue_actual_period / active_customers_count_actual_period AS avg_revenue_by_active_customer_actual_period 

FROM actual_period_purchases_count_by_by_department AS a_purchases_count
JOIN previous_period_purchases_count_by_by_department AS p_purchases_count
    ON p_purchases_count.customer_department = a_purchases_count.customer_department
ORDER BY customer_department
;
