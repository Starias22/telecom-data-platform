\ir 01_create_schemas.sql
\ir 02_create_ref_tables.sql
\ir 03_populate_ref_tables.sql
\ir 04_create_pipeline_metadata_tables.sql
\ir 05_initialize_watermark.sql
\ir 06_create_staging_tables.sql
\ir 07_create_dq_tables.sql
\ir 08_create_dw_tables.sql
\ir 09_set_platform_state.sql


\dn;
\dt ref.*;
\dt pipeline_metadata.*;
\dt staging.*
\dt data_quality.*;
\dt dw.*;