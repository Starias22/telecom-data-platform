import psycopg
from config.config import DATA_PLATFORM_DB, USER, PASSDWORD, HOST

def get_connection(dbname=DATA_PLATFORM_DB):
        connection = psycopg.connect(
                host=HOST,
                port=5432,
                dbname=dbname,
                user=USER,
                password=PASSDWORD
        )
        return connection


