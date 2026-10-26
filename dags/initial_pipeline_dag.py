
from airflow import DAG

from dags.utils.pipeline_factory import build_pipeline

with DAG(
        dag_id="initial_pipeline_dag",
        description="This DAG runs data pipeline for inital data extraction, quality checks, and loading processes.",

) as dag:
        build_pipeline(dag,
                       incremental=False
                       )