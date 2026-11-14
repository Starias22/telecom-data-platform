from src.utils.db_connector import get_connection
from config.config import WATERMARK_TABLE, LAST_SUCCESSFUL_WATERMARK_COL, UPDATED_AT_COL
from src.utils.logger import get_logger

logger = get_logger(__name__)


def get_last_watermark():
        logger.info("Getting last successful watermark")
        connection = get_connection()

        query = f"""
        SELECT {LAST_SUCCESSFUL_WATERMARK_COL}
        FROM {WATERMARK_TABLE};
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(query)
                last_successful_watermark = cursor.fetchone()[0].strftime("%Y-%m-%d %H:%M:%S")
                logger.info(f"Last successful watermark was {last_successful_watermark}")
                return last_successful_watermark


def update_watermark(new_watermark):
        logger.info("Updating watermark")
        connection = get_connection()
        query = f"""
        UPDATE {WATERMARK_TABLE}
        SET {LAST_SUCCESSFUL_WATERMARK_COL} = '{new_watermark}',
            {UPDATED_AT_COL} = CURRENT_TIMESTAMP;
        """  
        print(query)      
        with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                logger.info("Watermark updated")



