#we want to keep a record of things going right or wrong, particularly where, why, with which
#inputs, a problem was caused

import os
import logging #python default logging system
from datetime import datetime

#every run gets a log file
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

#where to store log file
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

#log file structure
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
#we will import this function in other files in src and specifify a message, the idea is to 
#generate a log file for the script in said file, with a message of our choice
    