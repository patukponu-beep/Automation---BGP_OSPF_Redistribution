# Network_Automation_BGP_OSPF_Redistribution

A production-grade network automation framework with **CI/CD pipeline**, **human-gated deployment**, and **concurrent execution** for network configuration management across Cisco infrastructure primarily. However, this can be utilised perfectly for other vendors with just a wee bit of modification explained below.

- [Network\_Automation\_BGP\_OSPF\_Redistribution](#network_automation_bgp_ospf_redistribution)
  - [🖼️ Network Topology](#️-network-topology)
  - [🚀 Quick Start](#-quick-start)
  - [🧠 Overview](#-overview)
    - [What It Does](#what-it-does)
  - [🔄 Reusing This Framework for Other Vendors](#-reusing-this-framework-for-other-vendors)
  - [🔄 Reusing This Framework for Other Projects](#-reusing-this-framework-for-other-projects)
    - [What You Can Change ✅](#what-you-can-change-)
      - [Templates (Full Flexibility)](#templates-full-flexibility)
      - [Template Helpers and Custom Filters](#template-helpers-and-custom-filters)
      - [Inventory Data (Full Flexibility)](#inventory-data-full-flexibility)
    - [What Must Stay the Same ⚠️](#what-must-stay-the-same-️)
      - [File Structure (Required)](#file-structure-required)
    - [Inventory Format (Flexible)](#inventory-format-flexible)
      - [Required Inventory Structure](#required-inventory-structure)
    - [To Customize Paths](#to-customize-paths)
    - [Real-World Use Cases](#real-world-use-cases)
  - [⚡ Performance \& Scale](#-performance--scale)
  - [🛡️ Safety Features](#️-safety-features)
    - [Positive-Action Bias Reversal](#positive-action-bias-reversal)
    - [Multi-Layer Protection](#multi-layer-protection)
  - [🎯 Interactive Deployment Flow](#-interactive-deployment-flow)
  - [🛡️ CI/CD: Human-Approved Deployment Model](#️-cicd-human-approved-deployment-model)
    - [CI (Continuous Integration) - Automated ✅](#ci-continuous-integration---automated-)
    - [CD (Continuous Deployment) - Human-Gated 🧑‍💻](#cd-continuous-deployment---human-gated-)
  - [⚙️ Project Structure](#️-project-structure)
  - [🧩 Key Features](#-key-features)
    - [Template \& Inventory Separation](#template--inventory-separation)
    - [Concurrent Execution](#concurrent-execution)
    - [Error Classification \& Retry Logic](#error-classification--retry-logic)
    - [Credential Management](#credential-management)
    - [Complete Audit Trail](#complete-audit-trail)
  - [🔧 Requirements](#-requirements)
  - [🚀 Usage](#-usage)
    - [Deployment From Main Branch](#deployment-from-main-branch)
  - [📂 Configuration Files](#-configuration-files)
    - [Inventory Structure (`Inventory/pseudoinventory.json`)](#inventory-structure-inventorypseudoinventoryjson)
    - [Credentials (`.env` file)](#credentials-env-file)
  - [📦 Output Locations](#-output-locations)
    - [Pre-Push Configs](#pre-push-configs)
    - [Post-Push Logs](#post-push-logs)
  - [🧪 CI Pipeline (GitHub Actions)](#-ci-pipeline-github-actions)
  - [🎓 Design Philosophy](#-design-philosophy)
    - [Murphy's Law Compliance](#murphys-law-compliance)
    - [Human-Centered Security](#human-centered-security)
  - [🔒 Security Considerations](#-security-considerations)
  - [🛠️ Troubleshooting](#️-troubleshooting)
    - ["TEMPLATE ERROR: ..."](#template-error-)
    - ["AUTH FAILURE"](#auth-failure)
    - ["TIMEOUT"](#timeout)
    - ["CLI ERROR IN OUTPUT"](#cli-error-in-output)
  - [🚧 Future Enhancements](#-future-enhancements)
  - [🤝 Contributing](#-contributing)
  - [📧 Contact](#-contact)
  - [🙏 Acknowledgments](#-acknowledgments)
  - [📄 License](#-license)

## 🖼️ Network Topology

![Network Diagram](Network%20Topology/Network%20Diagram.png)

---

## 🚀 Quick Start

| Step | Action | Notes |
|------|--------|-------|
| **1. Clone and Navigate** | `git clone https://github.com/patukponu-beep/Automation---BGP_OSPF_Redistribution.git`<br>`cd Automation---BGP_OSPF_Redistribution` | Navigate to the project root where the virtual environment will sit. |
| **2. Install** | `pip install jinja2 netmiko python-dotenv` | Installs required libraries into an isolated Python environment. |
| **3. Activate Venv** | `.\venv\Scripts\activate` | Ensures the `python` command uses the correct interpreter with all dependencies installed. |
| **4. Credentials and Inventory** | `export NET_USERNAME=your_username`<br>Update `Inventory/pseudoinventory.*` | Prepare connection data and configuration variables before execution. |
| **5. Run Dry Run (Safe Validation)** | `python PythonCode/main_concurrency.py`<br>Choose **Y** for Dry Run | Renders configurations locally without connecting to devices. |
| **6. Review Configs** | Check output in `Saved_render_config/pre_push/` | Verify rendered configurations before pushing anything. |
| **7. Deploy (Real Run)** | `python PythonCode/main_concurrency.py`<br>Choose **N** for Real Run and confirm warnings | Executes the concurrent configuration push after validation. |

---

## 🧠 Overview

This project automates network configuration deployment using **Jinja2 templates**, **Netmiko SSH connections**, and structured **JSON/YAML inventories**. It features intelligent concurrency, retry logic, and a clean separation of concerns that isolates templating, data modeling, and deployment execution, alongside human-centered safety controls designed for production network environments.

**While this repository demonstrates BGP/OSPF redistribution**, the framework is **protocol-agnostic** and can be adapted for any network automation task (VXLAN, QoS, ACLs, VPNs, etc.).

### What It Does

- ✅ Renders device-specific configs from Jinja2 templates
- ✅ Validates configurations via automated dry-run (CI pipeline)
- ✅ Deploys configs concurrently with intelligent error handling
- ✅ Creates complete audit trail (pre/post deployment logs)
- ✅ Provides interactive safety gates with positive-action bias reversal
- ✅ Auto-detects CI environments (GitHub Actions, GitLab CI, Jenkins)

---

## 🔄 Reusing This Framework for Other Vendors
This framework was originally built for Cisco devices, but it works with any vendor as long as the inventory structure and SSH parameters are valid.
The only vendor-specific tuning you need is inside the push_concurrent function:
-  Update the bad_markers list with error messages unique to your vendor.
-  Example: JunOS, Arista EOS, Nokia SR-OS all return different CLI error strings.
-  Adding those patterns ensures accurate detection of config failures during deployment.
See the Python script for reference.

---

## 🔄 Reusing This Framework for Other Projects

**This automation framework is not limited to BGP/OSPF.** The script is designed to be **protocol-agnostic** and can be adapted for any network automation task.

### What You Can Change ✅

#### Templates (Full Flexibility)
- ✅ Delete `bgp.j2`, `ospf.j2`, `redistribution.j2` if not needed
- ✅ Create your own templates (e.g., `vxlan.j2`, `qos.j2`, `acl.j2`)
- ✅ `main.j2` is the entry point - include your custom templates here
- ✅ Use any Jinja2 features (loops, conditionals, filters, macros)

**Example `main.j2` for a different project:**
```jinja2
{# Custom VXLAN/EVPN deployment #}
{% include 'interfaces.j2' %}
{% include 'vxlan.j2' %}
{% include 'evpn.j2' %}
```
#### Template Helpers and Custom Filters
A custom Jinja filter, ipaddr, is registered to convert CIDR notation strings (e.g., 192.168.1.1/24) into callable IP address objects, allowing direct access to properties like **.ip** and **.netmask** within templates.
This means that template authors can easily and reliably extract specific components (like the host IP, subnet mask, or network address) from a CIDR string using simple dot notation **(e.g., | ipaddr.netmask)**, simplifying network configuration generation significantly.


#### Inventory Data (Full Flexibility)
- ✅ Modify device-specific data to match your topology and Device Vendor
- ✅ Add custom fields (e.g., `vlans`, `vrfs`, `acls`)
- ✅ Change IP addresses, hostnames, ASN numbers
- ✅ Scale from 2 to 200+ devices

**Example custom inventory:**
```json
{
  "devices": {
    "LEAF-01": {
      "hostname": "LEAF-01",
      "connection": { ... },
      "vlans": [10, 20, 30],
      "vxlan_vtep": "10.1.1.1",
      "your_custom_data": "..."
    }
  }
}
```

### What Must Stay the Same ⚠️

#### File Structure (Required)
```
├── Inventory/
│   └── pseudoinventory.json    # ← Name must match OR update in script
├── Templates/
│   └── main.j2                 # ← Entry point (required)
├── PythonCode/
│   └── main_concurrency.py
└── Saved_render_config/        # ← Auto-created if missing
```

### Inventory Format (Flexible)

The framework supports both **JSON** and **YAML** inventory formats:

**JSON** (`pseudoinventory.json`):
```json
{
  "devices": {
    "R1": {
      "hostname": "R1",
      "connection": {
        "device_type": "cisco_ios", 
        "host": "192.168.1.1",
        "username": "",
        "password": ""
      }
    }
  }
}
```

**YAML** (`pseudoinventory.yaml`):
```yaml
devices:
  R1:
    hostname: R1
    connection:
      device_type: cisco_ios
      host: 192.168.1.1
      username: ""
      password: ""
```

**The script auto-detects the format based on file extension** - use whichever you prefer. YAML is often more human-readable for complex configurations.

#### Required Inventory Structure

Regardless of format (JSON or YAML), these keys are **required**:
```yaml
devices:                    # ← "devices" key required
  DEVICE_NAME:              # ← Device names become filenames
    hostname: "..."         # ← Used in templates
    connection:             # ← Required for Netmiko (name "connection" MUST NOT BE CHANGED)
      device_type: cisco_ios # ← Change to match specific vendor e.g device_type: juniper_junos
      host: 192.168.1.1
      username: ""          # ← Set via .env or prompt
      password: ""          # ← Set via prompt
    # Add your custom data here (bgp, ospf, vlans, etc.)
```

**Critical:** The `connection` dictionary is passed directly to Netmiko and must follow [Netmiko's connection parameters](https://github.com/ktbyers/netmiko#getting-started).

### To Customize Paths (Optional)

**HIGHLY RECOMMENDED**: Do NOT change file/folder names or inventory filename

Everything is deliberately hard-coded and interconnected:

- Inventory file **must** be named `pseudoinventory.yaml`, `.yml`, or `.json`  
- Templates folder **must** stay `Templates`  
- Output root **must** stay `Saved_render_config`  
- `pre_push` and `post_push` subfolders are fixed  

**Why?**  
Because every single path in the script, CI workflow, and audit logic is wired together.  
Changing any of them requires a full refactor across multiple files and function(s) — and one missed path breaks the entire audit trail, CI dry-run, or deployment.

This is **not arbitrary**.  
This is **intentional coupling for correctness and production safety**.

If you need different names → fork and own the full refactor.  
For 99 % of users (and all teams), just keep the default names.  
It works. It’s proven. It’s battle-tested.

Zero configuration = zero surprises.

**Note:** The script will auto-detect whether you're using `.json`, `.yaml`, or `.yml` files.

### Real-World Use Cases

This framework has been designed for:
- ✅ BGP/OSPF redistribution (this repo's example)
- ✅ VXLAN/EVPN fabric deployment
- ✅ QoS policy rollout
- ✅ ACL standardization
- ✅ Interface description updates
- ✅ SNMP/NTP/logging configuration
- ✅ Multi-site VPN deployment

**Key principle**: Separate your **data** (inventory) from your **logic** (templates) from your **execution** (Python script). This makes the framework reusable across projects.

---

## ⚡ Performance & Scale

| Metric | Value |
|--------|-------|
| **Deployment Speed** | Sub-6 seconds for 7 devices |
| **Concurrency** | Dynamic worker scaling (1-20 threads) |
| **Success Rate** | 100% with intelligent retry logic |
| **Scale** | Supports 100+ devices with zero code changes |
| **Time Savings** | 95% reduction vs manual CLI configuration |

---

## 🛡️ Safety Features

### Positive-Action Bias Reversal
- **Default = Safe**: Pressing 'Y' runs non-destructive dry-run
- **Dangerous = Explicit**: Real deployment requires 'N' + multiple confirmations
- Protects against reflexive "Enter" presses during fatigue/pressure

### Multi-Layer Protection
- ✅ **Double Confirmation Gates**: Real runs require "yes" confirmation with "back" option
- ✅ **Intelligent Retry Logic**: 
  - Auth failures → Fail fast (credentials won't fix themselves)
  - Timeouts → Exponential backoff (3 attempts)
  - CLI errors → Immediate flagging, no retry
- ✅ **Complete Audit Trail**: Timestamped pre-push configs + post-push session logs
- ✅ **CI Auto-Detection**: Forces dry-run in CI environments (no prompts, no credentials needed)

---

## 🎯 Interactive Deployment Flow
```
Select run mode:
Y - Dry Run (simulation only)
N - Normal Run (real execution)
Enter Y or N: n

⚠️ WARNING: NORMAL RUN mode selected!
   • Real configurations will be pushed to network devices
   • This will make actual changes to your infrastructure

Type 'yes' to continue, 'no' to cancel, or 'back' to return: yes

🚀 Starting NORMAL RUN mode...

==============================================================
MODE: REAL RUN
DEPLOYING TO 7 DEVICES CONCURRENTLY
WORKERS: 7
==============================================================

DEPLOYMENT SUMMARY
==============================================================
TOTAL DEVICES: 7
SUCCESSFUL: 7
FAILED: 0

PERCENTAGE SUCCESSFUL: 100.0%
TOTAL DEPLOYMENT TIME: 5.98 seconds
```

---

## 🛡️ CI/CD: Human-Approved Deployment Model

This project implements a **safe CI/CD model** designed for critical network infrastructure, where destructive actions must never run automatically.

### CI (Continuous Integration) - Automated ✅
- Runs **dry-run mode automatically** on every commit
- Renders all templates and validates structure
- Saves pre-push configs as artifacts
- **Zero risk**: No SSH connections, no device changes
- Blocks merges if validation fails

### CD (Continuous Deployment) - Human-Gated 🧑‍💻
- Requires an engineer to **manually invoke** the script
- Interactive menu with confirmation steps
- Only then performs real device changes
- **Fully auditable** and intentional

**This model follows industry best practice** for critical infrastructure ("Human-in-the-loop CD" / "Approval-gated deployments"), used by:
- Google SRE
- Netflix infrastructure teams
- Banking and financial networks
- Telecom production environments

**Philosophy**: Automate validation, gate execution. Code should protect operators from themselves, not just secure networks.

---

## ⚙️ Project Structure
```
BGP_OSPF_Redistribution/
│
├── .github/
│   └── workflows/
│       └── ci-dryrun.yml         # GitHub Actions CI pipeline
│
├── Inventory/
│   └── pseudoinventory.json      # Device definitions (JSON)
│
├── Templates/
│   ├── main.j2                   # Master template (entry point)
│   ├── bgp.j2                    # BGP configuration
│   ├── ospf.j2                   # OSPF configuration
│   ├── interfaces.j2             # Interface configs
│   └── redistribution.j2         # Route redistribution
│
├── PythonCode/
│   └── main_concurrency.py      # Concurrent deployment   
│
├── Saved_render_config/
│   ├── pre_push/                 # Rendered configs before deployment
│   └── post_push/                # Session logs after deployment
│
├── Network Topology/
│   └── Network Diagram.png
│
├── .env.example                  # Template for credentials
├── .gitignore
└── README.md
```

---

## 🧩 Key Features

### Template & Inventory Separation
- **Jinja2 templates** for configuration logic
- **JSON/YAML inventory** for device-specific data
- Change data without touching code
- Protocol-agnostic design (BGP/OSPF is just one example)

### Concurrent Execution
- Uses Python's `ThreadPoolExecutor` for parallel deployment
- **Dynamic worker scaling**: Automatically adjusts thread count (1-20) based on device count
- Each device runs independently
- Full per-device error reporting

### Error Classification & Retry Logic
```python
✅ Success → Save logs, mark complete
❌ Auth Failure → Fail fast (no retry)
⏱️ Timeout → Retry with 3-second delay (max 3 attempts)
🔴 CLI Error → Flag immediately, no retry
❓ Unknown Error → Retry with backoff
```

### Credential Management
- **Hybrid approach**: Username from `.env`, password via interactive prompt
- Fallback to full interactive if `.env` not present
- CI mode: Auto-skips credential prompts in dry-run

### Complete Audit Trail
- **Pre-push**: Rendered configs saved with timestamp
- **Post-push**: Full SSH session logs with device responses
- Per-device folder organization
- Git-trackable desired state

---

## 🔧 Requirements
```bash
pip install jinja2 netmiko python-dotenv
```

**Optional** (for enhanced output):
```bash
pip install rich colorama
```

**Python Version**: 3.8+ (tested up to 3.12)

---

## 🚀 Usage

### Deployment From Main Branch
```bash
python PythonCode/main_concurrency.py
```

**Features:**
- Human-Centered Safety & Security: Positive-Action Bias Reversal
- Inventory file-type Auto-detection: Loads Inventory from JSON or YAML file 
- Multi-Layer Confirmation Gates: Double confirmation with "back" option for real deployments
- CI auto-detection + concurrent execution + complete audit trail (all-in-one) 
- Human-Gated CD: CD requires manual approval (industry best practice)
- 100+ Device Scale: Zero code changes, role-based architecture

## 📂 Configuration Files

### Inventory Structure (`Inventory/pseudoinventory.json`)
```json
{
  "devices": {
    "R1": {
      "hostname": "R1",
      "role": "edge_router",
      "asn": 65001,
      "loopback": "1.1.1.1/32",
      "connection": { "device_type": "cisco_ios", "ip": "192.168.22.153", "username": "", "password": "", "secret": "" },
      "links": [
        { "name": "Gi0/1", "ip": "10.1.2.1/30", "desc": "to R2", "peer": "R2", "peer_intf": "Gi0/1" },
        { "name": "Gi0/3", "ip": "10.1.3.1/30", "desc": "to R3", "peer": "R3", "peer_intf": "Gi0/3" }
      ],
      "sublinks": [
        { "name": "Gi0/0.10", "vlan_id": 10, "ip": "192.168.1.254/24", "desc": "SITE1 VLAN10 gateway" },
        { "name": "Gi0/0.20", "vlan_id": 20, "ip": "172.16.1.254/24", "desc": "SITE1 VLAN20 gateway" }
      ],
      "vlans": { "10": { "name": "VLAN10_SITE1" }, "20": { "name": "VLAN20_SITE1" } },
      "ospf": { "process_id": 1, "area": 0, "ifaces": ["Gi0/0.10", "Gi0/0.20"] },
      "bgp": {
        "neighbors": [
          { "peer_ip": "10.1.2.2", "remote_as": 65002 },
          { "peer_ip": "10.1.3.2", "remote_as": 65003 }
        ],
        "advertise_prefixes": ["192.168.1.0/24", "172.16.1.0/24"]
      },
      "redistribution": { "ospf_to_bgp": true, "bgp_to_ospf": true }
        }
    }
}
```

### Credentials (`.env` file)
```bash
NET_USERNAME=*whatever you set your SSH username to be on the file*
# Password will be prompted interactively (more secure)
```

---

## 📦 Output Locations

### Pre-Push Configs
```
Saved_render_config/pre_push/<device_name>/<device_name>_YYYYMMDD_HHMMSS.txt
```
- Rendered configuration before deployment
- Used for validation and audit
- Git-trackable desired state

### Post-Push Logs
```
Saved_render_config/post_push/<device_name>/<device_name>_session_YYYYMMDD_HHMMSS.log
```
- Full SSH session output
- Device responses to each command
- Used for troubleshooting and compliance

---

## 🧪 CI Pipeline (GitHub Actions)

The project includes a `.github/workflows/ci-dryrun.yml` that automatically:

1. ✅ Runs on every push/PR
2. ✅ Installs dependencies
3. ✅ Executes dry-run validation
4. ✅ Renders all templates
5. ✅ Saves artifacts (rendered configs)
6. ✅ Reports success/failure

**No credentials required** - CI auto-detects environment and skips device connections.

---

## 🎓 Design Philosophy

### Murphy's Law Compliance
> "If an engineer CAN hit Enter without reading at 2 AM, they WILL."

This tool assumes operators work under:
- ⏰ Fatigue (midnight pages)
- 🔥 Pressure (customers down)
- 📱 Distractions (Slack notifications)
- 🧠 Cognitive load (multiple terminals open)

**Solution**: Design systems that protect operators from themselves through safe defaults, not just policies and training.

### Human-Centered Security
Traditional approach:
> "Humans are the weakest link" → More training, stricter policies

This project's approach:
> "Humans are operators to protect" → Safe defaults, confirmation gates, audit trails

Code serves humans, not the other way around.

---

## 🔒 Security Considerations

- ✅ Credentials never stored in code or git
- ✅ Password prompted interactively (not in `.env`)
- ✅ Session logs saved locally (not transmitted)
- ✅ `.env` in `.gitignore` by default
- ✅ No plaintext passwords in CI/CD

**For production**: Integrate with HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault.

---

## 🛠️ Troubleshooting

### "TEMPLATE ERROR: ..."
- Check Jinja2 syntax in `Templates/` folder
- Verify inventory data matches template expectations
- Run dry-run to validate before deploying

### "AUTH FAILURE"
- Verify the **SSH username and password** (entered via prompt or `.env`)
- Test connectivity manually:  
  `ssh your_username@device_ip`
- Ensure the user has **privilege level 15** (or sufficient rights to enter configuration mode)  
  → This tool does **not** use or prompt for an enable secret. If you decide to use enable secret, add the secret key and value to devices['connection'][secret] of the inventory.

### "TIMEOUT"
- Check network connectivity to devices
- Verify device IPs in inventory
- Increase timeout in Netmiko connection parameters

### "CLI ERROR IN OUTPUT"
- Review post-push logs in `Saved_render_config/post_push/`
- Check for typos in templates
- Verify device supports commands (IOS version, feature set)

---

## 🚧 Future Enhancements

- [ ] Rollback capability (capture pre-change configs, restore on failure)
- [ ] Web UI (Flask/FastAPI frontend for non-CLI users)
- [ ] Multi-vendor support (Arista, Juniper via NAPALM)
- [ ] Config drift detection (compare running vs intended state)
- [ ] Slack/Teams notifications on deployment
- [ ] Integration tests with mock devices (pytest + netmiko-mock)

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📧 Contact

- **Author**: Patrick Ukponu
- Network Engineer|CCNP Enterprise|Cyber Security Specialist|
- **LinkedIn**: https://www.linkedin.com/in/patrick-u-78a001176/
- **Email**: pat.ukponu@gmail.com

---

## 🙏 Acknowledgments

Built with:
- [Jinja2](https://jinja.palletsprojects.com/) - Template engine
- [Netmiko](https://github.com/ktbyers/netmiko) - SSH automation
- [Python ThreadPoolExecutor](https://docs.python.org/3/library/concurrent.futures.html) - Concurrency

Inspired by the need for **human-centered automation** in network operations.

## 📄 License

MIT License - See LICENSE file for details

---

**⭐ If this project helped you, please star the repo!**