
from datetime import timedelta

from airflow import DAG

from dags.utils.pipeline_factory import build_pipeline, DEFAULT_ARGS



with DAG(
        dag_id="incremental_data_pipeline",
        description="This DAG is designed to runs the data pipeline daily for incremental (ie differential) extraction, storage, quality checks and loading processes.",
        default_args=DEFAULT_ARGS

) as dag:
        build_pipeline(dag,
                       incremental=True
                       )