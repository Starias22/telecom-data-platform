
from datetime import timedelta

from airflow import DAG

from dags.utils.pipeline_factory import build_pipeline

default_args = {
        "retries":2,
        "retry_delay":timedelta(seconds=10)
}

with DAG(
        dag_id="incremental_data_pipeline",
        description="This DAG is designed to runs the data pipeline daily for incremental (ie differential) extraction, storage, quality checks and loading processes.",
        default_args=default_args

) as dag:
        build_pipeline(dag,
                       incremental=True
                       )