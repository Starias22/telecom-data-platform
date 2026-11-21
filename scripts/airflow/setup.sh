export PROJECT_ROOT="/home/starias/myprojects/telecom-data-platform"


export AIRFLOW_HOME="$PROJECT_ROOT/airflow"
echo $AIRFLOW_HOME

export AIRFLOW__LOGGING__BASE_LOG_FOLDER="$AIRFLOW_HOME/logs"
echo $AIRFLOW__LOGGING__BASE_LOG_FOLDER
airflow config get-value logging base_log_folder


export AIRFLOW__CORE__DAGS_FOLDER="$PROJECT_ROOT/dags" 
echo $AIRFLOW__CORE__DAGS__FOLDER
airflow config get-value core dags_folder

export PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH"



airflow standalone