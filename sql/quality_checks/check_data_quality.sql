-- !!! Cest auoi lq difference entre chqrlength et length
-- !!!avoid duplicates ... batch
-- !!! Suquery vs JOIN  quand faire quoi

SELECT CONCAT('Data quality check for batch ', :'batch_id');

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


/*Table offers*/
UPDATE current_batch_offers SET name = INITCAP(TRIM(name)),
type = UPPER((TRIM(type)));

/*Table billings (N/A)*/

/*Table offer configurations (N/A)*/

/*Table customers*/
UPDATE current_batch_customers
SET customer_type = UPPER(TRIM(customer_type)),
gender = UPPER(TRIM(gender)),
status = UPPER(TRIM(status)),
customer_segment = UPPER(TRIM(customer_segment)),
city = INITCAP(TRIM(CITY));

/*Table subscriptions*/
UPDATE current_batch_subscriptions
SET phone_number = REGEXP_REPLACE(phone_number, '((\+)?229)?(01)?', ''); -- Revove prefixes such as +229, 229, 01, ...

/*Table purchases*/
UPDATE current_batch_purchases
SET purchase_channel = UPPER(TRIM(purchase_channel)),
payment_method = UPPER(TRIM(payment_method));



/*Table: offers*/
WITH offers_count_by_name AS (
SELECT batch_id, id, COUNT(*) OVER(PARTITION BY name) AS offers_count, ROW_NUMBER() OVER(PARTITION BY name) AS rn  FROM current_batch_offers
) -- Et voila un exemple vivant de lutilite des window functions, on ne peut pas sen passer ici
INSERT INTO data_quality.issues (batch_id, table_name, column_name, record_id, issue_type, issue_code, issue_description)
-- Completness
SELECT batch_id,  'offers', 'start_date', id, 'Completness', 'OFFER_START_DATE_NULL', 'The start date of the offer is NULL' FROM current_batch_offers WHERE start_date IS NULL UNION ALL
SELECT batch_id,  'offers', 'created_at', id, 'Completness', 'OFFER_CREATED_AT_NULL', 'The creation date of the offer is NULL' FROM current_batch_offers WHERE created_at IS NULL UNION ALL
-- Validity
SELECT batch_id,  'offers', 'type', id, 'Validity', 'OFFER_TYPE_INVALID', 'The type of offer is invalid' FROM current_batch_offers WHERE UPPER(type) NOT IN('DATA', 'MOBILE', 'BUNDLE') UNION ALL
SELECT batch_id,  'offers', 'price_xof', id, 'Validity', 'OFFER_PRICE_INVALID', 'The price of the offer is invalid' FROM current_batch_offers WHERE price_xof < 0 UNION ALL
-- Uniqueness
SELECT batch_id,  'offers', NULL, id, 'Uniqueness', 'OFFER_NAME_DUPLICATED', CONCAT('The name of the offer is duplicated (', offers_count,' records)') FROM offers_count_by_name WHERE rn > 1 UNION ALL -- Keep the first row and reject all the others
-- Consistency(cohérence)
SELECT batch_id,  'offers', NULL, id, 'Consistency', 'OFFER_AVAILABILITY_DATES_INCOHERENT', 'The end date of the offer is prior to its start date' FROM current_batch_offers WHERE start_date > end_date UNION ALL
SELECT batch_id,  'offers', NULL, id, 'Consistency', 'OFFER_TRACK_DATES_INCOHERENT', 'The date of last update of the data is prior to the date of creation' FROM current_batch_offers WHERE updated_at < created_at;


/*Table: offer_billings*/
WITH offer_billings_count_by_params AS (
SELECT batch_id, id, COUNT(*) OVER(w) AS offer_billings_count, ROW_NUMBER() OVER(w) AS rn  FROM current_batch_offer_billings
WINDOW w AS (PARTITION BY xof_per_second, xof_per_sms, xof_per_mb)
)
INSERT INTO data_quality.issues (batch_id, table_name, column_name, record_id, issue_type, issue_code, issue_description)
-- Completness
SELECT batch_id,  'offer_billings', 'created_at', id, 'Completness', 'OFFER_BILLING_CREATED_AT_NULL', 'The creation date of the offer billing is NULL' FROM current_batch_offer_billings WHERE created_at IS NULL UNION ALL
-- Validity
SELECT batch_id,  'offer_billings', 'xof_per_second', id, 'Validity', 'OFFER_BILLING_PRICE_PER_SECOND_INVALID', 'The price per second of the offer billing is invalid' FROM current_batch_offer_billings WHERE xof_per_second < 0 UNION ALL
SELECT batch_id,  'offer_billings', 'xof_per_sms', id, 'Validity', 'OFFER_BILLING_PRICE_PER_SMS_INVALID', 'The price per SMS of the offer billing is invalid' FROM current_batch_offer_billings WHERE xof_per_sms < 0 UNION ALL
SELECT batch_id,  'offer_billings', 'xof_per_mb', id, 'Validity', 'OFFER_BILLING_PRICE_PER_MB_INVALID', 'The price per MB of the offer billing is invalid' FROM current_batch_offer_billings WHERE xof_per_mb < 0 UNION ALL
SELECT batch_id,  'offer_billings', NULL, id, 'Validity', 'ALL_BILLING_PARAMS_NULL', 'Both billing price per MB, seonds and SMS are NULL' FROM current_batch_offer_billings WHERE xof_per_mb IS NULL AND xof_per_second IS NULL AND xof_per_sms IS NULL UNION ALL
-- Uniqueness
SELECT batch_id,  'offer_billings', NULL, id, 'Uniqueness', 'OFFER_BILLING_DUPLICATED', CONCAT('The offer billing is duplicated (', offer_billings_count,' records)') FROM offer_billings_count_by_params WHERE rn > 1 UNION ALL -- Keep the first row and reject all the others
-- Consistency(cohérence)
SELECT batch_id,  'offer_billings', NULL, id, 'Consistency', 'OFFER_BILLING_TRACK_DATES_INCOHERENT', 'The date of last update of the data is prior to the date of creation' FROM current_batch_offer_billings WHERE updated_at < created_at;



/*Table: offer_configurations*/
INSERT INTO data_quality.issues (batch_id, table_name, column_name, record_id, issue_type, issue_code, issue_description)
-- Completness
SELECT batch_id,  'offer_configurations', 'created_at', id, 'Completness', 'OFFER_CONFIG_CREATED_AT_NULL', 'The creation date of the offer configuration is NULL' FROM current_batch_offer_configurations WHERE created_at IS NULL UNION ALL
-- Validity
SELECT batch_id,  'offer_configurations', 'value_xof', id, 'Validity', 'OFFER_CONFIG_VALUE_XOF_INVALID', 'The benefice value of the configured offer is invalid' FROM current_batch_offer_configurations WHERE value_xof < 0 UNION ALL
SELECT batch_id,  'offer_configurations', 'value_mb', id, 'Validity', 'OFFER_CONFIG_VALUE_MB_INVALID', 'The MB value of the configured offer is invalid' FROM current_batch_offer_configurations WHERE value_mb < 0 UNION ALL
SELECT batch_id,  'offer_configurations', 'validity_days', id, 'Validity', 'OFFER_CONFIG_VALIDITY_DAYS_INVALID', 'The validity days of the configured offer is invalid' FROM current_batch_offer_configurations WHERE validity_days <= 0 UNION ALL
-- Uniqueness
-- Consistency(cohérence)
SELECT batch_id,  'offer_configurations', NULL, id, 'Consistency', 'OFFER_CONFIG_AVAILABILITY_DATES_INCOHERENT', 'The end date of the configured offer is prior to its start date' FROM current_batch_offer_configurations WHERE start_date > end_date UNION ALL
SELECT batch_id,  'offer_configurations', NULL, id, 'Consistency', 'OFFER_CONFIG_TRACK_DATES_INCOHERENT', 'The date of last update of the configured offer is prior to its date of creation' FROM current_batch_offer_configurations WHERE updated_at < created_at UNION ALL
-- Referential Integrity
-- Cest quoi la meilleure approche pour ceci? EXISTS ou bien LEFT JOIN? Bien maitriser aussi laproche LEFT JOIn et ausi les ani semi join
SELECT batch_id,  'offer_configurations', 'offer_id', id, 'Referential Integrity', 'OFFER_ID_NOT_IN_OFFERS_TABLE', 'The offer id of the configured offer is not available in the offers table' FROM current_batch_offer_configurations AS oc WHERE NOT EXISTS(SELECT 1 FROM staging.offers AS o WHERE  o.id = oc.offer_id) UNION ALL
SELECT batch_id,  'offer_configurations', 'offer_id', id, 'Referential Integrity', 'OFFER_BILLING_ID_NOT_IN_OFFER_BILLINGS_TABLE', 'The offer billing id of the configured offer is not available in the offer billings table' FROM current_batch_offer_configurations AS oc WHERE billing_id IS NOT NULL AND NOT EXISTS(SELECT 1 FROM staging.offer_billings AS ob WHERE  ob.id = oc.billing_id);


/*Table: customers : Customer city invalid(typo), customer segment NULL*/
INSERT INTO data_quality.issues (batch_id, table_name, column_name, record_id, issue_type, issue_code, issue_description)
-- Completness
SELECT batch_id,  'customers', 'city', id, 'Completness', 'CUSTOMER_CITY_NULL', 'The city of the customer is NULL' FROM current_batch_customers WHERE city IS NULL UNION ALL
SELECT batch_id,  'customers', 'customer_type', id, 'Completness', 'CUSTOMER_TYPE_NULL', 'The type of customer is NULL' FROM current_batch_customers WHERE customer_type IS NULL UNION ALL
SELECT batch_id,  'customers', 'customer_segment', id, 'Completness', 'CUSTOMER_SEGMENT_NULL', 'The segment of the customer is NULL' FROM current_batch_customers WHERE customer_segment IS NULL UNION ALL
SELECT batch_id,  'customers', 'birthdate', id, 'Completness', 'CUSTOMER_BIRTHDATE_NULL', 'The birthdate of the customer is NULL' FROM staging.customers WHERE birthdate IS NULL UNION ALL
SELECT batch_id,  'customers', 'registration_date', id, 'Completness', 'CUSTOMER_REG_DATE_NULL', 'The registration date of the customer is NULL' FROM current_batch_customers WHERE registration_date IS NULL UNION ALL
SELECT batch_id,  'customers', 'status', id, 'Completness', 'CUSTOMER_STATUS_NULL', 'The status of the customer is NULL' FROM current_batch_customers WHERE status IS NULL UNION ALL
SELECT batch_id,  'customers', 'created_at', id, 'Completness', 'CUSTOMER_CREATED_AT_NULL', 'The registration date of the customer is NULL' FROM current_batch_customers WHERE registration_date IS NULL UNION ALL
-- Validity
SELECT batch_id,  'customers', 'city', id, 'Validity', 'CUSTOMER_CITY_INVALID', 'The city of the customer is invalid (may be typo)' FROM current_batch_customers WHERE city NOT IN (SELECT city FROM ref.cities) UNION ALL -- !!!
SELECT batch_id,  'customers', 'customer_type', id, 'Validity', 'CUSTOMER_TYPE_INVALID', 'The type of the customer is invalid' FROM current_batch_customers WHERE customer_type NOT IN('INDIVIDUAL', 'BUSINESS') UNION ALL
SELECT batch_id,  'customers', 'gender', id, 'Validity', 'CUSTOMER_GENDER_INVALID', 'The gender of the customer is invalid' FROM current_batch_customers WHERE gender IS NOT NULL AND gender NOT IN('M', 'F') UNION ALL
SELECT batch_id,  'customers', 'customer_segment', id, 'Validity', 'CUSTOMER_SEGMENT_INVALID', 'The segment of the customer is invalid' FROM current_batch_customers WHERE customer_segment NOT IN('YOUTH', 'STANDARD', 'SME', 'PREMIUM') UNION ALL

SELECT batch_id,  'customers', 'status', id, 'Validity', 'CUSTOMER_STATUS_INVALID', 'The status of the customer is invalid' FROM current_batch_customers WHERE status NOT IN('ACTIVE', 'INACTIVE', 'SUSPENDED', 'TERMINATED') UNION ALL
-- Uniqueness (Not Applied here cause we have no personal identification info of the customers)
-- Consistency(cohérence)
SELECT batch_id,  'customers', NULL, id, 'Consistency', 'INDIVIDUAL_WITHOUT_GENDER', 'An individual customer without gender' FROM current_batch_customers WHERE customer_type = 'INDIVIDUAL' AND gender IS NULL UNION ALL -- !!!Completness or consistency?
SELECT batch_id,  'customers', NULL, id, 'Consistency', 'CUSTOMER_INCOHERENT_WITH_SEGMENT', 'A customer with inconsistent(customer_type, customer_gender)' FROM current_batch_customers WHERE (customer_type = 'INDIVIDUAL' AND customer_segment IS NOT NULL AND customer_segment NOT  IN ('STANDARD', 'YOUTH', 'PREMIUM')) OR (customer_type = 'BUSINESS' AND customer_segment NOT IN ('SME', 'PREMIUM')) UNION ALL
SELECT batch_id,  'customers', NULL, id, 'Consistency', 'NON_TERMINATED_CUSTOMER_WITH_TERMINATION_DATE', 'A non-terminated customer with termination date' FROM current_batch_customers WHERE status <> 'TERMINATED' AND termination_date IS NOT NULL UNION ALL
SELECT batch_id,  'customers', NULL, id, 'Consistency', 'CUSTOMER_BIRTH_AND_REG_DATE_INCOHERENT', 'A customer with registration date prior to birthdate' FROM current_batch_customers WHERE registration_date < birthdate UNION ALL
SELECT batch_id,  'customers', NULL, id, 'Consistency', 'CUSTOMER_REG_AND_TERMINATION_DATES_INCOHERENT', 'A customer with termination date date prior to registration date' FROM current_batch_customers WHERE termination_date < registration_date UNION ALL
SELECT batch_id,  'customers', NULL, id, 'Consistency', 'CUSTOMER_TRACK_DATES_INCOHERENT', 'The date of last update of the customer is prior to his registration date' FROM current_batch_customers WHERE updated_at < registration_date;


/*Table: Subscriptions*/
-- Later update the generator to support the case a customer that onnce used a phone number thta is beeing used by another
WITH subscriptions_count_by_phone_number_and_customer AS (
SELECT batch_id, id, COUNT(*) OVER() AS subscriptions_count, ROW_NUMBER() OVER(w) AS rn  FROM current_batch_subscriptions
WINDOW w AS (PARTITION BY phone_number, customer_id)
)
INSERT INTO data_quality.issues (batch_id, table_name, column_name, record_id, issue_type, issue_code, issue_description)
-- Completness
SELECT batch_id,  'subscriptions', 'phone_number', id, 'Completness', 'SUBSCRIPTION_WITHOUT_PHONE_NUMBER', 'The phone number of the subscription is NULL' FROM current_batch_subscriptions WHERE phone_number IS NULL UNION ALL
SELECT batch_id,  'subscriptions', 'customer_id', id, 'Completness', 'SUBSCRIPTION_WITHOUT_CUSTOMER', 'The customer id of the subscripton is NULL' FROM current_batch_subscriptions WHERE customer_id IS NULL UNION ALL
SELECT batch_id,  'subscriptions', 'registration_date', id, 'Completness', 'SUBSCRIPTION_WITHOUT_REG_DATE', 'The registration date of the subscription is NULL' FROM current_batch_subscriptions WHERE registration_date IS NULL UNION ALL
SELECT batch_id,  'subscriptions', 'status', id, 'Completness', 'SUBSCRIPTION_WITHOUT_STATUS', 'The status of the subscription is NULL' FROM current_batch_subscriptions WHERE status IS NULL UNION ALL
-- Validity
SELECT batch_id,  'subscriptions', 'phone_number', id, 'Validity', 'SUBSCRIPTION_PHONE_NUMBER_INVALID', 'The phone number of the subscription is invalid' FROM current_batch_subscriptions WHERE LENGTH(phone_number) <> 8 OR LEFT(phone_number,2) NOT IN ('30', '32', '34', '36', '38', '70', '72', '74') UNION ALL
SELECT batch_id,  'subscriptions', 'status', id, 'Validity', 'SUBSCRIPTION_STATUS_INVALID', 'The status of the subscription is invalid' FROM current_batch_subscriptions WHERE status NOT IN('ACTIVE', 'INACTIVE', 'SUSPENDED', 'TERMINATED') UNION ALL
-- Uniqueness (Not Applied here cause we have no personal identification info of the customers)
SELECT batch_id,  'subscriptions', NULL, id, 'Uniqueness', 'SUBSCRIPTION_DUPLICATED', CONCAT('The subscription is duplicated (', subscriptions_count,' records)')  FROM subscriptions_count_by_phone_number_and_customer WHERE rn > 1 UNION ALL
-- Consistency(cohérence)
SELECT batch_id,  'subscriptions', NULL, id, 'Consistency', 'NON_TERMINATED_SUBSCRIPTION_WITH_TERMINATION_DATE', 'A non-terminated subscription with termination date' FROM current_batch_subscriptions WHERE status <> 'TERMINATED' AND termination_date IS NOT NULL UNION ALL
SELECT batch_id,  'subscriptions', NULL, id, 'Consistency', 'SUBSCRIPTION_REG_AND_TERMINATION_DATES_INCOHERENT', 'A subscription with termination date prior to registration date' FROM current_batch_subscriptions WHERE termination_date < registration_date UNION ALL
SELECT batch_id,  'subscriptions', NULL, id, 'Consistency', 'SUBSCRIPTION_TRACK_DATES_INCOHERENT', 'The date of last update of the subscription is prior to its registration date' FROM current_batch_subscriptions WHERE updated_at < registration_date UNION ALL
-- Referential Integrity
-- Cest quoi la meilleure approche pour ceci? EXISTS ou bien LEFT JOIN? Bien maitriser aussi laproche LEFT JOIn et ausi les ani semi join
SELECT batch_id,  'subscriptions', 'customer_id', id, 'Referential Integrity', 'CUSTOMER_ID_NOT_IN_CUSTOMERS_TABLE', 'The customer id is not available in customers table' FROM current_batch_subscriptions AS s WHERE NOT EXISTS(SELECT 1 FROM staging.customers AS c WHERE  c.id = s.customer_id);


/*Table: Purchases*/
INSERT INTO data_quality.issues (batch_id, table_name, column_name, record_id, issue_type, issue_code, issue_description)
-- Completness
SELECT batch_id,  'purchases', 'subscription_id', id, 'Completness', 'PURCHASE_WITHOUT_SUBSCRIPTION', 'The subscription id of the purchase is NULL' FROM current_batch_purchases WHERE subscription_id IS NULL UNION ALL
SELECT batch_id,  'purchases', 'offer_config_id', id, 'Completness', 'PURCHASE_WITHOUT_OFFER_CONFIG', 'The  offer config id of the purchase is NULL' FROM current_batch_purchases WHERE offer_config_id IS NULL UNION ALL
SELECT batch_id,  'purchases', 'purchased_at', id, 'Completness', 'PURCHASE_WITHOUT_PURCHASE_DATE', 'The date of the purchase is NULL' FROM current_batch_purchases WHERE purchased_at IS NULL UNION ALL
SELECT batch_id,  'purchases', 'purchase_channel', id, 'Completness', 'PURCHASE_WITHOUT_CHANNEL', 'The channel used for the purchase is NULL' FROM current_batch_purchases WHERE purchase_channel IS NULL UNION ALL
SELECT batch_id,  'purchases', 'payment_method', id, 'Completness', 'PURCHASE_WITHOUT_PAYMENT_METHOD', 'The payment method used for the purchase is NULL' FROM current_batch_purchases WHERE payment_method IS NULL UNION ALL
-- Validity
SELECT batch_id,  'purchases', 'purchase_channel', id, 'Validity', 'PURCHASE_CHANNEL_INVALID', 'The purchase channel is invalid' FROM current_batch_purchases WHERE purchase_channel NOT IN('USSD', 'MOBILE_APP', 'DEALER', 'WEB') UNION ALL
SELECT batch_id,  'purchases', 'payment_method', id, 'Validity', 'PURCHASE_PAYMENT_METHOD_INVALID', 'The payment method of the purchase is invalid' FROM current_batch_purchases WHERE payment_method NOT IN('MOBILE_MONEY', 'AIRTIME') UNION ALL
-- Uniqueness (Not Applied here cause we have no personal identification info of the customers that did the purchase) [!!!Reqlly?]
-- Consistency(cohérence)
SELECT p.batch_id,  'purchases', NULL, p.id, 'Consistency', 'PURCHASE_AND_SUB_REG_DATE_INCOHERENT', 'A purchase with date prior to the registration date of the corresponding subscription' FROM current_batch_purchases AS p JOIN staging.subscriptions AS s ON s.id = p.subscription_id WHERE p.purchased_at < s.registration_date UNION ALL
SELECT p.batch_id,  'purchases', NULL, p.id, 'Consistency', 'PURCHASED_ON_TERMINATED_SUB', 'A purchase made on a subscription which is already terminated' FROM current_batch_purchases AS p JOIN staging.subscriptions AS s ON s.id = p.subscription_id WHERE p.purchased_at > s.termination_date UNION ALL
SELECT p.batch_id,  'purchases', NULL, p.id, 'Consistency', 'PURCHASED_NON_EXISTING_YET_OFFER_CONFIG', 'A purchase of an offer configuration which does not exist yet' FROM current_batch_purchases AS p JOIN staging.offer_configurations AS oc ON oc.id = p.offer_config_id WHERE p.purchased_at < oc.start_date UNION ALL
SELECT p.batch_id,  'purchases', NULL, p.id, 'Consistency', 'PURCHASED_NON_EXISTING_ANYMORE_OFFER_CONFIG', 'A purchase of an offer configuration which does not exist anymore' FROM current_batch_purchases AS p JOIN staging.offer_configurations AS oc ON oc.id = p.offer_config_id WHERE p.purchased_at > oc.end_date UNION ALL
-- Referential Integrity
-- Cest quoi la meilleure approche pour ceci? EXISTS ou bien LEFT JOIN? Bien maitriser aussi laproche LEFT JOIn et ausi les ani semi join
SELECT batch_id,  'purchases', 'subscription_id', id, 'Referential Integrity', 'SUBSCRIPTION_ID_NOT_IN_SUBSCRIPTIONS_TABLE', 'The subscriptionid is not available in subscriptions table' FROM current_batch_purchases AS p WHERE NOT EXISTS(SELECT 1 FROM staging.subscriptions AS s WHERE  s.id = p.subscription_id) UNION ALL
SELECT batch_id,  'purchases', 'offer_config_id', id, 'Referential Integrity', 'OFFER_CONFIG_ID_NOT_IN__TABLE', 'The subscriptionid is not available in subscriptions table' FROM current_batch_purchases AS p WHERE NOT EXISTS(SELECT 1 FROM staging.subscriptions AS s WHERE  s.id = p.subscription_id);


/*Table: services_usage*/
WITH service_usage_count AS (
SELECT batch_id, id, COUNT(*) OVER(w) AS duplicated_rows_count, ROW_NUMBER() OVER(w) AS duplicated_row_number FROM current_batch_services_usage AS su
-- WINDOW w AS (PARTITION BY purchase_id, subscription_id, timestamp, service_type)
WINDOW w AS (PARTITION BY purchase_id, subscription_id, timestamp, service_type)
)
INSERT INTO data_quality.issues (batch_id, table_name, column_name, record_id, issue_type, issue_code, issue_description)
-- Completness
SELECT batch_id,  'services_usage', 'purchase_id', id, 'Completness', 'SERVICE_USAGE_WITHOUT_PURCHASE', 'The purchase of offer used for the service is NULL' FROM current_batch_services_usage WHERE purchase_id IS NULL UNION ALL
SELECT batch_id,  'services_usage', 'subscription_id', id, 'Completness', 'SERVICE_USAGE_WITHOUT_SUBSCRIPTION', 'The id of the subscription that used the service is NULL' FROM current_batch_services_usage WHERE subscription_id IS NULL UNION ALL
SELECT batch_id,  'services_usage', 'timestamp', id, 'Completness', 'SERVICE_USAGE_WITHOUT_USAGE_DATE', 'The date of usage of the service is NULL' FROM current_batch_services_usage WHERE timestamp IS NULL UNION ALL
SELECT batch_id,  'services_usage', 'service_type', id, 'Completness', 'SERVICE_USAGE_WITHOUT_SERVICE_TYPE', 'The type of the service used is NULL' FROM current_batch_services_usage WHERE service_type IS NULL UNION ALL
-- Validity
SELECT batch_id,  'services_usage', 'service_type', id, 'Validity', 'SERVICE_TYPE_INVALID', 'The type of service is invalid' FROM current_batch_services_usage WHERE service_type NOT IN('DATA', 'CALL', 'SMS') UNION ALL
SELECT batch_id,  'services_usage', 'data_mb', id, 'Validity', 'SERVICE_USAGE_DATA_MB_INVALID', 'The quantity of MB used is invalid' FROM current_batch_services_usage WHERE data_mb < 0 UNION ALL
SELECT batch_id,  'services_usage', 'call_seconds', id, 'Validity', 'SERVICE_USAGE_CALL_SECONDS_INVALID', 'The duration of call in seconds is invalid' FROM current_batch_services_usage WHERE call_seconds < 0 UNION ALL
SELECT batch_id,  'services_usage', 'sms_count', id, 'Validity', 'SERVICE_USAGE_SMS_COUNT_INVALID', 'The number of SMS sent is invalid' FROM current_batch_services_usage WHERE sms_count < 0 UNION ALL
SELECT batch_id,  'services_usage', NULL, id, 'Validity', 'SERVICE_USAGE_INVALID', 'Both service usage parameters (data_mb, call_seconds, sms_count) are NULL' FROM current_batch_services_usage WHERE data_mb IS NULL AND call_seconds IS NULL AND sms_count IS NULL UNION ALL
-- Uniqueness (On ne peut pas avoir deux enregistrements d'utlisation de service de communication téléphonique pour un meme achat dune meme souscription a une meme heur et pour un meme service)
SELECT batch_id,  'services_usage', NULL, id, 'Uniqueness', 'DUPLICATE_SERVICE_USAGE_RECORD', CONCAT('Multiple records for the same service usage event (', duplicated_rows_count, ' records)') FROM service_usage_count WHERE duplicated_rows_count > 1 UNION ALL -- Keep the first row and reject all the others
-- Consistency(cohérence)
SELECT su.batch_id,  'services_usage', NULL, p.id, 'Consistency', 'SERVICE_USAGE_DATE_ AND_PURCHASE_DATE_INCOHERENT', 'A service used before its offer has been purchased' FROM current_batch_services_usage AS su JOIN staging.purchases AS p ON p.id = su.purchase_id WHERE  su.timestamp < p.purchased_at  UNION ALL
SELECT su.batch_id,  'services_usage', NULL, su.id, 'Consistency', 'SERVICE_USAGE_DATE_AND_TERMINATION_DATE_INCOHERENT', 'A service used after the corresponding subscription has been terminated' FROM current_batch_services_usage AS su JOIN staging.subscriptions AS s ON s.id = su.subscription_id WHERE  su.timestamp > s.termination_date  UNION ALL
-- Referential Integrity
-- Cest quoi la meilleure approche pour ceci? EXISTS ou bien LEFT JOIN? Bien maitriser aussi laproche LEFT JOIn et ausi les ani semi join
SELECT batch_id,  'services_usage', 'purchase_id', id, 'Referential Integrity', 'PURCHASE_ID_NOT_IN_SUBSCRIPTIONS_TABLE', 'The purchase id is not available in subscriptions table' FROM current_batch_services_usage AS su WHERE NOT EXISTS(SELECT 1 FROM staging.subscriptions AS s WHERE  s.id = su.subscription_id) UNION ALL
SELECT batch_id,  'services_usage', 'subscription_id', id, 'Referential Integrity', 'SUBSCRIPTION_ID_NOT_IN_SUBSCRIPTIONS_TABLE', 'The subscription id is not available in subscriptions table' FROM current_batch_services_usage AS su WHERE NOT EXISTS(SELECT 1 FROM staging.subscriptions AS s WHERE  s.id = su.subscription_id);

-- Summarize data quality issues
SELECT DISTINCT issue_type, issue_code FROM data_quality.issues;

-- !!!Queries to calculte count and statistics for each type/code of issue (the number of rows concerned)



