#this module configures logging for the project,
# - creates a log with important steps on the process and errors
# - names it uniquely based on time and date

import os #work with paths and dirs, code works in any OS
import logging #python built in logging sys
from datetime import datetime #used for naming

#create var for naming file
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
#as we want a unique file per run, we use date and time to create unique names
####datetime.now() - current date and time
####.strftime() - converts current date and time to specific format

#create storing file
logs_dir = os.path.join(os.getcwd(), "logs") #create var for logs folder: current path + 'logs'
os.makedirs(logs_dir, exist_ok=True) #create folder
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE) #crate var log file

#python built in logging sys; basicConfig() configures logging for the whole project
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    #log looks like: [time] line_number module_name - LEVEL - custom message
    #e.g. [ 03_18_2026_12_30_00 ] 45 data_ingestion - INFO - Train test split initiated
    level=logging.INFO, #there are 5 logging levels, ordered by severity. This stores levels 2-5 (1 too noisy)
)


    