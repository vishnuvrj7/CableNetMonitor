# scanner.py
import ipaddress

def generate_ip_range(start_ip, end_ip):
    """
    Generate a list of IPs in dotted-decimal format from start_ip to end_ip.
    Example: 192.168.1.1 to 192.168.1.10
    """
    try:
        start = int(ipaddress.IPv4Address(start_ip))
        end = int(ipaddress.IPv4Address(end_ip))

        if start > end:
            raise ValueError("Start IP must be less than or equal to End IP.")

        ip_list = [str(ipaddress.IPv4Address(ip)) for ip in range(start, end + 1)]
        return ip_list

    except Exception as e:
        print(f"[!] Error generating IP range: {e}")
        return []
