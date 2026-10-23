from src.ingestion.utils.db_connector import get_connection
from src.ingestion.utils.batch_manager import start_batch, complete_batch

from src.ingestion.extract_to_raw import extract_from_database, extract_purchases, extract_service_usage
from src.staging.move_from_raw_to_staging import move_to_staging

from src.quality_checks.main import check_quality
from src.load.main import load



def run_pipeline():
        connection = get_connection()
        batch_id, started_at = start_batch(connection)
        print(batch_id, started_at)
     
        print("Extracting from database")

        extraction_start_date = "1900-01-01"
        extraction_end_date = "9999-12-12"
        output_dir = "/home/starias/myprojects/telecom-offer-performance-analytics-platform/data/raw/2026-10-20"


        extract_from_database("2026-10-20", extraction_start_date, extraction_end_date, batch_id)
        extract_purchases(output_dir, batch_id, extraction_start_date, extraction_end_date)
        extract_service_usage(output_dir, batch_id)
        

        move_to_staging(output_dir)
        check_quality()
        load(incremental=False)
        


        finished_at = complete_batch(connection, batch_id)
        print(finished_at)
        # print(type(finished_at))


if __name__ == "__main__":
        print("Hi")
        run_pipeline()