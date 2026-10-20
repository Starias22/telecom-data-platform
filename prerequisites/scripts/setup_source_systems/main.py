import subprocess
import os
import time
import signal

from dotenv import load_dotenv


from config.config import HOST, USER
from config.paths import PRODUCTION_DB_SETUP_SQL_CODE_PATH, PREREQUISITES_ENV_FILE_PATH, KAFKA_SETUP_SCRIPT_PATH
from scripts.setup_source_systems.produce_telecom_usage_events import produce_events



load_dotenv(PREREQUISITES_ENV_FILE_PATH)
env = os.environ.copy()

def setup_database():
        print("Setting up transactional database")
        subprocess.run(
                [
                        "psql",
                        "-h", HOST,
                        "-U", USER,
                        "-f", PRODUCTION_DB_SETUP_SQL_CODE_PATH
                ], env=env
        )
        print("Done")

def setup_kafka():
        print("Setting up Kaka")
        subprocess.run(
                [
                  "chmod", "+x", KAFKA_SETUP_SCRIPT_PATH
                ]
        )
        kafka = subprocess.Popen(["bash", KAFKA_SETUP_SCRIPT_PATH], start_new_session=True)
        time.sleep(5)

        try:
                # Produce telecom usage events
                produce_events()
                print("Done")
        finally:
                os.killpg(kafka.pid, signal.SIGTERM)
                try:
                        kafka.wait(timeout=10)
                except subprocess.TimeoutExpired:
                        os.killpg(kafka.pid, signal.SIGKILL)
                        kafka.wait()

if __name__ == "__main__":
        setup_database()
        setup_kafka()