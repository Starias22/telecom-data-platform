import psycopg
from config.config import DATA_PLATFORM_DB, USER, PASSDWORD, HOST

def get_connection():
        connection = psycopg.connect(
                host=HOST,
                port=5432,
                dbname=DATA_PLATFORM_DB,
                user=USER,
                password=PASSDWORD
        )
        return connection


