-- Number of distinct purchase of offer and offer penetration rate
WITH selected_period AS (
SELECT
    DATE '2020-06-01' AS start_date,
    DATE '2020-06-30' AS end_date
),
offer_metrics AS (
SELECT    
    offer_id,
    SUM(revenue) AS total_revenue,
    COUNT(DISTINCT customer_id) AS distinct_customers_count,
    COUNT(purchase_id) AS purchases_count
FROM dw.fact_purchase AS fp
JOIN dw.dim_customer AS dc ON dc.customer_key = fp.customer_key
JOIN dw.dim_offer AS dof ON dof.offer_config_id = fp.offer_config_id
JOIN dw.dim_date AS dd ON dd.date_key = fp.date_key
JOIN selected_period AS sp
    ON full_date >= sp.start_date -- Period start
        AND full_date <= sp.end_date -- Period end
GROUP BY
    offer_id
),
count_active_subscriptions AS (
SELECT COUNT(*) AS active_subscriptions_count
FROM dw.dim_subscription AS ds
JOIN selected_period AS sp
    ON ds.registration_date <= sp.end_date -- Period end
        AND (
            ds.termination_date IS NULL
            OR ds.termination_date >= sp.start_date -- Period start
        )
)
,
offer_details_map AS (
SELECT DISTINCT
    offer_category,
    offer_type,
    price_xof,
    
    offer_id
FROM dw.dim_offer
)
SELECT
    offer_category,
    offer_type,
    price_xof,

    om.offer_id,    
    total_revenue,
    distinct_customers_count,
    ROUND(
            100.0 * distinct_customers_count / NULLIF(active_subscriptions_count, 0), -- 100.0 to force the division to be real and not integer diviser
            2
    ) AS penetration_rate,
    purchases_count
FROM offer_metrics AS om
CROSS JOIN count_active_subscriptions
JOIN offer_details_map AS odm ON odm.offer_id = om.offer_id
ORDER BY
    offer_category,
    offer_type,
    price_xof
;

