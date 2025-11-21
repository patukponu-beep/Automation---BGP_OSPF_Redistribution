import json
import os
import time
import getpass
from ipaddress import ip_interface
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv

from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
from jinja2 import FileSystemLoader, Environment, TemplateError

load_dotenv()  # Load environment variables from .env file
MAX_RETRIES = 2  # number of retries after the first attempt
RETRY_DELAY = 3  # seconds between retries


def load_inventory(inventorypath):
    """Loading Inventory from file"""
    with open(inventorypath, 'r') as f:
        inventory = json.load(f)
    return inventory


def render_jinja(inventory, jinjafolderpath, jinjatemp):
    """Loads a Jinja2 template and renders it with the provided data"""
    JinjaFolderLoader = FileSystemLoader(jinjafolderpath)
    env = Environment(loader=JinjaFolderLoader)

    def ip_converter(value):
        """Converts slash notation to IP + netmask object."""
        return ip_interface(value)

    env.filters['ipaddr'] = ip_converter
    # -----------------------------------------
    template = env.get_template(jinjatemp)
    render_cfg = []

    for dev_name, dev_data in inventory['devices'].items():
        output = template.render(device=dev_data)
        commands = [line for line in output.splitlines() if line.strip()]

        render_cfg.append({
            "devices": dev_name,
            "commands": commands
        })
    return render_cfg


def save_render_config(dev_name, commands, pre_push):
    """Per Network Device: Saves the rendered Template to Local Path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_folder = os.path.join(pre_push, dev_name)
    os.makedirs(device_folder, exist_ok=True)
    filename = os.path.join(device_folder, f"{dev_name}_{timestamp}.txt")
    config_string = "\n".join(commands)
    with open(filename, "w") as f:
        f.write(config_string)
    return filename


def push_config(dev_data, commands):
    """Per Network Device: Netmiko Connection and Configuration"""
    ssh_info = dev_data['connection']

    with ConnectHandler(**ssh_info) as conn:
        conn.enable()  # Not always needed but best practice
        output = conn.send_config_set(commands)
        # save_output = conn.save_config()  # or conn.send_command('write memory')
        # full_output = f"{output}----WRITE MEMORY----{save_output}"
        # Commented out because I can...But also cuz of separation of concerns
        # The script should be only be applying commands, not also saving to NVRAM

    return output


def save_push_config(dev_name, output, post_push):
    """Per Network Device: Saves the Configuration to Local Path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_folder = os.path.join(post_push, dev_name)
    os.makedirs(device_folder, exist_ok=True)
    filename = os.path.join(device_folder, f"{dev_name}_session_{timestamp}.log")
    with open(filename, "w") as f:
        f.write(output)
    return filename


def push_concurrent(dev_name, dev_data, commands, pre_push, post_push, dry_run=False,
                    max_retries=MAX_RETRIES, retry_delay=RETRY_DELAY):
    """Sets Up Functions for Concurrent Automation"""
    status_info = {"devices": dev_name,
                   "mode": "DRY RUN" if dry_run else "REAL RUN",
                   "status": "success",
                   "reason": None,
                   "push_attempts": 0}
    try:
        save_render_config(dev_name, commands, pre_push)
    except Exception as e:
        status_info['status'] = "UNKNOWN FAILURE"
        status_info['reason'] = f"PRE-SAVE ERROR: {e}"

        return status_info  # Because, i don't wanna continue when i can't save my rendered template concurrently

    if dry_run:
        status_info['status'] = "DRY RUN"
        status_info['reason'] = "RENDERED & SAVED ONLY"
        status_info['push_attempts'] = 0
        return status_info  # Because, this a dry run don't wanna continue with push_config

    bad_markers = [
        "invalid input detected",
        "bad ip address or host name",
        "invalid input detected while parsing",
        "invalid input detected at '^' marker.",
        "invalid input detected while parsing",
        "invalid input detected at '^' position",
        "invalid input",
        "ambiguous command",
        "incomplete command"
    ]
    for attempt in range(1, max_retries + 2):
        """Sets Up the Retry loop with Conditions"""
        status_info['push_attempts'] = attempt
        try:
            output = push_config(dev_data, commands)
            save_push_config(dev_name=dev_name, output=output, post_push=post_push)

            output_cf = output.casefold()
            if any(m in output_cf for m in bad_markers):
                status_info['status'] = "CONFIG ERROR"
                status_info['reason'] = "CLI ERROR IN OUTPUT"
            else:
                status_info['status'] = "success"
                status_info['reason'] = None
            break  # cuz there's a success or config error - we don't run the loop again here.

        except NetmikoAuthenticationException as e:
            status_info['status'] = "AUTH FAILURE"
            status_info['reason'] = str(e)
            break  # cuz if there's an auth failure(wrong credentials obviously) why retry ?

        except NetmikoTimeoutException as e:
            status_info['status'] = "TIMEOUT"
            status_info['reason'] = str(e)

        except Exception as e:
            status_info['status'] = "UNKNOWN FAILURE"
            status_info['reason'] = str(e)
        #     But we gonna retry here because it's either a Timeout or an unknown error

        if attempt <= max_retries:
            time.sleep(retry_delay)
        else:
            break

    return status_info


def get_user_preference():
    while True:
        print("\nSelect run mode:")
        print("Y - Dry Run (simulation only)")
        print("N - Normal Run (real execution)")

        choice = input("Enter Y or N: ").strip().lower()

        if choice in ['y', 'yes', '1']:
            print("Starting DRY RUN mode...")
            return True  # dry_run=True ie Dry_Run activated from main
        elif choice in ['n', 'no', '2']:
            print("\n⚠️ WARNING: NORMAL RUN mode selected!")
            print("   • Real configurations will be pushed to network devices")
            print("   • This will make actual changes to your infrastructure")

            # Inner loop for confirmation with back option
            while True:
                confirm = input(
                    "\nType 'yes' to continue, 'no' to cancel, or 'back' to return to main menu: ").strip().lower()

                if confirm in ['yes', 'y', '1']:
                    print("\n🚀 Starting NORMAL RUN mode...")
                    return False  # dry_run=False ie Real Run activated from main
                elif confirm in ['no', 'n', '2']:
                    print("Operation cancelled. Exiting...")
                    exit()  # exits all loops
                elif confirm in ['back', 'b', 'return']:
                    print("Returning to main menu...")
                    break  # exists just the 2nd loop to the 1st loop
                else:
                    print("❌ Invalid input! Please enter 'yes', 'no', or 'back'.")

        else:
            print("❌ Invalid input! Please enter only 'Y' or 'N'.")


def main_concurrency(dry_run=False):
    """----Orchestration----"""
    """Get the directory where this script lives"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    inventorypath = os.path.join(base_dir, "..", "Inventory", "pseudoinventory.json")
    jinjafolderpath = os.path.join(base_dir, "..", "Templates")
    jinjatemp = "main.j2"
    pre_push = os.path.join(base_dir, "..", "Saved_render_config", "pre_push")
    post_push = os.path.join(base_dir, "..", "Saved_render_config", "post_push")
    # --------------------------------------------------------------------------#

    """Get credentials ONCE at startup"""
    try:
        inventory = load_inventory(inventorypath)
        renderedjinja = render_jinja(inventory, jinjafolderpath, jinjatemp)

    except TemplateError as e:
        print(f"TEMPLATE ERROR: {e}")
        return
    except Exception as e:
        print(f"LOAD/RENDER ERROR: {e}")
        return
    # ------------------------------------------------------------------------#
    """Setting up Hybrid Username and Password(.env & getpass)"""
    username = os.getenv("NET_USERNAME")

    if not username:
        if dry_run:
            username = "dummy_password"
        else:
            username = input("NETWORK USERNAME: ")
    password = None

    if not dry_run:
        password = getpass.getpass("NETWORK PASSWORD: ")
    # ------------------------------------------------------------------------#
    """Setting up a Dynamic Threadpool size """
    active_blocks = [b for b in renderedjinja if b["commands"]]
    num_targets = len(active_blocks)

    if num_targets == 0:
        print("NO DEVICES WITH CONFIG TO DEPLOY")
        return

    # Dynamic ThreadPool size, capped at 20 workers
    max_workers = min(20, num_targets)
    # ------------------------------------------------------------------------#
    print("\n")
    print(f"==" * 30)
    print(f"MODE: {'DRY RUN' if dry_run else 'REAL RUN'}")
    print(f"DEPLOYING TO {num_targets} DEVICES CONCURRENTLY")
    print(f"WORKERS: {max_workers}")
    print(f"==" * 30)
    print(f"\n")

    start_time = time.time()  # Starting Timer For ThreadPoolExecutor
    status_info = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for block in active_blocks:
            dev_name = block['devices']
            commands = block['commands']

            if dev_name not in inventory['devices']:
                print(f"DEVICE {dev_name} MISSING IN INVENTORY")
                continue

            dev_data = inventory['devices'][dev_name].copy()
            if not dry_run:
                dev_data['connection']['username'] = username
                dev_data['connection']['password'] = password

            fut = executor.submit(push_concurrent, dev_name, dev_data, commands, pre_push, post_push, dry_run)

            futures.append(fut)

        for fut in as_completed(futures):
            dev_status = fut.result()
            status_info.append(dev_status)

    elapsed = time.time() - start_time  # Ends Timer For ThreadpoolExecutor
    total = len(status_info)
    success = sum(1 for r in status_info if r['status'] in ["success", "DRY RUN"])
    failed = total - success
    success_percentage = success / total * 100 if total > 0 else 0
    print(f"==" * 30)
    print(f"DEPLOYMENT SUMMARY")
    print(f"==" * 30)
    if dry_run:
        print(f"DRY RUN MODE – configurations rendered only and saved to {pre_push}\n")
    print(f"TOTAL DEVICES: {total}")
    print(f"SUCCESSFUL: {success}")
    print(f"FAILED: {failed}\n")
    print(f"PERCENTAGE SUCCESSFUL: {success_percentage:.1f}%\n")
    print(f"TOTAL DEPLOYMENT TIME: {elapsed:.2f} seconds")

    if failed > 0:
        failed_devices = [r for r in status_info if r['status'] not in ["success", "DRY RUN"]]
        print(failed_devices)


if __name__ == "__main__":
    # ============ CI MODE DETECTION ============
    # If running in CI (GitHub Actions, GitLab CI, Jenkins, etc.)
    # → skip all prompts, force dry-run, no password asked
    ci_value = (os.getenv("CI") or "").lower()
    in_ci = (ci_value == "true") or ("CI" in os.environ)

    if in_ci:
        print("CI ENVIRONMENT DETECTED – AUTO RUNNING DRY RUN MODE")
        main_concurrency(dry_run=True)
    # ============ INTERACTIVE MODE ============
    else:
        dry_run = get_user_preference()
        main_concurrency(dry_run=dry_run)


