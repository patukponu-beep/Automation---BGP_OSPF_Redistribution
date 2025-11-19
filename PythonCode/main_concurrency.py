import json
import os
import getpass
from ipaddress import ip_interface
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException
from jinja2 import FileSystemLoader, Environment, TemplateError


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
    """Saves the rendered Template to Device Path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_folder = os.path.join(pre_push, dev_name)
    os.makedirs(device_folder, exist_ok=True)
    filename = os.path.join(device_folder, f"{dev_name}_{timestamp}.txt")
    config_string = "\n".join(commands)
    with open(filename, "w") as f:
        f.write(config_string)
    return filename


def push_config(dev_data, commands):
    """Per Network Device Netmiko Connection and Configuration"""
    ssh_info = dev_data['connection']

    with ConnectHandler(**ssh_info) as conn:
        conn.enable()
        output = conn.send_config_set(commands)
        save_output = conn.save_config()  # or conn.send_command('write memory')
        full_output = f"{output}----WRITE MEMORY----{save_output}"

    return full_output


def save_push_config(dev_name, output, post_push):
    """Saves the Configuration Per Network Device to Device Path"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_folder = os.path.join(post_push, dev_name)
    os.makedirs(device_folder, exist_ok=True)
    filename = os.path.join(device_folder, f"{dev_name}_session_{timestamp}.log")
    with open(filename, "w") as f:
        f.write(output)
    return filename


def push_concurrent(dev_name, dev_data, commands, pre_push, post_push):
    """Sets Up Functions for Concurrent Automation"""
    status_info = {"devices": dev_name, "status": "success", "reason": None}
    try:
        save_render_config(dev_name, commands, pre_push)
        output = push_config(dev_data, commands)
        save_push_config(dev_name=dev_name, output=output, post_push=post_push)

        bad_markers = [

            "invalid input detected",
            "ambiguous command",
            "incomplete command"
        ]

        output_cf = output.casefold()
        if any(m in output_cf for m in bad_markers):
            status_info['status'] = "CONFIG ERROR"
            status_info['reason'] = "CLI ERROR IN OUTPUT"

    except NetmikoTimeoutException as e:
        status_info['status'] = "TIMEOUT"
        status_info['reason'] = str(e)
    except NetmikoAuthenticationException as e:
        status_info['status'] = "AUTH FAILURE"
        status_info['reason'] = str(e)
    except Exception as e:
        status_info['status'] = "UNKNOWN FAILURE"
        status_info['reason'] = str(e)

    return status_info


def main_concurrency():
    """----Orchestration----"""
    """Get the directory where this script lives"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    inventorypath = os.path.join(base_dir, "..", "Inventory", "pseudoinventory.json")

    jinjafolderpath = os.path.join(base_dir, "..", "Templates")

    jinjatemp = "main.j2"
    pre_push = os.path.join(base_dir, "..", "Saved_render_config", "pre_push")

    post_push = os.path.join(base_dir, "..", "Saved_render_config", "post_push")

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

    username = input("Network username: ")
    password = getpass.getpass("Network password: ")

    print(f"==" * 30)
    print(f"DEPLOYING TO {len(renderedjinja)} DEVICES CONCURRENTLY")
    print(f"==" * 30)
    print(f"\n")

    status_info = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for block in renderedjinja:
            dev_name = block['devices']
            commands = block['commands']

            if not commands:
                print(f"SKIPPING {dev_name} - NO CONFIG TO APPLY")
                continue
            if dev_name not in inventory['devices']:
                print(f"DEVICE {dev_name} MISSING IN INVENTORY")
                continue

            dev_data = inventory['devices'][dev_name].copy()
            dev_data['connection']['username'] = username
            dev_data['connection']['password'] = password

            fut = executor.submit(push_concurrent, dev_name, dev_data, commands, pre_push, post_push)

            futures.append(fut)

        for fut in as_completed(futures):
            dev_status = fut.result()
            status_info.append(dev_status)

    total = len(status_info)
    success = sum(1 for r in status_info if r['status'] == "success")
    failed = total - success
    success_percentage = success/total * 100
    print(f"==" * 30)
    print(f"DEPLOYMENT SUMMARY")
    print(f"==" * 30)
    print(f"TOTAL DEVICES: {total}")
    print(f"SUCCESSFUL: {success}")
    print(f"FAILED: {failed}\n")
    print(f"PERCENTAGE SUCCESSFUL: {success_percentage}%")
    
    if failed > 0:
        failed_devices = [r for r in status_info if r['status'] != "success"]
        print(failed_devices)


if __name__ == "__main__":
    main_concurrency()
