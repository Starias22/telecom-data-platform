-- !!!  Faut il assigner un  PK aux differentes tables du staging? (Je pense que non, quil faut ls laisser flexibles)
CREATE TABLE staging.offers(
        id INT,
        name TEXT,
        type TEXT,
        price_xof INT,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        batch_id INT NOT NULL,
        FOREIGN KEY(batch_id) REFERENCES pipeline_metadata.batch_logs(batch_id)
         -- source_system VARCHAR (si les donnees de la tabe proviennent de sources differentes) (pareille pour les autres tables de staging)

);

CREATE TABLE staging.offer_billings(
        id INT,
        xof_per_second NUMERIC,
        xof_per_sms NUMERIC,
        xof_per_mb NUMERIC,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        batch_id INT NOT NULL,
        FOREIGN KEY(batch_id) REFERENCES pipeline_metadata.batch_logs(batch_id)
);

CREATE TABLE staging.offer_configurations(
        id INT,
        offer_id INT NOT NULL,
        value_xof INT,
        value_mb NUMERIC,
        validity_days INT,
        billing_id INT,
        is_limitless BOOLEAN,
        start_date TIMESTAMP,
        end_date TIMESTAMP,
        created_at TIMESTAMP,
        updated_at TIMESTAMP,
        batch_id INT NOT NULL,
        FOREIGN KEY(batch_id) REFERENCES pipeline_metadata.batch_logs(batch_id)
);

CREATE TABLE staging.customers(
        id INT,
        city TEXT,
        customer_type TEXT,
        gender TEXT,
        customer_segment TEXT,
        birthdate DATE,
        registration_date TIMESTAMP,
        status TEXT,
        termination_date TIMESTAMP,
        updated_at TIMESTAMP,
        batch_id INT NOT NULL,
        FOREIGN KEY(batch_id) REFERENCES pipeline_metadata.batch_logs(batch_id)
);

CREATE TABLE staging.subscriptions(
        id INT,
        phone_number TEXT,
        customer_id INT,
        registration_date TIMESTAMP,
        status TEXT,
        termination_date TIMESTAMP,
        updated_at TIMESTAMP,
        batch_id INT NOT NULL,
        FOREIGN KEY(batch_id) REFERENCES pipeline_metadata.batch_logs(batch_id)
);

CREATE TABLE staging.purchases(
        id INT,
        subscription_id INT,
        offer_config_id INT,
        purchased_at TIMESTAMP,
        purchase_channel TEXT,
        payment_method TEXT,
        batch_id INT NOT NULL,
        FOREIGN KEY(batch_id) REFERENCES pipeline_metadata.batch_logs(batch_id)
);

CREATE TABLE staging.services_usage(
        id SERIAL PRIMARY KEY, -- possible to use (message_partition, message_offset) as PK? But i do this because I need to insert the id in the dataquality table
        purchase_id INT,
        subscription_id INT,
        timestamp TIMESTAMP,
        service_type TEXT,
        data_mb NUMERIC,
        sms_count INT,
        call_seconds INT,
        message_partition SMALLINT NOT NULL, -- !!!Chercher le type de int approprie: sammll int?bigint?
        message_offset INT NOT NULL, -- !!!Chercher le type de int approprie: sammll int?bigint?
        batch_id INT NOT NULL,
        UNIQUE(message_partition, message_offset),
        FOREIGN KEY(batch_id) REFERENCES pipeline_metadata.batch_logs(batch_id)
);