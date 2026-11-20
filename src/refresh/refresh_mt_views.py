import os
from dotenv import load_dotenv

from config.paths import ENV_FILE_PATH, MT_VIEWS_REFRESH_SQL_FILE_PATH
from config.config import HOST, DATA_PLATFORM_DB, USER
from src.utils.psql_client import PsqlClient
from src.utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv(ENV_FILE_PATH)
env = os.environ.copy()

def resfresh_mt_views():

        output = PsqlClient(user=USER, 
                                 db=DATA_PLATFORM_DB, 
                                 host=HOST, env=env, 
                                 ).execute(
                                         MT_VIEWS_REFRESH_SQL_FILE_PATH,
                is_sql_file=True
        )
        logger.info(output)
        
        
if __name__ ==  "__main__":
      resfresh_mt_views()