"""
Projection diagnostics for the EIM tri-lobe audit.

This module currently provides lightweight proxy diagnostics for the
rho3, rho3-prime, and rho5 channels. It is intentionally conservative:
these are not full A5 spectral projectors yet. They are import-safe
diagnostics used by the simulation layer.
"""

from __future__ import annotations

import numpy as np


def _node_scar_weight(G, node):
    """Return total scar weight incident on a node."""
    total = 0.0
    for neighbor in G.neighbors(node):
        total += G.edges[node, neighbor].get("scar_weight", 0.0)
    return float(total)


def calculate_rho_proxies(node_data, G):
    """
    Calculate lightweight rho-channel proxies.

    Parameters
    ----------
    node_data:
        Mapping from node id to per-node simulation state.
    G:
        NetworkX graph with optional edge scar weights.

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        rho3, rho3_prime, rho5 proxy vectors.
    """
    nodes = list(G.nodes())

    rho3 = np.array(
        [node_data[n].get("local_load", 0.0) for n in nodes],
        dtype=float,
    )

    rho3_prime = np.array(
        [_node_scar_weight(G, n) for n in nodes],
        dtype=float,
    )

    rho5 = np.array(
        [node_data[n].get("saturation", 0.0) for n in nodes],
        dtype=float,
    )

    return rho3, rho3_prime, rho5


def calculate_memory_seam_vectors_and_norms(G, node_data):
    """
    Return diagnostic norms for the Memory seam proxy.

    The Memory sector is represented here by rho3 and rho3-prime proxies.
    The Interaction sector is represented elsewhere by the rho5 proxy.
    """
    rho3, rho3_prime, _ = calculate_rho_proxies(node_data, G)

    rho3_norm = float(np.linalg.norm(rho3))
    rho3_prime_norm = float(np.linalg.norm(rho3_prime))
    seam_norm = rho3_norm + rho3_prime_norm

    return {
        "p_rho3_norm": rho3_norm,
        "p_rho3_prime_norm": rho3_prime_norm,
        "seam_norm": seam_norm,
        "seam_fraction": rho3_norm / (seam_norm + 1e-12),
    }


def calculate_seam_asymmetry(node_data, G):
    """
    Return a simple scalar asymmetry diagnostic across node loads.
    """
    loads = np.array(
        [node_data[n].get("local_load", 0.0) for n in G.nodes()],
        dtype=float,
    )
    return float(np.std(loads))
