from config.categorical_constants import TYPO_TYPES, DELETE, DUPLICATE, SWAP
import pandas as pd
from glob import glob
from config.paths import RECHARGE_TRANSACTIONS_DIR, BILLING_RECORDS_CSV_FILE_PATH, OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH, OFFER_RECORDS_CSV_FILE_PATH
from config.column_names import BILLING_ID_COL, OFFER_CONFIG_ID_COL, START_DATE_COL, END_DATE_COL, OFFER_ID_COL, ID_COL, PURCHASE_ID_COL, PURCHASED_AT_COL, SUBSCRIPTION_ID_COL, VALUE_XOF_COL, VALUE_MB_COL, TYPE_COL, VALIDITY_DAYS_COL, IS_LIMITLESS_COL, XOF_PER_MB_COL, XOF_PER_SEC_COL, XOF_PER_SMS_COL


def inject_typo(value, rng):
        if len(value) < 4:
                return value
        typo_type = rng.choice(TYPO_TYPES)
        chars = list(value)
        if typo_type == DELETE:
                pos = rng.integers(1, len(chars) -1)
                del chars[pos]
        elif typo_type == DUPLICATE:
                pos = rng.integers(1, len(chars) -1)
                chars.insert(pos, chars[pos])
        elif typo_type == SWAP:
                pos = rng.integers(1, len(chars) -2)
                chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
        return "".join(chars)


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

        offer_configs_df.drop(columns=[OFFER_ID_COL, BILLING_ID_COL, ID_COL, f"{ID_COL}_y", f"{START_DATE_COL}_y", f"{END_DATE_COL}_y"], inplace=True)
        # Rename id_x to id(config id)
        offer_configs_df.rename(columns={f"{ID_COL}_x": ID_COL}, inplace=True)

        print(offer_configs_df)
        print(offer_configs_df.columns)


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