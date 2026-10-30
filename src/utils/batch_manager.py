from config.config import BATCH_LOGS_TABLE, BATCH_STATUS_COL, RUNNING,SUCCES, BATCH_ID_COL, STARTED_AT, COMPLETED_AT, BATCH_ERROR_MESSAGE_COL, PLATFORM_INITIALIZATION_NOT_DONE_OR_INCOMPLET, PLATFORM_INITIALIZATION_SUCCESSFUL, PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET, BATCH_TYPE_COL
from datetime import date
from src.utils.db_connector import get_connection
from src.utils.platform_manager import mark_platform_initialized
from psycopg.errors import UndefinedTable

def start_batch(incremental=True):
        connection = get_connection()
        x = "INCREMENTAL" if incremental else "INITIAL"
        query = f"""
                INSERT INTO {BATCH_LOGS_TABLE} ({BATCH_TYPE_COL}, {BATCH_STATUS_COL}) VALUES ('{"INCREMENTAL" if incremental else "INITIAL"}', '{RUNNING}') RETURNING {BATCH_ID_COL}, {STARTED_AT};
                """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                    query    
                )
                
                batch_id= cursor.fetchone()[0]
                
                connection.commit()
                result = { "batch_id":batch_id,
                        #"started_at":started_at
                        }
                print(result)
                return batch_id
        
        

def complete_batch(batch_id, termination_status = SUCCES, platform_initialization=None):
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
                # return finished_at

if __name__ == "__main__":
        batch_id = 20
        error_message = "An errror occured"
        # mark_batch_as_failed(batch_id, error_message)
        start_batch()
        start_batch(incremental=False)