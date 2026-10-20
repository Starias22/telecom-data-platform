from datetime import date, datetime
import os
import numpy as np
import pandas as pd

from config.paths import CUSTOMER_RECORDS_FILE, DATA_GENERATOR_OUTPUT_DIR
from config.column_names import CITY_COL, CUSTOMER_TYPE_COL, BIRTHDATE_COL, GENDER_COL, STATUS_COL, TERMINATION_DATE_COL, REGISTRATION_DATE_COL, CUSTOMER_SEGMENT_COL, ID_COL, UPDATED_AT_COL
from config.categorical_constants import INDIVIDUAL, TERMINATED, MALE, FEMALE, BUSINESS
from config.config import SEED, CITY_PROBABILITIES, CUSTOMERS_MIN_AGE, NUM_CUSTOMERS, CUSTOMER_STATUS_PROBABILITIES, CUSTOMER_TYPE_PROBABILITIES, TELECOM_CREATION_DATE, CUSTOMER_SEGMENT_PROBABILITIES, MIN_BIRTHDATE

UPDATED_AT = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(UPDATED_AT)

def generate_customers():
        TODAY = date.today()

        rng = np.random.default_rng(SEED)

        customers_df = pd.DataFrame()

        # Customer city
        customers_df[CITY_COL] =  rng.choice(list(CITY_PROBABILITIES.keys()), p=list(CITY_PROBABILITIES.values()), size=NUM_CUSTOMERS)

        # Customer type and gender
        customers_df[CUSTOMER_TYPE_COL] =  rng.choice(list(CUSTOMER_TYPE_PROBABILITIES.keys()), p=list(CUSTOMER_TYPE_PROBABILITIES.values()), size=NUM_CUSTOMERS)
        individual_customer_mask = customers_df[CUSTOMER_TYPE_COL] == INDIVIDUAL
        customers_df.loc[individual_customer_mask, GENDER_COL] = rng.choice([MALE, FEMALE], size=individual_customer_mask.sum())

        # Customer segment

        customers_df.loc[individual_customer_mask, CUSTOMER_SEGMENT_COL] = rng.choice(list(CUSTOMER_SEGMENT_PROBABILITIES[INDIVIDUAL].keys()), p=list(CUSTOMER_SEGMENT_PROBABILITIES[INDIVIDUAL].values()), size = individual_customer_mask.sum())
        customers_df.loc[~individual_customer_mask, CUSTOMER_SEGMENT_COL] = rng.choice(list(CUSTOMER_SEGMENT_PROBABILITIES[BUSINESS].keys()), p=list(CUSTOMER_SEGMENT_PROBABILITIES[BUSINESS].values()), size = (~individual_customer_mask).sum())

        # Customer status
        customers_df[STATUS_COL] = rng.choice(list(CUSTOMER_STATUS_PROBABILITIES.keys()), p=list(CUSTOMER_STATUS_PROBABILITIES.values()), size=NUM_CUSTOMERS)

        # Customer registration date
        min_registration_date = pd.Timestamp(TELECOM_CREATION_DATE)
        max_registration_date = pd.Timestamp(TODAY)
        registration_days_range_max_day = (max_registration_date - min_registration_date).days
        print(registration_days_range_max_day)
        registration_dates = min_registration_date + pd.to_timedelta(
                rng.integers(0, registration_days_range_max_day+1, size=NUM_CUSTOMERS), 
                unit="days")
        print(registration_dates)
        customers_df[REGISTRATION_DATE_COL] = registration_dates.strftime("%Y-%m-%d")
        print(customers_df)

        # Customer birthdate
        min_birthdate = pd.Timestamp(MIN_BIRTHDATE)
        max_birthdates = registration_dates
        birth_dates = pd.Series(min_birthdate +  pd.to_timedelta(rng.integers(0, (registration_dates - min_birthdate).days +1), unit="days"))
        individual_customers_max_birthdates = registration_dates[individual_customer_mask] - pd.DateOffset(years=CUSTOMERS_MIN_AGE)
        individual_customers_birthdates = min_birthdate +  pd.to_timedelta(rng.integers(0, (individual_customers_max_birthdates -min_birthdate).days +1), unit="days")
        birth_dates.loc[individual_customer_mask] = individual_customers_birthdates
        customers_df[BIRTHDATE_COL] = birth_dates.dt.strftime("%Y-%m-%d")

        # Customer termination date
        terminated_customer_mask = customers_df[STATUS_COL] == TERMINATED
        min_termination_dates = registration_dates[terminated_customer_mask]
        max_termination_date = pd.Timestamp(TODAY)
        termination_dates = pd.Series(min_termination_dates +  pd.to_timedelta(rng.integers(0, (max_termination_date - min_termination_dates).days +1), unit="days"))

        print(terminated_customer_mask.sum())
        print(termination_dates.isna().sum())
        customers_df.loc[terminated_customer_mask, TERMINATION_DATE_COL] = termination_dates.dt.strftime("%Y-%m-%d").to_numpy() #!!! Without to_numpy I ggot many NUL values in the clmn trminated date (I did not know why)
        print(customers_df.loc[terminated_customer_mask, TERMINATION_DATE_COL].isna().sum())

        # Unique ids
        customers_df[ID_COL] = customers_df.index + 1
        customers_df[UPDATED_AT_COL] = UPDATED_AT # Update it later, so that it will be random and timestemp

        # Save customer records to CSV
        customers_df = customers_df[[ID_COL, CITY_COL, CUSTOMER_TYPE_COL, GENDER_COL, CUSTOMER_SEGMENT_COL, BIRTHDATE_COL, REGISTRATION_DATE_COL, STATUS_COL, TERMINATION_DATE_COL, UPDATED_AT_COL]]

        print(customers_df)
        os.makedirs(DATA_GENERATOR_OUTPUT_DIR, exist_ok=True)
        print("Saving customer records to CSV file")
        customers_df.to_csv(CUSTOMER_RECORDS_FILE, index=False)
        print("Done")
