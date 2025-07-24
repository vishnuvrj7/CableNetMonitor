
import csv
from datetime import datetime

def log_result(ip, status, latency, filename="ping_log.csv"):
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), ip, status, latency])
