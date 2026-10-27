
import os

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from dotenv import load_dotenv

from config.paths import ENV_FILE_PATH, SQL_INITIAL_SETUP_MAIN_FILE_PATH
from config.config import HOST, PLATFORM_INITIALIZATION_NOT_DONE_OR_INCOMPLET, PLATFORM_INITIALIZATION_SUCCESSFUL, PLATFORM_SETUP_NOT_DONE_OR_INCOMPLET, USER, SETUP_COMPLETED, INITIALIZED

from src.utils.platform_manager import is_platform_setup, setup_platform_database, get_platform_state

# load_dotenv(ENV_FILE_PATH)

def setup_data_platform():
        platform_state = get_platform_state()
        if platform_state == SETUP_COMPLETED:
                print("Platform setup already performed")
                return
        if platform_state == INITIALIZED:
                print("Platform setup already performed (Platform even initialized)")
                return 
        setup_platform_database()



with DAG(
        dag_id="data_platform_setup_dag",
        description="This DAG simply setup the data platform by creating all neccessary schemas and tables for cities reference, pipeline metadata, staging, data quality, and the datawarehouse",

):
        setup_platform_task = PythonOperator(
                task_id="setup_data_platform",
                python_callable=setup_data_platform
        )