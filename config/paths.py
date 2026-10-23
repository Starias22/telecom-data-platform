from pathlib import Path
PROJECT_ROOT = "/home/starias/myprojects/telecom-offer-performance-analytics-platform"

DATA_DIR = Path(PROJECT_ROOT) / "data"
RAW_DATA_DIR = Path(DATA_DIR) / "raw"

OFFERS_OUTPUT_FILE_NAME = "offers.csv"
OFFER_BILLINGS_OUTPUT_FILE_NAME = "offer_billings.csv"
OFFER_CONFIGS_OUTPUT_FILE_NAME = "offer_configs.csv"

CURSTOMERS_OUTPUT_FILE_NAME = "customers.csv"
SUBSCRIPTIONS_OUTPUT_FILE_NAME = "subscriptions.csv"
PURCHASES_OUTPUT_FILE_NAME = "purchases.csv"
SERVICES_USAGE_OUTPUT_FILE_NAME = "services_usage.csv"


PURCHASES_FILE_PATH = '/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/purchases'

PURCHASES_DIR = DATA_DIR / "purchases"

SQL_DIR = Path(PROJECT_ROOT) / "sql/"
SQL_INITIAL_SETUP_MAIN_FILE_PATH = SQL_DIR / "initial_setup/main.sql"
SQL_QUALITY_CHECKS_FILE_PATH = SQL_DIR / "quality_checks/check_data_quality.sql"

SQL_LOAD_DIR = SQL_DIR / "load"
INITIAL_LOAD_SQL_FILE_PATH = SQL_LOAD_DIR / "initial_load.sql"
INCREMENTAL_LOAD_SQL_FILE_PATH = SQL_LOAD_DIR / "incremental_load.sql"

ENV_FILE_PATH = Path(PROJECT_ROOT) / ".env"



