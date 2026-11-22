WITH analysis_month AS (
SELECT
    -- DATE '2025-05-01' AS start_date
    :'analysis_month'::DATE AS start_date

    
),
current_period AS (
SELECT
    start_date,
    (start_date + INTERVAL '1 month -1 day')::DATE AS end_date
FROM analysis_month
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
    (start_date - (end_date - start_date) - INTERVAL '1 day') :: DATE AS start_date,
    (start_date - INTERVAL '1 day') :: DATE AS end_date
FROM current_period
)
-- SELECT * FROM comparaison_periods;
,
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
    period_type,
    customer_id   
FROM customers_activity
),
analyzed_customers AS ( -- Customers that have been active in both previous and current periods
SELECT customer_id FROM active_customers WHERE period_type = 'previous'
INTERSECT
SELECT customer_id FROM active_customers WHERE period_type = 'current'
)
-- SELECT * FROM analyzed_customers;
-- SELECT COUNT(*) FROM analyzed_customers;
,
target_purchases AS (
SELECT
    period_type,
    customer_id,
    purchase_id
FROM dw.fact_purchase AS fp
JOIN dw.dim_customer AS dc
    ON dc.customer_key = fp.customer_key
JOIN dw.dim_date AS dd
    ON dd.date_key = fp.purchase_date_key
JOIN comparaison_periods AS cp
    ON full_date >= cp.start_date
        AND full_date <= cp.end_date
WHERE EXISTS(
    SELECT 1 FROM analyzed_customers AS tg WHERE tg.customer_id = dc.customer_id
)   
)
-- SELECT * FROM target_purchases;
,
target_consumptions AS (
SELECT
    period_type,
    customer_id,
    call_duration_seconds,
    sms_sent_count,
    data_used_mb 
FROM dw.fact_consumption AS fc
JOIN dw.dim_customer AS dc
    ON dc.customer_key = fc.customer_key
JOIN dw.dim_date AS dd
    ON dd.date_key = fc.consumption_date_key
JOIN comparaison_periods AS cp
    ON full_date >= cp.start_date
        AND full_date <= cp.end_date
WHERE EXISTS(
    SELECT 1 FROM analyzed_customers AS tg WHERE tg.customer_id = dc.customer_id
)   
)
-- SELECT * FROM target_consumptions;
,
purchase_metrics AS (
SELECT
    customer_id,
    COUNT(purchase_id) FILTER(WHERE period_type = 'current') AS current_purchases,
    COUNT(purchase_id) FILTER(WHERE period_type = 'previous') AS previous_purchases
FROM target_purchases
GROUP BY
    customer_id
)
-- SELECT * FROM purchase_metrics;
,
consumption_metrics AS (
SELECT
    customer_id,
    SUM(data_used_mb) FILTER(WHERE period_type = 'current') AS current_data_used_mb,
    SUM(data_used_mb) FILTER(WHERE period_type = 'previous') AS previous_data_used_mb,

    SUM(call_duration_seconds) FILTER(WHERE period_type = 'current') AS current_call_duration_seconds,
    SUM(call_duration_seconds) FILTER(WHERE period_type = 'previous') AS previous_call_duration_seconds,

    SUM(sms_sent_count) FILTER(WHERE period_type = 'current') AS current_sms_sent_count,
    SUM(sms_sent_count) FILTER(WHERE period_type = 'previous') AS previous_sms_sent_count

FROM target_consumptions
GROUP BY
    customer_id
)
-- SELECT * FROM consumption_metrics;

,

activity_metrics AS (
SELECT
    tg.customer_id,

    current_purchases,
    previous_purchases,

    current_data_used_mb,
    previous_data_used_mb,

    current_call_duration_seconds,
    previous_call_duration_seconds,

    current_sms_sent_count,
    previous_sms_sent_count,

    CASE
        WHEN previous_purchases IS NULL AND current_purchases IS NULL THEN 'INACTIVE_BOTH'
        WHEN previous_purchases IS NOT NULL  AND current_purchases IS NULL THEN 'INACTIVE_CURRENT'
        WHEN previous_purchases IS NULL  AND current_purchases IS NULL THEN 'NEW_OR_RESUMED_ACTIVITY'
        -- decreasing_metrics_count >= 2 THEN TRUE -- ! Faire en sorte que le 2 soit parametrable
        -- ELSE NULL
    END AS activity_status

FROM analyzed_customers AS tg
LEFT JOIN purchase_metrics AS pm
    ON pm.customer_id = tg.customer_id
LEFT JOIN consumption_metrics AS cm
    ON cm.customer_id = tg.customer_id
)
-- SELECT * FROM activity_metrics;

,
activity_growth AS (
SELECT
    customer_id,

    current_purchases,
    previous_purchases,
    activity_status,

    CASE
        WHEN activity_status IS NULL THEN 
                    ROUND(
            (current_purchases - previous_purchases
            ) * 100.0
            / NULLIF(previous_purchases, 0),
            2
            )
    END AS purchases_growth_rate,

    current_data_used_mb,
    previous_data_used_mb,

    CASE
        WHEN activity_status IS NULL THEN
                        ROUND(
                        (current_data_used_mb - previous_data_used_mb
                        ) * 100.0
                        / NULLIF(previous_data_used_mb, 0),
                        2
                        )
    END AS data_consumption_growth_rate,

    current_call_duration_seconds,
    previous_call_duration_seconds,

    CASE
        WHEN activity_status IS NULL THEN
                    ROUND(
                    (current_call_duration_seconds - previous_call_duration_seconds
                    ) * 100.0
                    / NULLIF(previous_call_duration_seconds, 0),
                    2
                    )
    END AS call_consumption_growth_rate,


    current_sms_sent_count,
    previous_sms_sent_count,

    CASE
        WHEN activity_status IS NULL THEN
                    ROUND(
                    (current_sms_sent_count - previous_sms_sent_count
                    ) * 100.0
                    / NULLIF(previous_sms_sent_count, 0),
                    2
                    )
    END AS sms_consumption_growth_rate
FROM activity_metrics
)
-- SELECT * FROM activity_growth;
,
activity_decrease_metrics AS (
SELECT
    customer_id,
    activity_status,

    current_purchases,
    previous_purchases,
    purchases_growth_rate,

    current_data_used_mb,
    previous_data_used_mb,
    data_consumption_growth_rate,

    current_call_duration_seconds,
    previous_call_duration_seconds,
    call_consumption_growth_rate,

    current_sms_sent_count,
    previous_sms_sent_count,
    sms_consumption_growth_rate,    

    CASE
        WHEN activity_status IS NULL THEN 
                                        COALESCE((purchases_growth_rate <= -30), FALSE)::INT + -- ! Faire en sorte que le 30 soit parametrable
                                        COALESCE((data_consumption_growth_rate <= -30), FALSE)::INT +
                                        COALESCE((call_consumption_growth_rate <= -30), FALSE)::INT +
                                        COALESCE((sms_consumption_growth_rate <= -30), FALSE)::INT 
    END AS decreasing_metrics_count

FROM activity_growth  
)
INSERT INTO analytics.customer_activity_analysis (analysis_month, customer_id, customer_type, customer_segment, customer_city, customer_department, current_purchases, previous_purchases, purchases_growth_rate, current_data_used_mb, previous_data_used_mb, data_consumption_growth_rate, current_call_duration_seconds, previous_call_duration_seconds, call_consumption_growth_rate, current_sms_sent_count, previous_sms_sent_count, sms_consumption_growth_rate, decreasing_metrics_count, activity_status)
SELECT
    am.start_date AS analysis_month,
    adm.customer_id,
    dc.customer_type,
    dc.customer_segment,
    dc.customer_city,
    dc.customer_department,


    current_purchases,
    previous_purchases,
    purchases_growth_rate,

    current_data_used_mb,
    previous_data_used_mb,
    data_consumption_growth_rate,

    current_call_duration_seconds,
    previous_call_duration_seconds,
    call_consumption_growth_rate,

    current_sms_sent_count,
    previous_sms_sent_count,
    sms_consumption_growth_rate,

    decreasing_metrics_count,

    CASE
        WHEN decreasing_metrics_count >= 2 THEN 'DECLINING_ACTIVITY'
        WHEN decreasing_metrics_count BETWEEN 0 AND 1 THEN 'STABLE_OR_GROWING_ACTIVITY'
        WHEN activity_status IS NOT NULL THEN activity_status
    END AS activity_status
FROM activity_decrease_metrics AS adm
JOIN dw.dim_customer AS dc ON dc.customer_id = adm.customer_id
CROSS JOIN analysis_month AS am
;






























/*
-- SELECT * FROM declining_customers;
,
customers_analyzed AS (
SELECT COUNT(*) FROM analyzed_customers
),
customers_with_activity AS (
SELECT COUNT(DISTINCT customer_id) FROM target_purchases
),
customers_activity_analysis_stats AS(
SELECT
    ca.count AS num_customers_analyzed,
    ca.count - cwa.count AS num_customers_without_activity,
    dc.count AS num_declining_customers,
    cwa.count - dc.count AS num_stable_customers
FROM customers_analyzed AS ca
CROSS JOIN customers_with_activity AS cwa
CROSS JOIN declining_customers AS dc
)
-- SELECT * FROM customers_activity_analysis_stats;

SELECT
    customer_id,

    current_purchases,
    previous_purchases,
    purchases_growth_rate,

    current_data_used_mb,
    previous_data_used_mb,
    data_consumption_growth_rate,

    current_call_duration_seconds,
    previous_call_duration_seconds,
    call_consumption_growth_rate,

    current_sms_sent_count,
    previous_sms_sent_count,
    sms_consumption_growth_rate,

    decreasing_metrics_count,

    overall_growth,

    in_decline,

    num_customers_analyzed,

    num_customers_without_activity,
    ROUND(100.0 * num_customers_without_activity / num_customers_analyzed, 2) AS customers_without_activity_rate,

    num_stable_customers,
    ROUND(100.0 * num_stable_customers / num_customers_analyzed, 2) AS stable_customers_rate,

    num_declining_customers,
    ROUND(100.0 * num_declining_customers / num_customers_analyzed, 2) AS declining_customers_rate

FROM declining_customers_ordered_by_activity_decrease AS dc
CROSS JOIN customers_activity_analysis_stats

UNION ALL

SELECT customer_id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM analyzed_customers AS tgc
WHERE NOT EXISTS(
    SELECT 1 FROM target_purchases AS cwa WHERE cwa.customer_id = tgc.customer_id
)

ORDER BY
    in_decline,
    decreasing_metrics_count DESC,
    overall_growth ASC
;
*/