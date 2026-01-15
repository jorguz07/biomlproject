import sys
from logger import logging #generate a log for the script in this file

#we create a function that takes an error from the system and transaltes is into something easier
#for us to read, as a string
def error_message_detail(error, error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename
    error_message="Error occured in python script [{0}] line number[{1}] error message[{2}]".format(
        file_name,exc_tb.tb_lineno,str(error))

    return error_message

#we create a class for the error message
class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
