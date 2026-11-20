SET ROLE super_admin;

--SELECT 'DROP DATABASE ' || quote_ident(datname) FROM pg_database WHERE datname = 'ben_telecom_data_platform'
-- \gexec

\echo '------------------------------------------------------------'
\echo 'Creating database (ben_telecom_data_platform)'
\ir 01_create_database.sql -- CREATE DATABASE cannot run inside a transaction block

BEGIN;

\echo '------------------------------------------------------------'
\echo 'Creating schemas(ref, pipeline_metadata, staging, data_quality, dw, analytics)'
\ir 02_create_schemas.sql

\echo '------------------------------------------------------------'
\echo 'Creating ref table (cities)'
\ir 03_create_ref_tables.sql


\echo '------------------------------------------------------------'
\echo 'Populating ref table (cities)'
\ir 04_populate_ref_tables.sql


\echo '------------------------------------------------------------'
\echo 'Creating pipeline metadata tables (batch_logs, watermark, platform_state)'
\ir 05_create_pipeline_metadata_tables.sql


\echo '------------------------------------------------------------'
\echo 'Initializing watermark'
\ir 06_initialize_watermark.sql


\echo '------------------------------------------------------------'
\echo 'Creating sataging tables'
\ir 07_create_staging_tables.sql


\echo '------------------------------------------------------------'
\echo 'Creating data quality table'
\ir 08_create_dq_tables.sql


\echo '------------------------------------------------------------'
\echo 'Creating data warehouse tables(dim_date, dim_offer, dim_customer, dim_subscription, fact_purchase, fact_consumption )'
\ir 09_create_dw_tables.sql


\echo '------------------------------------------------------------'
\echo 'Creating analytical objects (materialided views for offer purchase and consumption analysis, table for customer acitivity analysis)'
\ir 10_create_analytical_objects.sql

\echo '------------------------------------------------------------'
\echo 'Setting platform state (SETUP_COMPLETED)'
\ir 11_set_platform_state.sql


\echo '------------------------------------------------------------'

\dn;
\dt ref.*;
\dt pipeline_metadata.*;
\dt staging.*
\dt data_quality.*;
\dt dw.*;
\dt analytics.*;

COMMIT;
