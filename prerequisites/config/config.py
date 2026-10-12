from config.categorical_constants import INDIVIDUAL, BUSINESS, STANDARD, YOUTH, PREMIUM, SME, ACTIVE, INACTIVE, SUSPENDED, TERMINATED, USSD, MOBILE_APP, WEB, DEALDER, AIRTIME, MOBILE_MONEY

NULL = None
SEED = 0

KAFKA_TOPIC = "TelecomUsage"
KAFKA_SERVERS = "localhost:9092"

NUM_CUSTOMERS = 5_000_000
TELECOM_CREATION_DATE = "2020-05-18"

MIN_BIRTHDATE = "1900-01-01"

CALL = "CALL"
SMS = "SMS"
DATA = "DATA"

CUSTOMER_TYPE_PROBABILITIES ={
        INDIVIDUAL:0.90,
        BUSINESS:0.10
}

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
TELECOM_PHONE_NUMBER_PREFIXES = [30, 32, 34, 36, 38, 70, 72, 74]  # Les prefixes de numeros de loperateur telecom


PURCHASE_CHANNEL_PROBABILITIES = {USSD:0.55, MOBILE_APP: 0.25, WEB: 0.05, DEALDER:0.15}

PAYMENT_METHOD_PROBABILITIES = {MOBILE_MONEY: 0.75, AIRTIME:0.25}

SUBSCRIPTIONS_COUNT_PROBABILITIES = {
        1:0.85,
        2:0.12,
        3:0.025,
        4:0.004,
        5:0.001
        }

