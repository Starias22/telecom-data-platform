CREATE TABLE IF NOT EXISTS dw.dim_date(
        date_key INT PRIMARY KEY,     
        full_date DATE NOT NULL,
        formatted_date VARCHAR(10) NOT NULL,
        day_of_week_num SMALLINT NOT NULL,
        day_of_week_name VARCHAR(10)NOT NULL,
        day_of_week_name_short VARCHAR(3) NOT NULL,
        day_of_month SMALLINT NOT NULL,
        day_of_year INT NOT NULL,
        month_num SMALLINT NOT NULL,
        month_name VARCHAR(10) NOT NULL,
        month_name_short VARCHAR(3) NOT NULL,
        quarter_num SMALLINT NOT NULL,
        quarter_name VARCHAR(10) NOT NULL,
        quarter_name_short VARCHAR(3) NOT NULL,
        year INT NOT NULL
);

CREATE TABLE IF NOT EXISTS dw.dim_offer(
        offer_config_id INT PRIMARY KEY,    
        offer_id INT NOT NULL, -- not nessasary anymore?
        offer_name VARCHAR(50) NOT NULL,
        offer_type VARCHAR(10) NOT NULL,
        offer_category VARCHAR(10) NOT NULL,
        validity_days SMALLINT,
        is_limitless BOOLEAN,
        price_xof INT CHECK(price_xof >= 0),
        value_xof INT  CHECK(value_xof >= 0),
        value_mb NUMERIC CHECK(value_mb >= 0),
        xof_per_call_second NUMERIC CHECK(xof_per_call_second >= 0),
        xof_per_sms_sent NUMERIC CHECK(xof_per_sms_sent >= 0),
        xof_per_mb_used NUMERIC CHECK(xof_per_mb_used >= 0),
        offer_start_date TIMESTAMP,
        offer_end_date TIMESTAMP
);

CREATE TABLE IF NOT EXISTS dw.dim_customer(
        customer_key SERIAL PRIMARY KEY,   
        customer_id INT NOT NULL,
        customer_city VARCHAR(25) NOT NULL,
        customer_department VARCHAR(20) NOT NULL,
        customer_type VARCHAR(50) NOT NULL,
        customer_segment VARCHAR(50) NOT NULL,
        gender CHAR(1) CHECK (gender IN ('M', 'F')),
        registration_date DATE NOT NULL,
        status VARCHAR(10),
        termination_date TIMESTAMP,

        /*Track History (SCD Type 2)*/
        valid_from TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        valid_to TIMESTAMP DEFAULT '9999-12-31',
        is_current BOOLEAN
        );

CREATE TABLE IF NOT EXISTS dw.fact_purchase(
        purchase_id INT PRIMARY KEY, -- !!! Faut-il faire faire FK(purchase_id)  references staging.purchases(id)?
        date_key INT NOT NULL,
        customer_key INT NOT NULL,
        offer_config_id INT NOT NULL,
        revenue INT, -- !!! Comment gerer les revenus des offres comme offre par defaut et Navigation en option libre
        FOREIGN KEY(date_key) REFERENCES dw.dim_date(date_key),
        FOREIGN KEY(customer_key) REFERENCES dw.dim_customer(customer_key),
        FOREIGN KEY(offer_config_id) REFERENCES dw.dim_offer(offer_config_id)
);

CREATE TABLE IF NOT EXISTS dw.fact_consumption(
        consumption_key SERIAL PRIMARY KEY,
        purchase_id INT NOT NULL,
        date_key INT NOT NULL,
        customer_key INT NOT NULL,
        offer_config_id INT NOT NULL,
        call_duration_seconds INT NOT NULL,
        sms_sent_count INT NOT NULL,
        data_used_mb NUMERIC NOT NULL,
        UNIQUE(purchase_id, date_key),
        FOREIGN KEY(date_key) REFERENCES dw.dim_date(date_key),
        FOREIGN KEY(customer_key) REFERENCES dw.dim_customer(customer_key),
        FOREIGN KEY(offer_config_id) REFERENCES dw.dim_offer(offer_config_id),
        CHECK (COALESCE(call_duration_seconds, sms_sent_count, data_used_mb) IS NOT NULL) -- Service parameters should not be all null
);
