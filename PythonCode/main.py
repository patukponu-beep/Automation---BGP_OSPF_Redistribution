import json
import os
import getpass
from datetime import datetime
from ipaddress import ip_interface

from jinja2 import Environment, FileSystemLoader, TemplateError
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException


def loadjsonfile(inventoryfilepath):
    """loads json inventory from folder"""
    with open(inventoryfilepath) as l:
        inventory = json.load(l)

    return inventory


def render_config(inventory, jinjafolderpath, jinjafile):
    """Loads a Jinja2 template and renders it with the provided data."""
    JinjaFolderLoader = FileSystemLoader(jinjafolderpath)
    env = Environment(loader=JinjaFolderLoader)

    # --- Register custom IP address filter ---
    def ip_converter(value):
        """Converts slash notation to IP + netmask object."""
        return ip_interface(value)

    env.filters["ipaddr"] = ip_converter
    # -----------------------------------------
    template = env.get_template(jinjafile)
    render_cfg = []
    for dev_name, dev_data in inventory['devices'].items():
        output = template.render(device=dev_data)
        cmd = [line for line in output.splitlines() if line.strip()]
        render_cfg.append({
            "devices": dev_name,
            "lines": cmd})
    return render_cfg


def save_config_file(dev_name, commands, pre_push):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_folder = os.path.join(pre_push, dev_name)
    os.makedirs(device_folder, exist_ok=True)

    filename = os.path.join(device_folder, f"{dev_name}_{timestamp}.txt")

    config_string = "\n".join(commands)

    with open(filename, "w") as f:
        f.write(config_string)

    print(f"[+] SAVED INTENT FOR {dev_name} → {filename}")

    return filename


def config_device(dev_name, dev_data, commands):
    ssh_info = dev_data['connection']
    print(f"[>] PUSHING TO {dev_name} ({ssh_info['ip']})...")

    with ConnectHandler(**ssh_info) as conn:
        conn.enable()
        output = conn.send_config_set(commands)
        save_output = conn.save_config()  # or net_connect.send_command('write memory').
        # ideally you'll need to have a separate script(save_output = conn.save_config())
        # for saving config, you don't want to push a config,
        # and it immediately saves your configuration to NVRAM.

        full_output = f"{output}\n\n--- WRITE MEMORY OUTPUT ---\n{save_output}"
        print(f"*** CONFIGURATION SUCCESSFUL ON {dev_name} ***")
    return full_output


def save_post_push(dev_name, post_push, pushed_config):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    device_folder = os.path.join(post_push, dev_name)
    os.makedirs(device_folder, exist_ok=True)
    filename = os.path.join(device_folder, f"{dev_name}_session_{ts}.log")
    with open(filename, "w") as l:
        l.write(pushed_config)
    print(f"[+] SAVED CONFIG FOR {dev_name} → {filename}")


def main():
    """Get the directory where this script lives"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    inventory_path = os.path.join(base_dir, "..", "Inventory", "pseudoinventory.json")

    jinja_folder = os.path.join(base_dir, "..", "Templates")

    jinja_template = "main.j2"
    pre_push = os.path.join(base_dir, "..", "Saved_render_config", "pre_push")

    post_push = os.path.join(base_dir, "..", "Saved_render_config", "post_push")

    """Get credentials ONCE at startup"""

    username = input("Network username: ")
    password = getpass.getpass("Network password: ")
    try:
        inventory = loadjsonfile(inventory_path)
        rendered_configs = render_config(jinjafolderpath=jinja_folder, jinjafile=jinja_template, inventory=inventory)
    except TemplateError as e:
        print(f"TEMPLATE ERROR: {e}")
        return
    except Exception as e:
        print(f"RENDER/LOADER ERROR {e}")
        return

    for block in rendered_configs:
        dev_name = block['devices']
        commands = block['lines']

        if not commands:
            print(f"[~] SKIPPING {dev_name} -NO CONFIG TO APPLY")
            continue

        if dev_name not in inventory['devices']:
            print(f"DEVICE IN INVENTORY MISSING: {dev_name}")
            continue

        dev_data = inventory['devices'][dev_name].copy()

        dev_data['connection']['username'] = username
        dev_data['connection']['password'] = password

        try:
            save_config_file(dev_name, commands, pre_push)
            out = config_device(dev_name, dev_data, commands)
            save_post_push(dev_name, post_push, pushed_config=out)
            print(f"{dev_name}------->OK\n")

        except NetmikoAuthenticationException as n:
            print(f"AUTHENTICATION FAILED ON {dev_name}", n)
        except NetmikoTimeoutException as n:
            print(f"TIMEOUT: {dev_name}", n)
        except Exception as n:
            print(f"UNKNOWN ERROR ON {dev_name}", n)


if __name__ == "__main__":
    main()
