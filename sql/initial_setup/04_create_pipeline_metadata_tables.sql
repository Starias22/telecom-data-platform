CREATE TABLE IF NOT EXISTS pipeline_metadata.batch_logs(
        batch_id SERIAL PRIMARY KEY, -- Bigint?
        started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
        finished_at TIMESTAMPTZ,
        status VARCHAR(10) CHECK (status IN ('RUNNING', 'SUCCESS','FAILED', 'INTERUPTED')),
        error_message TEXT

);

CREATE TABLE IF NOT EXISTS pipeline_metadata.watermark(
        -- source_name VARCHAR(20) PRIMARY KEY,
        last_successful_watermark TIMESTAMPTZ NOT NULL,
        updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP--!!! Normal?
);

CREATE TABLE IF NOT EXISTS pipeline_metadata.platform_state(
        id INT PRIMARY KEY DEFAULT 1,
        state VARCHAR(20) --,
        --completed_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);



/*-- Create a role for data engineers
CREATE ROLE data_engineer;

-- Grant neccessary permissions on the test database to data engineers: connection, access of schemas, reading the tables
GRANT CONNECT ON DATABASE ben_telecom TO data_engineer;

\c ben_telecom

GRANT USAGE ON SCHEMA offers_catalog TO data_engineer;
GRANT USAGE ON SCHEMA crm TO data_engineer;
GRANT USAGE ON SCHEMA subscriptions TO data_engineer;

GRANT SELECT ON ALL TABLES IN SCHEMA offers_catalog TO data_engineer;
GRANT SELECT ON ALL TABLES IN SCHEMA crm TO data_engineer;
GRANT SELECT ON ALL TABLES IN SCHEMA subscriptions TO data_engineer;


CREATE USER starias22 WITH password 'my_password';
GRANT data_engineer TO starias22;*/

-- Create a role for data engineers
/*CREATE ROLE data_engineer;

-- Grant neccessary permissions on the test database to data engineers: connection, access of schemas, reading the tables
GRANT CONNECT ON DATABASE ben_telecom_data_platform TO data_engineer;

\c ben_telecom_data_platform 

-- GRANT USAGE ON SCHEMA staging TO data_engineer;
GRANT INSERT ON ALL TABLES IN SCHEMA staging TO data_engineer;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA staging TO data_engineer;

GRANT USAGE ON SCHEMA pipeline_metadata TO data_engineer;
GRANT INSERT, SELECT, UPDATE ON TABLE pipeline_metadata.batch_logs TO data_engineer;
GRANT USAGE ON ALL SEQUENCES IN SCHEMA pipeline_metadata TO data_engineer;


TRUNCATE pipeline_metadata.batch_logs  RESTART IDENTITY;


CREATE USER starias22 WITH password 'my_password';
GRANT data_engineer TO starias22;



GRANT INSERT ON ALL TABLES IN SCHEMA data_quality TO data_engineer;*/