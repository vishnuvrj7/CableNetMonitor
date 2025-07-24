# 📡 CableNetMonitor

<div align="center">

![Python](https://img.shields.io/badge/Python-3.7+-blue?style=for-the-badge&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**A powerful Python-based CLI tool to monitor and visualize your local network in real-time**

*Monitor device uptime • Track network latency • Generate beautiful topology maps*

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Screenshots](#-screenshots) • [Contributing](#-contributing)

</div>

---

## 🌟 Overview

CableNetMonitor is an intuitive network monitoring solution that provides comprehensive insights into your local area network. It continuously pings devices within your specified IP range, logs their connectivity status, and generates beautiful visual topology maps labeled with device hostnames.

### ✨ Key Highlights

- **Real-time Monitoring**: Track device availability and network performance
- **Visual Network Maps**: Generate topology diagrams with hostname labels
- **Comprehensive Logging**: Export data to CSV for analysis
- **MAC & Vendor Discovery**: Identify device manufacturers and physical addresses
- **QR Code Integration**: Generate shareable QR codes for network information
- **Gateway Auto-Detection**: Automatically monitor your network gateway
- **Flexible Scheduling**: One-time scans or continuous monitoring
- **Cross-platform**: Works on Windows, Linux, and macOS

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🎯 **Smart IP Scanning** | Ping devices in custom IP ranges with configurable intervals |
| 📊 **Detailed Logging** | Track IP, latency, hostname, MAC address, and timestamps |
| 🕐 **Automated Scheduling** | Set up recurring scans every X minutes or run one-time scans |
| 🗺️ **Network Visualization** | Generate beautiful topology graphs with device relationships |
| 🏷️ **Hostname Labels** | Automatically resolve and display device hostnames |
| 🔍 **MAC Address Discovery** | Retrieve and log physical addresses of network devices |
| 🏢 **Vendor Identification** | Automatically identify device manufacturers from MAC addresses |
| 📱 **QR Code Generation** | Generate QR codes for IP addresses and hostnames for easy sharing |
| 🌐 **Gateway Auto-Detection** | Automatically includes and monitors your default gateway |
| 🎨 **Colored Terminal** | Intuitive color-coded output (🟢 UP / 🔴 DOWN) |
| 📱 **User-friendly CLI** | Emoji-based interface designed for beginners |

---

## 📦 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Quick Install

1. **Clone the repository**
   ```bash
   git clone https://github.com/vishnuvrj7/CableNetMonitor.git
   cd CableNetMonitor
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Required Dependencies

```txt
ping3>=4.0.0
networkx>=2.8
matplotlib>=3.5.0
colorama>=0.4.4
qrcode>=7.3.0
pillow>=9.0.0
requests>=2.28.0
```

---

## 🛠️ Usage

### Quick Start

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Configure your scan**
   - **Start IP**: Enter the beginning of your IP range (e.g., `192.168.1.1`)
   - **End IP**: Enter the end of your IP range (e.g., `192.168.1.50`)
   - **Scan Interval**: 
     - Enter `0` for a one-time scan
     - Enter any number `> 0` for continuous monitoring (in minutes)

### Example Configuration

```
🌐 CableNetMonitor - Network Scanner
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📍 Start IP: 192.168.1.1
📍 End IP: 192.168.1.50
⏱️  Scan Interval: 5

🚀 Starting network scan...
```

---

## 📁 Project Structure

```
CableNetMonitor/
├── 📄 main.py              # CLI entry point and user interface
├── 🌐 pinger.py            # Core ping functionality
├── 🔍 scanner.py           # IP range generation and scanning logic
├── 📝 logger.py            # CSV logging and data persistence
├── 🎨 visualizer.py        # Network topology visualization
├── 📱 qr_generator.py      # QR code generation for devices
├── 🏢 vendor_lookup.py     # MAC address vendor identification
├── 📊 ping_log.csv         # Generated log file
├── 🖼️ topology.png         # Generated network diagram
├── 📱 qr_codes/            # Directory for generated QR codes
├── 📋 requirements.txt     # Python dependencies
└── 📖 README.md           # Project documentation
```

---

## 📈 Output Files

### 📊 Log File: `ping_log.csv`

The tool generates a comprehensive CSV log with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `Timestamp` | When the ping was performed | `2025-07-24 01:03:20` |
| `IP` | Target IP address | `192.168.1.8` |
| `Status` | Device availability | `UP` / `DOWN` |
| `Latency` | Response time in ms | `1.28` |
| `Hostname` | Resolved device name | `desktop-hp` |
| `MAC Address` | Physical address | `d8:50:e6:12:3a:9c` |
| `Vendor` | Device manufacturer | `Hewlett Packard Enterprise` |

### 🗺️ Network Topology: `topology.png`

- Visual representation of your network structure
- Devices connected to gateway/router
- Hostname labels for easy identification
- Color-coded status indicators
- Automatic gateway detection and inclusion

### 📱 QR Codes: `qr_codes/`

- Generated QR codes for each discovered device
- Contains IP address and hostname information
- Easy sharing and mobile device access
- Organized in dedicated folder structure

---

## 📸 Screenshots

<div align="center">

### Network Topology Visualization
![Network Topology](topology.png)

*Example network topology showing connected devices with hostnames*

### Terminal Output
```
🌐 Gateway: 192.168.1.1 (router.local) - Vendor: Cisco Systems
🟢 192.168.1.1    UP     2.1ms   router.local           00:14:22:01:23:45  Cisco Systems
🟢 192.168.1.8    UP     1.3ms   desktop-hp             d8:50:e6:12:3a:9c  Hewlett Packard Enterprise  
🔴 192.168.1.15   DOWN   ---     unknown                ---                Unknown
🟢 192.168.1.22   UP     0.8ms   laptop-work            ac:de:48:00:11:22  Apple, Inc.
📱 QR codes generated in ./qr_codes/ directory
🗺️ Network topology saved as topology.png
```

</div>

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**If you find this project helpful, please consider giving it a ⭐!**

[![GitHub stars](https://img.shields.io/github/stars/vishnuvrj7/CableNetMonitor?style=social)](https://github.com/vishnuvrj7/CableNetMonitor/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/vishnuvrj7/CableNetMonitor?style=social)](https://github.com/vishnuvrj7/CableNetMonitor/network)


</div>