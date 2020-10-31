import calendar
import json
import os
import time

from datetime import datetime, timedelta
from typing import Tuple

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(dir_path, "..", "vasa_registration.json")) as file:
    vasa_registration_json = json.load(file)


def check_time_to_register() -> Tuple[str, str]:
    """
    Check if it's time to register for desired class in vasa_registration.json.
    Classes will be returned starting 48h 5m minutes prior to the registration open.
    """

    # get day of week
    two_day_offset = (datetime.today() + timedelta(days=2)).weekday()  # TODO: use UTC to get MT day of week
    offset_day = calendar.day_name[two_day_offset]  # Wednesday
    # get mt time
    time_now = (datetime.utcnow() - timedelta(hours=6, minutes=-2))
    time_now = time_now.strftime("%I").lstrip("0") + time_now.strftime(":%M%p")  # 8:55AM

    for class_type, class_times in vasa_registration_json[offset_day].items():
        if time_now in class_times:
            return class_type, time_now  # ( "CARDIO", "9:30AM" )
    print(f"No registrations wanted for {time_now} on {offset_day}")
    exit(0)


def retry(seconds: int, attempts: int):
    """Retry function for 5 minutes at 5 second intervals"""

    def inner(func):
        def wrapper(*args, **kwargs):
            nonlocal attempts
            while attempts > 0:
                attempts -= 1
                print("*** Attempt: ", attempts)
                time.sleep(seconds)
                try:
                    return func(*args, **kwargs)
                except AssertionError as e:
                    print(e)
            raise LookupError(f"Retries exceeded {attempts} attempts, exiting program")

        return wrapper

    return inner
