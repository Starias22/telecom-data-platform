SET ROLE super_admin;

SELECT 'DROP DATABASE ' || quote_ident(datname) FROM pg_database WHERE datname = 'ben_telecom_data_platform'
\gexec

CREATE DATABASE ben_telecom_data_platform;

\connect ben_telecom_data_platform;

CREATE SCHEMA staging;
CREATE SCHEMA  data_quality;
CREATE SCHEMA dw;
CREATE SCHEMA pipeline_metadata;

