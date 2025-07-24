
from ping3 import ping

def ping_device(ip):
    try:
        latency = ping(ip, timeout=2)
        if latency:
            return True, round(latency * 1000, 2)  # in ms
        else:
            return False, None
    except Exception:
        return False, None
