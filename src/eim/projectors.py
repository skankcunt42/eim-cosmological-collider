import numpy as np


def calculate_rho_proxies(node_data, G):
    """Return proxy vectors for rho3, rho3-prime, and rho5 channels.

    These are diagnostic proxies, not full A5 spectral projectors. They keep the
    tri-lobe simulation importable while the exact H1 projector layer is audited.
    """
    nodes = list(G.nodes())
    rho3 = np.array([node_data[n]["local_load"] for n in nodes], dtype=float)
    rho3_prime = np.array([
        sum(G.edges[n, nb].get("scar_weight", 0.