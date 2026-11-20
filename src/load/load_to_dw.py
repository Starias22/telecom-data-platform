import os
from dotenv import load_dotenv

from config.paths import ENV_FILE_PATH, INITIAL_LOAD_SQL_FILE_PATH, INCREMENTAL_LOAD_SQL_FILE_PATH
from config.config import HOST, DATA_PLATFORM_DB, USER
from src.utils.psql_client import PsqlClient

# from src.run_pipeline import run_pipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)

load_dotenv(ENV_FILE_PATH)
env = os.environ.copy()

def load(incremental=True, batch_id=None):

        output = PsqlClient(user=USER, 
                                 db=DATA_PLATFORM_DB, 
                                 host=HOST, env=env, 
                                 variable_assignment=f"batch_id={batch_id}" if batch_id is not None else None
                                 ).execute(
                INCREMENTAL_LOAD_SQL_FILE_PATH if incremental else INITIAL_LOAD_SQL_FILE_PATH,
                is_sql_file=True
        )
        logger.info(output)
        
        
if __name__ ==  "__main__":
        load(incremental=False)