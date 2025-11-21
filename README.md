# BGP_OSPF_Redistribution

A Python-based network automation project that simplifies BGP and OSPF
configuration deployment using **Jinja2**, **Netmiko**, and structured
**JSON inventories**.\
It supports scalable deployment and includes both **sequential** and
**concurrent** configuration execution.

## 🖼️ Network Diagram

![Network Diagram](Network%20Topology/Network%20Diagram.png)

## 🧠 Overview

This project automates:

-   Template rendering for Cisco routers and switches\
-   Configuration generation using **Jinja2**\
-   Secure SSH-based deployment via **Netmiko**\
-   Organized storage of rendered configs (pre-push and post-push)\
-   Structured device management using JSON inventories\
-   **Optional concurrent deployment using ThreadPoolExecutor**

## ⚙️ Project Structure

    BGP_OSPF_Redistribution/
    │
    ├── Inventory/
    │   └── pseudoinventory.json
    │
    ├── Templates/
    │   ├── main.j2
    │   ├── bgp.j2
    │   ├── ospf.j2
    │   ├── interfaces.j2
    │   └── redistribution.j2
    │
    ├── PythonCode/
    │   ├── main.py                # Sequential deployment
    │   └── main_concurrency.py    # Concurrent deployment version
    │
    ├── Saved_render_config/
    │   ├── pre_push/
    │   └── post_push/
    │
    └── .gitignore


## ✅ Standalone Script Note

The Python scripts are standalone and can be run directly without modifying the code.
However, the project relies on the current folder layout and inventory format.

To run successfully, keep:
- the Inventory folder at the same level shown in Project Structure
- the file name pseudoinventory.json
- the devices JSON structure and keys (devices, connection, etc.) unchanged
- the Templates folder and template names in place

If you want to use a differenct inventory file or folder path, update the inventorypath and jinjafolderpath variables in the script.

## ⚡ NEW: Concurrent Deployment (ThreadPoolExecutor)

This project includes a high-speed **concurrent configuration engine**
built using Python's `ThreadPoolExecutor`.

### Benefits

-   Faster than sequential execution\
-   Ideal for multiple devices (10--200+)\
-   Each device runs independently\
-   Full per-device reporting (success, timeout, auth failure, CLI
    error)

### How It Works

1.  Jinja2 renders per-device configuration\
2.  Pre-push config stored locally\
3.  Config pushes run **in parallel threads**\
4.  Post-push logs and deployment outcomes stored per device\
5.  Summary report printed at the end

### Example Summary

    ==============================
    DEPLOYMENT SUMMARY
    ==============================
    TOTAL DEVICES: 4
    SUCCESSFUL: 4
    FAILED: 0

## 🚀 Running the Script

### Sequential (standard):

``` bash
python main.py
```

### Concurrent (parallel):

``` bash
python main_concurrency.py
```

## 🧩 Key Features

-   Template, inventory, and logic separation\
-   Modular and extendable structure\
-   Concurrent execution with error handling\
-   Saves pre-push and post-push logs\
-   Uses JSON for easy device scaling\
-   Compatible with Windows, Linux, and macOS
-   Includes per-device retry logic for transient SSH failures
-   Safe dry-run with interactive mode selection and double confirmation

## 🔧 Requirements

``` bash
pip install jinja2 netmiko
```

Optional:

``` bash
pip install rich colorama
```

## 📦 Output Locations

    Saved_render_config/
    ├── pre_push/
    └── post_push/

## 🧑‍💻 Author

Patrick Ukponu\
Network Engineer \| Cyber Security Specialist\
GitHub: https://github.com/patukponu-beep

## 📄 License

For educational and professional demonstration purposes. Modification
allowed with attribution.
