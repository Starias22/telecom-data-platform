from config.config import BATCH_LOGS_TABLE, BATCH_STATUS_COL, RUNNING,SUCCES, BATCH_ID_COL, STARTED_AT, COMPLETED_AT, BATCH_ERROR_MESSAGE_COL
from src.utils.db_connector import get_connection
from src.utils.platform_manager import mark_platform_initialized

from src.utils.logger import get_logger

logger = get_logger(__name__)

def start_batch():
        logger.info("Starting batch")
        connection = get_connection()
        query = f"""
                INSERT INTO {BATCH_LOGS_TABLE} ({BATCH_STATUS_COL}) VALUES ('{RUNNING}') RETURNING {BATCH_ID_COL}, {STARTED_AT};
                """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                    query    
                )
                
                batch_id= cursor.fetchone()[0]
                
                connection.commit()
                logger.info(f"Batch {batch_id} started")
                
                return batch_id
        
        

def complete_batch(batch_id, termination_status = SUCCES, platform_initialization=None):

        logger.info(f"Completing batch {batch_id}")
        connection = get_connection()
        query = f"""
        UPDATE {BATCH_LOGS_TABLE}
        SET {BATCH_STATUS_COL} = '{termination_status}',
            {COMPLETED_AT} = CURRENT_TIMESTAMP
        WHERE {BATCH_ID_COL} = {batch_id}
        RETURNING {COMPLETED_AT};
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                    query    
                )
                finished_at = cursor.fetchone()[0]
                connection.commit()
        if platform_initialization:
                mark_platform_initialized(connection)
        logger.info(
                f"Batch {batch_id} completed"
                )                
        return finished_at
        

def mark_batch_as_failed(batch_id, error_message):
        connection = get_connection()
        query = f"""
        UPDATE {BATCH_LOGS_TABLE}
        SET {BATCH_STATUS_COL} = %s,
            {BATCH_ERROR_MESSAGE_COL} = CONCAT_WS(%s::TEXT, {BATCH_ERROR_MESSAGE_COL}, %s::TEXT),
            {COMPLETED_AT} = CURRENT_TIMESTAMP
        WHERE {BATCH_ID_COL} = %s;
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                    query, 
                    (
                            'FAILED',
                             ' && ',
                               error_message,
                               batch_id)    
                )
                # finished_at = cursor.fetchone()[0]
                connection.commit()
                logger.info(f"Batch {batch_id} marked as failed")

if __name__ == "__main__":
        batch_id = 20
        error_message = "An errror occured"
        # mark_batch_as_failed(batch_id, error_message)
        start_batch()
        start_batch(incremental=False)