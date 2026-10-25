
import os

from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from dotenv import load_dotenv

from config.paths import ENV_FILE_PATH, SQL_INITIAL_SETUP_MAIN_FILE_PATH
from config.config import HOST, USER

load_dotenv(ENV_FILE_PATH)



with DAG(
        dag_id="data_platform_setup_dag",
        description="This DAG simply setup the data platform by creating all neccessary schemas and tables for cities reference, pipeline metadata, staging, data quality, and the datawarehouse",

):
        setup_platform_task = BashOperator(
                task_id="setup_data_platform",
                bash_command=f"psql -h {HOST} -U {USER} -f {SQL_INITIAL_SETUP_MAIN_FILE_PATH}" 
        )