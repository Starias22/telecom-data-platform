\ir 01_create_schemas.sql
\ir 02_create_staging_tables.sql
\ir 03_create_dq_tables.sql
\ir 04_create_dw_tables.sql
\ir 05_create_pipeline_metadata_tables.sql

\dt staging.*
\dt data_quality.*;
\dt dw.*;
\dt pipeline_metadata.*;
