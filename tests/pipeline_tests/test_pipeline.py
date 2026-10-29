from datetime import datetime
import json
from pathlib import Path

from kafka import KafkaProducer

from config.config import KAFKA_SERVERS, KAFKA_TOPIC, OFFERS_TABLE, TRX_DB_NAME, ID_COL, OFFER_CONFIGS_TABLE,START_DATE_COL, END_DATE_COL, CUSTOMERS_TABLE
from config.config import BUNDLE
from  src.utils.db_connector import get_connection
from src.utils.utils import fmt_datetime

NAME_COL = "name"
TYPE_COL = "type"
PRICE_XOF_COL = "price_xof"
ID_COL = "id"
OFFER_ID_COL = "offer_id"
VALUE_XOF_COL = "value_xof"
VALIDITY_DAYS_COL = "validity_days"
BILLING_ID_COL = "billing_id"

CITY_COL = "city"
CUSTOMER_TYPE_COL = "customer_type"
GENDER_COL = "gender"
CUSTOMER_SEGMENT_COL = "customer_segment"
BIRTHDATE_COL = "birthdate"
TERMINATION_DATE_COL = "termination_date"
INDIVIDUAL = "INDIVIDUAL"
YOUTH = "YOUTH"

USSD = "USSD"
AIRTIME = "AIRTIME"
OFFER_CONFIG_ID_COL = "offer_config_id"
SUBSCRIPTION_ID_COL = "subscription_id"
PURCHASED_AT_COL = "purchased_at"
PURCHASE_CHANNEL_COL = "purchase_channel"
PAYMENT_METHOD_COL =  "payment_method"
PURCHASE_ID_COL = "purchase_id"
TIMESTAMP_COL = "timestamp"
SERVICE_TYPE_COL = "service_type"
DATA_MB_COL = "data_mb"
CALL_SECONDS_COL = "call_seconds"
SMS_COUNT_COL = "sms_count"
PURCHASE_DATA_DIR = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/purchases"
SEED = 1




import pandas as pd


import numpy as np
import pandas as pd


def generate_usage_events_for_purchase(
    purchase_id=10_000_000,
    subscription_id=9,
    purchased_at="2026-10-28 17:52:34",
    value_xof=1666,
    xof_per_mb=1,
    xof_per_sec=2,
    xof_per_sms=2,
    validity_days=7,
    seed=SEED
):
    rng = np.random.default_rng(seed)

    purchased_at = pd.Timestamp(purchased_at)
    validity_end = purchased_at + pd.Timedelta(days=validity_days)

    # Répartition aléatoire du prix entre DATA, VOICE et SMS.
    # À remplacer par les quotas réels si ceux-ci sont disponibles.
    allocations = rng.multinomial(100, [0.50, 0.30, 0.20])

    data_budget = value_xof * allocations[0] // 100
    voice_budget = value_xof * allocations[1] // 100
    sms_budget = value_xof - data_budget - voice_budget

    # Volumes maximaux estimés à partir des tarifs unitaires.
    max_data_mb = int(data_budget // xof_per_mb)
    max_call_seconds = int(voice_budget // xof_per_sec)
    max_sms_count = int(sms_budget // xof_per_sms)

    # Le client ne consomme qu'une fraction de chaque volume disponible.
    data_usage_pct = rng.uniform(0.20, 0.90)
    voice_usage_pct = rng.uniform(0.20, 0.90)
    sms_usage_pct = rng.uniform(0.20, 0.90)

    consumed_data_mb = int(max_data_mb * data_usage_pct)
    consumed_call_seconds = int(max_call_seconds * voice_usage_pct)
    consumed_sms_count = int(max_sms_count * sms_usage_pct)

    def distribute_quantity(total_quantity, max_events=10):
        """Répartit une quantité consommée entre plusieurs événements."""
        if total_quantity <= 0:
            return []

        n_events = int(rng.integers(1, min(max_events, total_quantity) + 1))

        # Chaque événement reçoit au moins une unité.
        quantities = (
            rng.multinomial(
                total_quantity - n_events,
                np.ones(n_events) / n_events
            ) + 1
        )

        return quantities.tolist()

    events = []

    service_usage = [
        ("DATA", consumed_data_mb, DATA_MB_COL),
        ("CALL", consumed_call_seconds, CALL_SECONDS_COL),
        ("SMS", consumed_sms_count, SMS_COUNT_COL),
    ]
    event_id = 50_000_000

    for service_type, total_quantity, quantity_field in service_usage:
        quantities = distribute_quantity(total_quantity)

        for quantity in quantities:
            # Date aléatoire comprise dans la période de validité.
            elapsed_seconds = rng.integers(
                0,
                max(1, int((validity_end - purchased_at).total_seconds()))
            )

            event_time = purchased_at + pd.Timedelta(
                seconds=int(elapsed_seconds)
            )

            event = {
                ID_COL:event_id,
                PURCHASE_ID_COL: purchase_id,
                SUBSCRIPTION_ID_COL:subscription_id,
                TIMESTAMP_COL: datetime.fromtimestamp(event_time.timestamp()).isoformat(),
                SERVICE_TYPE_COL: service_type,
                DATA_MB_COL: 0,
                CALL_SECONDS_COL: 0,
                SMS_COUNT_COL: 0,
            }

            event[quantity_field] = quantity
            event = {key:value for key, value in event.items() if value !=0 }
            events.append(event)
            event_id += 1

    # Trier les evenements par timestamp
    events.sort(key=lambda event:event[TIMESTAMP_COL])
    print(events)

    return events

def produce_usage_events(events):
     producer = KafkaProducer(
          bootstrap_servers = KAFKA_SERVERS,
          key_serializer=lambda key:str(key).encode("utf-8"),
          value_serializer=lambda value:json.dumps(value).encode("utf-8")
        )     
     
     """events =  [
                {k:v for k, v in record.items() if pd.notna(v)} for record in events
        ]"""
     for record in events:
        print(record)
        producer.send(
                        KAFKA_TOPIC,
                        key = record[SUBSCRIPTION_ID_COL],
                        value=record)
     producer.flush()

def get_test_service_usage_batches():
        events = generate_usage_events_for_purchase()
        firt_batch_events = events[:5]
        second_batch_events = events[5:10]
        third_batch_events = events[10:]
        return firt_batch_events, second_batch_events, third_batch_events
        

def create_new_customer(connection, id, city ="Covè", customer_type=INDIVIDUAL, gender="M",  customer_segment=YOUTH, birthdate="2002-06-13"):
        
        query = f"""
        INSERT INTO {CUSTOMERS_TABLE} ({ID_COL}, {CITY_COL}, {CUSTOMER_TYPE_COL}, {GENDER_COL}, {CUSTOMER_SEGMENT_COL}, {BIRTHDATE_COL})
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        print(query)
        with connection.cursor() as cursor:
                cursor.execute(
                        query, 
                        (id, city, customer_type, gender, customer_segment, birthdate)
                        )
                connection.commit()

def create_new_offer(connection, id, name = "Forfait Maxi Appel + Internet 2000 F", type=BUNDLE, price=2_000):
        
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
                        

def update_customer_scd1_attribute(connection, customer_id, new_gender):
    query = f"""
        UPDATE {CUSTOMERS_TABLE}
        SET {GENDER_COL} = %s
        WHERE {ID_COL} = %s;
        """
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query,
                       (new_gender, customer_id) )
        connection.commit()

def update_customer_scd2_attribute(connection, customer_id, new_city):
    query = f"""
        UPDATE {CUSTOMERS_TABLE}
        SET {CITY_COL} = %s 
        WHERE {ID_COL} = %s;
        """
    print(query)
    with connection.cursor() as cursor:
        cursor.execute(query,
                       (new_city, customer_id) )
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

def roll_back_to_original_state_before_test_create_new_customer(connection, customer_id):
      query = f"""
      DELETE FROM {CUSTOMERS_TABLE} WHERE id = {customer_id};
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

def test_update_customer_scd1_attribute(connection):
  customer_id = 7
  old_gender = "F"
  new_gender = "M"
  roll_back_to_original_state_before_test_customer_scd1_attribute(connection=connection, customer_id=customer_id, old_gender=old_gender)
  update_customer_scd1_attribute(connection, customer_id=customer_id, new_gender=new_gender)
  # SELECT * FROM crm.customers WHERE id = 7;
  # SELECT * FROM dw.dim_customer WHERE customer_id = 7;


def test_update_customer_scd2_attribute(connection):
  customer_id = 7
  old_city = "Djougou"
  new_city = "Pobè"
  
  roll_back_to_original_state_before_test_customer_scd2_attribute(connection=connection, customer_id=customer_id, old_city=old_city)
  update_customer_scd2_attribute(connection, customer_id=customer_id, new_city=new_city)
  # SELECT * FROM crm.customers WHERE id = 7;
  # SELECT * FROM dw.dim_customer WHERE customer_id = 7;  -- Two versions of customers in the dw with the old oone out to date and the new one current;


def roll_back_to_original_state_before_test_customer_scd2_attribute(connection, customer_id, old_city):
      query = f"""
        UPDATE {CUSTOMERS_TABLE}
        SET {CITY_COL} = %s
        WHERE {ID_COL} = %s;
        """
      print(query)
      with connection.cursor() as cursor:
        cursor.execute(query,
                       (old_city, customer_id) )
        connection.commit()

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

def roll_back_to_original_state_before_test_customer_scd1_attribute(connection, customer_id, old_gender):
      query = f"""
        UPDATE {CUSTOMERS_TABLE}
        SET {GENDER_COL} = %s
        WHERE {ID_COL} = %s;
        """
      print(query)
      with connection.cursor() as cursor:
        cursor.execute(query,
                       (old_gender, customer_id) )
        connection.commit()

def test_update_offer_config(connection):
  offer_config_id = 97
  roll_back_to_original_state_before_test_update_offer_config(connection=connection,offer_config_id=offer_config_id)
  update_offer_config(connection, offer_config_id=offer_config_id)
  # SELECT * FROM dw.dim_offer WHERE offer_config_id = 97;


def test_add_new_customer(connection):
    customer_id = 10_000_000
    roll_back_to_original_state_before_test_create_new_customer(connection, customer_id=customer_id)
    create_new_customer(connection=connection, id=customer_id)
    # SELECT * FROM dw.dim_customer WHERE customer_id = 10000000;
    

def test_purchase_an_offer():
     purchase_id = 10_000_000
     subscription_id = 9
     ofer_config_id = 97
     purchased_at = "2026-10-20 15:45:18"
     purchased_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
     purchase_channel = USSD
     payment_method = AIRTIME
     purchase_df = pd.DataFrame({
          ID_COL:[purchase_id],
          SUBSCRIPTION_ID_COL:[subscription_id],
          OFFER_CONFIG_ID_COL:[ofer_config_id],
          PURCHASED_AT_COL:[purchased_at],
          PURCHASE_CHANNEL_COL:[purchase_channel],
          PAYMENT_METHOD_COL:[payment_method]
          })
     print(purchase_df)
     date_part = fmt_datetime(purchased_at)
     print(date_part)
     file_name = f"{date_part}.parquet"
     file_path = Path(PURCHASE_DATA_DIR) / file_name
     print(file_name)
     print(file_path)
     purchase_df.to_parquet(file_path)
     # SELECT * FROM dw.fact_purchase WHERE purchase_id = 10000000; -- The purchase is effectively loaded into the DW
     # SELECT dc.customer_id, s.id AS subscription_id  FROM dw.dim_customer AS dc JOIN staging.subscriptions AS s ON s.customer_id = dc.customer_id WHERE customer_key = 1189472 -- Verifier que ca correspond effecivement au bon customer

    

    
    
def test_usage_events_accross_multiple_days(batch_1):
     produce_usage_events(batch_1)
     
      
if __name__ == "__main__":
        
        connection = get_connection(dbname=TRX_DB_NAME)
        """test_add_new_offer() # Passed

        
        test_update_offer(connection) # Passed
        
        test_update_offer_config(connection) # Passed
        
        test_add_new_customer(connection) # Passed
        test_update_customer_scd2_attribute(connection) # Passed        
        
        test_update_customer_scd2_attribute(connection) # Passed  

        test_update_customer_scd1_attribute(connection) # Passed
        test_purchase_an_offer() # Passed
        """  
        b1, b2, b3 = get_test_service_usage_batches()

        print("Batch 1")
        print(pd.DataFrame(b1))
        test_usage_events_accross_multiple_days(b1) # Passed

        """print("Batch 2")
        print(pd.DataFrame(b2))

        print("Batch 3")
        print(pd.DataFrame(b3))"""
        
        


        
        """get_new_offer_created(connection, id=offer_id)
        get_new_offer_config_created(connection, id=offer_config_id)"""
        
        

