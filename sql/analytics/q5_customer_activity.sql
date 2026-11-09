WITH selected_period AS (
SELECT
    DATE '2020-12-01' AS start_date,
    DATE '2020-12-31' AS end_date,
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
    period_type,
    customer_id   
FROM customers_activity
),
active_customers_both AS ( -- Customers that have bee active in both previous and current periods
SELECT customer_id FROM active_customers WHERE period_type = 'previous'
INTERSECT
SELECT customer_id FROM active_customers WHERE period_type = 'current'
),
target_customers AS (
SELECT customer_id FROM active_customers_both
)
-- SELECT * FROM target_customers;
-- SELECT COUNT(*) FROM target_customers;

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
    ON dd.date_key = fp.date_key
JOIN comparaison_periods AS cp
    ON full_date >= cp.start_date
        AND full_date <= cp.end_date
WHERE EXISTS(
    SELECT 1 FROM target_customers AS tg WHERE tg.customer_id = dc.customer_id
)   
)
-- SELECT * FROM target_purchases;

-- SELECT COUNT(*) FROM target_purchases;
-- SELECT COUNT(DISTINCT customer_id) FROM target_purchases;

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
    ON dd.date_key = fc.date_key
JOIN comparaison_periods AS cp
    ON full_date >= cp.start_date
        AND full_date <= cp.end_date
WHERE EXISTS(
    SELECT 1 FROM target_customers AS tg WHERE tg.customer_id = dc.customer_id
)   
)
-- SELECT * FROM target_consumptions;
,
purchase_metrics AS (
SELECT
    customer_id,
    COUNT(purchase_id) FILTER(WHERE period_type = 'current') AS current_purchases,
    COUNT(purchase_id) FILTER(WHERE period_type = 'previous') AS previous_purchases
    -- SUM(revenue) FILTER(WHERE period_type = 'current') AS current_revenue,
    -- SUM(revenue) FILTER(WHERE period_type = 'previous') AS previous_revenue
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
    previous_sms_sent_count


    -- current_revenue,
    -- previous_revenue,
    -- current_revenue / NULLIF(current_active_customers, 0) AS avg_revenue_per_active_customer
FROM target_customers AS tg
JOIN purchase_metrics AS pm
    ON pm.customer_id = tg.customer_id
JOIN consumption_metrics AS cm
    ON cm.customer_id = tg.customer_id
)
-- SELECT * FROM activity_metrics;

,
activity_growth AS (
SELECT
    customer_id,

    current_purchases,
    previous_purchases,
    ROUND(
    (current_purchases - previous_purchases
    ) * 100.0
    / NULLIF(previous_purchases, 0),
    2
    ) AS purchases_growth_rate,

    current_data_used_mb,
    previous_data_used_mb,
    ROUND(
    (current_data_used_mb - previous_data_used_mb
    ) * 100.0
    / NULLIF(previous_data_used_mb, 0),
    2
    ) AS data_consumption_growth_rate,

    current_call_duration_seconds,
    previous_call_duration_seconds,
    ROUND(
    (current_call_duration_seconds - previous_call_duration_seconds
    ) * 100.0
    / NULLIF(previous_call_duration_seconds, 0),
    2
    ) AS call_consumption_growth_rate,


    current_sms_sent_count,
    previous_sms_sent_count,
    ROUND(
    (current_sms_sent_count - previous_sms_sent_count
    ) * 100.0
    / NULLIF(previous_sms_sent_count, 0),
    2
    ) AS sms_consumption_growth_rate
FROM activity_metrics
)
-- SELECT * FROM activity_growth;
,
activity_decrease_metrics AS (
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
    

    COALESCE((purchases_growth_rate <= -30), FALSE)::INT + -- ! Faire en sorte que le 3 soit parametrable
    COALESCE((data_consumption_growth_rate <= -30), FALSE)::INT +
    COALESCE((call_consumption_growth_rate <= -30), FALSE)::INT +
    COALESCE((sms_consumption_growth_rate <= -30), FALSE)::INT AS decreasing_metrics_count

FROM activity_growth  
)
,
customers_decline AS (
SELECT
    *,
    COALESCE(purchases_growth_rate, 0) + COALESCE(data_consumption_growth_rate, 0) + COALESCE(call_consumption_growth_rate, 0) + COALESCE(sms_consumption_growth_rate, 0) AS overall_growth,
    CASE
        WHEN decreasing_metrics_count >= 2 THEN TRUE -- ! Faire en sorte que le 2 soit parametrable
        ELSE FALSE
    END AS in_decline

FROM activity_decrease_metrics 
)

-- SELECT * FROM customers_decline;
,
declining_customers_ordered_by_activity_decrease AS (
SELECT * FROM customers_decline
)

-- SELECT * FROM declining_customers_ordered_by_activity_decrease;
,
declining_customers AS (
SELECT
    COUNT(*)
FROM declining_customers_ordered_by_activity_decrease WHERE in_decline
)

-- SELECT * FROM declining_customers;
,
customers_analyzed AS (
SELECT COUNT(*) FROM target_customers
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

SELECT customer_id, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL FROM target_customers AS tgc
WHERE NOT EXISTS(
    SELECT 1 FROM target_purchases AS cwa WHERE cwa.customer_id = tgc.customer_id
)

ORDER BY
    in_decline,
    decreasing_metrics_count DESC,
    overall_growth ASC
;