import time
from utils.scanner import get_ip_range, scan_ip
from utils.topology import generate_topology_image
from utils.mac_lookup import get_mac_and_vendor
from utils.hostname import resolve_hostname
import ipaddress
import os

def get_ip_range_from_cidr(cidr_notation):
    try:
        network = ipaddress.ip_network(cidr_notation, strict=False)
        return [str(ip) for ip in network.hosts()]
    except ValueError:
        print("[!] Invalid CIDR. Example: 192.168.1.0/24")
        return []

def monitor(ip_list):
    scan_results = []

    for ip in ip_list:
        status, latency = scan_ip(ip)
        hostname = resolve_hostname(ip) if status == "UP" else "N/A"
        mac, vendor = get_mac_and_vendor(ip) if status == "UP" else ("N/A", "N/A")
        print(f"{ip} - {status} - {latency} ms - {hostname} - {vendor}")
        scan_results.append({
            "ip": ip,
            "status": status,
            "latency": latency,
            "hostname": hostname,
            "vendor": vendor
        })

    generate_topology_image(scan_results)
    print("[+] Network topology saved to topology.png")

def main():
    print("==== CableNetMonitor CLI ====")
    use_cidr = input("Use CIDR notation? (y/N): ").lower().strip() == 'y'

    if use_cidr:
        cidr_input = input("Enter CIDR (e.g., 192.168.1.0/29): ").strip()
        ip_list = get_ip_range_from_cidr(cidr_input)
        if not ip_list:
            return
    else:
        start_ip = input("Enter start IP [default: 192.168.1.1]: ") or "192.168.1.1"
        end_ip = input("Enter end IP   [default: 192.168.1.10]: ") or "192.168.1.10"
        ip_list = get_ip_range(start_ip, end_ip)

    interval = input("Scan every X minutes? (Enter 0 for once): ").strip()
    interval = int(interval) if interval.isdigit() else 0

    print(f"\n[+] Monitoring IPs from {ip_list[0]} to {ip_list[-1]}")

    if interval == 0:
        monitor(ip_list)
    else:
        while True:
            monitor(ip_list)
            print(f"[+] Waiting {interval} minutes before next scan...\n")
            time.sleep(interval * 60)

if __name__ == "__main__":
    main()
