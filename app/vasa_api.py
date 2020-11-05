import json
import os
import re

from datetime import datetime, timedelta

from requests import Session

from app.helper import retry, utc_time

dir_path = os.path.dirname(os.path.realpath(__file__))


class VasaApi:
    """Minimal wrapper for the Vasa Fitness API"""

    def __init__(self, username: str, password: str):
        self._memb_num = None
        self._session = Session()
        self._login(username=username, password=password)

    def _login(self, username: str, password: str):
        # create session
        login_url = "https://www.gympayment.com/login.aspx"
        headers = {"Connection": "keep-alive", "Accept": "*"}
        response = self._session.get(url=login_url, headers=headers)
        response_html = response.text

        # parse out form session variables
        view_state_generator = re.findall('id="__VIEWSTATEGENERATOR" value="(.*?)"', response_html)[0]
        event_validation = re.findall('id="__EVENTVALIDATION" value="(.*?)"', response_html)[0]
        view_state = re.findall('id="__VIEWSTATE" value="(.*?)"', response_html)[0]

        # create auth cookie
        payload = {"__EVENTTARGET": "",
                   "__EVENTARGUMENT": "",
                   "__VIEWSTATE": view_state,
                   "__VIEWSTATEGENERATOR": view_state_generator,
                   "__EVENTVALIDATION": event_validation,
                   "ctl00$Main$Login$UserName": username,
                   "ctl00$Main$Login$Password": password,
                   "ctl00$Main$Login$Login": "Login", }
        headers = {
            "Accept": "*",
            "Accept-Encoding": "*",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        self._session.post(url=login_url, data=payload, headers=headers)
        assert self._session.cookies.get_dict().get("authCookie"), "error creating the authCookie"

        # get membership ID
        membership_url = "https://www.gympayment.com/service.asmx/GetMemberships"
        self._session.headers.update({"Content-Type": "application/json;charset=UTF-8"})
        response = self._session.post(url=membership_url)
        self._memb_num = response.json()["d"][0]["membNum"]
        assert self._memb_num, "error finding member number"

    @retry(seconds=2, attempts=300)
    def search(self, club_id: str, class_type: str, class_time: str) -> int:
        """Return a list of all classes found and their respective metadata"""
        with open(os.path.join(dir_path, "..", "vasa_class_map.json")) as file:
            class_map = json.load(file)
        class_type_id = class_map[class_type]
        search_url = "https://www.gympayment.com/service.asmx/LoadClasses"
        class_date = utc_time() + timedelta(days=2)
        payload = {"classType": class_type_id,
                   "clubAt": club_id,
                   "clubID": club_id,
                   "start": f"{class_date.isoformat()[:10]}T00:00:00.000",
                   "end": f"{class_date.isoformat()[:10]}T23:00:00.000",
                   "membNum": self._memb_num, }
        response_json = self._session.post(url=search_url, json=payload).json()
        assert (classes := response_json["d"]), f"did not find any classes for: {class_type} on {class_date}"
        for _class in classes:
            if _class["ClassTime"].startswith(class_time):  # "4:00PM - 5:00PM".startswith("4:00PM")
                return _class["Id"]
        raise AssertionError(f"did not find any {class_type} classes starting at: {class_time}")

    def register(self, class_id: int) -> dict:
        """Register for vasa class by ID"""
        register_url = "https://www.gympayment.com/service.asmx/RegisterForClass"
        payload = {"ID": class_id}
        response = self._session.post(url=register_url, json=payload)
        response_json = response.json()["d"]
        if response_json["Success"] is False:
            raise ValueError(f"Error signing up for class ({class_id})")
        return response_json
