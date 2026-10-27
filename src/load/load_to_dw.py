import os
import subprocess

from dotenv import load_dotenv

from config.paths import SQL_INITIAL_SETUP_MAIN_FILE_PATH, ENV_FILE_PATH, SQL_QUALITY_CHECKS_FILE_PATH, INITIAL_LOAD_SQL_FILE_PATH, INCREMENTAL_LOAD_SQL_FILE_PATH
from config.config import HOST, DATA_PLATFORM_DB, USER

# from src.run_pipeline import run_pipeline

load_dotenv(ENV_FILE_PATH)
env = os.environ.copy()

def load(incremental=True, batch_id=None):
        command = [
                        "psql",
                        "-h", HOST,
                        "-U", USER,
                        "-d", DATA_PLATFORM_DB,
                        "-f", INCREMENTAL_LOAD_SQL_FILE_PATH if incremental else INITIAL_LOAD_SQL_FILE_PATH
                ]
        
        command.extend(["-v", f"batch_id={batch_id}"] if batch_id is not None else [])
        subprocess.run(command, env=env)
        
if __name__ ==  "__main__":
        load(incremental=False)