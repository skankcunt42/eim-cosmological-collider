import numpy as np

def _scar(G,n):
    return sum(G.edges[n,nb].get('scar_weight',0.0) for nb in G.neighbors(n))

def calculate_rho_proxies(node_data,G):
    nodes=list(G.nodes())
    a=np.array([node_data[n]['local_load'] for n in nodes],float)
    b=np.array([_scar(G,n) for n in nodes],float)
    c=np.array([node_data[n]['saturation'] for n in nodes],float)
    return a,b,c

def