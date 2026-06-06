import numpy as np


def calculate_rho_proxies(node_data, G):
    nodes = list(G.nodes())
    loads = np.array([node_data[n]['local_load'] for n in nodes], dtype=float)
    scars = np.array([sum(G.edges[n, nb].get('scar_weight', 0.0) for nb in G.neighbors(n)) for n in nodes], dtype=float)
    sats = np.array([node_data[n]['saturation'] for n in nodes], dtype=float)
    return loads, scars, sats


def calculate_memory_seam_vectors_and_norms(G, node_data):
    rho3, rho3p, _ = calculate_rho_proxies(node_data, G)
    n3 = float(np.linalg.norm(rho3))
    n3p