from os import makedirs
from pathlib import Path
import subprocess
import duckdb
import json
from kafka import KafkaConsumer
import pandas as pd
from glob import glob
from config.paths import RAW_DATA_DIR, OFFER_BILLINGS_OUTPUT_FILE_NAME, OFFER_CONFIGS_OUTPUT_FILE_NAME, CURSTOMERS_OUTPUT_FILE_NAME, SUBSCRIPTIONS_OUTPUT_FILE_NAME, PURCHASES_DIR
from config.column_names import PURCHASE_ID_COL, SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL, SERVICE_TYPE_COL, DATA_MB_COL, SMS_COUNT_COL, CALL_SECONDS_COL, MESSAGE_PARTITION_COL, MESSAGE_OFFSET_COL, BATCH_ID_COL
from config.config import get_extraction_params, TRX_DB_NAME, HOST, USER, KAFKA_SERVERS, KAFKA_TOPIC, PASSDWORD


def extract_from_database(extraction_date, extraction_start_date, extraction_end_date, batch_id):        
        queries = []
        output_dir = Path(RAW_DATA_DIR) / extraction_date
        makedirs(output_dir, exist_ok=True)
        EXTRACTION_PARAMS = get_extraction_params(output_dir)
        # !!! uncomment it latermkdir(output_dir)

        
        for i in EXTRACTION_PARAMS.values():
                table = i["query_table"]
                insert_date = i["insert_date_col"]
                last_update_date = i["update_date_col"]
                output_path = i["output_path"]

                query = f"""\\copy ( SELECT *, {batch_id} AS batch_id FROM {table} WHERE {insert_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}' OR {last_update_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}') TO {output_path} WITH (FORMAT CSV, HEADER TRUE)"""
                # !!!For prudcution environment think about COPY query keyword instead of \copy of psql
                # query = f"""copy ( SELECT * FROM {table} WHERE {insert_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}' OR {last_update_date} BETWEEN '{extraction_start_date}' AND '{extraction_end_date}') To STDOUT WITH (FORMAT CSV, HEADER TRUE);"""

                queries.append(query)

        query = "\n".join(queries)
        print(query)
        # exit()

        command = [
                "psql",
                "-U", USER,
                "-h", HOST,
                "-d", TRX_DB_NAME

        ]

        result = subprocess.run(command, input=query, capture_output=True, text=True)
        # !!!later :  ahndle errors and get th eouptut to ... the number of records extracted CompletedProcess(args=['psql', '-U', 'starias22', '-h', 'localhost', '-d', 'ben_telecom'], returncode=0, stdout='COPY 28\nCOPY 15\nCOPY 0\nCOPY 5000000\nCOPY 5928704\n', stderr='')
        # !!!Handle it so that the password wll not be prompted fro the command line
        print(result)

        
        """command = [
                "psql",
                "-U", "starias22",
                "-h", "localhost",
                "-d", "ben_telecom_dev",
                "-c", query
        ]"""
        # with open()
        # subprocess.run(command)
        return




def extract_purchases(output_dir, bath_id, extraction_start_date="1900-01-01", extraction_end_date="2026-10-14"):

        connection = duckdb.connect()
        # print(str(PURCHASES_DIR / "*"))
        

        purchase_files = glob(f"{PURCHASES_DIR}/*.parquet")
        # print(purchase_files)
        # !!! Trouver une altenatic a cete approcha car siu des millins de fichiers, .., tres lent

        files_to_extract = []
        start_date = extraction_start_date.replace("-", "")
        end_date = extraction_end_date.replace("-", "")

        for f in purchase_files:
                file_generation_date = f.removesuffix(".parquet")[-8:]
                # print(file_generation_date)
                if file_generation_date >= start_date and file_generation_date <= end_date:
                        files_to_extract.append(f)
        print(files_to_extract[:10])


        query = f"""COPY(
        SELECT *, {bath_id} AS batch_id FROM read_parquet(?)
        )
        TO '{output_dir}/purchases.csv'
        WITH (FORMAT CSV, HEADER TRUE);
        """
        print(query)
        connection.execute(query, [files_to_extract]
        )

        connection.close()


def extract_service_usage(output_dir, batch_id, output_file_name = "services_usage.csv"):
        consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers = KAFKA_SERVERS,
        auto_offset_reset="earliest",
        group_id = "batch-consumer-test-8", # !!! Gerer cas ou les messages ont ete conomes mais une erreur faisant que ... k=jusqu la fin
        consumer_timeout_ms = 5000
        )        
        message_records = []
        for message in consumer:
                # Topic + partition + offset uniquely identify a kafka message
                # Since we have only one topic, let us use partition + offset to avoid duplicates
                record = json.loads(message.value.decode("utf-8"))
                record[MESSAGE_PARTITION_COL] = message.partition
                record[MESSAGE_OFFSET_COL] = message.offset

                message_records.append(record)
        
        consumer.close()
        usage_df = pd.DataFrame(message_records)        
        print(usage_df)
        if len(usage_df!=0):
                usage_df = usage_df[[PURCHASE_ID_COL, SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL, SERVICE_TYPE_COL, DATA_MB_COL, SMS_COUNT_COL, CALL_SECONDS_COL, MESSAGE_PARTITION_COL, MESSAGE_OFFSET_COL]]
                
                
                usage_df[SMS_COUNT_COL] = usage_df[SMS_COUNT_COL].astype("Int64")
                usage_df[CALL_SECONDS_COL] = usage_df[CALL_SECONDS_COL].astype("Int64")
        usage_df[BATCH_ID_COL] = batch_id

        print(usage_df)
        # !!! Later handle scalability for ex by usin chuncsize? and avoid stroing all  the usage_df.... in the memory
        ### !!!Hqndle cqse zhere there is no record fethec

        usage_df.to_csv(f"{output_dir}/{output_file_name}", index=False)

# extract_from_database("2026-10-14", "1900-01-01", "2026-10-14", 100 )

## extract_purchases("/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/raw/2026-10-14", "100")

# extract_service_usage("/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/raw/2026-10-14")


# # extract("/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/raw/2026-10-14")



if __name__ == "main":
        # extract_purchases()
        pass