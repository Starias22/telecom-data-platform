
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator

from dags.utils.pipeline_factory import build_pipeline
from src.utils.platform_manager import get_platform_state

from config.config import INITIALIZED, PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET, PLATFORM_INITIALIZATION_NOT_DONE_OR_INCOMPLET, PLATFORM_INITIALIZATION_SUCCESSFUL, SETUP_COMPLETED


def run_initial_pipeline(dag):
        platform_state = get_platform_state()
        
        if platform_state == PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET:
                print("Platform setup incomplete or not performed at all.")
        if platform_state == INITIALIZED:
                print("Platform already initialized)")
                return 
        if platform_state == SETUP_COMPLETED:
                build_pipeline(dag,
                        incremental=False
                        )

with DAG(
        dag_id="initial_pipeline_dag",
        description="This DAG runs data pipeline for inital data extraction, quality checks, and loading processes.",

) as dag:
        
        run_initial_pipeline(dag)
        