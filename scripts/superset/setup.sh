export SUPERSET_CONFIG_PATH="$(pwd)/superset/config.py"

export FLASK_APP=superset


superset db upgrade

superset fab create-admin

superset init

superset run -p 8088 --with-threads --reload # I used 8088 instead of 8080 which is already used  by airflow

# http://localhost:8088

