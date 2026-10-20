import subprocess
import os
from dotenv import load_dotenv

from config.paths import SQL_INITIAL_SETUP_MAIN_FILE_PATH, ENV_FILE_PATH
from config.config import HOST, DATA_PLATFORM_DB, USER

from src.run_pipeline import run

load_dotenv(ENV_FILE_PATH)
env = os.environ.copy()

def setup_data_platform_database():
        subprocess.run(
                [
                        "psql",
                        "-h", HOST,
                        "-U", USER,
                        # "-d", DATA_PLATFORM_DB,
                        "-f", SQL_INITIAL_SETUP_MAIN_FILE_PATH
                ],
                env=env
        )

if __name__ == "__main__":
        setup_data_platform_database()