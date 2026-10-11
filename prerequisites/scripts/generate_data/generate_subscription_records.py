from datetime import date
from pathlib import Path
import sys
from dateutil.relativedelta import relativedelta
import os
import numpy as np
import pandas as pd


from config.config import SEED, PHONE_NUMBER_COL, STATUS_COL, REGISTRATION_DATE_COL, TERMINATION_DATE_COL, ACTIVE, INACTIVE, SUSPENDED, TERMINATED, ID_COL, SUBSCRIPTION_STATUS_PROBABILITIES, NUM_CUSTOMERS, CUSTOMER_RECORDS_FILE, DATA_GENERATOR_OUTPUT_DIR, SUBSCRIPTIONS_RECORDS_FILE, CUSTOMER_ID_COL


phone_number = "32619691"

PHONE_NUMBER_PREFIX_SETTING_DATE = "2025-01-01" # ?? Search on Google and change later

rng = np.random.default_rng(SEED)


subsription_counts = rng.choice(
        [1, 2, 3, 4, 5], p=[0.85, 0.12, 0.025, 0.004, 0.001], size=NUM_CUSTOMERS)

subsriptions_num = sum(subsription_counts)
print(subsription_counts)
print(f"Total Number of subscriptions: {subsriptions_num}")
customer_ids = np.arange(1, NUM_CUSTOMERS + 1)
print(customer_ids)

subscription_customer_ids = np.repeat(customer_ids, subsription_counts)

# Shuffle
rng.shuffle(subscription_customer_ids)
print(subscription_customer_ids)

assert len(subscription_customer_ids) == subsriptions_num


telecom_prefixes = [30, 32, 34, 36, 38, 70, 72, 74]  # Les prefixes de numeros de loperateur telecom
phone_numbers_pool = []
for prefix in telecom_prefixes:
        start = int(str(prefix) + 6*"0")
        end = int(str(prefix) + 6*"9")+1 # In order to include the last one
        phone_numbers_pool.extend(np.arange(start, end))
        

assert len(phone_numbers_pool) == len(telecom_prefixes) * (10**6)
print(phone_numbers_pool[-1])

phone_numbers =rng.choice(phone_numbers_pool, size=subsriptions_num, replace=False)

subsriptions_df = pd.DataFrame()


subsriptions_df[PHONE_NUMBER_COL] = phone_numbers.astype(str)

subsriptions_df[CUSTOMER_ID_COL] = subscription_customer_ids
subsriptions_df[STATUS_COL] = rng.choice(list(SUBSCRIPTION_STATUS_PROBABILITIES.keys()), p=list(SUBSCRIPTION_STATUS_PROBABILITIES.values()), size=subsriptions_num)

TODAY = date.today()

CUSTOMER_REGISTRATION_DATE_COL = "customer_registration_date"

customers_df = pd.read_csv(CUSTOMER_RECORDS_FILE, usecols=[ID_COL, REGISTRATION_DATE_COL]).rename(columns={REGISTRATION_DATE_COL:CUSTOMER_REGISTRATION_DATE_COL})
print(customers_df)

subsriptions_df = subsriptions_df.merge(customers_df, left_on=CUSTOMER_ID_COL, right_on=ID_COL)
print(subsriptions_df)



# Subscription registration date
mins_subscription_registration_date = pd.to_datetime(subsriptions_df[CUSTOMER_REGISTRATION_DATE_COL])
max_subscription_registration_date = pd.Timestamp(TODAY)
subscription_registration_days_range_max_day = (max_subscription_registration_date - mins_subscription_registration_date).dt.days
print(subscription_registration_days_range_max_day)

subscription_registration_dates = mins_subscription_registration_date + pd.to_timedelta(
rng.integers(0, (max_subscription_registration_date - mins_subscription_registration_date).dt.days +1, size=subsriptions_num), unit="days")
print(subscription_registration_dates)
subsriptions_df[REGISTRATION_DATE_COL] = subscription_registration_dates.dt.strftime("%Y-%m-%d")



# Customer termination date
terminated_subscriptions_mask = subsriptions_df[STATUS_COL] == TERMINATED
min_termination_dates = subscription_registration_dates[terminated_subscriptions_mask]
max_termination_date = pd.Timestamp(TODAY)
termination_dates = pd.Series(min_termination_dates +  pd.to_timedelta(rng.integers(0, (max_termination_date - min_termination_dates).dt.days +1), unit="days"))
subsriptions_df.loc[terminated_subscriptions_mask, TERMINATION_DATE_COL] = termination_dates.dt.strftime("%Y-%m-%d")

# Unique ids
subsriptions_df[ID_COL] = subsriptions_df.index + 1

print(subsriptions_df)
 
# Save subscription records to CSV
subsriptions_df = subsriptions_df[[ID_COL, PHONE_NUMBER_COL, CUSTOMER_ID_COL, REGISTRATION_DATE_COL, STATUS_COL, TERMINATION_DATE_COL]]
print(subsriptions_df)
os.makedirs(DATA_GENERATOR_OUTPUT_DIR, exist_ok=True)
print("Saving subscription records to CSV file")
subsriptions_df.to_csv(SUBSCRIPTIONS_RECORDS_FILE, index=False)
print("Done")





