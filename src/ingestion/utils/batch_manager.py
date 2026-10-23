from config.config import BATCH_LOGS_TABLE, BATCH_STATUS_COL, RUNNING,SUCCES, BATCH_ID_COL, STARTED_AT, FINISHED_AT

def start_batch(connection):
        
        
        query = f"""
                INSERT INTO {BATCH_LOGS_TABLE} ({BATCH_STATUS_COL}) VALUES ('{RUNNING}') RETURNING {BATCH_ID_COL}, {STARTED_AT};
                """
        with connection.cursor() as cursor:
                cursor.execute(
                    query    
                )
                
                batch_num, started_at = cursor.fetchone()
                connection.commit()
                return batch_num, started_at

def complete_batch(connection, batch_id, terminaton_status = SUCCES):
        query = f"""
        UPDATE {BATCH_LOGS_TABLE} SET {BATCH_STATUS_COL} = '{terminaton_status}', {FINISHED_AT} = CURRENT_TIMESTAMP WHERE {BATCH_ID_COL} = {batch_id} RETURNING {FINISHED_AT};
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                    query    
                )
                finished_at = cursor.fetchone()[0]
                connection.commit()
                return finished_at
        



