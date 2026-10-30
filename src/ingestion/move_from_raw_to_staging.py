import os
import subprocess

from config.config import HOST, USER, get_staging_params, DATA_PLATFORM_DB

def move_to_staging(staging_raw_data_dir):

        queries = []
        STAGING_PARAMS = get_staging_params(staging_raw_data_dir)
        
        
        for i in STAGING_PARAMS.values():
                table = i["table"]
                file_path = i["file_path"]
                if not file_path.exists():
                        print(f"No data to move to {table}")
                        continue
                query = f"""\\copy {table} FROM {file_path} WITH (FORMAT CSV, HEADER TRUE)"""
        
                # !!!For prudcution environment think about COPY query keyword instead of \copy of psql
                # query = f"""copy ( SELECT * FROM {table} WHERE {insert_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}' OR {last_update_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}') To STDOUT WITH (FORMAT CSV, HEADER TRUE);"""

                queries.append(query)
       
        if len(queries) == 0:
                print("No data moved to staging cause no data extracted from any sources")
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
                print(query)
                queries[-1] = query # Replace last query

        query = "\n".join(queries)
        # query = queries[-1]
        print(query)
        

        command = [
                "psql",
                "-U", USER,
                "-h", HOST,
                "-d", DATA_PLATFORM_DB,
        
        ]
        print(command)
        # exit()
        

        try:
               subprocess.run(command, input=query, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
                error_message = e.stderr
                print(error_message)
                raise RuntimeError(error_message) from e
        # !!!later :  ahndle errors and get th eouptut to ... the number of records extracted CompletedProcess(args=['psql', '-U', 'starias22', '-h', 'localhost', '-d', 'ben_telecom'], returncode=0, stdout='COPY 28\nCOPY 15\nCOPY 0\nCOPY 5000000\nCOPY 5928704\n', stderr='')
        # !!!Handle it so that the password wll not be prompted fro the command line


        return

# move_to_staging("/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/raw/2026-10-14")