from os import makedirs
import os
from pathlib import Path
import subprocess
import duckdb
import json
from kafka import KafkaConsumer
from kafka.errors import BrokerNotAvailableError, KafkaTimeoutError
import pandas as pd
from glob import glob
from config.paths import PURCHASES_DIR
from config.column_names import PURCHASE_ID_COL, SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL, SERVICE_TYPE_COL, DATA_MB_COL, SMS_COUNT_COL, CALL_SECONDS_COL, MESSAGE_PARTITION_COL, MESSAGE_OFFSET_COL, BATCH_ID_COL
from config.config import get_extraction_params, TRX_DB_NAME, HOST, USER, KAFKA_SERVERS, KAFKA_TOPIC
import csv
from src.utils.utils import fmt_datetime
# !!! Later add excepion handling approch to all extractors, and also define a utlity function for running psql cmd with python

def is_csv_empty(file_path):
       with open(file_path, mode="r", newline="") as f:
              reader = csv.reader(f)
              next(reader, None) # Ignore/spik header
              return next(reader, None)  is None
              

def extract_from_db_table(batch_id, extraction_output_dir, table_name, watermark, extraction_cut_off_date):
    print(watermark)
    # watermark = ast.literal_eval(watermark)[table_name]
    
    EXTRACTION_PARAMS = get_extraction_params(extraction_output_dir)
    

    
    extraction_params = EXTRACTION_PARAMS[table_name]
    table = extraction_params["query_table"]
    last_update_date = extraction_params["update_date_col"]
    output_path = extraction_params["output_path"]
    

    makedirs(extraction_output_dir, exist_ok=True)
    output_path = str(output_path)
    temp_output_file = str(output_path) + ".tmp"
    query = f"""\\copy ( SELECT *, {int(batch_id)} AS batch_id FROM {table} WHERE {last_update_date} > '{watermark}' AND {last_update_date} <= '{extraction_cut_off_date}' ) TO '{temp_output_file}' WITH (FORMAT CSV, HEADER TRUE)"""
    print(query)
    command = [
                        "psql",
                        "-U", USER,
                        "-h", HOST,
                        "-d", TRX_DB_NAME
                ]    
    try:
        subprocess.run(
        command, input=query,
          capture_output=True,
            text=True)
        if is_csv_empty(temp_output_file):
           print(f"No data extracted from table {table_name}, so CSV file removed")
           os.remove(temp_output_file)
           return
        os.rename(temp_output_file, output_path)
    except subprocess.CalledProcessError as e:
          os.remove(temp_output_file)
          raise RuntimeError(e.stderr) from e
    
    
    


def extract_purchases(extraction_output_dir, batch_id, watermark, extraction_cut_off_date):
        # watermark = ast.literal_eval(watermark)["purchases"]
        print(watermark)
        
        
        try:
              connection = duckdb.connect()
              purchase_files = glob(f"{PURCHASES_DIR}/*.parquet")
              print(purchase_files)
              # !!! Trouver une altenatic a cete approcha car siu des millins de fichiers, .., tres lent
              files_to_extract = []
              start_date = fmt_datetime(watermark )
              extraction_cut_off_date = fmt_datetime(extraction_cut_off_date)
              print(start_date)
              # start_date / 0 # Simulate an
              
              for f in purchase_files:
                        file_generation_date = fmt_datetime(Path(f).stem)
                        print(file_generation_date)
                        # print(file_generation_date)
                        if file_generation_date > start_date and file_generation_date <= extraction_cut_off_date:
                        # if file_generation_date >= start_date and file_generation_date <= end_date:
                                files_to_extract.append(f)
                        """
                        if file_generation_date == "20261028175234": # In order to be aple to test purcase add
                                print("Yes correct")
                                """
              if len(files_to_extract) == 0:
                print("No new purchase file generated")
                return
              print(files_to_extract[:10])
              output_file_path = f"{extraction_output_dir}/purchases.csv"
              temp_output_file = output_file_path + ".tmp"

              query = f"""COPY(
                SELECT *, {int(batch_id)} AS batch_id FROM read_parquet(?)
                )
                TO '{temp_output_file}'
                WITH (FORMAT CSV, HEADER TRUE);
                """
              print(query)
              makedirs(extraction_output_dir, exist_ok=True)
              connection.execute(query, [files_to_extract]
                )
              connection.close()
              os.rename(temp_output_file, output_file_path)
        except Exception as e:
              os.remove(temp_output_file)
              raise RuntimeError(str(e)) from e


def extract_service_usage(extraction_output_dir, batch_id, output_file_name = "services_usage.csv"):
        
        try:
            print("Going to start")
            consumer = KafkaConsumer(
            KAFKA_TOPIC,
            bootstrap_servers = KAFKA_SERVERS,
            enable_auto_commit=False,
            auto_offset_reset="earliest",
            group_id = "batch-consumer-test-900", # !!! PLus tard Gerer cas ou les messages ont ete conomes mais une erreur faisant que ... k=jusqu la fin
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

            # INtentionaly simulate an error during processing
            # The consumer offset will not be committed so the consumer can still consume the message at retry
            # print(44/0) # Error simulation (0 division error)
            # The comment the code and execite the batcj again, all .... will be consumed       
            
            if len(message_records) == 0:
                   print("No new event has been produced")
                   return
            usage_df = pd.DataFrame(message_records)

            for col in [CALL_SECONDS_COL, SMS_COUNT_COL, DATA_MB_COL]:
                if col not in usage_df.columns:
                   usage_df[col] = None
            print(usage_df)
            usage_df = usage_df[[PURCHASE_ID_COL, SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL, SERVICE_TYPE_COL, DATA_MB_COL, SMS_COUNT_COL, CALL_SECONDS_COL, MESSAGE_PARTITION_COL, MESSAGE_OFFSET_COL]]
            usage_df[SMS_COUNT_COL] = usage_df[SMS_COUNT_COL].astype("Int64")
            usage_df[CALL_SECONDS_COL] = usage_df[CALL_SECONDS_COL].astype("Int64")
            # !!! Later plan for callability (for eg proceesing shucnks of events)
            print(usage_df)
            print(batch_id)
            usage_df[BATCH_ID_COL] = int(batch_id)

            print(usage_df)
            # !!! Later handle scalability for ex by usin chuncsize? and avoid stroing all  the usage_df.... in the memory
            ### !!!Hqndle cqse zhere there is no record fethec

            makedirs(extraction_output_dir, exist_ok=True)
            usage_df.to_csv(f"{extraction_output_dir}/{output_file_name}", index=False)
            # Now that all the messages have been consumed and the file has been saved we can commit to notify Kafka that we have read them
            # This avoid lossing ie not processing some events caused by an instance of the task extraction of service usage which failed ...
            consumer.commit()
            consumer.close()
        except (BrokerNotAvailableError, KafkaTimeoutError) as e:
               print("Error occured", e)
               print("*****************")
               error_message = str(e)
               if "Unable to bootstrap from" in error_message:
                
                      print("Broker not available")
               raise RuntimeError(error_message) from e
        except Exception as e:
               error_message = str(e)
               raise RuntimeError(error_message) from e
              
               

if __name__ == "__main__":
        # extract_purchases()
        pass