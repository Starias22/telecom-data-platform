from config.config import BATCH_LOGS_TABLE, BATCH_STATUS_COL, RUNNING,SUCCES, BATCH_ID_COL, STARTED_AT, FINISHED_AT, BATCH_ERROR_MESSAGE_COL, PLATFORM_INITIALIZATION_NOT_DONE_OR_INCOMPLET, PLATFORM_INITIALIZATION_SUCCESSFUL, PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET
from datetime import date
from src.utils.db_connector import get_connection
from psycopg.errors import UndefinedTable

def start_batch():
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
                result = { "batch_id":batch_id,
                        #"started_at":started_at
                        }
                print(result)
                return batch_id
                
                return result

def complete_batch(batch_id, termination_status = SUCCES):
        connection = get_connection()
        query = f"""
        UPDATE {BATCH_LOGS_TABLE}
        SET {BATCH_STATUS_COL} = '{termination_status}',
            {FINISHED_AT} = CURRENT_TIMESTAMP
        WHERE {BATCH_ID_COL} = {batch_id}
        RETURNING {FINISHED_AT};
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                    query    
                )
                finished_at = cursor.fetchone()[0]
                connection.commit()
                return finished_at
        

def mark_batch_as_failed(batch_id, error_message):
        connection = get_connection()
        query = f"""
        UPDATE {BATCH_LOGS_TABLE}
        SET {BATCH_STATUS_COL} = %s,
            {BATCH_ERROR_MESSAGE_COL} = %s,
            {FINISHED_AT} = CURRENT_TIMESTAMP
        WHERE {BATCH_ID_COL} = {batch_id};
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                    query, ('FAILED', error_message,)    
                )
                # finished_at = cursor.fetchone()[0]
                connection.commit()
                # return finished_at

