import psycopg
from config.config import DATA_PLATFORM_DB, USER, PASSDWORD, HOST
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_connection(dbname=DATA_PLATFORM_DB):
        connection = psycopg.connect(
                host=HOST,
                port=5432,
                dbname=dbname,
                user=USER,
                password=PASSDWORD
        )
        logger.info(f"Connected to database '{dbname}' as user '{USER}'")
        return connection

if __name__ == "__main__":
        connection = get_connection()
        # print(connection)


