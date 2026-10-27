SET ROLE super_admin;

--SELECT 'DROP DATABASE ' || quote_ident(datname) FROM pg_database WHERE datname = 'ben_telecom_data_platform'
-- \gexec

CREATE DATABASE ben_telecom_data_platform;

\connect ben_telecom_data_platform;

CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS ref;
CREATE SCHEMA  IF NOT EXISTS data_quality;
CREATE SCHEMA IF NOT EXISTS dw;
CREATE SCHEMA IF NOT EXISTS pipeline_metadata;

