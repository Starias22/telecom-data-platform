import psycopg
from config.config import DATA_PLATFORM_DB, USER, PASSDWORD, HOST
from src.utils.logger import get_logger

logger = get_logger(__name__)

def get_connection():
        connection = psycopg.connect() # Connection infos are automatically read from .env
        user = connection.info.user
        db = connection.info.dbname
        port = connection.info.port
        host = connection.info.host
        
        logger.info(f"Connected to database '{db}' as user '{user}' at '{host}' on port {port}")
        return connection

if __name__ == "__main__":
        connection = get_connection()
        


