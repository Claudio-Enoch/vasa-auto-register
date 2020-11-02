import calendar
import json
import os
import time

from datetime import datetime, timedelta
from typing import Tuple

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "..", "vasa_registration.json")) as file:
    vasa_registration_json = json.load(file)


def utc_time():
    return datetime.utcnow() - timedelta(hours=7)


def check_time_to_register() -> Tuple[str, str]:
    """
    Check if it's time to register for desired class in vasa_registration.json.
    Classes will be found starting 47 hours 2 min prior to the registration open (start searching 2 min early).
    """

    # get day of week
    two_day_offset = (utc_time() + timedelta(days=2)).weekday()
    offset_day = calendar.day_name[two_day_offset]  # Wednesday
    # get mt time
    utc_offset = (utc_time() + timedelta(minutes=2))
    offset_time = utc_offset.strftime("%I").lstrip("0") + utc_offset.strftime(":%M%p")  # 8:55AM

    for class_type, class_times in vasa_registration_json[offset_day].items():
        if offset_time in class_times:
            print(f"{utc_time()} - Registering for {class_type} at {offset_time} on {offset_day}")
            return class_type, offset_time  # ( "CARDIO", "9:30AM" )
    print(f"{utc_time()} - ... skipped {offset_time} on {offset_day}")
    exit(0)


def retry(seconds: int, attempts: int):
    """Retry function for 5 minutes at 5 second intervals"""

    def inner(func):
        def wrapper(*args, **kwargs):
            nonlocal attempts
            while attempts > 0:
                attempts -= 1
                print(f"{utc_time()} *** attempt # {attempts}")
                time.sleep(seconds)
                try:
                    return func(*args, **kwargs)
                except AssertionError as e:
                    print(e)
            print(f"Retries exceeded {attempts} attempts, exiting program")
            exit(0)

        return wrapper

    return inner
