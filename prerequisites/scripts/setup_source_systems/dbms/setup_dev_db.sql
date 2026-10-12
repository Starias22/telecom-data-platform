-- Make a copy of the production database for development purpose
CREATE DATABASE ben_telecom_dev WITH TEMPLATE ben_telecom; -- PLus tard remplacer par pgdump et pgrestore car ca requiert quil ny ai aucune autre user connecte a la bdd (ce qui nest pas trop coll/pertient pour une base de donne production)

-- Create a role for data engineers
CREATE ROLE data_engineer;

-- Grant neccessary permissions on the test database to data engineers: connection, access of schemas, reading the tables
GRANT CONNECT ON DATABASE ben_telecom_dev TO data_engineer;

\c ben_telecom_dev

GRANT USAGE ON SCHEMA offers_catalog TO data_engineer;
GRANT USAGE ON SCHEMA crm TO data_engineer;
GRANT USAGE ON SCHEMA subscriptions TO data_engineer;

GRANT SELECT ON ALL TABLES IN SCHEMA offers_catalog TO data_engineer;
GRANT SELECT ON ALL TABLES IN SCHEMA crm TO data_engineer;
GRANT SELECT ON ALL TABLES IN SCHEMA subscriptions TO data_engineer;


CREATE USER starias22 WITH password 'my_password';
GRANT data_engineer TO starias22;

