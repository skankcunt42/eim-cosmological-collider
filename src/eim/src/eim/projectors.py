import networkx as nx
import numpy as np
from scipy.signal import find_peaks

def calculate_rho_proxies(node_data, G):
    """Proxy projectors for ρ₃, ρ₃', ρ₅"""
    rho3 = np.array([node_data[n]['local_load'] for n in G.nodes()])  # Memory load
    rho3_prime = np.array([sum(G.edges[n, nb]['scar_weight'] for nb in G.neighbors(n)) 
                          for n in G.nodes()])  # Conjugate scar residue
    rho5 = np.array([node_data[n]['saturation'] for n in G.nodes()])  # Interaction gradient
    return rho3, rho3_prime, rho5

def calculate_memory_seam_vectors_and_norms(G, node_data):
    """Spectral projection norms for Memory seam (ρ₃ ⊕ ρ₃')"""
    loads = np.array([node_data[n]['local_load'] for n in G.nodes()])
    scars = np.array([sum(G.edges[n, nb]['scar_weight'] for nb in G.neighbors(n)) 
                     for n in G.nodes()])
    
    # Simple L2 norms (full eigenvector projection can be added later)
    p_rho3_norm = np.linalg.norm(loads)
    p_rho3_prime_norm = np.linalg.norm(scars)
    seam_norm = p_rho3_norm + p_rho3_prime_norm
    seam_fraction = p_rho3_norm / (seam_norm + 1e-9)
    
    return {
        'p_rho3_norm': p_rho3_norm,
        'p_rho3_prime_norm': p_rho3_prime_norm,
        'seam_norm': seam_norm,
        'seam_fraction': seam_fraction
    }

# Alias for compatibility with older code
calculate_seam_asymmetry = lambda node_data, G: np.std([node_data[n]['local_load'] for n in G.nodes()])
