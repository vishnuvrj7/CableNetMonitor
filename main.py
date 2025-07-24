# main.py
from scanner import generate_ip_range
from pinger import ping_device
from logger import log_result
from visualizer import draw_topology
import time

def monitor_once(start_ip, end_ip):
    ip_list = generate_ip_range(start_ip, end_ip)
    active_nodes = []

    print(f"\n[+] Monitoring IPs from {start_ip} to {end_ip}")
    for ip in ip_list:
        status, latency = ping_device(ip)
        status_str = "UP" if status else "DOWN"
        print(f"{ip} - {status_str} - {latency if latency else 'N/A'} ms")
        log_result(ip, status_str, latency)
        if status:
            active_nodes.append(ip)
        time.sleep(0.2)  # avoid ping flooding

    draw_topology(active_nodes)  # only draw UP devices

def main():
    print("==== CableNetMonitor CLI ====")
    start_ip = input("Enter start IP [default: 192.168.1.1]: ") or "192.168.1.1"
    end_ip = input("Enter end IP   [default: 192.168.1.10]: ") or "192.168.1.10"
    interval = input("Scan every X minutes? (Enter 0 for once): ") or "0"

    interval = int(interval)
    if interval <= 0:
        monitor_once(start_ip, end_ip)
    else:
        while True:
            monitor_once(start_ip, end_ip)
            print(f"[+] Waiting {interval} minutes...\n")
            time.sleep(interval * 60)

if __name__ == "__main__":
    main()
