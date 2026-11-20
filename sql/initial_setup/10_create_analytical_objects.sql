CREATE VIEW analytics.customers AS -- !!! IF NOT EXISTS?
SELECT
    customer_id,
    customer_segment,
    customer_department
FROM dw.dim_customer;

CREATE VIEW analytics.subscriptions AS
SELECT
    customer_id,
    registration_date,
    termination_date
FROM dw.dim_customer;


CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_offer_purchases AS
SELECT    
    full_date AS purchase_date,
    purchase_id,

    customer_id,
    customer_segment,
    customer_department,

    revenue,

    offer_id,
    offer_category,
    offer_family    
FROM dw.fact_purchase AS fp
JOIN dw.dim_customer AS dc ON dc.customer_key = fp.customer_key
JOIN dw.dim_offer AS dof ON dof.offer_config_id = fp.offer_config_id
JOIN dw.dim_date AS dd ON dd.date_key = fp.purchase_date_key
;

CREATE MATERIALIZED VIEW IF NOT EXISTS analytics.mv_offer_consumption AS
WITH consumption_by_purchase_id AS (
SELECT
    purchase_id,
    SUM(call_duration_seconds) AS total_call_seconds_used,
    SUM(sms_sent_count) AS total_sms_sent,
    SUM(data_used_mb) AS total_mb_used
FROM dw.fact_consumption
GROUP BY purchase_id
)
,
x AS (
SELECT
    cbp.purchase_id,
    purchase_date.full_date AS purchase_date,
    purchase_date.full_date + dof.validity_days AS offer_expiration_date,

    -- COALESCE pour genere les achats qui nont pas devenement de consommation (les achats qui ont pas ete utilise du tout)
    COALESCE(total_call_seconds_used, 0) AS total_call_seconds_used,
    COALESCE(total_sms_sent, 0) AS total_sms_sent,
    COALESCE(total_mb_used, 0.0) AS total_mb_used,    

    value_xof AS value_xof_allocated,
    value_mb AS value_mb_allocated,

    xof_per_call_second,
    xof_per_sms_sent,
    xof_per_mb_used,

    offer_id,
    offer_category,
    offer_family
FROM consumption_by_purchase_id AS cbp
-- LEFT JOIN car les achats qui nont pas encore devenement de consommation ne doivent pas etre ignores, sinon le calcul des XOF ou MB aloous serait faux
LEFT JOIN dw.fact_purchase AS fp ON fp.purchase_id = cbp.purchase_id
JOIN dw.dim_date AS purchase_date ON purchase_date.date_key = fp.purchase_date_key
JOIN dw.dim_offer AS dof ON dof.offer_config_id = fp.offer_config_id
),
y AS (
SELECT
    purchase_id,
    purchase_date,
    offer_expiration_date,

    total_call_seconds_used,
    total_call_seconds_used * xof_per_call_second AS call_xof_equiv,

    total_sms_sent,
    total_sms_sent * xof_per_sms_sent AS sms_sent_xof_equiv,

    total_mb_used,
    total_mb_used * xof_per_mb_used AS data_used_xof_equiv,


    value_xof_allocated,
    value_mb_allocated,

    offer_id,
    offer_category,
    offer_family
FROM x
)
SELECT
    purchase_id,
    purchase_date,
    offer_expiration_date,

    total_call_seconds_used,
    call_xof_equiv,

    total_sms_sent,
    sms_sent_xof_equiv,

    total_mb_used,
    data_used_xof_equiv,

    call_xof_equiv + sms_sent_xof_equiv + COALESCE(data_used_xof_equiv, 0.0) AS all_services_used_xof_equiv,


    value_xof_allocated,
    value_mb_allocated,

    offer_id,
    offer_category,
    offer_family
FROM y;


CREATE TABLE IF NOT EXISTS analytics.customer_activity (
    analysis_month DATE DEFAULT DATE_TRUNC('month', CURRENT_DATE)::DATE,
    customer_id INT NOT NULL ,--!!! should reference dw.dim_customers?
    customer_type VARCHAR(50) NOT NULL,--!!! should reference dw.dim_customers?
    customer_segment VARCHAR(50) NOT NULL,--!!! should reference dw.dim_customers?
    customer_city VARCHAR(25) NOT NULL,--!!! should reference dw.dim_customers?
    customer_department VARCHAR(25) NOT NULL,--!!! should reference dw.dim_customers?
    current_purchases INT,
    previous_purchases INT,
    purchases_growth_rate NUMERIC,
    current_data_used_mb NUMERIC,
    previous_data_used_mb NUMERIC,
    data_consumption_growth_rate NUMERIC,
    current_call_duration_seconds INT,
    previous_call_duration_seconds INT,
    call_consumption_growth_rate NUMERIC,
    current_sms_sent_count INT,
    previous_sms_sent_count INT,
    sms_consumption_growth_rate NUMERIC,
    decreasing_metrics_count SMALLINT,
    activity_status VARCHAR(30) NOT NULL,

    UNIQUE (analysis_month, customer_id)
);
