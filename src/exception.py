#this module creates a custom exception that
# - summarizes exception info
# - logs it

#when coding, we raise errors, usually as 'raise e'. 
#here we will use 'raise somecustomerror(e, sys)

import sys
from src.logger import logging #we want errors to be logged too!

#function that translates error from sys
def error_message_detail(error, error_detail:sys): #define object type of error_detail
    ''' Takes error object and its details from system and creates a string that shows script where
    error is, line and then the original system error '''
    _,_,exc_tb=error_detail.exc_info() #extract throwback: exception location
    file_name=exc_tb.tb_frame.f_code.co_filename #script that produced error
    error_line=exc_tb.tb_lineno #line in script that produced error
    error_message="Error occured in python script [{0}] line number[{1}] error message[{2}]".format(
        file_name,error_line,str(error)) #custom message, gives sys error at the end anyways

    return error_message
#sys.exec_info() returns (type, value, traceback), i.e. exception type, message, location

#custom exception (subclass of Exception)
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys): #error and details
        self.error_message=error_message_detail(error_message,error_detail=error_detail) #translating function
        logging.error(self.error_message) #logging
        super().__init__(error_message) #calling parent class Exception, so sys recognizes it as exception
        #we call CustomException() with error and error details as input; the moment the obj is created, it
        #logs the error message and its created as an Exception
        
    def __str__(self): #defines what to print when printing Exception
        return self.error_message
