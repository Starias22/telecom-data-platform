
CREATE DATABASE ben_telecom;

\connect ben_telecom;

CREATE SCHEMA offers_catalog;
CREATE SCHEMA crm; -- Customer Reletion Management (CRM)
CREATE SCHEMA subscriptions;

CREATE TABLE offers_catalog.offers(
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL,
        type VARCHAR(10) NOT NULL CHECK (type IN('DATA', 'MOBILE', 'BUNDLE')),
        price_xof INT, -- Nullable
        start_date DATE,
        end_date DATE
);

CREATE TABLE offers_catalog.offer_billings(
        id SERIAL PRIMARY KEY,
        xof_per_second DECIMAL,
        xof_per_sms DECIMAL,
        xof_per_mb DECIMAL
);

CREATE TABLE offers_catalog.offer_configurations(
        id SERIAL PRIMARY KEY,
        offer_id INT NOT NULL,
        value_xof INT,
        value_mb DECIMAL,
        validity_days INT,
        billing_id INT, -- Nullable (Les forfaits internet n'ont pas de facturation)
        is_limitless boolean,
        start_date DATE,
        end_date DATE,
        FOREIGN KEY(offer_id) REFERENCES offers_catalog.offers(id),
        FOREIGN KEY(billing_id) REFERENCES offers_catalog.offer_billings(id)
);

CREATE TABLE crm.customers(
        id SERIAL PRIMARY KEY,
        city VARCHAR(50),
        customer_type VARCHAR(10),
        gender CHAR(1),
        customer_segment VARCHAR(10),
        birthdate DATE,
        registration_date DATE,
        status VARCHAR(10),
        termination_date DATE
);

CREATE TABLE subscriptions.subscriptions(
        id SERIAL PRIMARY KEY,
        phone_number VARCHAR(20),
        customer_id INT,
        registration_date DATE,
        status VARCHAR(10),
        termination_date DATE,
        FOREIGN KEY (customer_id) REFERENCES crm.customers(id)
);

\dt offers_catalog.*;
\dt crm.*;
\dt subscriptions.*;

\copy offers_catalog.offers
FROM '/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/offers_catalog/offers.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

\copy offers_catalog.offer_billings
FROM '/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/offers_catalog/offer_billings.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

\copy offers_catalog.offer_configurations
FROM '/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/offers_catalog/offer_configurations.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

\copy crm.customers
FROM '/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/customers.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

\copy subscriptions.subscriptions
FROM '/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/subscriptions.csv'
WITH (FORMAT CSV, HEADER TRUE, DELIMITER ',');

SELECT * FROM offers_catalog.offer_configurations;
SELECT * FROM crm.customers;
SELECT * FROM subscriptions.subscriptions;
