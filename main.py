
from scanner import generate_ip_range
from pinger import ping_device
from logger import log_result
from visualizer import draw_topology
import socket
import subprocess
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return "Unknown"

def get_mac_address(ip):
    try:
        arp_output = subprocess.check_output(["arp", "-a"], text=True)
        for line in arp_output.splitlines():
            if ip in line:
                return line.split()[1].replace("-", ":")
    except Exception:
        pass
    return "N/A"

def monitor_once(start_ip, end_ip):
    ip_list = generate_ip_range(start_ip, end_ip)
    active_nodes = []

    print(f"\n[+] Monitoring IPs from {start_ip} to {end_ip}\n")
    for ip in ip_list:
        status, latency = ping_device(ip)
        hostname = get_hostname(ip) if status else "-"
        mac = get_mac_address(ip) if status else "-"

        if status:
            status_text = Fore.GREEN + " UP"
        else:
            status_text = Fore.RED + " DOWN"

        latency_text = f"{latency} ms" if latency else "N/A"
        print(f"{ip} - {status_text} - {latency_text} - Hostname: {hostname} - MAC: {mac}")
        
        log_result(ip, "UP" if status else "DOWN", latency, hostname, mac)

        if status:
            active_nodes.append(ip)
        time.sleep(0.2)

    draw_topology(active_nodes)

def main():
    print("==== CableNetMonitor CLI ====\n")
    start_ip = input("Enter start IP [default: 192.168.1.1]: ") or "192.168.1.1"
    end_ip = input("Enter end IP   [default: 192.168.1.10]: ") or "192.168.1.10"
    interval = input("Scan every X minutes? (Enter 0 for once): ") or "0"

    try:
        interval = int(interval)
    except ValueError:
        print("[!] Invalid interval. Defaulting to one-time scan.")
        interval = 0

    if interval <= 0:
        monitor_once(start_ip, end_ip)
    else:
        while True:
            monitor_once(start_ip, end_ip)
            print(f"\n[+] Waiting {interval} minutes before next scan...\n")
            time.sleep(interval * 60)

if __name__ == "__main__":
    main()
