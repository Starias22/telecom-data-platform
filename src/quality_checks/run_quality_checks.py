import os

from dotenv import load_dotenv

from config.paths import ENV_FILE_PATH, SQL_QUALITY_CHECKS_FILE_PATH
from config.config import HOST, DATA_PLATFORM_DB, USER
from src.utils.psql_client import PsqlClient
from src.utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv(ENV_FILE_PATH)
env = os.environ.copy()

def check_quality(batch_id=1):
    output = PsqlClient(
         user=USER,
         host=HOST,
         db=DATA_PLATFORM_DB,
         variable_assignment=f"batch_id={batch_id}",
         env=env            
        ).execute(
             input=SQL_QUALITY_CHECKS_FILE_PATH,
             is_sql_file=True
        )
    logger.info(output)
        
if __name__ ==  "__main__":
        check_quality()