-- To be runed in PostgreSQL admin account
CREATE ROLE super_admin WITH NOLOGIN SUPERUSER;
CREATE USER starias22 WITH PASSWORD 'my_password';
GRANT super_admin TO starias22;
CREATE DATABASE starias22 OWNER starias22;
