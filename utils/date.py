from datetime import timedelta
import datetime
from configuration.config import EXECUTION_TIME_INTERVAL

def get_last_hour_date_string():
    """
    Returns the previous hour's date in ISO 8601 format.
    :return: str
    """

    current_date = datetime.datetime.utcnow()
    delta = timedelta(hours=-EXECUTION_TIME_INTERVAL, minutes=-10)
    previous_hour_date = current_date + delta
    return previous_hour_date.strftime("%Y-%m-%dT%H:%M:%S-00:00")

