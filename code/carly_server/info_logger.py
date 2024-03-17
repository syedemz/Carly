import logging
from typing import NoReturn
from functools import wraps
import botocore
logger = logging.getLogger()
logger.setLevel(logging.INFO)



def global_logger(logtype: str, alertlevel: str, logmessage:str) -> NoReturn:
    """_summary_

    Args:
        logtype (str): _description_

    Returns:
        NoReturn: _description_
    """
    if(alertlevel == 'error'):
        logger.error("%s : %s", logtype, logmessage)
    else:
        logger.info("%s : %s", logtype, logmessage)
    


def dynamo_fetch_record(func) -> NoReturn:
    """_summary_

    Args:
        func (_type_): _description_

    Returns:
        _type_: _description_
    """
    @wraps(func)  # Preserves function metadata
    def wrapper_fetch_record(*args, **kwargs) -> object:
        try:
            # Call the original fetch_record function
            response = func(*args, **kwargs)
            return response
        except botocore.exceptions.ClientError as e:
            # Log the error
            global_logger('Server Error', 'error', f"Error fetching / updating record: {str(e)}")
            return None
        except KeyError as e:
            global_logger('Server Error', 'error',  f"Retrieved record seems to be invalid or have missing information: {str(e)}")
    return wrapper_fetch_record