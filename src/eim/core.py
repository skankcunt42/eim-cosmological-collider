import networkx as nx
import numpy as np

def make_macro_dodec_cluster(num_cells=5):
    G = nx.Graph()
    current_node_offset = 0
    node_offsets = []
    dodec_node_count = nx.dodecahedral_graph().number_of_nodes()

    for i in range(num_cells):
        dodec_graph = nx.dodecahedral_graph()
        mapping = {node: node + current_node_offset for node in dodec_graph.nodes()}
        for u, v in dodec_graph.edges():
            G.add_edge(mapping[u], mapping[v])
        node_offsets.append(current_node_offset)
        current_node_offset += dodec_node_count

    # Sparse seams
    for i in range(num_cells - 1):
        original_node1 = np.random.choice(dodec_node_count)
        node1_global_id = original_node1 + node_offsets[i]
        original_node2 = np.random.choice(dodec_node_count)
        node2_global_id = original_node2 + node_offsets[i+1]
        G.add_edge(node1_global_id, node2_global_id)

    for u, v in G.edges():
        G.edges[u, v]['weight'] = np.random.uniform(1.0, 2.0)
        G.edges[u, v]['scar_weight'] = 0.0

    return G, node_offsets[0]

def initialize_observer_defect(G, first_graph_node_offset):
    observer_node = first_graph_node_offset + 0
    for u, v in list(G.edges(observer_node)):
        G.edges[u, v]['weight'] *= 15.0
    return observer_node

def calculate_local_load_and_capacity(G, kappa=143.9):
    node_data = {}
    for node in G.nodes():
        local_load = sum(G.edges[node, neighbor]['weight'] + G.edges[node, neighbor]['scar_weight'] 
                        for neighbor in G.neighbors(node))
        local_capacity = kappa * G.degree(node)
        saturation = local_load / local_capacity
        node_data[node] = {
            'local_load': local_load,
            'local_capacity': local_capacity,
            'saturation': saturation
        }
    return node_data
