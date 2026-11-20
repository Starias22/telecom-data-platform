import os

from dotenv import load_dotenv
from dateutil.relativedelta import relativedelta

from src.utils.psql_client import PsqlClient
from config.config import DATA_PLATFORM_DB, USER, HOST
from config.paths import CUSTOMER_ACTIVITY_ANALYSIS_SQL_FILE_PATH, ENV_FILE_PATH
from datetime import date, timedelta

from src.utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv(ENV_FILE_PATH)

env = os.environ.copy()

def analyze_customer_activity(analysis_month):
    output = PsqlClient(
        user=USER,
        host=HOST,
        env=env,
        db=DATA_PLATFORM_DB,
        variable_assignment=f"analysis_month={analysis_month}"
    ).execute(
        input=CUSTOMER_ACTIVITY_ANALYSIS_SQL_FILE_PATH,
        is_sql_file=True
    )
    logger.info(output)

def historical_backfill():
    current_month = date(year=2000, month=1, day=1)
    
    
    while current_month <= date.today():
        
        
        analysis_month = current_month.strftime("%Y-%m-%d")

        logger.info(f"Current month: {analysis_month}")
        analyze_customer_activity(analysis_month=analysis_month)
        current_month += relativedelta(months=1)
    return

if __name__ == "__main__":
    # analyze_customer_activity(analysis_month="2025-05-01")

    # historical_backfill()
    pass
    