from datetime import datetime, timedelta
from pathlib import Path
from airflow.providers.standard.operators.python import PythonOperator, ShortCircuitOperator
from airflow.task.trigger_rule import TriggerRule

from config.config import SOURCE_NAMES, CUSTOMER_ACTIVITY_ANALYSIS_DAY_OF_MONTH
from config.paths import RAW_DATA_DIR
from src.ingestion.extract_to_raw import (
        extract_from_db_table,
        extract_purchases, 
        extract_service_usage)
from src.ingestion.move_from_raw_to_staging import move_to_staging

from src.quality_checks.run_quality_checks import check_quality

from src.load.load_to_dw import load
from src.refresh.refresh_mt_views import resfresh_mt_views
from src.analytics.analyze_customer_activity import historical_backfill, analyze_customer_activity
from src.utils.batch_manager import start_batch, complete_batch, mark_batch_as_failed
from src.utils.watermark_manager import get_last_watermark, update_watermark
from src.utils.platform_manager import customer_activity_already_analyzed

from src.utils.logger import get_logger

logger = get_logger(__name__)

DEFAULT_ARGS = {
        "retries":2,
        "retry_delay":timedelta(seconds=10) # !!! To be changed later
}

SOURCE_NAMES = SOURCE_NAMES[:-1]

def mark_batch_failed(context):
        task_instance = context["task_instance"]
        task_id = task_instance.task_id
        batch_id = task_instance.xcom_pull(task_ids="start_batch")
        if batch_id:                
                mark_batch_as_failed(
                        batch_id=batch_id,
                        error_message=f"Task '{task_id}' failed: "
                                      f"{context.get('exception', 'Unkown error')}"
                )

def is_customer_activity_to_be_analyzed(**context):
       current_date = context["logical_date"]
       to_be_analyzed = current_date.day == CUSTOMER_ACTIVITY_ANALYSIS_DAY_OF_MONTH and not customer_activity_already_analyzed(current_date.strftime("%Y-%m-%d"))
       logger.info(f"Is customers activity to be analyzed? {'Yes' if to_be_analyzed else 'No'}")
       
       return to_be_analyzed

def run_customer_activity_analysis(**context):
       analysis_month =  context["logical_date"].date().replace(day=1)
       analyze_customer_activity(analysis_month=analysis_month)


def build_pipeline(dag, incremental:bool=False):
    start_batch_task = PythonOperator(
                task_id="start_batch",
                python_callable=start_batch,
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
    
    
    refresh_mt_views_task = PythonOperator(
                    task_id="refresh_materialized_views",
                    python_callable = resfresh_mt_views,
                    dag=dag
            ) 

    analytical_tasks = [refresh_mt_views_task]

    if not incremental:
           customer_activity_historical_backfill_task = PythonOperator(
                                    task_id="customer_activity_historical_backfill",
                                    python_callable = historical_backfill,
                                    dag=dag
           )
           analytical_tasks.append(customer_activity_historical_backfill_task)
    else:
           check_customer_activity_to_be_analyzed = ShortCircuitOperator(
                  task_id="check_if_customer_activity_is_to_be_analyzed",
                python_callable = is_customer_activity_to_be_analyzed,
                ignore_downstream_trigger_rules=False,
                                      dag=dag
           )
           analyze_customer_activity = PythonOperator(
                  task_id="analyze_customer_activity",
                                  python_callable = run_customer_activity_analysis,
                                
                                                        dag=dag
           )

           start_batch_task >> check_customer_activity_to_be_analyzed >> analyze_customer_activity

           analytical_tasks.append(analyze_customer_activity) 


    complete_batch_task = PythonOperator(
                task_id="complete_batch",
                trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
                python_callable=complete_batch,
                op_kwargs= {
                        "batch_id":batch_id,
                        "platform_initialization":not incremental
                        },
                        dag=dag             
        )
        
    (
                
        start_batch_task >>
         
        get_watermark_task >> 

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

        analytical_tasks >>

        complete_batch_task

        )

    return start_batch_task # This is just for inital pipeline dag to handle "already executed" in a simple manner

