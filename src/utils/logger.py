import logging
import os
from dotenv import load_dotenv
from config.paths import ENV_FILE_PATH

def get_logger(name):
    load_dotenv(ENV_FILE_PATH)
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    # print("LOG_LEVEL:", LOG_LEVEL)
    logging.basicConfig(level=LOG_LEVEL,
                        format = "[%(asctime)s] %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S"
                        )
    logger = logging.getLogger(name)
    return logger

if __name__ == "__main__":
    logger = get_logger(__name__)
    logger.debug("This is a debug (For eg. Executing SQL query SELECT * FROM customers)") # It does not print if and only if you specify debug as log level (cause the rvel configired is info which is > debug)
    logger.info("This is an information (for eg. Starting customer extractioon)")
    logger.warning("This is a warning ( for eg no new customer records foound)")
    logger.error("This is an error (for eg. Failed to extract customer records)")
    logger.critical("This is critical (eg. Database connection unavailable)")
    

    


