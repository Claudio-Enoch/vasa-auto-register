import os

import dotenv

from app.helper import check_time_to_register
from app.vasa_api import VasaApi

dotenv.load_dotenv()
USERNAME = os.environ.get("VASA_USERNAME")
PASSWORD = os.environ.get("VASA_PASSWORD")
CLUB_ID = os.environ.get("VASA_CLUB_ID")

if __name__ == '__main__':
    class_type, hour = check_time_to_register()

    vasa = VasaApi(username=USERNAME, password=PASSWORD)

    class_id = vasa.search(club_id=CLUB_ID, class_type=class_type, class_time=hour)

    r = vasa.register(class_id=class_id)

    print(f'Registered for {r["scheduledClass"]["ClassName"]}, {r["scheduledClass"]["Availability"]} slots available')
