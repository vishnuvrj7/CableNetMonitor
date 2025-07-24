
import networkx as nx
import matplotlib.pyplot as plt

def draw_topology(active_ips, gateway_ip="192.168.1.1"):
    G = nx.Graph()
    G.add_node(gateway_ip)

    for ip in active_ips:
        if ip != gateway_ip:
            G.add_edge(gateway_ip, ip)

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=1200, node_color="lightblue", font_size=10, font_weight='bold')
    plt.title("LAN Topology Map")
    plt.savefig("topology.png")
    print("[+] Network topology saved to topology.png\n")
