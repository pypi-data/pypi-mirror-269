
from datetime import datetime as dt
import time
import pytz

def get_unix_timestamp() -> int:
    return int(time.time())
    #
def get_dt_timestamp() -> dt:
    return dt.now()
    #
def dt_to_unix(now: dt) -> int:
    return int(time.mktime(now.timetuple()))
    #
def unix_to_dt(unix_time: int) -> dt:
    unix_timestamp = unix_time
    utc_datetime = dt.utcfromtimestamp(unix_timestamp)
    desired_timezone = 'Asia/Phnom_Penh'
    timezone_object = pytz.timezone(desired_timezone)
    localized_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(timezone_object)
    return localized_datetime#.strftime('%Y-%m-%d %H:%M')
    #















