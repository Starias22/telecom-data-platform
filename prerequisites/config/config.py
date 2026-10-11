from pathlib import Path
import pandas as pd
from glob import glob


CUSTOMER_ID_COL = "customer_id"

NULL = None
TELECOM_CREATION_DATE = "2020-05-18"
NUM_CUSTOMERS = 5_000_000
ID_COL = "id"
GENDER_COL = "gender"
BIRTHDATE_COL = "birthdate"
PHONE_NUMBER_COL = "phone_number"
CITY_COL = "city"
CUSTOMER_TYPE_COL = "customer_type"
CUSTOMER_SEGMENT_COL =  "customer_segment"


TYPE_COL = "type"

MOBILE = "MOBILE"
BUNDLE = "BUNDLE"
DATA = "DATA"

VALUE_XOF_COL = "value_xof"
VALUE_MB_COL = "value_mb"

XOF_PER_SEC_COL = "xof_per_sec"
XOF_PER_SMS_COL = "xof_per_sms"
XOF_PER_MB_COL = "xof_per_mb"
IS_LIMITLESS_COL = "is_limitless"


SUBSCRIPTION_ID_COL = "subscription_id"

REGISTRATION_DATE_COL = "registration_date"
TERMINATION_DATE_COL = "termination_date"

STATUS_COL = "status"
OFFER_ID_COL = "offer_id"
BILLING_ID_COL = "billing_id"
START_DATE_COL = "start_date"
END_DATE_COL = "end_date"
OFFER_CONFIG_ID_COL = "offer_config_id"
PURCHASED_AT_COL = "purchased_at"
VALIDITY_DAYS_COL = "validity_days"




ACTIVE =  "ACTIVE"
INACTIVE = "INACTIVE"
SUSPENDED = "SUSPENDED"
TERMINATED = "TERMINATED"



MALE = "M"
FEMALE = "F"


DATA_GENERATOR_OUTPUT_DIR = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/"
CUSTOMER_RECORDS_FILE = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/customers.csv"
SUBSCRIPTIONS_RECORDS_FILE = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/subscriptions.csv"

CUSTOMER_RECORDS_SOURCES_FILE = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/customers.csv"
SUBSCRIPTIONS_RECORDS_SOURCES_FILE = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/subscriptions.csv"

SOURCES_DIR = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/"

SEED = 0

BUSINESS = "BUSINESS"

INDIVIDUAL = "INDIVIDUAL"
SME = "SME"
# CORPORATE = "CORPORATE"

CUSTOMER_TYPE_PROBABILITIES ={
        INDIVIDUAL:0.90,
        BUSINESS:0.10
}



STANDARD = "STANDARD"
YOUTH = "YOUTH"
PREMIUM = "PREMIUM"
SME = "SME"

CUSTOMER_SEGMENT_PROBABILITIES ={
        INDIVIDUAL: {
                STANDARD: 0.60,
                YOUTH: 0.25,
                PREMIUM: 0.15
        },
        BUSINESS: {
                SME: 0.85,
                PREMIUM: 0.15
        }

}




CITY_PROBABILITIES = {
    "Cotonou": 0.25,
    "Porto-Novo": 0.10,
    "Abomey-Calavi": 0.15,
    "Parakou": 0.08,
    "Djougou": 0.04,
    "Bohicon": 0.04,
    "Abomey": 0.03,
    "Natitingou": 0.03,
    "Ouidah": 0.03,
    "Lokossa": 0.025,
    "Savalou": 0.02,
    "Kandi": 0.02,
    "Malanville": 0.010,
    "Sakété": 0.015,
    "Pobè": 0.015,
    "Aplahoué": 0.015,
    "Azovè": 0.01,
    "Comè": 0.01,
    "Grand-Popo": 0.005,
    "Allada": 0.01,
    "Ketou": 0.01,
    "Nikki": 0.01,
    "Bassila": 0.01,
    "Bembèrèkè": 0.01,
    "Tanguiéta": 0.01,
    "Banikoara": 0.01,
    "Covè": 0.005,
    "Dassa-Zoumè": 0.01,
    "Savè": 0.01,
    "Tchaourou": 0.01
}

"""def str_to_date_object(date_str:str)-> date:
        year, month, day_num = [int(i) for i in date_str.split("-")]
        return date(year=year, month=month, day=day_num)

def str_format_date(date_object:date) -> str:
        return date_object.strftime("%Y-%m-%d")"""


CUSTOMER_STATUS_PROBABILITIES = {

ACTIVE:0.90,
INACTIVE:0.07,
SUSPENDED:0.02,
TERMINATED:0.01
}

SUBSCRIPTION_STATUS_PROBABILITIES = {
ACTIVE:0.85,
SUSPENDED:0.07,
INACTIVE:0.05,
TERMINATED:0.03
}
CUSTOMERS_MIN_AGE = 15

RECHARGE_TRANSACTIONS_DIR = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/purchases"

OFFERS_CATALOG_DIR = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/offers_catalog/"
OFFER_RECORDS_CSV_FILE_PATH = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/offers_catalog/offers.csv"

BILLING_RECORDS_CSV_FILE_PATH = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/offers_catalog/offer_billings.csv"
OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/clean/offers_catalog/offer_configurations.csv"

SUBSCRIPTIONS_DIR = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/prerequisites/outputs/sources/subscriptions/"


TIMESTAMP_MILLISECONDS_COL = "timestamp"

DATA_USAGE_COL = "data_usage"
CALLS_USAGE_COL = "calls_usage"
SMS_USAGE_COL = "sms_usage"
PURCHASE_ID_COL = "purchase_id"

DATA_MB_COL = "data_mb"
SMS_COUNT_COL = "sms_count"
CALL_SECONDS_COL = "call_seconds"

SERVICE_TYPE_COL = "service_type"
CALL = "CALL"
SMS = "SMS"

def get_purchase_details():

        recharge_transaction_files = glob(f"{RECHARGE_TRANSACTIONS_DIR}/*")

        offers_df = pd.read_csv(OFFER_RECORDS_CSV_FILE_PATH)

        print(offers_df)

        billings_df = pd.read_csv(BILLING_RECORDS_CSV_FILE_PATH)
        offer_configs_df = pd.read_csv(OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH)

        offer_configs_df = offer_configs_df.merge(offers_df, left_on=OFFER_ID_COL, right_on=ID_COL)


        print(offer_configs_df)


        print(offer_configs_df)
        print(offer_configs_df.columns)
        print(offer_configs_df.index)
        billings_df.index +=1
        print(billings_df)

        offer_configs_df = offer_configs_df.join(billings_df, how='left', on=BILLING_ID_COL, lsuffix='_x', rsuffix='_y')
        offer_configs_df.index += 1
        print(offer_configs_df)
        print(offer_configs_df.columns)


        # drop OFFER_ID_COL BILLING_ID_COL 'id'(billing id) 'id_y'(offer id) 'name' 
        offer_configs_df.drop(columns=[OFFER_ID_COL, BILLING_ID_COL, ID_COL, f"{ID_COL}_y", f"{START_DATE_COL}_y", f"{END_DATE_COL}_y"], inplace=True)
        # Rename id_x to id(config id)
        offer_configs_df.rename(columns={f"{ID_COL}_x": ID_COL}, inplace=True)

        print(offer_configs_df)
        print(offer_configs_df.columns)




        # purchases_df = pd.concat([pd.read_csv(file, parse_dates=[PURCHASED_AT_COL]) for file in  recharge_transaction_files ])
        purchases_df = pd.concat([pd.read_parquet(file) for file in  recharge_transaction_files ])

        print(purchases_df)
        

        purchases_df = pd.merge(purchases_df, offer_configs_df, left_on=OFFER_CONFIG_ID_COL, right_on=ID_COL).drop(columns=OFFER_CONFIG_ID_COL).rename(columns = {f"{ID_COL}_x":PURCHASE_ID_COL})


        print(purchases_df)
        print(purchases_df.columns)

        purchases_df = purchases_df[
                [
                PURCHASE_ID_COL,
                SUBSCRIPTION_ID_COL,
                PURCHASED_AT_COL,
                VALUE_XOF_COL,
                VALUE_MB_COL,
                TYPE_COL,
                VALIDITY_DAYS_COL,
                IS_LIMITLESS_COL,
                XOF_PER_SEC_COL,
                XOF_PER_SMS_COL,
                XOF_PER_MB_COL
                ]
                ]
        print(purchases_df)
        
        
        return purchases_df