import os
from tqdm import tqdm

import numpy as np
import pandas as pd
import sys
from pathlib import Path
from datetime import date


from config.config import TELECOM_CREATION_DATE, NULL, DATA_GENERATOR_OUTPUT_DIR, ID_COL, SUBSCRIPTIONS_RECORDS_FILE, REGISTRATION_DATE_COL, TERMINATION_DATE_COL, SEED, PHONE_NUMBER_COL, STATUS_COL, ACTIVE, RECHARGE_TRANSACTIONS_DIR, OFFER_CONFIG_ID_COL, PURCHASED_AT_COL, OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH, VALIDITY_DAYS_COL, SUBSCRIPTION_ID_COL

RECHARGE_TRANSACTIONS_DIR = Path(RECHARGE_TRANSACTIONS_DIR)

# Purchase channels
PURCHASE_CHANNEL_COL = "purchase_channel"
USSD = "USSD"
MOBILE_APP = "MOBILE_APP"
WEB = "WEB"
DEALDER = "DEALER"
PURCHASE_CHANNEL_PROBABILITIES = {USSD:0.55, MOBILE_APP: 0.25, WEB: 0.05, DEALDER:0.15}

# Payment methods
PAYMENT_METHOD_COL = "payment_method"
AIRTIME = "AIRTIME"
MOBILE_MONEY = "MOBILE_MONEY"
PAYMENT_METHOD_PROBABILITIES = {MOBILE_MONEY: 0.75, AIRTIME:0.25}

rng = np.random.default_rng(SEED)
TODAY = date.today().strftime("%Y-%m-%d")
DAILY_PURCHASE_RATE = 0.15

offer_configs_df = pd.read_csv(OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH)


subscriptions_df = pd.read_csv(SUBSCRIPTIONS_RECORDS_FILE, parse_dates=[REGISTRATION_DATE_COL, TERMINATION_DATE_COL])
print(subscriptions_df[REGISTRATION_DATE_COL].dtype)
print(subscriptions_df[TERMINATION_DATE_COL].dtype)


RECHARGE_TRANSACTIONS_DIR.mkdir(exist_ok=True)



print(subscriptions_df)





# Determine global date range
first_operational_date = subscriptions_df[REGISTRATION_DATE_COL].min()


last_operational_date = pd.Timestamp(TODAY)
# last_operational_date = pd.Timestamp("2023-12-31")


print(first_operational_date)
print(last_operational_date)
print(type(first_operational_date))
print(type(last_operational_date))


operational_dates = pd.date_range(
        start=first_operational_date,
        end=last_operational_date,
        freq="D"
)
print(operational_dates)


print(f"Generating purchases from {first_operational_date} to {last_operational_date} ({len(operational_dates)} days)")
# os.makedirs(RECHARGE_TRANSACTIONS_FOLDER, exist_ok=True)

cpt = 1
for current_date in tqdm(operational_dates):
        print(current_date)
        
        
        # Subscriptions that exist on this day
        active_subscriptions_mask = (
        ( subscriptions_df[REGISTRATION_DATE_COL] <= current_date) & 
        (subscriptions_df[TERMINATION_DATE_COL].isna() | (subscriptions_df[TERMINATION_DATE_COL] >= current_date)
                                                                            )
        )
        
        
        active_subscriptions_df = subscriptions_df.loc[active_subscriptions_mask]
        """if len(active_subscriptions_df) >= 10:
                print(active_subscriptions_df[[ID_COL, REGISTRATION_DATE_COL]].sort_values(ID_COL))
                exit()"""

        print(active_subscriptions_mask.sum())
        
        
        num_active = len(active_subscriptions_df)
        if num_active == 0:
                print("No active subscription")
                continue        
        
        # Generate the number of purchases for each subscription: they are in {0, 1, 2, ... N=? purchases}
        purchases_counts = rng.poisson(DAILY_PURCHASE_RATE, size = num_active)
        
        total_purchases = purchases_counts.sum()
        if total_purchases == 0:
                print("No purchase generated")
                continue

       
        purchases_df = active_subscriptions_df.loc[active_subscriptions_df.index.repeat(purchases_counts)]
        
        

        
        
        
        purchases_df.rename(columns={ID_COL:SUBSCRIPTION_ID_COL}, inplace = True)
        # purchases_df[SUBSCRIPTION_ID_COL] = purchases_df.index + 1

        
        
        
        
        # Generate a random time (in seconds) for each purchase of this day
        random_num_seconds = rng.integers(0,
                                      24 * 60 * 60, 
                                      size = len(purchases_df)
                                

        )
        purchases_df[PURCHASED_AT_COL] = (
                current_date + pd.to_timedelta(random_num_seconds, unit="seconds")
        )
        
        
        
        purchases_df[PAYMENT_METHOD_COL] = rng.choice(
                list(PAYMENT_METHOD_PROBABILITIES.keys()), size=len(purchases_df), p=list(PAYMENT_METHOD_PROBABILITIES.values())
                )
        
        purchases_df[PURCHASE_CHANNEL_COL] = rng.choice(
                list(PURCHASE_CHANNEL_PROBABILITIES.keys()),
                size=len(purchases_df),
                p=list(PURCHASE_CHANNEL_PROBABILITIES.values())
        )
        purchases_df[OFFER_CONFIG_ID_COL] = rng.integers(1, len(offer_configs_df)+1, size=len(purchases_df))
        # Sort by time
        purchases_df.sort_values(PURCHASED_AT_COL, inplace=True)
        
        purchases_df[ID_COL] = np.arange(cpt, cpt + len(purchases_df))

        

        invalid_mask = (
                purchases_df[PURCHASED_AT_COL].dt.normalize()
                < purchases_df[REGISTRATION_DATE_COL].dt.normalize()
        )
        

        if invalid_mask.any():
                print("*************************")
                print(purchases_df.loc[invalid_mask,
                                       [
                                               SUBSCRIPTION_ID_COL,
                                               REGISTRATION_DATE_COL,
                                               PURCHASED_AT_COL
                                       ]].head(20))
                print("+++++++++++++++++++++++")
                # exit()
                
                raise ValueError(
                        f"{invalid_mask.sum()} achats anyterieurs a la date danregistrement++++++++++"
                )
                
        # Keep only needed columns
        purchases_df = purchases_df[
                [       ID_COL,
                        SUBSCRIPTION_ID_COL,
                        OFFER_CONFIG_ID_COL,
                        PURCHASED_AT_COL,
                        PURCHASE_CHANNEL_COL,
                        PAYMENT_METHOD_COL
                ]
        ] 

        

        print(purchases_df)
        print("##########")
        
        file = RECHARGE_TRANSACTIONS_DIR / f"{current_date.strftime('%Y%m%d')}.parquet"
        # file = RECHARGE_TRANSACTIONS_DIR / f"{current_date.strftime('%Y%m%d')}.csv"
        purchases_df.to_parquet(file, index=False)
      

        """if active_subscriptions_mask.sum() >= 1000:
            
            print(active_subscriptions_df[REGISTRATION_DATE_COL].max())
            print(f"current date: {current_date}")
            
            print(active_subscriptions_df[REGISTRATION_DATE_COL].max())
            print(purchases_df[PURCHASED_AT_COL].min())
            
            # print(purchases_df)
            df = pd.read_parquet(file, index=False)
            
            print(df[PURCHASED_AT_COL].min()) 

            exit()"""
        
        cpt += len(purchases_df)

        if len(purchases_df) >= 1_000:
                # print(purchases_df[[ID_COL, SUBSCRIPTION_ID_COL, PURCHASED_AT_COL, REGISTRATION_DATE_COL]])
                exit()


exit()

