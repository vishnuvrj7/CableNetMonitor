
from scanner import generate_ip_range
from pinger import ping_device
from logger import log_result
import time

def monitor_network(start_ip, end_ip):
    ip_list = generate_ip_range(start_ip, end_ip)
    
    print("Starting CableNetMonitor...\n")
    for ip in ip_list:
        status, latency = ping_device(ip)
        status_str = "UP" if status else "DOWN"
        print(f"{ip} - {status_str} - {latency if latency else 'N/A'} ms")
        log_result(ip, status_str, latency)
        time.sleep(0.5)  # small delay to avoid flooding

if __name__ == "__main__":
    monitor_network("192.168.1.1", "192.168.1.10")
