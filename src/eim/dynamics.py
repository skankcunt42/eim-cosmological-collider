import numpy as np
import collections

def update_evap_state(G, node_data, node_evap_state, threshold_high=0.95, threshold_low=0.85, scar_increment=0.08):
    current_state_switches = 0
    for node in G.nodes():
        s_x = node_data[node]['saturation']
        current_evap_state = node_evap_state.get(node, False)
        if not current_evap_state:
            if s_x >= threshold_high:
                node_evap_state[node] = True
                current_state_switches += 1
        else:
            if s_x <= threshold_low:
                node_evap_state[node] = False
                current_state_switches += 1
                for neighbor in G.neighbors(node):
                    if G.has_edge(node, neighbor):
                        G.edges[node, neighbor]['scar_weight'] += scar_increment
    return current_state_switches

def update_edge_weights(G, node_data, node_evap_state, eta=0.05):
    forman_ricci_proxy = 1.0
    for u, v in list(G.edges()):
        s_u = node_data[u]['saturation']
        s_v = node_data[v]['saturation']
        weight_u_v = G.edges[u, v]['weight']
        if (node_evap_state.get(u, False) and s_u > s_v) or (node_evap_state.get(v, False) and s_v > s_u):
            G.edges[u, v]['weight'] = weight_u_v * np.exp(-eta * forman_ricci_proxy)
        else:
            G.edges[u, v]['weight'] = weight_u_v * np.exp(eta * forman_ricci_proxy)

def update_interaction_pressure(G, node_data, interaction_pressure):
    new_pressure = {}
    seam = 0.1 * np.std([node_data[n]['local_load'] for n in G.nodes()])
    for node in G.nodes():
        pressure = interaction_pressure.get(node, 0.0)
        pressure = pressure * 0.95 + seam - 0.01 * pressure**2
        new_pressure[node] = max(0, min(1.0, pressure))
    return new_pressure

def obs_commit(G, interaction_pressure, node_evap_state, observer_node, threshold=0.05):
    commit_asym = 0.0
    for node in G.neighbors(observer_node):
        p = interaction_pressure.get(node, 0.0)
        if node_evap_state.get(node, False):
            commit_asym += p
    return commit_asym > threshold

def move_observer_with_gravity(G, current_observer, node_data, defect_strength=15.0):
    for neighbor in list(G.neighbors(current_observer)):
        if G.has_edge(current_observer, neighbor):
            G.edges[current_observer, neighbor]['weight'] /= defect_strength

    neighbors = list(G.neighbors(current_observer))
    if not neighbors:
        return current_observer

    loads = np.array([node_data[n]['local_load'] for n in neighbors])
    probabilities = loads / (np.sum(loads) + 1e-9)
    new_observer = np.random.choice(neighbors, p=probabilities)

    for neighbor in list(G.neighbors(new_observer)):
        if G.has_edge(new_observer, neighbor):
            G.edges[new_observer, neighbor]['weight'] *= defect_strength

    return new_observer

def inject_gravitational_wave(G, center_node, strength=8.0, radius=4):
    for neighbor in G.neighbors(center_node):
        if G.has_edge(center_node, neighbor):
            G.edges[center_node, neighbor]['scar_weight'] += strength

    visited = set()
    queue = collections.deque([(center_node, 0)])
    while queue:
        node, dist = queue.popleft()
        if node in visited or dist > radius:
            continue
        visited.add(node)
        for neighbor in G.neighbors(node):
            if G.has_edge(node, neighbor):
                G.edges[node, neighbor]['weight'] *= (1 + strength * 0.1 / (dist + 1))
                G.edges[node, neighbor]['scar_weight'] += strength * 0.05 / (dist + 1)
            if neighbor not in visited:
                queue.append((neighbor, dist + 1))
