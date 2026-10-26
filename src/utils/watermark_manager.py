from src.utils.db_connector import get_connection
from config.config import WATERMARK_TABLE, LAST_SUCCESSFUL_WATERMARK_COL, UPDATED_AT_COL

SOURCE_NAME_COL = "source_name"


def get_last_watermark():
        connection = get_connection()

        query = f"""
        SELECT {LAST_SUCCESSFUL_WATERMARK_COL}
        FROM {WATERMARK_TABLE};
        """
        with connection.cursor() as cursor:
                cursor.execute(query)
                last_successful_water_mark = cursor.fetchone()[0].strftime("%Y-%m-%d %H:%M:%S")
                return last_successful_water_mark


def update_watermark(new_watermark):
        connection = get_connection()
        print(new_watermark)

        query = f"""
        UPDATE {WATERMARK_TABLE}
        SET {LAST_SUCCESSFUL_WATERMARK_COL} = '{new_watermark}',
            {UPDATED_AT_COL} = CURRENT_TIMESTAMP;
        """        
        with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()



