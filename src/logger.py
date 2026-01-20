#we want to keep a record of things going right or wrong, particularly where, why, with which
#inputs

import os #work with paths and dirs, code works in any OS
import logging #python default logging system
from datetime import datetime

#NAMING LOG FILE
#we want a unique file per run, we use date and time to create unique names
LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
#datetime.now() returns current date and time
#.strftime() converts date and time data to a string of specific format

#STORING LOG FILE
logs_dir = os.path.join(os.getcwd(), "logs") #path to logs folder
os.makedirs(logs_dir, exist_ok=True) #craetes logs folder based on path
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE) #path to log file
#os.getcwd() returns string of current path
#os.path.joins() joins strings

#CREATING LOG FILE
#we import this function to toher scripts in src right after a piece of code we want to evaluate,
#we add a custom message on each use
logging.basicConfig(
    filename=LOG_FILE_PATH, #notice, whole path! w/o this logs go to terminal
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    #date and time, line, level (in this case, info, warning, error, critical), message (customizable)
    level=logging.INFO, #what we store, INFO stores (INFO, WARNING, ERROR, CRITICAL), there are other 'levels'
)

    