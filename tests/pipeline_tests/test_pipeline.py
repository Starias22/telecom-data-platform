from config.config import OFFERS_TABLE, TRX_DB_NAME, ID_COL, OFFER_CONFIGS_TABLE
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
    
    pass


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

def roll_back_to_original_state(connection, offer_config_id, offer_id):
      query = f"""
      DELETE FROM {OFFER_CONFIGS_TABLE} WHERE id = {offer_config_id};
      DELETE FROM {OFFERS_TABLE} WHERE id = {offer_id};
        """
      print(query)
      with connection.cursor() as cursor:
            cursor.execute(query)
            connection.commit()

def test_add_new_offer():
    offer_config_id = 1000
    offer_id = 100
    roll_back_to_original_state(connection, offer_config_id=offer_config_id, offer_id=offer_id)
    create_new_offer(connection=connection)
    create_new_offer_config(connection=connection)
      
if __name__ == "__main__":
        
        connection = get_connection(dbname=TRX_DB_NAME)
        test_add_new_offer()

        
        """get_new_offer_created(connection, id=offer_id)
        get_new_offer_config_created(connection, id=offer_config_id)"""
        
        

