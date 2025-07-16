import os, sys, re, argparse, importlib, pkgutil
from collections import defaultdict
from burplabs import labs
from prompt_toolkit import prompt
from colorama import init, Fore, Style
from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()
init(autoreset=True)
LABS_DIR = os.path.join(os.path.dirname(__file__), "labs")


def print_help():
    console.print(Panel.fit(
        "[bold cyan]PortSwigger Labs Automation Toolkit[/bold cyan]",
        subtitle="Automate Web Security Academy Labs"
    ))

    console.print("[bold yellow]Usage:[/bold yellow]")
    console.print(
        "  [green]burplabs[/green] [cyan][--list-labs | --interactive | <lab>] [--url URL] [--payload PAYLOAD] [--proxy PROXY | --no-proxy][/cyan]\n")

    console.print("[bold yellow]Examples:[/bold yellow]")
    console.print("  [green]burplabs --list-labs[/green]")
    console.print(
        "  [green]burplabs sql_lab1 --url https://0afe006b046.web-security-academy.net --payload \"'+OR+1=1--\" --no-proxy[/green]")
    console.print(
        "  [green]burplabs --interactive[/green] (then follow the steps)\n")

    console.print("[bold yellow]ATTENTION:[/bold yellow]")
    console.print("  • Use [cyan]--no-proxy[/cyan] if you are not using Burp!")
    console.print(
        "  • Use [cyan]--list-labs[/cyan] to see all available labs.\n")

    console.print("[bold magenta]Happy Hacking![/bold magenta]")


def extract_lab_number(lab_name):
    match = re.search(r'lab(\d+)', lab_name)
    return int(match.group(1)) if match else float('inf')

def list_available_labs():
    print(Fore.YELLOW + "[*] Available Labs:\n" + Style.RESET_ALL)
    grouped = defaultdict(list)

    lab_files = [f for f in os.listdir(LABS_DIR) if f.endswith(".py") and f != "__init__.py"]

    for lab_file in lab_files:
        lab_name = lab_file[:-3]
        category = lab_name.split('_')[0].upper()
        try:
            module = importlib.import_module(f'burplabs.labs.{lab_name}')
            title = getattr(module, "LAB_NAME", "")
            grouped[category].append((lab_name, title))
        except Exception:
            grouped[category].append((lab_name, ""))

    for category in sorted(grouped):
        print(f"{category}")
        for lab_name, title in sorted(grouped[category], key=lambda x: extract_lab_number(x[0])):
            print(f"    - {lab_name} : {title}" if title else f"    - {lab_name}")


def main():
    # === Global args ===
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument(
        "--no-proxy", action="store_true", help="Disable proxy")
    global_parser.add_argument("--proxy", help="Custom proxy URL")
    global_parser.add_argument(
        "--list-labs", action="store_true", help="List available labs and exit")
    global_parser.add_argument(
        "--interactive", action="store_true", help="Run in interactive mode")

    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        return

    # === First parse to catch --interactive early
    pre_args, _ = global_parser.parse_known_args()
    if pre_args.interactive:
        run_interactive_mode()
        return

    # === Full parser with subcommands
    parser = argparse.ArgumentParser(add_help=False, parents=[global_parser])

    parser.add_argument("lab", nargs="?", help="Lab to run (e.g., sql_lab1)")
    parser.add_argument("--url", help="Target URL")
    parser.add_argument("--payload", help="Payload string")
    args = parser.parse_args()

    if args.list_labs:
        list_available_labs()
        return

    if not args.lab or not args.url or not args.payload:
        print_help()
        return

    # === Proxy config
    proxies = None
    if not args.no_proxy:
        proxy_url = args.proxy or "http://127.0.0.1:8080"
        proxies = {
            "http": proxy_url,
            "https": proxy_url
        }

    # === Import and run selected lab
    try:
        lab_module = importlib.import_module(f"burplabs.labs.{args.lab}")
        result = lab_module.run(args.url, args.payload, proxies)
        if result:
            print(Fore.GREEN +
                  "[+] Lab solved successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "[-] Lab exploit failed." + Style.RESET_ALL)
    except ModuleNotFoundError:
        print(
            f"[!] Lab '{args.lab}' not found. Use --list-labs to see available labs.")
    except AttributeError:
        print(f"[!] Lab '{args.lab}' does not have a 'run()' function.")


def run_interactive_mode():
    print("\n=== PortSwiggerLab Interactive Mode ===")

    lab_base = labs.__path__[0]

    # Step 1: Discover categories
    excluded = {"__pycache__"}
    categories = [f.name for f in os.scandir(lab_base) if f.is_dir() and f.name not in excluded]
    categories.sort()

    print("\nAvailable Categories:")
    for idx, cat in enumerate(categories, start=1):
        print(f"{idx}. {cat.upper()}")

    # Step 2: Select category
    try:
        cat_index = int(prompt("\nSelect a category number: ")) - 1
        selected_category = categories[cat_index]
    except (ValueError, IndexError):
        print("[!] Invalid category selection.")
        return
    except KeyboardInterrupt:
        print("\n[!] Exiting interactive mode.")
        return

    # Step 3: List labs inside category
    category_path = os.path.join(lab_base, selected_category)
    available_labs = sorted(
        [name for _, name, _ in pkgutil.iter_modules([category_path]) if not name.startswith('_')],
        key=lambda name: int(re.search(r'lab(\d+)', name).group(1)) if re.search(r'lab(\d+)', name) else float('inf')
    )

    print(f"\n[{selected_category.upper()} Labs]")
    for i, lab in enumerate(available_labs, start=1):
        try:
            module = importlib.import_module(f'burplabs.labs.{selected_category}.{lab}')
            title = getattr(module, "LAB_NAME", "")
            print(f"{i}. {lab} : {title}")
        except:
            print(f"{i}. {lab}")

    # Step 4: Select lab
    try:
        lab_index = int(prompt("\nSelect a lab number: ")) - 1
        selected_lab = available_labs[lab_index]
    except (ValueError, IndexError):
        print("[!] Invalid lab selection.")
        return
    except KeyboardInterrupt:
        print("\n[!] Exiting interactive mode.")
        return

    # Step 5: URL + Payload + Proxy
    try:
        url = prompt("Target URL: ").strip()
        if not url.startswith("http"):
            url = "https://" + url
        payload = prompt("Payload: (Optional, Just skip it.) ").strip()
        use_proxy = prompt("Use Burp proxy (127.0.0.1:8080)? [Y/n]: ").lower().strip()
    except KeyboardInterrupt:
        print("\n[!] Exiting interactive mode.")
        return

    proxies = None
    if use_proxy in ("", "y", "yes"):
        proxies = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}

    # Step 6: Run
    print(f"\n[>] Running {selected_lab} from {selected_category} with payload: {payload}")
    try:
        lab_module = importlib.import_module(f"burplabs.labs.{selected_category}.{selected_lab}")
        result = lab_module.run(url, payload, proxies)
        if result:
            print("[+] Lab solved successfully!")
        else:
            print("[-] Lab exploit failed.")
    except Exception as e:
        print(f"[!] Error running lab: {e}")