import os
import numpy as np
import pandas as pd
import sys
from pathlib import Path

from config.config import TELECOM_CREATION_DATE, NULL, ID_COL, OFFER_ID_COL, OFFER_RECORDS_CSV_FILE_PATH, BILLING_RECORDS_CSV_FILE_PATH, OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH, BILLING_ID_COL, START_DATE_COL, END_DATE_COL, VALIDITY_DAYS_COL, MOBILE, DATA, BUNDLE, TYPE_COL, VALUE_MB_COL, VALUE_XOF_COL, XOF_PER_MB_COL, XOF_PER_SEC_COL, XOF_PER_SMS_COL, IS_LIMITLESS_COL, OFFERS_CATALOG_DIR


NAME_COL = "name"
PRICE_XOF_COL = "price_xof"

# !! Add offer publication/creation/mise a dispotion date


offer_names = ["Offre par Défaut", "Navigation Internet Option Libre"]
offer_types = [MOBILE, DATA]
offer_prices = [pd.NA, pd.NA]


maxi_offer_prices = [100, 150, 200, 500, 1000, 2500, 5000]
offer_names.extend([f"Forfait Maxi Appel {price} F" for price in maxi_offer_prices])
offer_types.extend([MOBILE for _ in maxi_offer_prices])
offer_prices.extend(maxi_offer_prices)

offer_names.extend([f"Forfait Maxi Appel + Internet {price} F" for price in maxi_offer_prices])
offer_types.extend([BUNDLE for _ in maxi_offer_prices])
offer_prices.extend(maxi_offer_prices)


volume_data_offer_prices = [100, 150, 200, 300, 500, 750, 1000, 2500, 5000]
offer_names.extend([f"Forfait Internet Volume {price} F" for price in volume_data_offer_prices])
offer_types.extend([DATA for _ in volume_data_offer_prices])
offer_prices.extend(volume_data_offer_prices)

limitless_data_offer_prices = [15_000, 20_000, 25_000]
offer_names.extend([f"Forfait Internet Illimité {price} F" for price in limitless_data_offer_prices])
offer_types.extend([DATA for _ in limitless_data_offer_prices])
offer_prices.extend(limitless_data_offer_prices)

# !! Add promotional offers
## !! Add start and end date: offers that used to exist but does not anymore

offers_df = pd.DataFrame({
        ID_COL: np.arange(1, len(offer_names) + 1),
        NAME_COL : offer_names,
        TYPE_COL : offer_types,
        PRICE_XOF_COL : offer_prices,
        START_DATE_COL: TELECOM_CREATION_DATE,
        END_DATE_COL: NULL
        })


print(offers_df)




BILLINGS_COLUMNS = [XOF_PER_SEC_COL, XOF_PER_SMS_COL, XOF_PER_MB_COL]

offer_billings_df = pd.DataFrame(np.array([
        # 2020-2021
        [1, 5, NULL], # Default offer
        [NULL, NULL, 1],# Navigation Internet Option libre
        [0.94, 5, NULL], # Forfait Appel
        [0.94, 5, 2.7],# Forfait Appel + Internet

        # 2022-2023
        [1, 4, NULL], # Default offer
        [NULL, NULL, 2],# Navigation Internet Option libre (2022-2025)
        [0.85, 5, NULL], # Forfait Appel
        [0.85, 5, 2.5], # Forfait Appel + Internet
        
        # 2024-2025
        [1, 3, NULL], # Default offer
        # Navigation Internet Option libre (Same as 2022-2023)
        [0.41, 2, NULL], # Forfait Appel
        [0.41, 2, 1], # Forfait Appel + Internet
        
        # 2026
        [1, 2, NULL], # Default offer
        [NULL, NULL, 3.09], # Navigation Internet Option libre
        [0.47, 2, NULL],# Forfait Appel
        [0.47, 2, 1], # Forfait Appel + Internet        

          ]),
        columns=BILLINGS_COLUMNS)

offer_billings_df[ID_COL] = np.arange(1, len(offer_billings_df) + 1)
# exit()
offer_billings_df = offer_billings_df[[ID_COL] + BILLINGS_COLUMNS]
print(offer_billings_df)

array = np.array(
                [
                        # Offre par Défaut
                        [1, NULL, NULL, NULL, 1, NULL, TELECOM_CREATION_DATE, "2021-12-31"],
                        [1, NULL, NULL, NULL, 5, NULL, "2022-01-01", "2023-12-31"],
                        [1, NULL, NULL, NULL, 9, NULL, "2024-01-01", "2025-12-31"],
                        [1, NULL, NULL, NULL, 12, NULL, "2026-01-01", NULL],

                        # Navigation en Option libre
                        [2, NULL, NULL, NULL, 2, NULL, TELECOM_CREATION_DATE, "2021-12-31"],
                        [2, NULL, NULL, NULL, 6, NULL, "2022-01-01", "2025-12-31"],
                        [2, NULL, NULL, NULL, 13, NULL, "2026-01-01", NULL],

                        # Offres de forfaits 
                        # 2020-2021
                        # Appel
                        [3, 166, NULL, 1, 3 , NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 100 F
                        [4, 250, NULL, 1, 3, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 150 F
                        [5, 333, NULL, 1, 3, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 200 F
                        [6, 833, NULL, 2, 3, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 500 F
                        [7, 1666, NULL, 7, 3, NULL, TELECOM_CREATION_DATE, "2021-12-31"],# 1000 F
                        [8, 4166, NULL, 15, 3, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 2500 F
                        [9, 8333, NULL, 30, 3, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 5000 F
                        # Appel + Internet
                        [10, 166, NULL, 1, 4 , NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 100 F
                        [11, 250, NULL, 1, 4, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 150 F
                        [12, 333, NULL, 1, 4, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 200 F
                        [13, 833, NULL, 2, 4, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 500 F
                        [14, 1666, NULL, 7, 4, NULL, TELECOM_CREATION_DATE, "2021-12-31"],# 1000 F
                        [15, 4166, NULL, 15, 4, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 2500 F
                        [16, 8333, NULL, 30, 4, NULL, TELECOM_CREATION_DATE, "2021-12-31"], # 5000 F
                        # Internet Volume
                        [17, NULL,166, 1, NULL , False, TELECOM_CREATION_DATE, "2021-12-31"], # 100 F
                        [18, NULL, 250, 1, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"], # 150 F
                        [19, NULL, 333, 1, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"], # 200 F
                        [20, NULL, 500, 1, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"], # 300 F
                        [21, NULL, 1000 , 1, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"], # 500 F
                        [22, NULL, 1000 , 2, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"], # 750 F
                        [23, NULL, 1666, 7, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"],# 1000 F
                        [24, NULL, 4166, 15, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"], # 2500 F
                        [25, NULL, 8333, 30, NULL, False, TELECOM_CREATION_DATE, "2021-12-31"], # 5000 F
                        # Internet Illimité
                        [26, NULL, 24.4 * 1000, 30, NULL , True, TELECOM_CREATION_DATE, "2021-12-31"], # 15 000 F
                        [27, NULL, 32.5 * 1000, 30, NULL, True, TELECOM_CREATION_DATE, "2021-12-31"], # 20 000F
                        [28, NULL, 40.7 * 1000, 30, NULL, True, TELECOM_CREATION_DATE, "2021-12-31"], # 25 000 F

                        # 2022-2023
                        # Appel
                        [3, 166, NULL, 1, 7 , NULL, "2022-01-01", "2023-12-31"], # 100 F
                        [4, 250, NULL, 1, 7, NULL, "2022-01-01", "2023-12-31"], # 150 F
                        [5, 333, NULL, 1, 7, NULL, "2022-01-01", "2023-12-31"], # 200 F
                        [6, 833, NULL, 2, 7, NULL, "2022-01-01", "2023-12-31"], # 500 F
                        [7, 1666, NULL, 7, 7, NULL, "2022-01-01", "2023-12-31"],# 1000 F
                        [8, 4166, NULL, 15, 7, NULL, "2022-01-01", "2023-12-31"], # 2500 F
                        [9, 8333, NULL, 30, 7, NULL, "2022-01-01", "2023-12-31"], # 5000 F
                        # Appel + Internet
                        [10, 166, NULL, 1, 8 , NULL, "2022-01-01", "2023-12-31"], # 100 F
                        [11, 250, NULL, 1, 8, NULL, "2022-01-01", "2023-12-31"], # 150 F
                        [12, 333, NULL, 1, 8, NULL, "2022-01-01", "2023-12-31"], # 200 F
                        [13, 833, NULL, 2, 8, NULL, "2022-01-01", "2023-12-31"], # 500 F
                        [14, 1666, NULL, 7, 8, NULL, "2022-01-01", "2023-12-31"],# 1000 F
                        [15, 4166, NULL, 15, 8, NULL, "2022-01-01", "2023-12-31"], # 2500 F
                        [16, 8333, NULL, 30, 8, NULL, "2022-01-01", "2023-12-31"], # 5000 F
                        # Internet Volume
                        [17, NULL,166, 1, NULL , False, "2022-01-01", "2023-12-31"], # 100 F
                        [18, NULL, 250, 1, NULL, False, "2022-01-01", "2023-12-31"], # 150 F
                        [19, NULL, 333, 1, NULL, False, "2022-01-01", "2023-12-31"], # 200 F
                        [20, NULL, 500, 1, NULL, False, "2022-01-01", "2023-12-31"], # 300 F
                        [21, NULL, 1000 , 1, NULL, False, "2022-01-01", "2023-12-31"], # 500 F
                        [22, NULL, 1000 , 2, NULL, False, "2022-01-01", "2023-12-31"], # 750 F
                        [23, NULL, 1666, 7, NULL, False, "2022-01-01", "2023-12-31"],# 1000 F
                        [24, NULL, 4166, 15, NULL, False, "2022-01-01", "2023-12-31"], # 2500 F
                        [25, NULL, 8333, 30, NULL, False, "2022-01-01", "2023-12-31"], # 5000 F
                        # Internet Illimité
                        [26, NULL, 24.4 * 1000, 30, NULL , True, "2022-01-01", "2023-12-31"], # 15 000 F
                        [27, NULL, 32.5 * 1000, 30, NULL, True, "2022-01-01", "2023-12-31"], # 20 000F
                        [28, NULL, 40.7 * 1000, 30, NULL, True, "2022-01-01", "2023-12-31"], # 25 000 F


                        # 2024-2025
                        # Appel
                        [3, 166, NULL, 1, 10, NULL, "2024-01-01", "2025-12-31"], # 100 F
                        [4, 250, NULL, 1, 10, NULL, "2024-01-01", "2025-12-31"], # 150 F
                        [5, 333, NULL, 1, 10, NULL, "2024-01-01", "2025-12-31"], # 200 F
                        [6, 833, NULL, 2, 10, NULL, "2024-01-01", "2025-12-31"], # 500 F
                        [7, 1666, NULL, 7, 10, NULL, "2024-01-01", "2025-12-31"],# 1000 F
                        [8, 4166, NULL, 15, 10,  NULL, "2024-01-01", "2025-12-31"], # 2500 F
                        [9, 8333, NULL, 30, 10, NULL, "2024-01-01", "2025-12-31"], # 5000 F
                        # Appel + Internet
                        [10, 166, NULL, 1, 11, NULL, "2024-01-01", "2025-12-31"], # 100 F
                        [11, 250, NULL, 1, 11, NULL, "2024-01-01", "2025-12-31"], # 150 F
                        [12, 333, NULL, 1, 11, NULL, "2024-01-01", "2025-12-31"], # 200 F
                        [13, 833, NULL, 2, 11, NULL, "2024-01-01", "2025-12-31"], # 500 F
                        [14, 1666, NULL, 7, 11, NULL, "2024-01-01", "2025-12-31"],# 1000 F
                        [15, 4166, NULL, 15, 11, NULL, "2024-01-01", "2025-12-31"], # 2500 F
                        [16, 8333, NULL, 30, 11, NULL, "2024-01-01", "2025-12-31"], # 5000 F
                        # Internet Volume
                        [17, NULL,166, 1, NULL , False, "2024-01-01", "2025-12-31"], # 100 F
                        [18, NULL, 250, 1, NULL, False, "2024-01-01", "2025-12-31"], # 150 F
                        [19, NULL, 333, 1, NULL, False, "2024-01-01", "2025-12-31"], # 200 F
                        [20, NULL, 500, 1, NULL, False, "2024-01-01", "2025-12-31"], # 300 F
                        [21, NULL, 1000 , 1, NULL, False, "2024-01-01", "2025-12-31"], # 500 F
                        [22, NULL, 1000 , 2, NULL, False, "2024-01-01", "2025-12-31"], # 750 F
                        [23, NULL, 1666, 7, NULL, False, "2024-01-01", "2025-12-31"],# 1000 F
                        [24, NULL, 4166, 15, NULL, False, "2024-01-01", "2025-12-31"], # 2500 F
                        [25, NULL, 8333, 30, NULL, False, "2024-01-01", "2025-12-31"], # 5000 F
                        # Internet Illimité
                        [26, NULL, 24.4 * 1000, 30, NULL , True, "2024-01-01", "2025-12-31"], # 15 000 F
                        [27, NULL, 32.5 * 1000, 30, NULL, True, "2024-01-01", "2025-12-31"], # 20 000F
                        [28, NULL, 40.7 * 1000, 30, NULL, True, "2024-01-01", "2025-12-31"], # 25 000 F

                        # 2026
                        # Appel
                        [3, 166, NULL, 1, 14, NULL, "2026-01-01", NULL], # 100 F
                        [4, 250, NULL, 1, 14, NULL, "2026-01-01", NULL], # 150 F
                        [5, 333, NULL, 1, 14, NULL, "2026-01-01", NULL], # 200 F
                        [6, 833, NULL, 2, 14, NULL, "2026-01-01", NULL], # 500 F
                        [7, 1666, NULL, 7, 14, NULL, "2026-01-01", NULL],# 1000 F
                        [8, 4166, NULL, 15, 14, NULL, "2026-01-01", NULL], # 2500 F
                        [9, 8333, NULL, 30, 14, NULL, "2026-01-01", NULL], # 5000 F
                        # Appel + Internet
                        [10, 166, NULL, 1, 15, NULL, "2026-01-01", NULL], # 100 F
                        [11, 250, NULL, 1, 15, NULL, "2026-01-01", NULL], # 150 F
                        [12, 333, NULL, 1, 15, NULL, "2026-01-01", NULL], # 200 F
                        [13, 833, NULL, 2, 15, NULL, "2026-01-01", NULL], # 500 F
                        [14, 1666, NULL, 7, 15, NULL, "2026-01-01", NULL],# 1000 F
                        [15, 4166, NULL, 15, 15, NULL, "2026-01-01", NULL], # 2500 F
                        [16, 8333, NULL, 30, 15, NULL, "2026-01-01", NULL], # 5000 F
                        # Internet Volume
                        [17, NULL,166, 1, NULL, False, "2026-01-01", NULL], # 100 F
                        [18, NULL, 250, 1, NULL, False, "2026-01-01", NULL], # 150 F
                        [19, NULL, 333, 1, NULL, False, "2026-01-01", NULL], # 200 F
                        [20, NULL, 500, 1, NULL, False, "2026-01-01", NULL], # 300 F
                        [21, NULL, 1000 , 1, NULL, False, "2026-01-01", NULL], # 500 F
                        [22, NULL, 1000 , 2, NULL, False, "2026-01-01", NULL], # 750 F
                        [23, NULL, 1666, 7, NULL, False, "2026-01-01", NULL],# 1000 F
                        [24, NULL, 4166, 15, NULL, False, "2026-01-01", NULL], # 2500 F
                        [25, NULL, 8333, 30, NULL, False, "2026-01-01", NULL], # 5000 F
                        # Internet Illimité
                        [26, NULL, 24.4 * 1000, 30, NULL, True, "2026-01-01", NULL], # 15 000 F
                        [27, NULL, 32.5 * 1000, 30, NULL, True, "2026-01-01", NULL], # 20 000F
                        [28, NULL, 40.7 * 1000, 30, NULL, True, "2026-01-01", NULL], # 25 000 F     

                ]
        )

CONFIG_COLUMNS = [OFFER_ID_COL, VALUE_XOF_COL, VALUE_MB_COL, VALIDITY_DAYS_COL, BILLING_ID_COL, IS_LIMITLESS_COL,  START_DATE_COL, END_DATE_COL]
offer_configs_df = pd.DataFrame(array, columns=CONFIG_COLUMNS
)
offer_configs_df[ID_COL] = np.arange(1, len(offer_configs_df) + 1)
offer_configs_df = offer_configs_df[[ID_COL] + CONFIG_COLUMNS]


print(offer_configs_df)
# Ne pas considerer offre par defaut (credit/airtime) et option libre pour le moment (!!!!Supprimer ce filtre plus tard pour les considerer plus tard)
offer_configs_df = offer_configs_df[~offer_configs_df[VALIDITY_DAYS_COL].isna()]
print(offer_configs_df)

print(offer_configs_df[offer_configs_df[OFFER_ID_COL].isin([10, 11, 12, 13, 14, 15, 16])])

os.makedirs(OFFERS_CATALOG_DIR, exist_ok=True)

offers_df.to_csv(OFFER_RECORDS_CSV_FILE_PATH, index=False)
offer_billings_df.to_csv(BILLING_RECORDS_CSV_FILE_PATH, index=False)
offer_configs_df.to_csv(OFFER_CONFIGURATION_RECORDS_CSV_FILE_PATH, index=False)




