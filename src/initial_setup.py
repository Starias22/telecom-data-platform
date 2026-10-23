import subprocess
import os
from dotenv import load_dotenv

from config.paths import SQL_INITIAL_SETUP_MAIN_FILE_PATH, ENV_FILE_PATH, DATA_DIR
from config.config import HOST, USER
from src.run_pipeline import run_pipeline


load_dotenv(ENV_FILE_PATH)
env = os.environ.copy()

def setup_data_platform_database():
        subprocess.run(
                [
                        "psql",
                        "-h", HOST,
                        "-U", USER,
                        "-f", SQL_INITIAL_SETUP_MAIN_FILE_PATH
                ],
                env=env
        )


def setup_kafka():
        subprocess.Popen(
                [
                        "./kafka/bin/kafka-server-start.sh", "./kafka/config/server.properties"
                ],
                cwd=DATA_DIR
        )
if __name__ == "__main__":
        setup_kafka()
        # exit()
        setup_data_platform_database()
        run_pipeline()
        print("************************")