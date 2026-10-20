from tqdm import tqdm
import numpy as np
import pandas as pd
from pathlib import Path
from datetime import date
import shutil

from config.paths import SUBSCRIPTIONS_RECORDS_FILE, RECHARGE_TRANSACTIONS_DIR, OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH
from config.column_names import TERMINATION_DATE_COL, REGISTRATION_DATE_COL, ID_COL, START_DATE_COL, END_DATE_COL, SUBSCRIPTION_ID_COL, PURCHASED_AT_COL, OFFER_CONFIG_ID_COL, PAYMENT_METHOD_COL, PURCHASE_CHANNEL_COL
from config.config import SEED, PAYMENT_METHOD_PROBABILITIES, PURCHASE_CHANNEL_PROBABILITIES

# !!! Update it so rhat it will genarete daily chunks of parquet file 
def generate_purchases():
        dir = Path(RECHARGE_TRANSACTIONS_DIR)
        rng = np.random.default_rng(SEED)
        TODAY = date.today().strftime("%Y-%m-%d")
        DAILY_PURCHASE_RATE = 0.15

        offer_configs_df = pd.read_csv(OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH, parse_dates=[START_DATE_COL, END_DATE_COL])


        subscriptions_df = pd.read_csv(SUBSCRIPTIONS_RECORDS_FILE, parse_dates=[REGISTRATION_DATE_COL, TERMINATION_DATE_COL])
        print(subscriptions_df[REGISTRATION_DATE_COL].dtype)
        print(subscriptions_df[TERMINATION_DATE_COL].dtype)
        
        if dir.exists():
                shutil.rmtree(dir)

        dir.mkdir()
        print(subscriptions_df)


        # Determine global date range
        first_operational_date = subscriptions_df[REGISTRATION_DATE_COL].min()

        last_operational_date = pd.Timestamp(TODAY)


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
                
                
                active_subscriptions_mask = (
                ( subscriptions_df[REGISTRATION_DATE_COL] <= current_date) & 
                (subscriptions_df[TERMINATION_DATE_COL].isna() | (subscriptions_df[TERMINATION_DATE_COL] >= current_date)
                                                                                )
                )
                
                active_subscriptions_df = subscriptions_df.loc[active_subscriptions_mask]

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
                current_offer_configs_df = offer_configs_df[(offer_configs_df[START_DATE_COL] <=current_date) & (offer_configs_df[END_DATE_COL] >= current_date)]
                purchases_df[OFFER_CONFIG_ID_COL] = rng.choice(current_offer_configs_df[ID_COL].unique(), size=len(purchases_df))
                # Sort by time
                purchases_df.sort_values(PURCHASED_AT_COL, inplace=True)
                
                purchases_df[ID_COL] = np.arange(cpt, cpt + len(purchases_df))

                        
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
                
                file = dir / f"{current_date.strftime('%Y%m%d')}.parquet"
                # file = RECHARGE_TRANSACTIONS_DIR / f"{current_date.strftime('%Y%m%d')}.csv"
                purchases_df.to_parquet(file, index=False)
                
                cpt += len(purchases_df)

                if len(purchases_df) >= 1_000:
                        # print(purchases_df[[ID_COL, SUBSCRIPTION_ID_COL, PURCHASED_AT_COL, REGISTRATION_DATE_COL]])
                        return
