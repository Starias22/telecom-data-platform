from datetime import date, datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from config.config import SOURCE_NAMES
from config.paths import RAW_DATA_DIR
from src.ingestion.extract_to_raw import (
        extract_from_db_table,
        extract_purchases, 
        extract_service_usage)
from src.ingestion.move_from_raw_to_staging import move_to_staging

from src.quality_checks.run_quality_checks import check_quality

from src.load.load_to_dw import load
from src.utils.batch_manager import start_batch, complete_batch, mark_batch_as_failed
from src.utils.watermark_manager import get_last_watermark, update_watermark

DEFAULT_ARGS = {
        "retries":2,
        "retry_delay":timedelta(seconds=10)
}

SOURCE_NAMES = SOURCE_NAMES[:-1]

def mark_batch_failed(context):
        task_instance = context["task_instance"]
        task_id = task_instance.task_id
        try_num = task_instance.try_number
        print(try_num)
        batch_id = task_instance.xcom_pull(task_ids="start_batch")
        print("*********")
        print(batch_id)
        print("*********")
        if batch_id:
                print("The batch is going to be marked as failed")

                mark_batch_as_failed(
                        batch_id=batch_id,
                        error_message=f"Task '{task_id}' failed: "
                                      f"{context.get('exception', 'Unkown error')}"
                )


def build_pipeline(dag, incremental:bool=False):
    start_batch_task = PythonOperator(
                task_id="start_batch",
                python_callable=start_batch,
                op_kwargs={"incremental":incremental},
                dag=dag           
                
        )
        
    batch_id = str(start_batch_task.output)

    get_watermark_task = PythonOperator(
                task_id="get_watermarks",
                python_callable=get_last_watermark,
                dag=dag
    )
    watermark = str(get_watermark_task.output)
         
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    extraction_cut_off_date = now
    today = now[:10] # Get the date part

    extraction_output_dir = str(Path(RAW_DATA_DIR) / today / f"batch_id={batch_id}")   
    extraction_params = {
                       "extraction_output_dir":extraction_output_dir,
                       # "watermark":watermarks["offers"],
                       "batch_id":batch_id
        }
    
    extract_offers_task = PythonOperator(
    task_id="extract_offers",
    python_callable = extract_from_db_table,
    op_kwargs= {
    "extraction_output_dir":extraction_output_dir,
    "watermark":watermark,
    "batch_id":batch_id,
    "table_name":"offers",
    "extraction_cut_off_date":extraction_cut_off_date
        },
                # on_failure_callback=mark_batch_failed,
                dag=dag
        )
    extract_billings_task = PythonOperator(
          task_id="extract_billings",
          python_callable = extract_from_db_table,
          op_kwargs= {
                "extraction_output_dir":extraction_output_dir,
                "watermark":watermark,
                "batch_id":batch_id,
                "table_name":"offer_billings",
                "extraction_cut_off_date":extraction_cut_off_date
        },
                # on_failure_callback=mark_batch_failed,
                dag=dag
        )

    extract_offer_configs_task = PythonOperator(
          task_id="extract_offer_configs",
          python_callable = extract_from_db_table,
          op_kwargs= {
                       "extraction_output_dir":extraction_output_dir,
                       "watermark":watermark,
                       "batch_id":batch_id,
                       "table_name":"offer_configurations",
                       "extraction_cut_off_date":extraction_cut_off_date
        },
                on_failure_callback=mark_batch_failed,
                dag=dag
        )

    extract_customers_task = PythonOperator(
                task_id="extract_customers",
                python_callable = extract_from_db_table,
                op_kwargs= {
                       "extraction_output_dir":extraction_output_dir,
                       "watermark":watermark,
                       "batch_id":batch_id,
                       "table_name":"customers",
                       "extraction_cut_off_date":extraction_cut_off_date
        },
                on_failure_callback=mark_batch_failed,
                dag=dag
        )

    extract_subscriptions_task = PythonOperator(
                task_id="extract_subscriptions",
                python_callable = extract_from_db_table,
                op_kwargs= {
                       "extraction_output_dir":extraction_output_dir,
                       "watermark":watermark,
                       "batch_id":batch_id,
                       "table_name":"subscriptions",
                       "extraction_cut_off_date":extraction_cut_off_date
        },
                on_failure_callback=mark_batch_failed,
                dag=dag
        )

    extract_purchases_task = PythonOperator(
                task_id="extract_purchases",
                python_callable = extract_purchases,
                op_kwargs={
                       "extraction_output_dir":extraction_output_dir,
                       "batch_id":batch_id,
                       "watermark":watermark,
                       "extraction_cut_off_date":extraction_cut_off_date
        },
                on_failure_callback=mark_batch_failed,
                dag=dag
        )

    extract_service_usage_task = PythonOperator(
                task_id="extract_service_usage",
                python_callable = extract_service_usage,
                op_kwargs=extraction_params,
                on_failure_callback=mark_batch_failed,
                dag=dag
        )
    move_to_staging_task = PythonOperator(
                task_id="move_to_staging",
                python_callable = move_to_staging,
                op_kwargs={
                        "staging_raw_data_dir":extraction_output_dir
                },
                on_failure_callback=mark_batch_failed,
                dag=dag
        )

    quality_checks_task = PythonOperator(
                task_id="run_quality_checks",
                python_callable = check_quality,
                op_kwargs={
                        "batch_id":batch_id
                        },
                on_failure_callback=mark_batch_failed,
                dag=dag
        )
    load_to_dw_task = PythonOperator(
                task_id="load_to_dw",
                python_callable = load,
                op_kwargs={
                        "incremental":incremental,# TO support both initial and incremental load
                        "batch_id":batch_id if incremental else None # Set batch id if and only if incrmental load
                        },
                on_failure_callback=mark_batch_failed,
                dag=dag
        )

    update_watermark_task = PythonOperator(
                task_id="update_watermark",
                python_callable=update_watermark,
                op_kwargs={
                        "new_watermark":extraction_cut_off_date
                },
                dag=dag
        )

    complete_batch_task = PythonOperator(
                task_id="complete_batch",
                python_callable=complete_batch,
                op_kwargs= {
                        "batch_id":batch_id,
                        "platform_initialization":not incremental
                        },
                        dag=dag             
        )
        
    (
                
        start_batch_task >> 

        [
            extract_offers_task,
            extract_billings_task,
            extract_offer_configs_task,

            extract_customers_task,
            extract_subscriptions_task,
            extract_purchases_task,
            extract_service_usage_task
        ] >>

        move_to_staging_task >>
        
        quality_checks_task >>
        load_to_dw_task >>
        update_watermark_task >>
        complete_batch_task

        )

