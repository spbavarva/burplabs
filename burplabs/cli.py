import os, sys, argparse, importlib, pkgutil
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
    console.print("  [green]burplabs[/green] [cyan][--list-labs | --interactive | <lab>] [--url URL] [--payload PAYLOAD] [--proxy PROXY | --no-proxy][/cyan]\n")

    console.print("[bold yellow]Examples:[/bold yellow]")
    console.print("  [green]burplabs --list-labs[/green]")
    console.print("  [green]burplabs sql_lab1 --url https://0afe006b046.web-security-academy.net --payload \"'+OR+1=1--\" --no-proxy[/green]")
    console.print("  [green]burplabs --interactive[/green] (then follow the steps)\n")

    console.print("[bold yellow]ATTENTION:[/bold yellow]")
    console.print("  • Use [cyan]--no-proxy[/cyan] if you are not using Burp!")
    console.print("  • Use [cyan]--list-labs[/cyan] to see all available labs.\n")

    console.print("[bold magenta]Happy Hacking![/bold magenta]")

def list_available_labs():
    print(Fore.YELLOW + "[*] Available Labs:\n" + Style.RESET_ALL)
    grouped = defaultdict(list)
    for lab_file in os.listdir(LABS_DIR):
        if lab_file.endswith(".py") and lab_file != "__init__.py":
            lab_name = lab_file[:-3]
            category = lab_name.split('_')[0].upper()

            # Import the module dynamically
            try:
                module = importlib.import_module(f'burplabs.labs.{lab_name}')
                title = getattr(module, "LAB_NAME", "")
                grouped.setdefault(category, []).append((lab_name, title))
            except Exception:
                grouped.setdefault(category, []).append((lab_name, ""))

    for category, labs in grouped.items():
        print(f"{category}")
        for lab_name, title in labs:
            if title:
                print(f"    - {lab_name} : {title}")
            else:
                print(f"    - {lab_name}")


def main():
    # === Global args ===
    global_parser = argparse.ArgumentParser(add_help=False)
    global_parser.add_argument("--no-proxy", action="store_true", help="Disable proxy")
    global_parser.add_argument("--proxy", help="Custom proxy URL")
    global_parser.add_argument("--list-labs", action="store_true", help="List available labs and exit")
    global_parser.add_argument("--interactive", action="store_true", help="Run in interactive mode")

    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        return

    # === First parse to catch --interactive early
    pre_args, _ = global_parser.parse_known_args()
    if pre_args.interactive:
        run_interactive_mode()
        return

    # === Full parser with subcommands
    parser = argparse.ArgumentParser(add_help=False,parents=[global_parser])

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
            print(Fore.GREEN + "[+] Lab solved successfully!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "[-] Lab exploit failed." + Style.RESET_ALL)
    except ModuleNotFoundError:
        print(f"[!] Lab '{args.lab}' not found. Use --list-labs to see available labs.")
    except AttributeError:
        print(f"[!] Lab '{args.lab}' does not have a 'run()' function.")


def run_interactive_mode():
    print("\n=== PortSwiggerLab Interactive Mode ===")

    # Step 1: List labs
    available_labs = [name for _, name, _ in pkgutil.iter_modules(labs.__path__) if not name.startswith('_')]
    for i, lab in enumerate(available_labs, start=1):
        try:
            module = importlib.import_module(f'burplabs.labs.{lab}')
            title = getattr(module, "LAB_NAME", "")
            print(f"{i}. {lab} : {title}")
        except:
            print(f"{i}. {lab}")

    # Step 2: Select lab
    try:
        while True:
            try:
                lab_index = int(prompt("\nSelect a lab number: ")) - 1
                if 0 <= lab_index < len(available_labs):
                    selected_lab = available_labs[lab_index]
                    break
                print("Invalid selection, try again.")
            except ValueError:
                print("Please enter a valid number.")
    except KeyboardInterrupt:
        print("\n[!] Exiting interactive mode.")
        return

    # Step 3: Enter URL
    try:
        url = prompt("Target URL: ").strip()
        payload = prompt("Payload: ").strip()
        use_proxy = prompt("Use Burp proxy (127.0.0.1:8080)? [Y/n]: ").lower().strip()
    except KeyboardInterrupt:
        print("\n[!] Exiting interactive mode.")
        return

    proxies = None
    if use_proxy in ("", "y", "yes"):
        proxies = {
            "http": "http://127.0.0.1:8080",
            "https": "http://127.0.0.1:8080"
        }

    # Step 6: Run
    print(f"\n[>] Running {selected_lab} with payload: {payload}")
    try:
        lab_module = importlib.import_module(f"burplabs.labs.{selected_lab}")
        result = lab_module.run(url, payload, proxies)
        if result:
            print("[+] Lab solved successfully!")
        else:
            print("[-] Lab exploit failed.")
    except Exception as e:
        print(f"[!] Error running lab: {e}")
