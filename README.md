# BGP_OSPF_Redistribution

A production-grade network automation framework with **CI/CD pipeline**, **human-gated deployment**, and **concurrent execution** for network configuration management across Cisco infrastructure.


## 🖼️ Network Topology

![Network Diagram](Network%20Topology/Network%20Diagram.png)

---

## 🚀 Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/patukponu-beep/Automation---BGP_OSPF_Redistribution.git
cd Automation---BGP_OSPF_Redistribution

# 2. Install dependencies
pip install jinja2 netmiko python-dotenv

# 3. (Optional) Set credentials in .env or export
export NET_USERNAME=cisco

# 4. Run dry-run first (safe validation)
python PythonCode/main_concurrency.py
# Select 'Y' for Dry Run when prompted

# 5. Review rendered configs in Saved_render_config/pre_push/

# 6. Deploy to devices (after validation)
python PythonCode/main_concurrency.py
# Select 'N' for Real Run, confirm warnings
```

---

## 🧠 Overview

This project automates network configuration deployment using **Jinja2 templates**, **Netmiko SSH connections**, and structured **JSON inventories**. It features intelligent concurrency, retry logic, and a clean separation of concerns that isolates templating, data modeling, and deployment execution, alongside human-centered safety controls designed for production network environments.

**While this repository demonstrates BGP/OSPF redistribution**, the framework is **protocol-agnostic** and can be adapted for any network automation task (VXLAN, QoS, ACLs, VPNs, etc.).

### What It Does

- ✅ Renders device-specific configs from Jinja2 templates
- ✅ Validates configurations via automated dry-run (CI pipeline)
- ✅ Deploys configs concurrently with intelligent error handling
- ✅ Creates complete audit trail (pre/post deployment logs)
- ✅ Provides interactive safety gates with positive-action bias reversal
- ✅ Auto-detects CI environments (GitHub Actions, GitLab CI, Jenkins)

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

#### Inventory Data (Full Flexibility)
- ✅ Modify device-specific data to match your topology
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
      device_type: cisco_ios
      host: 192.168.1.1
      username: ""          # ← Set via .env or prompt
      password: ""          # ← Set via prompt
    # Add your custom data here (bgp, ospf, vlans, etc.)
```

**Critical:** The `connection` dictionary is passed directly to Netmiko and must follow [Netmiko's connection parameters](https://github.com/ktbyers/netmiko#getting-started).

### To Customize Paths

If you want different folder names or inventory files:

**Edit these variables in `main_concurrency.py` (around line 195):**
```python
# Default paths
inventorypath = os.path.join(base_dir, "..", "Inventory", "pseudoinventory.json")
jinjafolderpath = os.path.join(base_dir, "..", "Templates")

# Customize to:
inventorypath = os.path.join(base_dir, "..", "MyInventory", "devices.yaml")  # JSON or YAML
jinjafolderpath = os.path.join(base_dir, "..", "MyTemplates")
```

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
- **JSON inventory** for device-specific data
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

**Python Version**: 3.7+

---

## 🚀 Usage

### Option 1: Concurrent Deployment (Recommended)
```bash
python PythonCode/main_concurrency.py
```

**Features:**
- Parallel execution across all devices
- Sub-6-second deployments for typical labs
- Dynamic worker scaling
- Interactive safety prompts

## 📂 Configuration Files

### Inventory Structure (`Inventory/pseudoinventory.json`)
```json
{
  "devices": {
    "R1": {
      "hostname": "R1",
      "connection": {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "",
        "password": "",
        "secret": "enable_password"
      },
      "interfaces": { 
        "GigabitEthernet0/0": {
          "ip": "10.1.1.1/24",
          "description": "To R2"
        }
      },
      "bgp": {
        "asn": 65001,
        "router_id": "1.1.1.1",
        "neighbors": [...]
      },
      "ospf": {
        "process_id": 1,
        "router_id": "1.1.1.1",
        "networks": [...]
      }
    }
  }
}
```

### Credentials (`.env` file)
```bash
NET_USERNAME=cisco
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
- Verify credentials in `.env` or when prompted
- Check device SSH access (test with `ssh user@device`)
- Confirm username/password/enable secret

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