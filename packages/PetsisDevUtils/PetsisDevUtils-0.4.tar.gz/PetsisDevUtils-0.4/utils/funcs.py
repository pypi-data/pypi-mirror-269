from datetime import datetime, timedelta
import hashlib
import os
import pyotp
import pytz
import random
import re
import requests
import secrets
import sys
import time
import uuid

from .Logga import *


def wait(n=1.0):
    log(f'utils.wait:{ln()}: waiting:{n}s')
    time.sleep(n)
    #
def rand_wait(n_min: float = 1, n_max: float = 2):
    n = random.uniform(n_min, n_max)
    t = round(n, 2)
    log(f'utils.rand_wait:{ln()}: waiting:{t}s')
    time.sleep(t)
    #
def ln():
    return sys._getframe(1).f_lineno

def get_unix_timestamp() -> int:
    return int(time.time())
    #
def get_dt_timestamp() -> datetime:
    return datetime.now()
    #
def dt_to_unix(now: datetime) -> int:
    return int(time.mktime(now.timetuple()))
    #
def unix_to_dt(unix_time: int) -> datetime:
    unix_timestamp = unix_time
    utc_datetime = datetime.utcfromtimestamp(unix_timestamp)
    desired_timezone = 'Asia/Phnom_Penh'
    timezone_object = pytz.timezone(desired_timezone)
    localized_datetime = utc_datetime.replace(tzinfo=pytz.utc).astimezone(timezone_object)
    return localized_datetime
    #
def get_unix_with_offset(hours: int = 1):
    timestamp = datetime.now() + timedelta(hours=hours)
    return dt_to_unix(timestamp)
    #
def get_next_time(current_time:datetime, time_range:tuple=(100, 2330)) -> datetime:
    best_times = time_range
    times = list()
    if best_times[0] > best_times[1]:
        for i in range(best_times[0], 2359):
            hour = str(i)[:2]
            minute = str(i)[-2:]
            if int(minute) < 60:
                times.append((hour, minute))

        for i in range(0, best_times[1]):
            hour = str(i)[:-2]
            if not len(hour):
                hour = "0"

            minute = str(i)[-2:]
            if len(minute) < 2:
                minute = f"0{minute}"

            if int(minute) < 60:
                times.append((hour, minute))
    else:
        for i in range(best_times[0], best_times[1]):
            hour = str(i)[:-2]
            if not len(hour):
                hour = "0"

            minute = str(i)[-2:]
            if len(minute) < 2:
                minute = f"0{minute}"

            if int(minute) < 60:
                times.append((hour, minute))

    midnight = current_time.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    best_time = secrets.choice(times)
    hour = int(best_time[0])
    minute = int(best_time[1])
    day = 0
    if not hour > current_time.hour:
        day = 1

    return midnight + timedelta(days=day, hours=hour, minutes=minute)
    #
def get_best_time():
    current = datetime.now()
    res = get_next_time(current)
    t = dt_to_unix(res)
    return t
    #


def get_2fa(secret_key):
    return pyotp.TOTP(secret_key).now()
    #
def generate_uuid(suffix: str = None):
    ids = str(uuid.uuid4())[:8]
    if suffix:
        ids += f"_{suffix}"
    return ids
def generate_api_signature(api_timestamp, api_nonce, api_secret):
    parameter_string = f"{api_timestamp}{api_nonce}{api_secret}"
    return hashlib.sha1(parameter_string.encode()).hexdigest()
    #


def download_file(file: dict):
    log(f'utils.download_file:{ln()}: downloading file...')
    url = file['url_short']
    res = requests.get(url)
    file_name = file['name']
    if '.' in file_name:
        file_name = file_name.split('.')[0]
    file_path = f"./Bot/FILES/{file_name}.{file['typ']}"
    file['relative_path'] = './Bot/FILES/'
    file['file_path'] = file_path

    try:
        with open(file_path, 'wb') as fp:
            fp.write(res.content)
            log(f'utils.download_file:{ln()}: file downloaded')
    except Exception as e:
        log(f'utils.download_file:{ln()}: error downloading: {e}', level='ERROR')

    return file
    #
def delete_local_file(path):
    os.remove(path)
    #
def remove_emojs(string:str):
    broad_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002702-\U000027B0"  # Dingbats
                               u"\U000024C2-\U0001F251"  # Enclosed characters
                               "]+", flags=re.UNICODE)
    text = broad_pattern.sub(r'', string)  # Remove everything matched by broad_pattern
    return text









