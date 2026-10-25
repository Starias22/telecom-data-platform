\ir 01_create_schemas.sql
\ir 02_create_ref_tables.sql
\ir 03_populate_ref_tables.sql
\ir 04_create_pipeline_metadata_tables.sql
\ir 05_create_staging_tables.sql
\ir 06_create_dq_tables.sql
\ir 07_create_dw_tables.sql


\dn;
\dt ref.*;
\dt pipeline_metadata.*;
\dt staging.*
\dt data_quality.*;
\dt dw.*;

-- \ir 07_check_data_quality.sql
-- \ir 08_initial_load.sql
