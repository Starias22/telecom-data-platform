

from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from airflow.exceptions import AirflowSkipException


from config.config import SETUP_COMPLETED, INITIALIZED

from src.utils.platform_manager import setup_platform_database, get_platform_state
from src.utils.logger import get_logger
from dags.utils.pipeline_factory import DEFAULT_ARGS

logger = get_logger(__name__)


def check_data_platform_setup_execution():
        platform_state = get_platform_state()
        if platform_state == SETUP_COMPLETED:
                logger.info("")
                raise AirflowSkipException(
                                "Platform setup already performed. Skipping setup."
                          )
        elif platform_state == INITIALIZED:
                raise AirflowSkipException(
                                                "Platform setup already performed (Platform even initialized). Skipping setup."
                                          )

        

def setup_data_platform():
        platform_state = get_platform_state()
        if platform_state == SETUP_COMPLETED:
                logger.info("Platform setup already performed. Skipping setup.")
        elif platform_state == INITIALIZED:
                logger.info("Platform setup already performed (Platform even initialized). Skipping setup.")
        
        else:
                logger.info("Setting up platform database (ben_telecom_data_platform)")
                output = setup_platform_database()
                logger.info(output)


with DAG(
        dag_id="data_platform_setup",
        description="This DAG simply setup the data platform by creating all neccessary schemas and tables for cities reference, pipeline metadata, staging, data quality, and the datawarehouse",
        default_args=DEFAULT_ARGS

):
        
        check_data_platform_setup_execution_task = PythonOperator(
                task_id="check_data_platform_setup_execution",
                python_callable=check_data_platform_setup_execution
        )
        setup_data_platform_task = PythonOperator(
                task_id="setup_data_platform",
                python_callable=setup_data_platform
        )
        check_data_platform_setup_execution_task >> setup_data_platform_task