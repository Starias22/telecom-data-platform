import os

from dotenv import load_dotenv

from config.config import HOST, PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET, USER, PLATFORM_STATE_COL, PLATFORM_STATE_TABLE, SETUP_COMPLETED, INITIALIZED
from config.paths import ENV_FILE_PATH, SQL_INITIAL_SETUP_MAIN_FILE_PATH
from src.utils.db_connector import get_connection
from psycopg2.errors import UndefinedTable, OperationalError

from src.utils.logger import get_logger
from src.utils.psql_client import PsqlClient

logger = get_logger(__name__)

def get_platform_state():
    logger.info("Getting platform state")
    try:
        connection = get_connection()
       
        query = f"""
                SELECT {PLATFORM_STATE_COL} FROM {PLATFORM_STATE_TABLE};
                """
        print(query)
            
        with connection.cursor() as cursor:
            cursor.execute(query)
            platform_state = cursor.fetchone()[0]
            # !!! Later replace by throwing execptions
    except OperationalError as e:
        if "database" in str(e) and "does not exist" in str(e):
                       return PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET
    except UndefinedTable as e:
              return PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET
    return platform_state # Setup completed / Initialized

def customer_activity_already_analyzed(analysis_month):
    
    connection = get_connection()
       
    query = f"""
                SELECT EXISTS (SELECT 1 FROM pipeline_metadata.batch_logs WHERE started_at::DATE = '{analysis_month}' AND status='SUCCESS');
                """
    print(query)
            
    with connection.cursor() as cursor:
            cursor.execute(query)
            analyzed = cursor.fetchone()[0]
            logger.info(f"Customer activity already analyzed this month? {'Yes' if analyzed else 'No'}")
            return analyzed
            
    

def is_platform_setup():
     platform_sate = get_platform_state()
     return platform_sate in [ SETUP_COMPLETED, INITIALIZED]

def setup_platform_database():
    load_dotenv(ENV_FILE_PATH)
    env = os.environ.copy()

    return PsqlClient(user=USER,
                             host=HOST,
                             env=env
                             ).execute(
                                    SQL_INITIAL_SETUP_MAIN_FILE_PATH, is_sql_file=True)

def mark_platform_initialized(connection):
        query = f"""
                UPDATE {PLATFORM_STATE_TABLE} 
                SET {PLATFORM_STATE_COL} = '{INITIALIZED}';
                """
        print(query)
        with connection.cursor() as cursor:
               cursor.execute(query)
               connection.commit()
        logger.info("Platform marked as initialized")

if __name__ ==  "__main__":
       # output = setup_platform_database()
       # print(output)
       # analyzed = check_customer_activity_analyzed('2026-11-18')
       # print(analyzed)

       pass