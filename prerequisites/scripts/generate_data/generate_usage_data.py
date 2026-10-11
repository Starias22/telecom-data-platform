import os
from pathlib import Path
from glob import glob
import pandas as pd
import numpy as np
import json



from config.config import RECHARGE_TRANSACTIONS_DIR, BILLING_RECORDS_CSV_FILE_PATH, OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH, OFFER_ID_COL, ID_COL, BILLING_ID_COL, START_DATE_COL, END_DATE_COL,  OFFER_CONFIG_ID_COL, PURCHASED_AT_COL, VALIDITY_DAYS_COL, SEED, TYPE_COL, DATA, VALUE_XOF_COL, VALUE_MB_COL, OFFER_RECORDS_CSV_FILE_PATH, BUNDLE, MOBILE, XOF_PER_SEC_COL, XOF_PER_SMS_COL, XOF_PER_MB_COL, SUBSCRIPTION_ID_COL, DATA_GENERATOR_OUTPUT_DIR, IS_LIMITLESS_COL, CUSTOMER_RECORDS_FILE, PHONE_NUMBER_COL, CUSTOMER_ID_COL, SUBSCRIPTIONS_RECORDS_FILE, TIMESTAMP_MILLISECONDS_COL, DATA_USAGE_COL, CALLS_USAGE_COL, SMS_USAGE_COL, PURCHASE_ID_COL, SMS_COUNT_COL, DATA_MB_COL, CALL_SECONDS_COL, SERVICE_TYPE_COL, CALL, SMS, get_purchase_details

rng = np.random.default_rng(SEED)



purchases_df = get_purchase_details()

print(purchases_df)
print(purchases_df.columns)



print(purchases_df[VALIDITY_DAYS_COL])
print(purchases_df[PURCHASED_AT_COL].dtype)

print(purchases_df[VALIDITY_DAYS_COL].dtype)

bundle_mask = purchases_df[TYPE_COL] == BUNDLE
print(bundle_mask.sum())
purchases_df.loc[bundle_mask, DATA_USAGE_COL] = rng.integers(0, 100 + 1, size=bundle_mask.sum())
purchases_df.loc[bundle_mask, CALLS_USAGE_COL] = rng.integers(0, 100 - purchases_df.loc[bundle_mask, DATA_USAGE_COL] + 1)



purchases_df.loc[bundle_mask, DATA_USAGE_COL] = ((purchases_df.loc[bundle_mask, DATA_USAGE_COL] / 100) * purchases_df.loc[bundle_mask, VALUE_XOF_COL]).astype(int)
purchases_df.loc[bundle_mask, CALLS_USAGE_COL] = ((purchases_df.loc[bundle_mask, CALLS_USAGE_COL] / 100) * purchases_df.loc[bundle_mask, VALUE_XOF_COL]).astype(int)
purchases_df.loc[bundle_mask, SMS_USAGE_COL] = purchases_df.loc[bundle_mask, VALUE_XOF_COL] - purchases_df.loc[bundle_mask, DATA_USAGE_COL] - purchases_df.loc[bundle_mask, CALLS_USAGE_COL]

# Data usage in MB, Call usage in seconds, SMS usage (number of SMS sent)
purchases_df.loc[bundle_mask, DATA_USAGE_COL] = (purchases_df.loc[bundle_mask, DATA_USAGE_COL] / purchases_df.loc[bundle_mask, XOF_PER_MB_COL]).astype(int)
purchases_df.loc[bundle_mask, CALLS_USAGE_COL] = (purchases_df.loc[bundle_mask, CALLS_USAGE_COL] / purchases_df.loc[bundle_mask, XOF_PER_SEC_COL]).astype(int)
purchases_df.loc[bundle_mask, SMS_USAGE_COL] = (purchases_df.loc[bundle_mask, SMS_USAGE_COL] / purchases_df.loc[bundle_mask, XOF_PER_SMS_COL]).astype(int)

print(purchases_df[bundle_mask])


mobile_mask = purchases_df[TYPE_COL] == MOBILE
print(mobile_mask.sum())
purchases_df.loc[mobile_mask, CALLS_USAGE_COL] = rng.integers(0, 100 + 1, size=mobile_mask.sum())
# purchases_df.loc[mobile_mask, SMS_USAGE_PERCENT_COL] = 100  - purchases_df.loc[mobile_mask, CALLS_USAGE_PERCENT_COL]
purchases_df.loc[mobile_mask, CALLS_USAGE_COL] = ((purchases_df.loc[mobile_mask, CALLS_USAGE_COL] / 100) * purchases_df.loc[mobile_mask, VALUE_XOF_COL]).astype(int)
purchases_df.loc[mobile_mask, SMS_USAGE_COL] = purchases_df.loc[mobile_mask, VALUE_XOF_COL] - purchases_df.loc[mobile_mask, CALLS_USAGE_COL]

purchases_df.loc[mobile_mask, CALLS_USAGE_COL] = (purchases_df.loc[mobile_mask, CALLS_USAGE_COL] / purchases_df.loc[mobile_mask, XOF_PER_SEC_COL]).astype(int)
purchases_df.loc[mobile_mask, SMS_USAGE_COL] = (purchases_df.loc[mobile_mask, SMS_USAGE_COL] / purchases_df.loc[mobile_mask, XOF_PER_SMS_COL]).astype(int)
print(purchases_df)


maxi_mask = bundle_mask | mobile_mask

print(purchases_df[maxi_mask])

data_mask = purchases_df[TYPE_COL] == DATA


purchases_df.loc[data_mask, DATA_USAGE_COL] = rng.integers(0, purchases_df.loc[data_mask, VALUE_MB_COL])

print(purchases_df[data_mask])

not_used_purchase_mask = (
        data_mask & (purchases_df[DATA_USAGE_COL] == 0) |
        (mobile_mask & (purchases_df[CALLS_USAGE_COL] == 0)  & (purchases_df[SMS_USAGE_COL] == 0) ) |
        (bundle_mask & (purchases_df[CALLS_USAGE_COL] == 0) & (purchases_df[SMS_USAGE_COL] == 0) & (purchases_df[DATA_USAGE_COL] == 0)) 
) 

print(purchases_df.loc[not_used_purchase_mask])

# Considérer uniquement les achats qui ont été utilisés (ne serait-ce qu'un tout petit peu)
purchases_df = purchases_df.loc[~not_used_purchase_mask]

print(purchases_df)
not_used_purchase_mask = (
        data_mask & (purchases_df[DATA_USAGE_COL] == 0) |
        (mobile_mask & (purchases_df[CALLS_USAGE_COL] == 0)  & (purchases_df[SMS_USAGE_COL] == 0) ) |
        (bundle_mask & (purchases_df[CALLS_USAGE_COL] == 0) & (purchases_df[SMS_USAGE_COL] == 0) & (purchases_df[DATA_USAGE_COL] == 0)) 
) 
print(not_used_purchase_mask.sum())



# Mettre a jour les masques (puisque les achats qui n'ont pas été utilisés du tout ont été supprimés)

mobile_mask = purchases_df[TYPE_COL] == MOBILE
data_mask = purchases_df[TYPE_COL] == DATA
bundle_mask = purchases_df[TYPE_COL] == BUNDLE

maxi_mask = bundle_mask | mobile_mask

data_usage_mask = (data_mask | bundle_mask) & (purchases_df[DATA_USAGE_COL] != 0)
call_usage_mask = (maxi_mask) & (purchases_df[CALLS_USAGE_COL] != 0)
sms_usage_mask = (maxi_mask) & (purchases_df[SMS_USAGE_COL] != 0)

call_usage_events_counts = rng.integers(
        1, 
        np.minimum(purchases_df.loc[call_usage_mask, CALLS_USAGE_COL], 5 # !!! Faire varier le 5 plus tard (le rendre aleatoire)
) + 1 )

sms_usage_events_counts = rng.integers(
        1, 
        np.minimum(purchases_df.loc[sms_usage_mask, SMS_USAGE_COL], 5 # !!! Faire varier le 5 plus tard (le rendre aleatoire)
) + 1 )

data_usage_events_counts = rng.integers(
        1, 
        np.minimum(purchases_df.loc[data_usage_mask, DATA_USAGE_COL], 5 # !!! Faire varier le 5 plus tard (le rendre aleatoire)
) + 1 )

print(purchases_df[call_usage_mask].index.repeat(call_usage_events_counts))
print(purchases_df.loc[purchases_df[call_usage_mask].index.repeat(call_usage_events_counts)])


call_usage_df = purchases_df.loc[purchases_df[call_usage_mask].index.repeat(call_usage_events_counts)]
sms_usage_df = purchases_df.loc[purchases_df[sms_usage_mask].index.repeat(sms_usage_events_counts)]
data_usage_df = purchases_df.loc[purchases_df[data_usage_mask].index.repeat(data_usage_events_counts)]




call_usage_df[SERVICE_TYPE_COL] = CALL
sms_usage_df[SERVICE_TYPE_COL] = SMS
data_usage_df[SERVICE_TYPE_COL] = DATA


data_usage_df[DATA_MB_COL] = rng.integers(1, 101, size = len(data_usage_df)) / 100
data_usage_df[DATA_MB_COL]  = (
data_usage_df.groupby(level=0).apply(
        lambda g: pd.Series(
                rng.multinomial(
                        g[DATA_USAGE_COL].iloc[0] - len(g), np.ones(len(g))/len(g)
                ) + 1,
                index = g.index
        )
).droplevel(0)
)
data_usage_df[DATA_MB_COL] = data_usage_df[DATA_MB_COL].round().astype(int)


call_usage_df[CALL_SECONDS_COL] = rng.integers(1, 101, size = len(call_usage_df)) / 100
call_usage_df[CALL_SECONDS_COL]  = (
call_usage_df.groupby(level=0).apply(
        lambda g: pd.Series(
                rng.multinomial(
                        g[CALLS_USAGE_COL].iloc[0] - len(g), np.ones(len(g))/len(g)
                ) + 1,
                index = g.index
        )
).droplevel(0)
)
call_usage_df[CALL_SECONDS_COL] = call_usage_df[CALL_SECONDS_COL].round().astype(int)



sms_usage_df[SMS_COUNT_COL] = rng.integers(1, 101, size = len(sms_usage_df)) / 100

sms_usage_df[SMS_COUNT_COL]  = (
sms_usage_df.groupby(level=0).apply(
        lambda g: pd.Series(
                rng.multinomial(
                        g[SMS_USAGE_COL].iloc[0] - len(g), np.ones(len(g))/len(g)
                ) + 1,
                index = g.index
        )
).droplevel(0)
)
sms_usage_df[SMS_COUNT_COL] = sms_usage_df[SMS_COUNT_COL].round().astype(int)

print(sms_usage_df[sms_usage_df[SMS_COUNT_COL] == 0])

print(call_usage_df)
print(sms_usage_df)
print(data_usage_df)


usage_df = pd.concat([
        call_usage_df, sms_usage_df, data_usage_df
]
)
print(usage_df)

print(usage_df[usage_df[DATA_USAGE_COL] == 0])
print(usage_df[usage_df[CALLS_USAGE_COL] == 0])
print(usage_df[usage_df[SMS_USAGE_COL] == 0])



usage_offset_seconds = rng.integers(0, usage_df[VALIDITY_DAYS_COL].to_numpy() * 24 * 60 * 60 + 1)


usage_df[TIMESTAMP_MILLISECONDS_COL] = usage_df[PURCHASED_AT_COL] + pd.to_timedelta(usage_offset_seconds, unit="seconds")


print(usage_df)
print(usage_df.columns)

subscriptions_df = pd.read_csv(SUBSCRIPTIONS_RECORDS_FILE, usecols=[ID_COL, CUSTOMER_ID_COL, PHONE_NUMBER_COL]).rename(columns={ID_COL:SUBSCRIPTION_ID_COL})

usage_df = usage_df.merge(
        subscriptions_df,
        on=SUBSCRIPTION_ID_COL,
        how="left"
)

print(usage_df)

usage_df = usage_df[
        [
PURCHASE_ID_COL,
SUBSCRIPTION_ID_COL,
TIMESTAMP_MILLISECONDS_COL,
SERVICE_TYPE_COL,
CALL_SECONDS_COL,
SMS_COUNT_COL,
DATA_MB_COL
]
]

usage_df[TIMESTAMP_MILLISECONDS_COL] = pd.to_datetime(usage_df[TIMESTAMP_MILLISECONDS_COL]).astype("int64") // 10 ** 6
usage_df.sort_values(by=[TIMESTAMP_MILLISECONDS_COL, SUBSCRIPTION_ID_COL], inplace=True)

usage_df[SMS_COUNT_COL] = usage_df[SMS_COUNT_COL].astype("Int64")

print(usage_df)
print(usage_df.columns)

usage_records = usage_df.to_dict(orient="records")

usage_records = [
        {k:v for k, v in record.items() if pd.notna(v)} for record in usage_records
]

file = Path(DATA_GENERATOR_OUTPUT_DIR) / "usage.json"

with open(file, "w") as file:
        for record in usage_records:
                file.write(json.dumps(record) + "\n")