import json
import os
from pathlib import Path
import numpy as np
import pandas as pd
import shutil

from config.paths import CUSTOMER_RECORDS_FILE, DATA_GENERATOR_OUTPUT_DIR, SUBSCRIPTIONS_RECORDS_FILE, CUSTOMER_RECORDS_SOURCES_FILE, SUBSCRIPTIONS_RECORDS_SOURCES_FILE, OFFERS_CATALOG_DIR, RECHARGE_TRANSACTIONS_DIR, DATA_SOURCES_DIR, PURCHASES_SOURCES_DIR, OFFERS_CATALOG_SOURCES_DIR, TELECOM_SERVICES_USAGE_SOURCES_FILE
from config.column_names import CITY_COL, CUSTOMER_TYPE_COL, PHONE_NUMBER_COL, DATA_MB_COL, CALL_SECONDS_COL, SMS_COUNT_COL, PURCHASE_ID_COL, TYPE_COL, VALUE_MB_COL, XOF_PER_SEC_COL, VALUE_XOF_COL, XOF_PER_SMS_COL, SERVICE_TYPE_COL, TIMESTAMP_MILLISECONDS_COL, SUBSCRIPTION_ID_COL
from config.categorical_constants import BUNDLE, MOBILE
from config.utils import inject_typo, get_purchase_details
from config.config import SEED, NULL
import subprocess


def inject_issues():
        # Intentionaly inject some data quality issues
        rng = np.random.default_rng(SEED)

        ## 1. Customers (type, city)
        customers_df = pd.read_csv(CUSTOMER_RECORDS_FILE)
        n = len(customers_df)

        ### Customer type NULLs
        customer_type_null_values_rate = 0.2 / 100
        count = int(n * customer_type_null_values_rate)
        print(f"{(customer_type_null_values_rate * 100):.2f} % of NULL values for customer types ({count} records)")
        indexes = rng.choice(customers_df.index, size=count, replace=False)
        customers_df.loc[indexes, CUSTOMER_TYPE_COL] = NULL
        print(customers_df)

        ### City names 
        #### in different formats: City names are mainly in capital case: inject lower, upper, and capital cases for some customer records
        customer_city_wrong_cases_rate = 0.5 / 100
        customer_city_wrong_cases_count = int(n * customer_city_wrong_cases_rate)
        print(f"{(customer_city_wrong_cases_rate * 100):.2f} % of wrong cases for customer cities ({customer_city_wrong_cases_count} records)")
        customer_city_wrong_case_indexes = rng.choice(customers_df.index, size=customer_city_wrong_cases_count, replace=False)
        lowercase_indexes, uppercase_indexes, swapcase_indexes = np.array_split(
                rng.permutation(customer_city_wrong_case_indexes),
                3
        )
        customers_df.loc[lowercase_indexes, CITY_COL] = customers_df.loc[lowercase_indexes, CITY_COL].str.lower()
        customers_df.loc[uppercase_indexes, CITY_COL] = customers_df.loc[uppercase_indexes, CITY_COL].str.upper()
        customers_df.loc[swapcase_indexes, CITY_COL] = customers_df.loc[swapcase_indexes, CITY_COL].str.swapcase()
        print(customers_df.iloc[lowercase_indexes])
        print(customers_df.iloc[uppercase_indexes])
        print(customers_df.iloc[swapcase_indexes])

        #### Typo in city names
        customer_city_typo_rate = 0.3 / 100
        count = int(n * customer_city_typo_rate)
        print(f"{(customer_city_typo_rate * 100):.2f} % of typo for customer cities ({count} records)")
        indexes = rng.choice(customers_df.index, size=count, replace=False)
        customers_df.loc[indexes, CITY_COL] = customers_df.loc[indexes, CITY_COL].apply(lambda city: inject_typo(city, rng=rng))
        print(customers_df.iloc[indexes])

        # 2. Subscriptions
        subscriptions_df = pd.read_csv(SUBSCRIPTIONS_RECORDS_FILE)
        # subscriptions_df = pd.read_csv(SUBSCRIPTIONS_RECORDS_FILE, usecols=[PHONE_NUMBER_COL])
        n = len(subscriptions_df)

        ## Phone Numbers
        ### Inconsistent format (with or without pefix 01 or 229 0r +229):
        #### 5% with prefix 01; 1% with prefix 229 (with or without the plus);
        prefix_01_rate = 5 / 100
        count = int(n * prefix_01_rate)
        print(f"{(prefix_01_rate * 100):.2f} % of customer phone numbers with prefix 01 ({count} records)")
        indexes = rng.choice(subscriptions_df.index, size=count, replace=False)
        subscriptions_df.loc[indexes, PHONE_NUMBER_COL] = "01" + subscriptions_df.loc[indexes, PHONE_NUMBER_COL].astype(str)
        subscriptions_df.loc[indexes]

        prefix_229_rate =  1/ 100
        prefix_229_count = int(n * prefix_229_rate)
        print(f"{(prefix_229_rate * 100):.2f} % of customer phone numbers with prefix 229 ({prefix_229_count} records)")
        prefix_229_indexes = rng.choice(subscriptions_df.index, size=prefix_229_count, replace=False)
        subscriptions_df.loc[prefix_229_indexes, PHONE_NUMBER_COL] = "229" + subscriptions_df.loc[prefix_229_indexes, PHONE_NUMBER_COL].astype(str)
        subscriptions_df.loc[prefix_229_indexes]
        print(subscriptions_df.iloc[prefix_229_indexes])

        prefix_plus_rate =  45/ 100 # 45% of prefixed 229-phone numbers will have plus as prefix
        prefix_plus_count = int(prefix_229_count * prefix_plus_rate)
        print(f"{(prefix_229_rate * 100):.2f} % of customer phone numbers with prefix +229 ({prefix_plus_count} records)")
        prefix_plus_indexes = rng.choice(prefix_229_indexes, size=prefix_plus_count, replace=False)
        subscriptions_df.loc[prefix_plus_indexes, PHONE_NUMBER_COL] = "+" + subscriptions_df.loc[prefix_229_indexes, PHONE_NUMBER_COL].astype(str)
        subscriptions_df.loc[prefix_plus_indexes]
        print(subscriptions_df.iloc[prefix_plus_indexes])

        # 3. Usage
        usage_df = pd.read_json(Path(DATA_GENERATOR_OUTPUT_DIR) / "usage.json", lines=True)
        n = len(usage_df)
        print(usage_df)

        ## Duplicate usage records
        duplicate_usage_rate =  0.10 / 100 
        count = int(n * duplicate_usage_rate)
        print(f"{(duplicate_usage_rate * 100):.2f} % of duplicate purchase records ({count} records)")
        indexes = rng.choice(usage_df.index, size=count, replace=False)
        duplicates = usage_df.loc[indexes].copy()


        n_copies = rng.integers(2, 5, size = count)
        duplicates = duplicates.loc[
                duplicates.index.repeat(n_copies)
        ]

        usage_df = pd.concat(
                [usage_df, duplicates],
                ignore_index=True
        )
        usage_df.sort_values(by=[TIMESTAMP_MILLISECONDS_COL, SUBSCRIPTION_ID_COL], inplace=True)

        duplicated_rows = usage_df[usage_df.duplicated(keep=False)]
        print(duplicated_rows)

        print(usage_df)


        # Save fles for source systems

        os.makedirs(DATA_SOURCES_DIR, exist_ok=True)

        customers_df.to_csv(CUSTOMER_RECORDS_SOURCES_FILE, index=False)


        print(subscriptions_df)

        subscriptions_df.to_csv(SUBSCRIPTIONS_RECORDS_SOURCES_FILE, index=False)

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
        usage_df[CALL_SECONDS_COL] = usage_df[CALL_SECONDS_COL].astype("Int64")


        print(usage_df)
        print(usage_df.columns)

        usage_records = usage_df.to_dict(orient="records")

        usage_records = [
                {k:v for k, v in record.items() if pd.notna(v)} for record in usage_records
        ]

        file = TELECOM_SERVICES_USAGE_SOURCES_FILE

        with open(file, "w") as file:
                for record in usage_records:
                        file.write(json.dumps(record) + "\n")
                

        #shutil.copytree(RECHARGE_TRANSACTIONS_DIR, PURCHASES_SOURCES_DIR, dirs_exist_ok=True)
        #shutil.copytree(OFFERS_CATALOG_DIR, OFFERS_CATALOG_SOURCES_DIR, dirs_exist_ok=True)
        subprocess.run([
                "rm", 
                "-rf", PURCHASES_SOURCES_DIR
                
                ]) # Remove the directory
        subprocess.run([
                "rm", 
                "-rf", OFFERS_CATALOG_SOURCES_DIR
                
                ]) # Remove the directory

        shutil.copytree(RECHARGE_TRANSACTIONS_DIR, PURCHASES_SOURCES_DIR)
        shutil.copytree(OFFERS_CATALOG_DIR, OFFERS_CATALOG_SOURCES_DIR)

        print("Data quality issues injected successfully")


if __name__ == "__main__":
        inject_issues()
