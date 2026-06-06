import numpy as np
import matplotlib.pyplot as plt
from .core import make_macro_dodec_cluster, initialize_observer_defect, calculate_local_load_and_capacity
from .projectors import calculate_rho_proxies, calculate_memory_seam_vectors_and_norms
from .dynamics import (
    update_evap_state, update_edge_weights, update_interaction_pressure,
    obs_commit, move_observer_with_gravity, inject_gravitational_wave
)

def run_tri_lobe_eim_simulation(
    max_steps=400,
    eta=0.05,
    num_cells=5,
    kappa=143.9,
    observer_defect_strength=15.0,
    scar_increment=0.08,
    threshold_high=0.95,
    threshold_low=0.85,
    gw_step=None,          # e.g. 150 for GW injection
    gw_strength=8.0,
    gw_radius=4,
    show_plots=True,
    randomize_observer=False
):
    G, first_offset = make_macro_dodec_cluster(num_cells=num_cells)
    observer_node = initialize_observer_defect(G, first_offset)
    current_observer = observer_node

    node_evap_state = {node: False for node in G.nodes()}
    interaction_pressure = {node: 0.0 for node in G.nodes()}

    mean_weights = []
    global_sats = []
    state_switches = []
    seam_commits = 0
    observer_path = [current_observer]
    seam_fractions = []
    signed_branch_means = []
    p_rho3_norms = []
    p_rho3p_norms = []
    p_rho5_norms = []

    print(f"Starting Tri-Lobe EIM Simulation: {G.number_of_nodes()} nodes")

    for step in range(max_steps):
        node_data = calculate_local_load_and_capacity(G, kappa=kappa)

        # Memory lobe
        switches = update_evap_state(G, node_data, node_evap_state,
                                   threshold_high=threshold_high,
                                   threshold_low=threshold_low,
                                   scar_increment=scar_increment)

        # Interaction lobe
        interaction_pressure = update_interaction_pressure(G, node_data, interaction_pressure)

        # OBS Commit
        committed = obs_commit(G, interaction_pressure, node_evap_state, current_observer)
        if committed:
            seam_commits += 1

        # Update weights (Ricci-like flow)
        update_edge_weights(G, node_data, node_evap_state, eta=eta)

        # Observer movement (gravity bias)
        if randomize_observer or step % 5 == 0:
            current_observer = move_observer_with_gravity(G, current_observer, node_data, observer_defect_strength)
            observer_path.append(current_observer)

        # GW Injection
        if gw_step is not None and step == gw_step:
            center = np.random.choice(list(G.nodes()))
            inject_gravitational_wave(G, center, strength=gw_strength, radius=gw_radius)
            print(f"GW injected at step {step} (center node {center})")

        # Diagnostics
        mean_weights.append(np.mean([G.edges[u,v]['weight'] for u,v in G.edges()]))
        global_sats.append(np.mean([d['saturation'] for d in node_data.values()]))
        state_switches.append(switches)

        rho3, rho3p, rho5 = calculate_rho_proxies(node_data, G)
        seam_info = calculate_memory_seam_vectors_and_norms(G, node_data)
        seam_fractions.append(seam_info['seam_fraction'])
        signed_branch_means.append(np.mean(rho3 - rho3p))
        p_rho3_norms.append(seam_info['p_rho3_norm'])
        p_rho3p_norms.append(seam_info['p_rho3_prime_norm'])
        p_rho5_norms.append(np.linalg.norm(rho5))

        if (step + 1) % 100 == 0:
            print(f"Step {step+1}: Commits={seam_commits}, MeanWeight={mean_weights[-1]:.2f}, SeamFrac={seam_fractions[-1]:.3f}")

    # Final diagnostics
    final_seam_fraction = seam_fractions[-1]
    final_signed_branch_mean = signed_branch_means[-1]

    if show_plots:
        fig, axes = plt.subplots(4, 3, figsize=(18, 14))
        axes = axes.flatten()
        
        axes[0].plot(mean_weights); axes[0].set_title('Mean Edge Weight')
        axes[1].plot(global_sats); axes[1].set_title('Global Saturation')
        axes[2].plot(state_switches); axes[2].set_title('State Switches')
        axes[3].plot(seam_fractions); axes[3].set_title('Seam Fraction')
        axes[4].plot(signed_branch_means); axes[4].set_title('Signed Branch Mean (ρ₃ - ρ₃\')')
        axes[5].plot(p_rho3_norms, label='P_ρ₃'); axes[5].plot(p_rho3p_norms, label='P_ρ₃\''); 
        axes[5].set_title('Memory Seam Norms'); axes[5].legend()
        axes[6].plot(p_rho5_norms); axes[6].set_title('ρ₅ (Interaction) Norm')
        
        # Observer path (simplified)
        unique, counts = np.unique(observer_path, return_counts=True)
        axes[7].bar(range(len(unique)), counts)
        axes[7].set_title('Observer Node Visits')
        
        plt.tight_layout()
        plt.show()

    print(f"\n=== SIMULATION COMPLETE ===")
    print(f"Total OBS Seam Commits: {seam_commits} ({seam_commits/max_steps*100:.1f}%)")
    print(f"Final Seam Fraction: {final_seam_fraction:.4f}")
    print(f"Final Signed Branch Mean: {final_signed_branch_mean:.4f}")
    print(f"Observer visited {len(set(observer_path))} unique nodes")

    return G, seam_commits, final_seam_fraction, final_signed_branch_mean, observer_path
