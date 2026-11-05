-- Number of distinct purchase of offer and offer penetration rate
WITH offer_buyers AS (SELECT
    
    offer_type,
    price_xof,
    COUNT(DISTINCT customer_id) AS distinct_customers_count
FROM dw.fact_purchase AS fp
JOIN dw.dim_customer AS dc ON dc.customer_key = fp.customer_key
JOIN dw.dim_offer AS dof ON dof.offer_config_id = fp.offer_config_id
JOIN dw.dim_date AS dd ON dd.date_key = fp.date_key
WHERE full_date >= '2020-01-01' -- Period start
        AND full_date <= '2020-05-31' -- Period end
GROUP BY offer_type, price_xof
),
count_active_subscriptions AS (
SELECT COUNT(*) AS active_subscriptions_count FROM dw.dim_subscription
WHERE registration_date <= '2020-05-31' -- Period end
        AND (
            termination_date IS NULL
            OR termination_date >= '2020-01-01' -- Period start
        )
)
SELECT
    ob.*,
    ROUND(
            100.0 * distinct_customers_count / NULLIF(active_subscriptions_count, 0), -- 100.0 to force the division to be real and not integer diviser
            2

    ) AS penetration_rate
FROM offer_buyers AS ob
CROSS JOIN count_active_subscriptions
ORDER BY
    offer_type,
    price_xof
;

