
from datetime import timedelta

from airflow import DAG

from dags.utils.pipeline_factory import build_pipeline, DEFAULT_ARGS
from config.config import DAGS_TAG




with DAG(
        dag_id="incremental_pipeline",
        description="This DAG is designed to runs the data pipeline daily for incremental (ie differential) extraction, storage, quality checks and loading processes.",
        tags=[DAGS_TAG],
        default_args=DEFAULT_ARGS

) as dag:
        build_pipeline(dag,
                       incremental=True
                       )