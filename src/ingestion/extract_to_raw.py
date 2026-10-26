from os import makedirs
from pathlib import Path
import subprocess
import duckdb
import json
from kafka import KafkaConsumer
from kafka.errors import BrokerNotAvailableError, KafkaTimeoutError
import pandas as pd
from glob import glob
from config.paths import RAW_DATA_DIR, OFFER_BILLINGS_OUTPUT_FILE_NAME, OFFER_CONFIGS_OUTPUT_FILE_NAME, CURSTOMERS_OUTPUT_FILE_NAME, SUBSCRIPTIONS_OUTPUT_FILE_NAME, PURCHASES_DIR
from config.column_names import PURCHASE_ID_COL, SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL, SERVICE_TYPE_COL, DATA_MB_COL, SMS_COUNT_COL, CALL_SECONDS_COL, MESSAGE_PARTITION_COL, MESSAGE_OFFSET_COL, BATCH_ID_COL
from config.config import get_extraction_params, TRX_DB_NAME, HOST, USER, KAFKA_SERVERS, KAFKA_TOPIC, PASSDWORD
# from src.utils.ba
import ast



def extract_from_db_table(batch_id, extraction_output_dir, table_name, watermark, extraction_cut_off_date):
    print(watermark)
    # watermark = ast.literal_eval(watermark)[table_name]
    
    EXTRACTION_PARAMS = get_extraction_params(extraction_output_dir)
    extraction_params = EXTRACTION_PARAMS[table_name]
    table = extraction_params["query_table"]
    last_update_date = extraction_params["update_date_col"]
    output_path = extraction_params["output_path"]
    query = f"""\\copy ( SELECT *, {int(batch_id)} AS batch_id FROM {table} WHERE {last_update_date} > '{watermark}' AND {last_update_date} <= '{extraction_cut_off_date}' ) TO '{output_path}' WITH (FORMAT CSV, HEADER TRUE)"""
    print(query)
    command = [
                        "psql",
                        "-U", USER,
                        "-h", HOST,
                        "-d", TRX_DB_NAME
                ]

    makedirs(extraction_output_dir, exist_ok=True)
    result = subprocess.run(command, input=query, capture_output=True, text=True)
    print(result)

## def extract_offers(batch_id, watermark, extraction_output_dir):
       

       
       
"""def extract_from_database(extraction_output_dir, watermark, batch_id):        
        queries = []
        print("Test")
        print(batch_id)
        print(type(batch_id))
        makedirs(extraction_output_dir, exist_ok=True)
        EXTRACTION_PARAMS = get_extraction_params(extraction_output_dir)
        
        for i in EXTRACTION_PARAMS.values():
            table = i["query_table"]
            last_update_date = i["update_date_col"]
            output_path = i["output_path"]

            query = f\\copy ( SELECT *, {int(batch_id)} AS batch_id FROM {table} WHERE {last_update_date} > '{watermark}' ) TO '{output_path}' WITH (FORMAT CSV, HEADER TRUE)

            # !!!For prudcution environment think about COPY query keyword instead of \copy of psql


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
        print(result)"""

                
def extract_purchases(extraction_output_dir, batch_id, watermark, extraction_cut_off_date):
        # watermark = ast.literal_eval(watermark)["purchases"]
        print(watermark)

        
        connection = duckdb.connect()
        # print(str(PURCHASES_DIR / "*"))
        

        purchase_files = glob(f"{PURCHASES_DIR}/*.parquet")
        # print(purchase_files)
        # !!! Trouver une altenatic a cete approcha car siu des millins de fichiers, .., tres lent

        files_to_extract = []
        start_date = watermark.replace("-", "")
        

        for f in purchase_files:
                file_generation_date = f.removesuffix(".parquet")[-8:]
                # print(file_generation_date)
                if file_generation_date > start_date and file_generation_date <= extraction_cut_off_date:
                # if file_generation_date >= start_date and file_generation_date <= end_date:
                        files_to_extract.append(f)
        if len(files_to_extract) == 0:
               print("No new purchase file generated")
               return
        print(files_to_extract[:10])


        query = f"""COPY(
        SELECT *, {int(batch_id)} AS batch_id FROM read_parquet(?)
        )
        TO '{extraction_output_dir}/purchases.csv'
        WITH (FORMAT CSV, HEADER TRUE);
        """
        print(query)
        makedirs(extraction_output_dir, exist_ok=True)
        connection.execute(query, [files_to_extract]
        )

        connection.close()


def extract_service_usage(extraction_output_dir, batch_id, output_file_name = "services_usage.csv"):
        
        
        try:
            print("Going to start")
            consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers = KAFKA_SERVERS,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            group_id = "batch-consumer-test-10", # !!! PLus tard Gerer cas ou les messages ont ete conomes mais une erreur faisant que ... k=jusqu la fin
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
            
            
            usage_df = pd.DataFrame(message_records)        
            print(usage_df)
            if len(usage_df!=0):
                    usage_df = usage_df[[PURCHASE_ID_COL, SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL, SERVICE_TYPE_COL, DATA_MB_COL, SMS_COUNT_COL, CALL_SECONDS_COL, MESSAGE_PARTITION_COL, MESSAGE_OFFSET_COL]]
                    
                    
                    usage_df[SMS_COUNT_COL] = usage_df[SMS_COUNT_COL].astype("Int64")
                    usage_df[CALL_SECONDS_COL] = usage_df[CALL_SECONDS_COL].astype("Int64")
                    print(usage_df)
                    print(batch_id)
                    usage_df[BATCH_ID_COL] = int(batch_id)

            print(usage_df)
            # !!! Later handle scalability for ex by usin chuncsize? and avoid stroing all  the usage_df.... in the memory
            ### !!!Hqndle cqse zhere there is no record fethec

            makedirs(extraction_output_dir, exist_ok=True)
            usage_df.to_csv(f"{extraction_output_dir}/{output_file_name}", index=False)
            # Now that all the messages have been consumed and the file has been saved we can commit to notify Kafka that we have read them
            consumer.commit()
            consumer.close()
        except (BrokerNotAvailableError, KafkaTimeoutError) as e:
               print("Error occured", e)
               print("*****************")
               if "Unable to bootstrap from" in str(e):
                
                      print("Broker not available")

if __name__ == "__main__":
        # extract_purchases()
        pass