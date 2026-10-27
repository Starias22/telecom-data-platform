import os
import subprocess

from dotenv import load_dotenv

from config.config import BATCH_LOGS_TABLE, BATCH_STATUS_COL, HOST, PLATFORM_INITIALIZATION_NOT_DONE_OR_INCOMPLET, PLATFORM_INITIALIZATION_SUCCESSFUL, PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET, USER, PLATFORM_STATE_COL, PLATFORM_STATE_TABLE, SETUP_COMPLETED, INITIALIZED
from config.paths import ENV_FILE_PATH, SQL_INITIAL_SETUP_MAIN_FILE_PATH
from src.utils.db_connector import get_connection
from psycopg.errors import UndefinedTable, OperationalError

def get_platform_state():
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
        print("*********")
        print(e)
        print(str(e))
        if "database" in str(e) and "does not exist" in str(e):
                       return PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET
    except UndefinedTable as e:
              return PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET
    return platform_state # Setep copleted / Initialized

def is_platform_setup():
     platform_sate = get_platform_state()
     print(platform_sate)
     return platform_sate in [ SETUP_COMPLETED, INITIALIZED]

def setup_platform_database():
        load_dotenv(ENV_FILE_PATH)
        env = os.environ.copy()
        subprocess.run(
                [
                        "psql",
                        "-h", HOST,
                        "-U", USER,
                        "-f", SQL_INITIAL_SETUP_MAIN_FILE_PATH
                ],
                env=env
        )

def mark_platform_initialized(connection):
        query = f"""
                UPDATE {PLATFORM_STATE_TABLE} 
                SET {PLATFORM_STATE_COL} = '{INITIALIZED}';
                """
        print(query)
        with connection.cursor() as cursor:
               cursor.execute(query)
               connection.commit()

if __name__ ==  "__main__":
       pass
        # print(is_platform_setup())