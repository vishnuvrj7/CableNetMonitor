
import csv
import os
from datetime import datetime

def log_result(ip, status, latency, hostname="Unknown", mac="N/A", filename="ping_log.csv"):
    file_exists = os.path.isfile(filename)

    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            # Write headers only if file is new
            writer.writerow(["Timestamp", "IP", "Status", "Latency (ms)", "Hostname", "MAC Address"])
        
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ip,
            status,
            latency if latency else "N/A",
            hostname,
            mac
        ])
