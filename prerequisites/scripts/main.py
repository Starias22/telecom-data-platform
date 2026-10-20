import subprocess
import os
import shutil
from scripts.generate_data.main import generate_data
from scripts.inject_data_quality_issues.main import inject_issues
from scripts.setup_source_systems.main import setup_database, setup_kafka

from config.paths import DATA_DIR, KAFKA_DIR, PURCHASES_SOURCES_DIR
import time

  

def copy_generated_data():
        
        subprocess.run([
                "rm", 
                "-rf", 
                DATA_DIR
                
                ]) # Remove the directory
        shutil.copytree(PURCHASES_SOURCES_DIR, DATA_DIR)
        shutil.copytree(KAFKA_DIR, DATA_DIR, dirs_exist_ok=True)




if __name__ == "__main__" :

        generate_data()

        inject_issues()

        setup_database()

        setup_kafka()

        copy_generated_data()