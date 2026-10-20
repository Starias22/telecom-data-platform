import json
from kafka import KafkaProducer
import pandas as pd
from tqdm import tqdm

from config.paths import TELECOM_SERVICES_USAGE_SOURCES_FILE
from config.column_names import SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL, CALL_SECONDS_COL, SMS_COUNT_COL
from config.config import KAFKA_TOPIC, KAFKA_SERVERS


def produce_events():
        producer = KafkaProducer(
        bootstrap_servers = KAFKA_SERVERS,
        key_serializer=lambda key:str(key).encode("utf-8"),
  
        value_serializer=lambda value:json.dumps(value).encode("utf-8"))

        print(producer)
        usage_df = pd.read_json(TELECOM_SERVICES_USAGE_SOURCES_FILE, lines=True)
        usage_df[CALL_SECONDS_COL] = usage_df[CALL_SECONDS_COL].astype("Int64")
        usage_df[SMS_COUNT_COL] = usage_df[SMS_COUNT_COL].astype("Int64")

        print(usage_df)

        usage_records = usage_df.to_dict(orient="records")
        usage_records = [
                {k:v for k, v in record.items() if pd.notna(v)} for record in usage_records
        ]


        for record in tqdm(usage_records,"Producing telecom usage events"): 
                if record[TIMESTAMP_MILLISECONDS_COL] is not None:
                        record[TIMESTAMP_MILLISECONDS_COL] = record[TIMESTAMP_MILLISECONDS_COL].isoformat()
                producer.send(
                        KAFKA_TOPIC,
                        key = record[SUBSCRIPTION_ID_COL],
                        value=record
                )
        producer.flush()

        print(f"{len(usage_records)} telecom usage events sent successfully")

