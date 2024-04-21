
import log_ex
import traceback

try:
    1/0
except ZeroDivisionError:
    log_ex.log(message='This is a test message' + '\n---- \n' + traceback.format_exc() + '---- \n', 
               type='ERROR', 
               verbose=False,
               logfile_by_day=False)