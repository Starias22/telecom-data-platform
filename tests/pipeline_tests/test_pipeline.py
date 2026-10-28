from config.config import OFFERS_TABLE, TRX_DB_NAME, ID_COL, OFFER_CONFIGS_TABLE,START_DATE_COL, END_DATE_COL
from config.config import BUNDLE
from  src.utils.db_connector import get_connection

NAME_COL = "name"
TYPE_COL = "type"
PRICE_XOF_COL = "price_xof"
ID_COL = "id"
OFFER_ID_COL = "offer_id"
VALUE_XOF_COL = "value_xof"
VALIDITY_DAYS_COL = "validity_days"
BILLING_ID_COL = "billing_id"
import pandas as pd


def create_new_offer(connection, id = 100, name = "Forfait Maxi Appel + Internet 2000 F", type=BUNDLE, price=2_000):
        
        query = f"""
        INSERT INTO {OFFERS_TABLE} ({ID_COL}, {NAME_COL}, {TYPE_COL}, {PRICE_XOF_COL})
        VALUES (%s, %s, %s, %s);
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                        query, 
                        (id, name, type, price)
                        )
                connection.commit()

def create_new_offer_config(connection, id=1000, offer_id=100, value_xof=3000, billing_id=15, validity_days=7):
    query = f"""
        INSERT INTO {OFFER_CONFIGS_TABLE} ({ID_COL}, {OFFER_ID_COL}, {VALUE_XOF_COL}, {BILLING_ID_COL}, {VALIDITY_DAYS_COL})
        VALUES (%s, %s, %s, %s, %s);
        """
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(
                        query, 
                        (id, offer_id, value_xof, billing_id, validity_days)
                        )
        connection.commit()
    

def update_offer_by_name(connection, old_name, new_name):
    query = f"""
        UPDATE {OFFERS_TABLE}
        SET {NAME_COL} = %s
        WHERE {NAME_COL} = %s;
        """
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query,
                       (new_name, old_name) )
        connection.commit()
                        
        
def get_new_offer_created(connection, id):
      query = f"""
    SELECT * FROM {OFFERS_TABLE} WHERE id = {id};
        """
      print(query)
      with connection.cursor() as cursor:
            cursor.execute(query)
            resultset = cursor.fetchone()
            print(pd.DataFrame(resultset))

def get_new_offer_config_created(connection, id):
      query = f"""
    SELECT * FROM {OFFER_CONFIGS_TABLE} WHERE id = {id};
        """
      print(query)
      with connection.cursor() as cursor:
            cursor.execute(query)
            resultset = cursor.fetchone()
            print(pd.DataFrame(resultset))          


def roll_back_to_original_state_before_test_add_new_offer(connection, offer_config_id, offer_id):
      query = f"""
      DELETE FROM {OFFER_CONFIGS_TABLE} WHERE id = {offer_config_id};
      DELETE FROM {OFFERS_TABLE} WHERE id = {offer_id};
        """
      print(query)
      with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

def roll_back_to_original_state_before_test_update_offer(connection, old_name, new_name):
      query = f"""
        UPDATE {OFFERS_TABLE}
        SET {NAME_COL} = %s
        WHERE {NAME_COL} = %s;
        """
      print(query)
      with connection.cursor() as cursor:
        cursor.execute(query,
                       (old_name, new_name) )
        connection.commit()
def test_add_new_offer(connection):
    offer_config_id = 1000
    offer_id = 100
    roll_back_to_original_state_before_test_add_new_offer(connection, offer_config_id=offer_config_id, offer_id=offer_id)
    create_new_offer(connection=connection)
    create_new_offer_config(connection=connection)



def test_update_offer(connection):
  oldname = "Forfait Internet Volume 750 F"
  new_name = "Forfait Internet Volume Profit 750 F (Updated)"
  roll_back_to_original_state_before_test_update_offer(connection=connection, old_name=oldname, new_name=new_name)
  update_offer_by_name(connection, oldname, new_name)
  # SELECT * FROM dw.dim_offer WHERE offer_id = 22; CES ofres ont eeffevtivment ete mis a jour dans le dw

def update_offer_config(connection, offer_config_id):
    # Mettre un terme a cette oonfiguration doffre (set end_date = curenttimsetemp)
    query = f"""
        UPDATE {OFFER_CONFIGS_TABLE}
        SET {END_DATE_COL} = CURRENT_TIMESTAMP
        WHERE {ID_COL} = %s;
        """
    print(query)
    with connection.cursor() as cursor:
      cursor.execute(query,
      (offer_config_id, ) )
      connection.commit()

def roll_back_to_original_state_before_test_update_offer_config(connection, offer_config_id):
      query = f"""
        UPDATE {OFFER_CONFIGS_TABLE}
        SET {END_DATE_COL} = NULL
        WHERE {ID_COL} = %s;
        """
      print(query)
      with connection.cursor() as cursor:
        cursor.execute(query,
                       (offer_config_id,) )
        connection.commit()

def test_update_offer_config(connection):
  offer_config_id = 97
  roll_back_to_original_state_before_test_update_offer_config(connection=connection,offer_config_id=offer_config_id)
  update_offer_config(connection, offer_config_id=offer_config_id)
  # SELECT * FROM dw.dim_offer WHERE offer_config_id = 97;



      
if __name__ == "__main__":
        
        connection = get_connection(dbname=TRX_DB_NAME)
        """test_add_new_offer() # Passed

        
        test_update_offer(connection) # Passed
        """
        test_update_offer_config(connection) # Passed
        


        
        """get_new_offer_created(connection, id=offer_id)
        get_new_offer_config_created(connection, id=offer_config_id)"""
        
        

