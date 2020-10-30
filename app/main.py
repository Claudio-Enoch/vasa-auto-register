from app.vasa_api import VasaApi
import requests
import re
import dotenv
import os

if __name__ == '__main__':
    dotenv.load_dotenv()
    headers = {
        "Connection": "keep-alive",
        "Accept": "*",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Dest": "document",
    }

    session = requests.Session()

    # GET LOGIN SESSION
    r_get_session = session.get(url="https://www.gympayment.com/login.aspx",
                                headers=headers
                                )
    r_get_session_html = r_get_session.text

    # LOGIN WITH CREDENTIALS
    view_state_generator = re.findall('id="__VIEWSTATEGENERATOR" value="(.*?)"', r_get_session_html)[0]
    view_state = re.findall('id="__VIEWSTATE" value="(.*?)"', r_get_session_html)[0]
    event_validation = re.findall('id="__EVENTVALIDATION" value="(.*?)"', r_get_session_html)[0]
    user_name = os.environ.get("USER_NAME")
    password = os.environ.get("PASSWORD")

    params = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": view_state,
        "__VIEWSTATEGENERATOR": view_state_generator,
        "__EVENTVALIDATION": event_validation,
        "ctl00$Main$Login$UserName": user_name,
        "ctl00$Main$Login$Password": password,
        "ctl00$Main$Login$Login": "Login"
    }
    headers = {
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://www.gympayment.com/login.aspx",
        "Accept-Encoding": "*",
    }

    r_login = session.post("https://www.gympayment.com/login.aspx",
                           data=params,
                           headers=headers,
                           allow_redirects=False)
    print("Hello world")
