import ipaddress
import subprocess
import platform
import time
import os
import socket
import qrcode
import shutil
from getmac import get_mac_address
from mac_vendor_lookup import MacLookup
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from colorama import init, Fore, Style
from logger import log_result

init(autoreset=True)

mac_lookup = MacLookup()
try:
    mac_lookup.update_vendors()
except:
    pass  # skip vendor update if offline


def ping_ip(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    try:
        output = subprocess.check_output(["ping", param, "1", str(ip)],
                                         stderr=subprocess.DEVNULL,
                                         universal_newlines=True)
        if "TTL=" in output or "ttl=" in output:
            latency_line = [line for line in output.split('\n') if "TTL=" in line or "ttl=" in line]
            latency = latency_line[0].split("time=")[-1].split()[0].replace("ms", "")
            return "UP", latency
    except subprocess.CalledProcessError:
        pass
    return "DOWN", "N/A"


def get_mac_and_vendor(ip):
    try:
        mac = get_mac_address(ip=str(ip))
        if mac:
            vendor = mac_lookup.lookup(mac)
        else:
            mac, vendor = "N/A", "N/A"
        return mac, vendor
    except:
        return "N/A", "N/A"


def get_hostname(ip):
    try:
        return socket.gethostbyaddr(str(ip))[0]
    except:
        return "N/A"


def draw_topology_png(active_hosts):
    G = nx.Graph()
    for ip, data in active_hosts.items():
        label = f"{data['hostname']}\n{ip}"
        G.add_node(label)

    nodes = list(G.nodes)
    for i in range(len(nodes) - 1):
        G.add_edge(nodes[i], nodes[i + 1])

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_size=2500, node_color='skyblue', font_size=9, font_weight='bold')
    plt.title("Network Topology")
    plt.savefig("topology.png")
    print(Fore.YELLOW + "[+] PNG topology saved to topology.png")


def draw_topology_html(active_hosts):
    labels = []
    x, y = [], []
    edges_x, edges_y = [], []

    G = nx.Graph()
    for ip, data in active_hosts.items():
        label = f"{data['hostname']} ({ip})"
        G.add_node(label)

    nodes = list(G.nodes)
    for i in range(len(nodes) - 1):
        G.add_edge(nodes[i], nodes[i + 1])

    pos = nx.spring_layout(G)

    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edges_x += [x0, x1, None]
        edges_y += [y0, y1, None]

    for node in G.nodes():
        x.append(pos[node][0])
        y.append(pos[node][1])
        labels.append(node)

    edge_trace = go.Scatter(x=edges_x, y=edges_y, line=dict(width=1, color='#888'), mode='lines')
    node_trace = go.Scatter(x=x, y=y, mode='markers+text', text=labels,
                            textposition='top center',
                            marker=dict(size=20, color='skyblue'),
                            hoverinfo='text')

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(title='Live Network Topology',
                                     titlefont_size=20,
                                     showlegend=False,
                                     hovermode='closest'))

    fig.write_html("topology.html")
    print(Fore.YELLOW + "[+] HTML topology saved to topology.html")


def generate_qr(ip, hostname):
    if not os.path.exists("qr"):
        os.makedirs("qr")

    data = f"http://{ip}"
    img = qrcode.make(data)
    filename = f"qr/{ip.replace('.', '_')}_{hostname}.png"
    img.save(filename)
    print(Fore.CYAN + f"[+] QR code saved: {filename}")


def get_default_gateway():
    if platform.system() == "Windows":
        result = subprocess.check_output("ipconfig", universal_newlines=True)
        for line in result.split("\n"):
            if "Default Gateway" in line:
                parts = line.split(":")
                if len(parts) > 1 and parts[1].strip():
                    return parts[1].strip()
    else:
        result = subprocess.check_output("ip route", shell=True, universal_newlines=True)
        for line in result.split("\n"):
            if line.startswith("default via"):
                return line.split()[2]
    return "192.168.1.1"


def scan_network(start_ip, end_ip):
    active_hosts = {}
    print(Fore.YELLOW + f"\n[+] Monitoring IPs from {start_ip} to {end_ip}")
    for ip in ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address(end_ip)):
        for host in ip:
            status, latency = ping_ip(host)
            mac, vendor = get_mac_and_vendor(host)
            hostname = get_hostname(host)

            color = Fore.GREEN if status == "UP" else Fore.RED
            print(f"{color}{str(host):<15} - {status:<4} - {latency:<6} ms - {mac:<18} - {vendor:<10} - {hostname}")

            log_result(str(host), status, latency, hostname, mac)

            if status == "UP":
                active_hosts[str(host)] = {
                    "latency": latency,
                    "mac": mac,
                    "vendor": vendor,
                    "hostname": hostname
                }

    draw_topology_png(active_hosts)
    draw_topology_html(active_hosts)
    return active_hosts


def main():
    print(Fore.CYAN + "==== CableNetMonitor CLI ====")
    default_gateway = get_default_gateway()
    print(Fore.MAGENTA + f"[+] Detected Default Gateway: {default_gateway}")

    start_ip = input(f"Enter start IP [default: {default_gateway}]: ") or default_gateway
    end_ip = input("Enter end IP   [default: 192.168.1.10]: ") or "192.168.1.10"
    interval = input("Scan every X minutes? (Enter 0 for once): ")

    try:
        interval = int(interval)
    except:
        interval = 0

    if interval == 0:
        hosts = scan_network(start_ip, end_ip)
        for ip, info in hosts.items():
            generate_qr(ip, info['hostname'])
    else:
        while True:
            hosts = scan_network(start_ip, end_ip)
            for ip, info in hosts.items():
                generate_qr(ip, info['hostname'])
            print(Fore.MAGENTA + f"\n[+] Waiting {interval} minutes for next scan...\n")
            time.sleep(interval * 60)


if __name__ == "__main__":
    main()
