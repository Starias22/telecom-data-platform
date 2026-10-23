from pathlib import Path
from config.paths import RAW_DATA_DIR, OFFERS_OUTPUT_FILE_NAME, OFFER_BILLINGS_OUTPUT_FILE_NAME, OFFER_CONFIGS_OUTPUT_FILE_NAME, CURSTOMERS_OUTPUT_FILE_NAME, SUBSCRIPTIONS_OUTPUT_FILE_NAME, PURCHASES_OUTPUT_FILE_NAME, SERVICES_USAGE_OUTPUT_FILE_NAME

ID_COL = "id"
SUBSCRIPTION_ID_COL = "subscription_id"
OFFER_CONFIG_ID_COL = "offer_config_id"
PURCHASED_AT_COL = "purchased_at"
PURCHASE_CHANNEL_COL= "purchase_channel"
PAYMENT_METHOD_COL= "payment_method"
REGISTRATION_DATE_COL = "registration_date"
TERMINATION_DATE_COL = "termination_date"
START_DATE_COL = "start_date"
END_DATE_COL = "end_date"


USSD = "USSD"
MOBILE_APP = "MOBILE_APP"
DEALER = "DEALER"
WEB = "WEB"
MOBILE_MONEY = "MOBILE_MONEY"
AIRTIME = "AIRTIME"


KAFKA_TOPIC = "TelecomUsage"
KAFKA_SERVERS = "localhost:9092"


QUERY_TABLE_FIELD = "query_table"
INSERTION_DATE_FIELD = "insertion_date"
UPDATE_DATE_FILED = "update_date"

OFFER_CATALOG_SCHEMA = "offers_catalog"
CRM_SCHEMA =  "crm"
SUBSCRIPTIONS_SCHEMA = "subscriptions"


OFFERS_TABLE_NAME = "offers"
OFFER_BILLINGS_TABLE_NAME = "offer_billings"
OFFER_CONFIGS_TABLE_NAME = "offer_configurations"

CUSTOMERS_TABLE_NAME = "customers"
SUBSCRIPTIONS_TABLE_NAME = "subscriptions"

OFFERS_INSERT_DATE_COL = "created_at"
OFFERS_UPDATE_DATE_COL = "updated_at"

OFFER_BILLINGS_INSERT_DATE_COL = "created_at"
OFFER_BILLINGS_UPDATE_DATE_COL = "updated_at"

OFFER_CONFIGS_INSERT_DATE_COL = "created_at"
OFFER_CONFIGS_UPDATE_DATE_COL = "updated_at"

CUSTOMER_INSERT_DATE_COL = "registration_date"
CUSTOMER_UPDATE_DATE_COL = "updated_at"

SUBSCRIPTION_INSERT_DATE_COL = "registration_date"
SUBSCRIPTION_UPDATE_DATE_COL = "updated_at"

table_absolute_name = lambda schema, table_name: f"{schema}.{table_name}"


OFFERS_TABLE = table_absolute_name(OFFER_CATALOG_SCHEMA, OFFERS_TABLE_NAME)
OFFER_BILLINGS_TABLE = table_absolute_name(OFFER_CATALOG_SCHEMA, OFFER_BILLINGS_TABLE_NAME)
OFFER_CONFIGS_TABLE = table_absolute_name(OFFER_CATALOG_SCHEMA, OFFER_CONFIGS_TABLE_NAME)

CUSTOMERS_TABLE = table_absolute_name(CRM_SCHEMA, CUSTOMERS_TABLE_NAME)
SUBSCRIPTIONS_TABLE = table_absolute_name(SUBSCRIPTIONS_SCHEMA, SUBSCRIPTIONS_TABLE_NAME)

PURCHASES_TABLE_NAME = "purchases"
SERVICES_USAGE_TABLE_NAME = "services_usage"

def get_extraction_params(output_dir): # !!! Find a more convenent name
        return {

        "offers":{
        "query_table":OFFERS_TABLE,
        "insert_date_col":OFFERS_INSERT_DATE_COL,
        "update_date_col":OFFERS_UPDATE_DATE_COL,
        "output_path":Path(output_dir) / OFFERS_OUTPUT_FILE_NAME
        },
        "offer_billings":{
        "query_table":OFFER_BILLINGS_TABLE,
        "insert_date_col":OFFER_BILLINGS_INSERT_DATE_COL,
        "update_date_col":OFFER_BILLINGS_UPDATE_DATE_COL,
        "output_path":Path(output_dir) / OFFER_BILLINGS_OUTPUT_FILE_NAME
        },
        "offer_configurations":{
        "query_table":OFFER_CONFIGS_TABLE,
        "insert_date_col":OFFER_CONFIGS_INSERT_DATE_COL,
        "update_date_col":OFFER_CONFIGS_UPDATE_DATE_COL,
        "output_path":Path(output_dir) / OFFER_CONFIGS_OUTPUT_FILE_NAME
        },
        "customers":{
        "query_table":CUSTOMERS_TABLE,
        "insert_date_col":CUSTOMER_INSERT_DATE_COL,
        "update_date_col":CUSTOMER_UPDATE_DATE_COL,
        "output_path":Path(output_dir) / CURSTOMERS_OUTPUT_FILE_NAME
        },
        "subscriptions":{
        "query_table":SUBSCRIPTIONS_TABLE,
        "insert_date_col":SUBSCRIPTION_INSERT_DATE_COL,
        "update_date_col":SUBSCRIPTION_UPDATE_DATE_COL,
        "output_path":Path(output_dir) / SUBSCRIPTIONS_OUTPUT_FILE_NAME
        }
}

def get_staging_params(staging_raw_data_dir, staging_schema="staging"): # !!! Find a more convenent name
        return {

        "offers":{
        "table":f"{staging_schema}.{OFFERS_TABLE_NAME}",
        "file_path":Path(staging_raw_data_dir) / OFFERS_OUTPUT_FILE_NAME
        },
        "offer_billings":{
        "table":f"{staging_schema}.{OFFER_BILLINGS_TABLE_NAME}",
        "file_path":Path(staging_raw_data_dir) / OFFER_BILLINGS_OUTPUT_FILE_NAME
        },
        "offer_configurations":{
        "table":f"{staging_schema}.{OFFER_CONFIGS_TABLE_NAME}",
        "file_path":Path(staging_raw_data_dir) / OFFER_CONFIGS_OUTPUT_FILE_NAME
        },
        "customers":{
        "table":f"{staging_schema}.{CUSTOMERS_TABLE_NAME}",
        "file_path":Path(staging_raw_data_dir) / CURSTOMERS_OUTPUT_FILE_NAME
        },
        "subscriptions":{
        "table":f"{staging_schema}.{SUBSCRIPTIONS_TABLE_NAME}",
        "file_path":Path(staging_raw_data_dir) / SUBSCRIPTIONS_OUTPUT_FILE_NAME
        },
        "purchases":{
        "table":f"{staging_schema}.{PURCHASES_TABLE_NAME}",
        "file_path":Path(staging_raw_data_dir) / PURCHASES_OUTPUT_FILE_NAME
        },
        "services_usage":{
        "table":f"{staging_schema}.{SERVICES_USAGE_TABLE_NAME}",
        "file_path":Path(staging_raw_data_dir) / SERVICES_USAGE_OUTPUT_FILE_NAME
        }
}

TRX_DB_NAME = "ben_telecom"
USER = "starias22"
HOST = "localhost"

DATA_PLATFORM_DB = "ben_telecom_data_platform"
PASSDWORD = "my_password"

PIPELINE_METADATA_SCHEMA = "pipeline_metadata"
BATCH_LOGS_TABLE_NAME = "batch_logs"

BATCH_LOGS_TABLE = f"{PIPELINE_METADATA_SCHEMA}.{BATCH_LOGS_TABLE_NAME}"
BATCH_STATUS_COL = "status"
RUNNING = "RUNNING"
SUCCES = "SUCCESS"
BATCH_ID_COL = "batch_id"
STARTED_AT = "started_at"
FINISHED_AT = "finished_at"


