import os
import subprocess

from config.config import HOST, USER, get_staging_params, DATA_PLATFORM_DB

from src.utils.logger import get_logger
from src.utils.psql_client import PsqlClient
from src.utils.utils import get_num_records
import pandas as pd

logger = get_logger(__name__)

def move_to_staging(staging_raw_data_dir):

        queries = []
        STAGING_PARAMS = get_staging_params(staging_raw_data_dir)
        tables_list = []
        
        
        for i in STAGING_PARAMS.values():
                table = i["table"]
                tables_list.append(table)
                file_path = i["file_path"]
                if not file_path.exists():
                        logger.warning(f"No data to move to {table}")
                        continue
                query = f"""\\copy {table} FROM {file_path} WITH (FORMAT CSV, HEADER TRUE)"""
        
                # !!!For prudcution environment think about COPY query keyword instead of \copy of psql
                # query = f"""copy ( SELECT * FROM {table} WHERE {insert_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}' OR {last_update_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}') To STDOUT WITH (FORMAT CSV, HEADER TRUE);"""

                queries.append(query)
       
        if len(queries) == 0:
                logger.warning("No data moved to staging cause no data extracted from any sources")
                return

        i = STAGING_PARAMS["services_usage"]
        table = i["table"]
        file_path = i["file_path"]
        if file_path.exists():
                temp_table = "tmp_service_usage"
                columns = "purchase_id, subscription_id, timestamp, service_type, data_mb, sms_count, call_seconds, message_partition, message_offset, batch_id"
                query = f"""
                BEGIN;
                CREATE TEMP TABLE {temp_table} AS SELECT {columns} FROM {table} WITH NO DATA ;
                \\copy {temp_table} FROM {file_path} WITH (FORMAT CSV, HEADER TRUE);
                INSERT INTO {table} ({columns}) SELECT * FROM {temp_table} ON CONFLICT (message_partition, message_offset) DO NOTHING;
                COMMIT;
                """
                queries[-1] = query # Replace last query

        query = "\n".join(queries)

        print(query)
        
        output = PsqlClient(
                       user=USER,
                       host=HOST,
                       db=DATA_PLATFORM_DB
               ).execute(
                       input=query
               )
        num_records = get_num_records(output) # Take just offers, billings, offer configs, customers, and subscriptions
        print(output)
        print(tables_list)
        print(num_records)

        num_records_df = pd.DataFrame({"Table":tables_list, "Num records moved": num_records})
        logger.info(f"\nReport of the data moved from Raw to Staging:\n {num_records_df.to_string(index=False)}\n {'-' * 100}")
        
        

# move_to_staging("/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/raw/2026-10-14")