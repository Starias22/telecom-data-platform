from scripts.generate_data.generate_offers_catalog import generate_offers_catalog
from scripts.generate_data.generate_customers import generate_customers
from scripts.generate_data.generate_subscriptions import generate_subscriptions
from scripts.generate_data.generate_purchases import generate_purchases
from scripts.generate_data.generate_usage_data import generate_service_usage_data


def generate_data():
        print("Generating offers catalog")
        generate_offers_catalog()
       

        print("Generating customers")
        generate_customers()

        print("Generating subscriptions")
        generate_subscriptions()

        print("Generating purchases")
        generate_purchases()

        print("Generating service usage data")
        generate_service_usage_data()

if __name__ == "__main__":
        generate_data()