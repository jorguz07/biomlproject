#we create a custom exception we want raised whenever an error happens. It summarizes error info
#in an easier to read way
 
import sys
from logger import logging #we want errors to be logged too!

#we create a function that takes an error from the system and transaltes it
def error_message_detail(error, error_detail:sys):
    '''Takes error object and its details from system and creates a string that summarizes it
    and makes it easier to read. Prints file that generated the error, line and system error msg'''
    _,_,exc_tb=error_detail.exc_info() #extract tb object
    file_name=exc_tb.tb_frame.f_code.co_filename #get file name from tb obj
    error_line=exc_tb.tb_lineno #get line from tb obj
    error_message="Error occured in python script [{0}] line number[{1}] error message[{2}]".format(
        file_name,error_line,str(error))

    return error_message
#sys.exec_info() returns a tuple (tuple, value, traceback) e.g. (ValueError, ValueError("bad input), <traceback object>")
#_ means we ignore the first two, we just store the traceback obj as exc_tb

#getting info from tb obj
#exc_tb.tb_frame.f_code.co_filename (somehow) extracts the name of the file that generated the error
#exc_tb.tb_lineno extracts line of code that generated error


#we create a custom exception that uses our error_message_detail function
class CustomException(Exception): #new class CustomException is an Exception
    def __init__(self, error_message, error_detail:sys): #def
        logging.error(self.error_message) #chatgpt recommendation
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self): #method
        return self.error_message
