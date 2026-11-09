WITH selected_period AS (
SELECT
    DATE '2020-06-01' AS start_date,
    DATE '2020-06-30' AS end_date,
    'M' AS selection_type
),
analysis_period_tmp AS (
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
analysis_period AS (
SELECT
    start_date,
    CASE selection_type
        WHEN 'M' THEN (start_date + INTERVAL '1 month' - INTERVAL '1 day') :: DATE
        WHEN 'Q' THEN (start_date + INTERVAL '4 month' - INTERVAL '1 day') :: DATE
        WHEN 'Y' THEN (start_date + INTERVAL '1 year' - INTERVAL '1 day') :: DATE
        ELSE end_date
    END AS end_date
FROM analysis_period_tmp
),
purchase_benefits_allocations AS(
SELECT
    purchase_id,
    SUM(value_xof) AS value_xof_allocated, -- Seulement pour les offres 'MAXI', les offres de category 'INTERNET' n'ont pas value_mb
    SUM(value_mb) AS value_mb_allocated -- Seulement pour les offres 'MAXI', les offres de category 'INTERNET' n'ont pas value_mb
FROM dw.fact_purchase AS fp
JOIN dw.dim_offer AS dof
    ON dof.offer_config_id = fp.offer_config_id
JOIN dw.dim_date AS dd ON dd.date_key = fp.date_key
JOIN analysis_period AS ap
    ON full_date BETWEEN ap.start_date
                   AND ap.end_date
    AND full_date + validity_days <= ap.end_date -- Considerer uniquement les forfaits qui sexpirent au plus a la fin de la periode danalyse
GROUP BY
    purchase_id
    --offer_category
)
-- SELECT * FROM purchase_benefits_allocations;

,
benefits_allocation_by_offer_config AS (
SELECT
    offer_config_id,
    SUM(value_xof_allocated) AS value_xof_allocated,
    SUM(value_mb_allocated) AS value_mb_allocated
FROM purchase_benefits_allocations AS pba
JOIN dw.fact_purchase AS fp
    ON fp.purchase_id = pba.purchase_id
GROUP BY
    offer_config_id
)
-- SELECT * FROM benefits_allocation_by_offer_config;
,
purchase_benefits_consumption AS(
SELECT
    fc.purchase_id,
    SUM(call_duration_seconds) AS call_duration_seconds,
    SUM(sms_sent_count) AS sms_sent_count,
    SUM(data_used_mb) AS data_used_mb
FROM dw.fact_consumption AS fc
JOIN dw.fact_purchase AS fp ON fp.purchase_id = fc.purchase_id
JOIN dw.dim_date AS dd ON dd.date_key = fp.date_key
JOIN dw.dim_offer AS dof ON dof.offer_config_id = fp.offer_config_id
JOIN analysis_period AS ap
    ON full_date BETWEEN ap.start_date
                        AND ap.end_date
                AND full_date + validity_days <= ap.end_date -- Considerer uniquement les offres qui s'expirent au plus tard le dernier jour de l'analyse
GROUP BY
    fc.purchase_id
)
/*SELECT
    pbc.purchase_id,
    fp.offer_config_id,

    call_duration_seconds,
    xof_per_call_second,

    sms_sent_count,
    xof_per_sms_sent,

    call_duration_seconds * xof_per_call_second + sms_sent_count * xof_per_sms_sent AS all_services_used_xof_equiv, 

    value_xof
FROM purchase_benefits_consumption AS pbc
JOIN dw.fact_purchase AS fp
    ON fp.purchase_id = pbc.purchase_id
JOIN dw.dim_offer AS dof
    ON dof.offer_config_id = fp.offer_config_id
WHERE fp.offer_config_id = 11
;*/


/*
SELECT bc.purchase_id, data_used_mb, value_mb_allocated
FROM purchase_benefits_consumption AS bc
JOIN purchase_benefits_allocations AS ba
    ON ba.purchase_id = bc.purchase_id
WHERE data_used_mb <> 0
    AND value_mb_allocated IS NOT NULL
    AND data_used_mb > value_mb_allocated
;
*/




,

benefits_consumption_by_offer_config AS (
SELECT
    offer_config_id,
    SUM(call_duration_seconds) AS total_call_seconds_used,
    SUM(sms_sent_count) AS total_sms_sent,
    SUM(data_used_mb) AS total_mb_used
FROM purchase_benefits_consumption AS pbc
JOIN dw.fact_purchase AS fp
    ON fp.purchase_id = pbc.purchase_id
GROUP BY
    offer_config_id
)
-- SELECT * FROM benefits_consumption_by_offer_config;

/*
SELECT bc.offer_config_id, total_mb_used, value_mb_allocated FROM benefits_consumption_by_offer_config AS bc
JOIN benefits_allocation_by_offer_config AS ba ON ba.offer_config_id = bc.offer_config_id
WHERE total_mb_used <> 0 AND value_mb_allocated IS NOT NULL AND total_mb_used > value_mb_allocated
;
*/

,
services_consumption_by_offer_config_xof_equiv AS (
SELECT
    dof.offer_config_id,
    offer_category,
    
    /*total_call_seconds_used,
    xof_per_call_second,
    total_sms_sent,
    xof_per_sms_sent,*/
    
    CASE offer_type
        WHEN 'BUNDLE' THEN total_mb_used * xof_per_mb_used
    END AS data_used_xof_equiv,

    CASE offer_category
        WHEN 'MAXI' THEN total_call_seconds_used * xof_per_call_second
    END AS call_xof_equiv,

    CASE offer_category
        WHEN 'MAXI' THEN total_sms_sent * xof_per_sms_sent
    END AS sms_sent_xof_equiv,

    CASE offer_category
        WHEN 'INTERNET' THEN total_mb_used
    END AS total_mb_used

FROM benefits_consumption_by_offer_config AS bcboc
JOIN dw.dim_offer AS dof
    ON dof.offer_config_id = bcboc.offer_config_id
)
--SELECT * FROM services_consumption_by_offer_config_xof_equiv;
,
xof_equiv_metrics_by_offer_config AS (
SELECT
    offer_config_id,
    total_mb_used,
    data_used_xof_equiv,
    call_xof_equiv,
    sms_sent_xof_equiv,
    CASE offer_category
        WHEN 'MAXI' THEN
            COALESCE(data_used_xof_equiv, 0) + -- Pour les forfait maxi appel
            call_xof_equiv + 
            sms_sent_xof_equiv
    END AS all_services_usage_xof_equiv
FROM services_consumption_by_offer_config_xof_equiv
)
/*SELECT
    xof_em.offer_config_id,
    data_used_xof_equiv,
    call_xof_equiv,
    sms_sent_xof_equiv,
    all_services_usage_xof_equiv,
    value_xof_allocated
FROM xof_equiv_metrics_by_offer_config AS xof_em
JOIN benefits_allocation_by_offer_config AS babo
    ON babo.offer_config_id = xof_em.offer_config_id;*/
  

-- SELECT * FROM xof_equiv_metrics_by_offer_config;
,
offer_consumption AS(
SELECT
    offer_id,
    SUM(total_mb_used) AS total_mb_used,
    SUM(value_mb_allocated) AS value_mb_allocated,
    SUM(data_used_xof_equiv) AS data_used_xof_equiv,
    SUM(call_xof_equiv) AS call_xof_equiv,
    SUM(sms_sent_xof_equiv) AS sms_sent_xof_equiv,
    SUM(all_services_usage_xof_equiv) AS all_services_usage_xof_equiv,
    SUM(value_xof_allocated) AS value_xof_allocated
FROM xof_equiv_metrics_by_offer_config AS xof_em
JOIN benefits_allocation_by_offer_config AS babo
    ON babo.offer_config_id = xof_em.offer_config_id
JOIN dw.dim_offer AS dof ON dof.offer_config_id = xof_em.offer_config_id
GROUP BY
    offer_id
)
/*SELECT
    offer_id,
    data_used_xof_equiv,
    call_xof_equiv,
    sms_sent_xof_equiv,
    all_services_usage_xof_equiv,
    value_xof_allocated
FROM offer_consumption_metrics;*/




-- SELECT * FROM offer_consumption_metrics;

,
offer_details_map AS (
SELECT DISTINCT
    offer_category,
    offer_type,
    price_xof,
    
    offer_id
FROM dw.dim_offer
),
offer_consumption_metrics AS (
SELECT
    offer_category,
    offer_type,
    price_xof,
    oc.offer_id,

    CASE
        -- Les offres MAXI (elles sont soi MOBILE soit BUNDLE)
        WHEN offer_category = 'MAXI' THEN ROUND(100 * all_services_usage_xof_equiv / value_xof_allocated, 2)
        -- Les offres INTERNET (Elles sont DATA)
        WHEN offer_category ='INTERNET' THEN ROUND(100 * total_mb_used / value_mb_allocated, 2)
    END AS benefits_global_consumption_rate,

    CASE
        WHEN offer_type = 'BUNDLE' THEN ROUND(100 * data_used_xof_equiv / value_xof_allocated, 2)
    END AS data_consumption_contribution,

    CASE
        WHEN offer_type = 'MOBILE' THEN ROUND(100 * call_xof_equiv / value_xof_allocated, 2)
    END AS call_consumption_contribution,

    CASE
        WHEN offer_type = 'MOBILE' THEN ROUND(100 * sms_sent_xof_equiv / value_xof_allocated, 2)
    END AS sms_consumption_contribution
FROM offer_consumption AS oc
JOIN offer_details_map AS odm ON odm.offer_id = oc.offer_id
)
SELECT
    offer_category,
    offer_type,
    price_xof,
    offer_id,
    benefits_global_consumption_rate,
    data_consumption_contribution,
    call_consumption_contribution,
    sms_consumption_contribution
FROM offer_consumption_metrics AS ocm
ORDER BY
    offer_category,
    offer_type,
    price_xof
;
