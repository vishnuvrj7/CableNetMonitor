
import networkx as nx
import matplotlib.pyplot as plt
import socket

def get_hostname(ip):
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return ip  # fallback to IP if no hostname

def draw_topology(active_ips, gateway_ip="192.168.1.1"):
    G = nx.Graph()

    # Label nodes with hostnames
    labels = {}
    G.add_node(gateway_ip)
    labels[gateway_ip] = get_hostname(gateway_ip)

    for ip in active_ips:
        if ip != gateway_ip:
            G.add_edge(gateway_ip, ip)
            labels[ip] = get_hostname(ip)

    plt.figure(figsize=(10, 7))
    pos = nx.spring_layout(G, k=0.8)
    
    nx.draw_networkx_nodes(G, pos, node_color="lightblue", node_size=1200)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, labels, font_size=9, font_weight="bold")
    
    plt.title("LAN Topology Map")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("topology.png")
    print("[+] Network topology saved to topology.png\n")
