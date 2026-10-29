-- !!! Later : code pour eviter qu'un achat deja existant se charge plusieurs fois
CREATE TEMP TABLE current_batch_offers AS(
SELECT * FROM staging.offers WHERE batch_id = ANY(STRING_TO_ARRAY(:'batch_id', ',')::INT[])
);

CREATE TEMP TABLE current_batch_offer_billings AS(
SELECT * FROM staging.offer_billings WHERE batch_id = ANY(STRING_TO_ARRAY(:'batch_id', ',')::INT[])
);


CREATE TEMP TABLE current_batch_offer_configurations AS(
SELECT * FROM staging.offer_configurations WHERE batch_id = ANY(STRING_TO_ARRAY(:'batch_id', ',')::INT[])
);

CREATE TEMP TABLE current_batch_customers AS(
SELECT * FROM staging.customers WHERE batch_id = ANY(STRING_TO_ARRAY(:'batch_id', ',')::INT[])
);


CREATE TEMP TABLE current_batch_subscriptions AS(
SELECT * FROM staging.subscriptions WHERE batch_id = ANY(STRING_TO_ARRAY(:'batch_id', ',')::INT[])
);

CREATE TEMP TABLE current_batch_purchases AS(
SELECT * FROM staging.purchases WHERE batch_id = ANY(STRING_TO_ARRAY(:'batch_id', ',')::INT[])
);

CREATE TEMP TABLE current_batch_services_usage AS(
SELECT * FROM staging.services_usage WHERE batch_id = ANY(STRING_TO_ARRAY(:'batch_id', ',')::INT[])
);

-- dim_date (Already loaded initially)

-- Dim offer (Je suppose SCD 1 donc en cas de changement juste updte): Je considere seuelemt le nom de loffre, sa date de debut et de fin (date de debut et de fin de loffre configuree), comme SCD1 et tous les autres attributs comme SCD 0 (vu que la source possede start date et end date, une nouvelle offre est creer lorsuqe les autres attributs changent) 
-- 1. Mettre a jour le nom pour toutes les offres du DW dont le nom a change dans le batch courant
UPDATE dw.dim_offer AS dof
SET offer_name = o.name
-- FROM staging.offer_configurations AS oc
FROM current_batch_offers AS o
-- JOIN staging.offers AS o ON o.id = oc.offer_id -- Considerer tous les offres car il se peut que loffre concernee ne soit pas dans le batch doffre courant
WHERE 
o.id = dof.offer_id AND 
(
        o.name IS DISTINCT FROM dof.offer_name

      );

UPDATE dw.dim_offer AS dof
SET offer_start_date = oc.start_date,
    offer_end_date = oc.end_date
FROM current_batch_offer_configurations AS oc
WHERE 
oc.id = dof.offer_config_id AND 
(
        oc.start_date IS DISTINCT FROM dof.offer_start_date
        OR oc.end_date IS DISTINCT FROM dof.offer_end_date
      );

-- 2. Inserer les nouvelles offres (ceux qui ne sont pas encore dans le DW)
INSERT INTO dw.dim_offer(offer_config_id, offer_id, offer_name, offer_type, offer_category, validity_days, is_limitless, price_xof, value_xof, value_mb, xof_per_call_second, xof_per_sms_sent, xof_per_mb_used, offer_start_date, offer_end_date)
SELECT oc.id AS offer_config_id,  o.id AS offer_id, o.name AS offer_name, o.type AS offer_type,
CASE
WHEN o.name ILIKE '%libre%' THEN 'OPTION LIBRE'
WHEN o.name ILIKE 'défaut' THEN 'OFFRE PAR DEFAUT'
ELSE UPPER((STRING_TO_ARRAY( o.name , ' '))[2])
END AS offer_category, 
oc.validity_days, oc.is_limitless, o.price_xof, oc.value_xof, oc.value_mb, ob.xof_per_second AS xof_per_call_second, ob.xof_per_sms AS xof_per_sms_sent, ob.xof_per_mb AS xof_per_mb_used, oc.start_date AS offer_start_date, oc.end_date AS offer_end_date
FROM current_batch_offer_configurations AS oc
-- FROM staging.offer_configurations AS oc
LEFT JOIN staging.offer_billings AS ob on ob.id = oc.billing_id -- Left JOIN to also consider offers without billing; Considerer tous les offres car il se peut que le billing concrne ne soit pas dans le batch couran
JOIN staging.offers AS o ON o.id = oc.offer_id -- Considerer tous les offres car il se peut que loffre concernee ne soit pas dans le batch courant
LEFT JOIN dw.dim_offer AS dof ON dof.offer_config_id = oc.id
WHERE dof.offer_config_id IS NULL; -- Les offres qui ne sont pas dans le DW


-- Dim customer

-- 1. Mettre a jour dans dim_customer les clients (avec toutes leurs versions) pour lesquels des attributs SCD 1 (gender, registration date et termination date) ont changé, avec leurs lignes correspondantes dans le staging
UPDATE dw.dim_customer AS dc
SET gender = c.gender, 
    registration_date = c.registration_date,
    termination_date = c.termination_date
FROM current_batch_customers AS c
WHERE c.id = dc.customer_id -- La ligne correspondante a la ligne courante dans le staging
      AND ( -- Cibler uniquement les lignes dont certains attributs SCD1 ont effectivement changé
            c.gender IS DISTINCT FROM dc.gender -- IS DISTINCT FROM permet  de gerer effectivement les NULL values
            OR c.registration_date IS DISTINCT FROM dc.registration_date -- OR pour cibler les clients dont au moins un attribut SCD1 a changé
            OR c.termination_date IS DISTINCT FROM dc.termination_date
      );

-- 2. Fermer toutes les versions courantes pour les clients dont des attributs SCD 2 (city, type, segment, status) ont changé
UPDATE dw.dim_customer AS dc
SET valid_to = CURRENT_TIMESTAMP,
    is_current = FALSE
FROM current_batch_customers AS c
WHERE c.id = dc.customer_id
      AND (
            c.city IS DISTINCT FROM dc.customer_city
            OR c.customer_type IS DISTINCT FROM dc.customer_type
            OR c.customer_segment IS DISTINCT FROM dc.customer_segment
            OR c.status IS DISTINCT FROM dc.status
      );

-- 3. Insérer les nouveaux clients ainsi que les nouvelles versions de clients (les clients du staging qui nont aucune version courante dans le DW)

INSERT INTO dw.dim_customer(customer_id, customer_city, customer_department, customer_segment, customer_type, gender, registration_date, status, termination_date, valid_from, is_current)
SELECT c.id AS customer_id,
COALESCE(rc.city, 'Unkown ('|| c.city || ')') AS customer_city,
COALESCE(rc.department, 'Unkown') AS customer_department,
c.customer_segment,
COALESCE(c.customer_type,
        CASE
        WHEN c.customer_segment = 'SME' THEN 'BUSINESS'
        WHEN c.customer_segment IN ('STANDARD', 'YOUTH') THEN 'INDIVIDUAL'
        ELSE 'Unkown'
        END) AS customer_type,
c.gender,
c.registration_date,
c.status,
c.termination_date,
CURRENT_TIMESTAMP as valid_from,
TRUE as is_current
-- FROM staging.customers AS c
FROM current_batch_customers AS c
LEFT JOIN ref.cities AS rc ON rc.city = c.city -- LEFT JOIN pour ne pas perdre les clients dont la ville n'est pas dans ref.cities (notamment les clients de ville mal ecrites)
LEFT JOIN dw.dim_customer AS dc -- LEFT JOIN pour ne pas perdre les nouveaux clients
                                ON dc.customer_id = c.id
                                AND dc.is_current = TRUE -- Pour faire correspondre les clients du staging avec leurs versions acuelles dans le dw
WHERE dc.customer_id IS NULL; -- Les clients du staging qui nont aucune version courante dans le DW(ie les nouveaux clients et les anciens dont toutes leurs versions courantes vieent juste detre fermee via le UPDATE)


-- Fact purchase
INSERT INTO dw.fact_purchase(purchase_id, date_key, customer_key, offer_config_id, revenue)
WITH x AS (SELECT
    p.id AS purchase_id,
    p.purchased_at,
    dc.customer_key,
    dof.offer_config_id,
    price_xof AS revenue
-- FROM staging.purchases AS p
FROM current_batch_purchases AS p
-- Now on veut le client qui a fait lacaht
-- L'id de souscription se trouve dans l'achat donc on fait une jointure avec la souscription pour avoir l'id du customer ayant fait lachat
JOIN staging.subscriptions AS s ON s.id = p.subscription_id -- Seulement les achats dont lid de la souscription est dans les souscritions
JOIN dw.dim_customer AS dc ON dc.customer_id = s.customer_id -- JOIN avec dim customer pour avoir la version de client qui a fait lacha; seulemt es souscriptions de custmer id exitant dans dimcustomer
                            AND dc.valid_from <= p.purchased_at  -- Choisir la version de cleint ayant fait lachat, ie celle valide au moment ou lachat a ete effectue
                            AND dc.valid_to > p.purchased_at
JOIN dw.dim_offer AS dof ON dof.offer_config_id = p.offer_config_id -- Seulemt les achats de config ud existant dans dimoffer
)
SELECT purchase_id, TO_CHAR(purchased_at, 'YYYYMMDD')::INT AS date_key, customer_key, offer_config_id, revenue FROM x;


-- Fact consumption
-- SELECT * FROM current_batch_services_usage;
INSERT INTO dw.fact_consumption(purchase_id, date_key, customer_key, offer_config_id, call_duration_seconds, sms_sent_count, data_used_mb)
WITH service_usage_deduplicated AS (
-- SELECT * FROM staging.services_usage AS su
SELECT * FROM current_batch_services_usage AS su
WHERE NOT EXISTS(
    SELECT 1 FROM data_quality.issues AS dqi WHERE table_name = 'services_usage'
                                             AND issue_type = 'Uniqueness'
                                             AND dqi.batch_id = su.batch_id
                                             AND dqi.record_id = su.id

                )
),
service_usage AS (
SELECT purchase_id, subscription_id,  timestamp::DATE AS usage_date, call_seconds, sms_count, data_mb FROM service_usage_deduplicated
),
service_usage_aggregated_ranked AS (
SELECT purchase_id, usage_date, subscription_id,
SUM(call_seconds) OVER(w) AS call_duration_seconds,
SUM(sms_count) OVER(w) AS sms_sent_count,
SUM(data_mb) OVER(w) AS data_used_mb,
ROW_NUMBER() OVER (w) AS rn
FROM service_usage
WINDOW w AS (PARTITION BY purchase_id, usage_date)      
),
service_usage_aggregated AS (
SELECT purchase_id, usage_date, subscription_id,  call_duration_seconds, sms_sent_count, data_used_mb
FROM service_usage_aggregated_ranked WHERE rn = 1
),
service_usage_aggregated_enriched AS(
SELECT purchase_id, usage_date, offer_config_id, customer_key, call_duration_seconds, sms_sent_count, data_used_mb
FROM service_usage_aggregated AS su
JOIN staging.purchases AS p ON p.id = su.purchase_id -- Pour avoir le offer config id
-- !!! Later : code pour eviter qu'un achat deja existant se charge plusieurs fois sinon la ligne precedente pose probleme dans le cas ou un ameme chat est charge plusieurs fois dans le staging: dans un tel cas toutes les lignes de cet achat seront joint
JOIN staging.subscriptions AS s ON s.id = su.subscription_id -- Pour avoir le customer id
JOIN dw.dim_customer AS dc ON dc.customer_id = s.customer_id -- Pour avoir la version de client ayant consommé le service
                            AND dc.valid_from <= usage_date
                            AND dc.valid_to > usage_date
),
service_consumption AS(
SELECT purchase_id,
TO_CHAR(usage_date, 'YYYYMMDD')::INT AS date_key,
customer_key,
offer_config_id,
COALESCE(call_duration_seconds, 0) AS call_duration_seconds, -- Use COALESCE to handle cases there is no use of a specific service for the aggregation (which result in NULL value)
COALESCE(sms_sent_count, 0) AS sms_sent_count,
COALESCE(data_used_mb, 0.0) AS data_used_mb
FROM service_usage_aggregated_enriched
)
SELECT * FROM service_consumption
ON CONFLICT (purchase_id, date_key)
DO UPDATE SET call_duration_seconds = dw.fact_consumption.call_duration_seconds + EXCLUDED.call_duration_seconds,
              sms_sent_count = dw.fact_consumption.sms_sent_count + EXCLUDED.sms_sent_count,
              data_used_mb = dw.fact_consumption.data_used_mb + EXCLUDED.data_used_mb;


