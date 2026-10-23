-- dim_date
WITH dates_range AS(
SELECT GENERATE_SERIES(DATE '2020-01-01', DATE '2030-12-31', INTERVAL '1 day') AS date
)
INSERT INTO dw.dim_date(date_key, full_date, formatted_date, day_of_week_num, day_of_week_name, day_of_week_name_short, day_of_month, day_of_year, month_num, month_name, month_name_short, quarter_num, quarter_name, quarter_name_short, year)
SELECT TO_CHAR(date, 'YYYYMMDD')::INT AS date_key,
date::DATE AS full_date,
TO_CHAR(date, 'DD/MM/YYYY') AS formatted_date,
EXTRACT(ISODOW FROM date) AS day_of_week_num,
TO_CHAR(date, 'Day') AS day_of_week_name,
LEFT(TO_CHAR(date, 'Day'), 3),
EXTRACT(DAY FROM date) AS day_of_month,
EXTRACT(DOY FROM date) AS day_of_year,
EXTRACT(MONTH FROM date) AS month_num,
TO_CHAR(date, 'Month') AS month_name,
TO_CHAR(date, 'Mon') AS month_name_short,
EXTRACT(QUARTER FROM date) AS quarter_num,
'Quarter ' || EXTRACT(QUARTER FROM date) AS quarter_name,
'Q' || EXTRACT(QUARTER FROM date) AS quarter_name_short,
EXTRACT(YEAR FROM date) AS year FROM dates_range;

-- Dim offer
INSERT INTO dw.dim_offer(offer_config_id, offer_id, offer_name, offer_type, offer_category, validity_days, is_limitless, price_xof, value_xof, value_mb, xof_per_call_second, xof_per_sms_sent, xof_per_mb_used, offer_start_date, offer_end_date, valid_from, is_current)
SELECT oc.id AS offer_config_id,  o.id AS offer_id, o.name AS offer_name, o.type AS offer_type, 
CASE
WHEN o.name ILIKE '%libre%' THEN 'OPTION LIBRE'
WHEN o.name ILIKE 'défaut' THEN 'OFFRE PAR DEFAUT'
ELSE UPPER((STRING_TO_ARRAY( o.name , ' '))[2])
END AS offer_category, 
oc.validity_days, oc.is_limitless, o.price_xof, oc.value_xof, oc.value_mb, ob.xof_per_second AS xof_per_call_second, ob.xof_per_sms AS xof_per_sms_sent, ob.xof_per_mb AS xof_per_mb_used, oc.start_date AS offer_start_date, oc.end_date AS offer_end_date, DATE '2020-01-01' AS valid_from, TRUE AS is_current -- pour le initial load considerer une date ancienne pour la valid from
FROM staging.offer_configurations AS oc
LEFT JOIN staging.offer_billings AS ob on ob.id = oc.billing_id -- Left JOIN to also consider offers without billing
JOIN staging.offers AS o ON o.id = oc.offer_id;


SELECT COUNT(*) FROM dw.dim_offer;
SELECT COUNT(*) FROM staging.offer_configurations;



-- Dim customer
INSERT INTO dw.dim_customer(customer_id, customer_city, customer_department, customer_segment, customer_type, gender, registration_date, status, termination_date, valid_from, is_current)
SELECT c.id AS customer_id, 
COALESCE(cities.city, 'Unkown ('|| c.city || ')') AS customer_city,
COALESCE(cities.department, 'Unkown') AS customer_department,
customer_segment,
COALESCE(c.customer_type,
        CASE
        WHEN customer_segment = 'SME' THEN 'BUSINESS'
        WHEN customer_segment IN ('STANDARD', 'YOUTH') THEN 'INDIVIDUAL'
        ELSE 'Unkown'
        END) AS customer_type,
c.gender, c.registration_date, c.status,  c.termination_date, c.registration_date AS valid_from, TRUE AS is_current -- pour le initial load considerer le registration date come le valid from
FROM staging.customers AS c 
LEFT JOIN ref.cities AS cities ON cities.city = c.city; -- LEFT JOIN pour ne pas perdre les clients dont la ville napparait as dans la table des villes (ie les clients de ville invalide)


SELECT COUNT(*) FROM dw.dim_customer;
SELECT COUNT(*) FROM staging.customers;



-- Fact purchase
WITH purchase_details AS(
SELECT p.id AS purchase_id, purchased_at::DATE AS purchase_date, customer_key, s.customer_id, dc.valid_from, dc.valid_to, offer_key, offer_id, price_xof AS revenue
FROM staging.purchases AS p
JOIN staging.subscriptions AS s ON s.id = p.subscription_id
JOIN dw.dim_customer AS dc ON dc.customer_id = s.customer_id
JOIN dw.dim_offer AS dof ON dof.offer_config_id = p.offer_config_id -- !!!Pourquoi des LEFT JOIN et pas simplement des INNER JOIN? (PLusieurs lignes restent inseres lorque jutilise INNER JOIN)
)
INSERT INTO dw.fact_purchase(purchase_id, date_key, customer_key, offer_key, revenue)
SELECT purchase_id, TO_CHAR(purchase_date, 'YYYYMMDD')::INT AS date_key, customer_key, offer_key, revenue FROM purchase_details;


SELECT COUNT(*) FROM dw.fact_purchase;
SELECT COUNT(*) FROM staging.purchases;



-- Fact consumption
WITH service_usage_records_deduplicated AS(
    SELECT * FROM staging.services_usage AS su WHERE NOT EXISTS (
        SELECT 1 FROM data_quality.issues AS i WHERE i.batch_id = su.batch_id AND table_name = 'services_usage' AND issue_type = 'Uniqueness' AND i.record_id = su.id
    )   
),
consumption_details AS (
SELECT su.id, purchase_id, timestamp::DATE AS consumption_date, customer_key, s.customer_id, dc.valid_from, dc.valid_to, offer_key, offer_id, call_seconds AS call_duration_seconds, sms_count AS sms_sent_count, data_mb AS data_used_mb
FROM service_usage_records_deduplicated AS su
JOIN staging.purchases AS p ON p.id = su.purchase_id
JOIN staging.subscriptions AS s ON s.id = su.subscription_id
JOIN dw.dim_customer AS dc ON dc.customer_id = s.customer_id
JOIN dw.dim_offer AS dof ON dof.offer_config_id = p.offer_config_id
),
customer_purchase_consumption_daily_events AS (
SELECT purchase_id, TO_CHAR(consumption_date, 'YYYYMMDD')::INT AS date_key, customer_key, offer_key, call_duration_seconds, sms_sent_count, data_used_mb  FROM consumption_details
),
customer_purchase_consumption_daily_events_aggregated AS (
SELECT purchase_id, date_key, customer_key, offer_key,
SUM(call_duration_seconds) OVER(w) AS call_duration_seconds,
SUM(sms_sent_count) OVER(w) AS sms_sent_count,
SUM(data_used_mb) OVER(w) AS data_used_mb,
ROW_NUMBER() OVER (w) AS rn
FROM customer_purchase_consumption_daily_events
WINDOW w AS (PARTITION BY purchase_id, date_key )
)
INSERT INTO dw.fact_consumption(purchase_id, date_key, customer_key, offer_key, call_duration_seconds, sms_sent_count, data_used_mb)
SELECT purchase_id, date_key, customer_key, offer_key, call_duration_seconds, sms_sent_count, data_used_mb
FROM customer_purchase_consumption_daily_events_aggregated
WHERE rn = 1;




SELECT COUNT(*) FROM dw.fact_consumption;
WITH service_usage_records_deduplicated AS(
    SELECT * FROM staging.services_usage AS su WHERE NOT EXISTS (
        SELECT 1 FROM data_quality.issues AS i WHERE i.batch_id = su.batch_id AND table_name = 'services_usage' AND issue_type = 'Uniqueness' AND i.record_id = su.id
    )   
),
service_usage_records_aggregated AS(
SELECT purchase_id, timestamp:: DATE AS date FROM service_usage_records_deduplicated GROUP BY purchase_id, date
)
SELECT COUNT(*) FROM service_usage_records_aggregated;

