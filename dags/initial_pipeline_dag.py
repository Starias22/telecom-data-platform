
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from airflow.exceptions import AirflowSkipException

from dags.utils.pipeline_factory import build_pipeline
from src.utils.platform_manager import get_platform_state
from config.config import INITIALIZED, DAGS_TAG

def check_initial_pipeline_execution():
    platform_state = get_platform_state()
    
    if platform_state == INITIALIZED:
          raise AirflowSkipException(
                "Initial pipeline has already been executed. Skipping execution."
          )
              
with DAG(
        dag_id="initial_pipeline",
        description="This DAG runs data pipeline for inital data extraction, quality checks, and loading processes.",
        tags=[DAGS_TAG],
) as dag:       
        
        check_initial_pipeline_execution_task = PythonOperator(
                task_id="check_initial_pipeline_execution",
                python_callable=check_initial_pipeline_execution,
                dag=dag           
                
        )
        check_initial_pipeline_execution_task >> build_pipeline(dag,
                        incremental=False
                        )
        