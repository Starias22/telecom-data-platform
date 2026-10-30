import os
import subprocess

from dotenv import load_dotenv

from config.paths import SQL_INITIAL_SETUP_MAIN_FILE_PATH, ENV_FILE_PATH, SQL_QUALITY_CHECKS_FILE_PATH
from config.config import HOST, DATA_PLATFORM_DB, USER

load_dotenv(ENV_FILE_PATH)
env = os.environ.copy()

def check_quality(batch_id=1):
        try:
            result = subprocess.run(
                [
                        "psql",
                        "-h", HOST,
                        "-U", USER,
                        "-d", DATA_PLATFORM_DB,
                        "-f", SQL_QUALITY_CHECKS_FILE_PATH,
                        "-v", f"batch_id={batch_id}",
                        "-v", "ON_ERROR_STOP=1" # Pour que la commande lance une exception CalledProcessError en cas d eprobleme / erreur
                ],
                env=env,
                capture_output=True,
                text=True,
                check=True
        )
        except subprocess.CalledProcessError as e:
            print(e.stdout)
            error_message = e.stderr           
            print(error_message)

            raise RuntimeError(error_message) from e # Relancer ie propage rlerreur
            
        
        
if __name__ ==  "__main__":
        check_quality()