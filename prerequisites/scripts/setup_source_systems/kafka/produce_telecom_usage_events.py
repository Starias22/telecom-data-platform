import json
from kafka import KafkaProducer
import pandas as pd
from pathlib import Path
from tqdm import tqdm
from config.config import SOURCES_DIR, SUBSCRIPTION_ID_COL, TIMESTAMP_MILLISECONDS_COL

topic = "TelecomUsage"
producer = KafkaProducer(
        bootstrap_servers = "localhost:9092",
        key_serializer=lambda key:str(key).encode("utf-8"),
  
        value_serializer=lambda value:json.dumps(value).encode("utf-8")
)

print(producer)

file = Path(SOURCES_DIR) / "usage.json"
usage_df = pd.read_json(file, lines=True)
usage_records = usage_df.to_dict(orient="records")
usage_records = [
        {k:v for k, v in record.items() if pd.notna(v)} for record in usage_records
]


for record in tqdm(usage_records,"Producing telecom usage events"): 
        if record[TIMESTAMP_MILLISECONDS_COL] is not None:
                record[TIMESTAMP_MILLISECONDS_COL] = record[TIMESTAMP_MILLISECONDS_COL].isoformat()
        producer.send(
                topic,
                key = record[SUBSCRIPTION_ID_COL],
                value=record
        )
producer.flush()

print(f"{len(usage_records)} telecom usage events sent successfully")

