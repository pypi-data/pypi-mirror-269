
import logging
import datetime as dt
import pdb


def log(message: str = '', 
        type: str = 'INFO', 
        verbose: bool = True, 
        logfile_by_day: bool = False) -> None:
    """_description_
    Simple logging function to log messages to the screen or to a file.

    Parameters
    ----------
    message : str, optional
        logging message, by default ''
    type : str, optional
        there are three types: ERROR, WARNING, INFO, by default 'INFO'
    verbose : str, optional
        show the messages in the screen, by default True
    logfile_by_day : bool, optional
        name of logfile is built by date, log-xxxxxxxx, by default False

    Returns
    -------
    _type_
        _description_
    """
    
    if verbose:
        logging.basicConfig(level=logging.DEBUG, 
                            format='[%(asctime)s] %(levelname)s - %(message)s')

        if type == 'INFO':
            logging.info(message)
            
        elif type == 'WARNING':
            logging.warning(message)
            
        elif type == 'ERROR':
            logging.error(message)

        
    if logfile_by_day:
        log_file = dt.datetime.now().strftime('%Y-%m-%d') + '.log'
    else:
        log_file = 'sys.log'
        
    
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(asctime)s] %(levelname)s - %(message)s',
                        filename=log_file,
                        filemode='a')

    if type == 'INFO':
        logging.info(message)
        
    elif type == 'WARNING':
        logging.warning(message)
        
    elif type == 'ERROR':
        logging.error(message)
        
    return None

        
