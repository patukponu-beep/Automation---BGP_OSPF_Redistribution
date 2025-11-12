# BGP_OSPF_Redistribution

A Python-based network automation project that simplifies BGP and OSPF configuration deployment using **Jinja2**, **Netmiko**, and structured **JSON inventories**.  
It is designed for scalability, separation of concerns, and easy customization across multiple network environments.

## 🖼️ Network Topology

![Network Diagram](Network_Topology/Network_Diagram.png)
---

## 🧠 Overview

This project automates:
- Template rendering for Cisco routers and switches.
- Configuration generation using **Jinja2**.
- Secure SSH-based deployment via **Netmiko**.
- Organized storage of rendered configs (pre- and post-push).
- Structured device management using JSON inventories.

---

## ⚙️ Project Structure

```
BGP_OSPF_Redistribution/
│
├── Inventory/
│   └── pseudoinventory.json          # Device data (hostnames, IPs, connection details)
│
├── Templates/                        # Jinja2 configuration templates
│   ├── main.j2
│   ├── bgp.j2
│   ├── ospf.j2
│   ├── interfaces.j2
│   └── redistribution.j2
│
├── PythonCode/
│   └── main.py                       # Main orchestration script
│
├── Saved_render_config/              # Auto-saved pre- and post-push configurations
│   ├── pre_push/
│   └── post_push/
│
└── .gitignore
```

---

## 🚀 How It Works

1. **Inventory Load** – The script reads `pseudoinventory.json` to get device details.  
2. **Template Rendering** – Each device’s configuration is generated using the appropriate Jinja2 template.  
3. **Pre-Push Save** – Configurations are saved locally before being sent to devices.  
4. **Device Deployment** – Configs are pushed via SSH using Netmiko.  
5. **Post-Push Save** – Command outputs are logged for validation and auditing.

---

## 🧩 Key Features

- **Separation of concerns:** Templates, inventories, and logic are modular.  
- **Resilience:** Handles authentication errors, timeouts, and connection drops gracefully.  
- **Scalable:** Easily extendable for hundreds of devices via JSON.  
- **Cross-platform:** Works on Windows, macOS, and Linux environments.

---

## 🔧 Requirements

Install dependencies via `pip`:
```bash
pip install jinja2 netmiko
```

Optional for future extensions:
```bash
pip install rich colorama
```

---

## 🧰 Usage

Run from the project root or directly inside `PythonCode/`:

```bash
python main.py
```

When prompted:
```
Network username: cisco
Network password: cisco
```
These credentials are for lab use only. Do not reuse on production systems.

The script will generate and push configurations automatically.

---

## 📦 Example Output

Pre-push configs and post-push logs will be stored under:
```
Saved_render_config/pre_push/
Saved_render_config/post_push/
```

---

## 🧑‍💻 Author

**Patrick Ukponu**  
Network Engineer | Cyber Security Specialist  
- MSc in Cyber Security  
- CCNP | CompTIA Security+  
- GitHub: [patukponu-beep](https://github.com/patukponu-beep)  

---

## 📄 License

This project is for educational and professional demonstration purposes.  
You may modify and adapt it with proper attribution.
