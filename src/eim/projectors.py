import numpy as np


def _scar(G, n):
    return sum(G.edges[n, nb].get('scar_weight', 0.0) for nb in G.neighbors(n))


def calculate_rho_proxies(node_data, G):
    nodes = list(G.nodes())
    rho3 = np.array([node_data[n]['local_load'] for n in nodes], dtype=float)
    rho3p = np.array([_scar(G, n) for n in nodes], dtype=float)
    rho5 = np.array([node_data[n]['saturation'] for n in nodes], dtype=float)
    return rho3, rho3p, rho5


def calculate_memory_seam