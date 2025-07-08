import argparse
import importlib
import os
import pkgutil
from portswiggerlab import labs
from collections import defaultdict

def list_available_labs():
    grouped = defaultdict(list)
    for _, name, _ in pkgutil.iter_modules(labs.__path__):
        if name.startswith('_'):
            continue
        category = name.split('_')[0].upper()
        grouped[category].append(name)
    
    print("[*] Available Labs:\n")
    for category in sorted(grouped.keys()):
        print(f"{category}")
        for lab in sorted(grouped[category]):
            print(f"    - {lab}")

def main():
    # === Global args ===
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("--no-proxy", action="store_true", help="Disable proxy")
    global_parser.add_argument("--proxy", help="Custom proxy URL")
    global_parser.add_argument("--list-labs", action="store_true", help="List available labs and exit")

    parser = argparse.ArgumentParser(
        description="PortSwigger Labs Automation Toolkit",
        parents=[global_parser]
    )
    parser.add_argument("lab", nargs="?", help="Lab to run (e.g., sql_lab1)")
    parser.add_argument("--url", help="Target URL")
    parser.add_argument("--payload", help="Payload string")

    args = parser.parse_args()

    if args.list_labs:
        list_available_labs()
        return


    if not args.lab or not args.url or not args.payload:
        parser.print_help()
        return

    # === Proxy config ===
    proxies = None
    if not args.no_proxy:
        proxy_url = args.proxy or "http://127.0.0.1:8080"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

    # === Dynamically import selected lab ===
    try:
        lab_module = importlib.import_module(f"portswiggerlab.labs.{args.lab}")
        result = lab_module.run(args.url, args.payload, proxies)
        if result:
            print("[+] Lab solved successfully!")
        else:
            print("[-] Lab exploit failed.")
    except ModuleNotFoundError:
        print(f"[!] Lab '{args.lab}' not found. Use --list-labs to see available labs.")
    except AttributeError:
        print(f"[!] Lab '{args.lab}' does not have a 'run()' function.")
