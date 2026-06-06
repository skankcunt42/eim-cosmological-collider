import matplotlib.pyplot as plt
import numpy as np

def plot_diagnostics(mean_weights, global_sats, state_switches, 
                    seam_fractions, signed_branch_means,
                    p_rho3_norms, p_rho3p_norms, p_rho5_norms,
                    observer_path, seam_commits, max_steps):
    fig, axes = plt.subplots(4, 3, figsize=(20, 16))
    axes = axes.flatten()
    
    axes[0].plot(mean_weights); axes[0].set_title('Mean Edge Weight')
    axes[1].plot(global_sats); axes[1].set_title('Global Saturation')
    axes[2].plot(state_switches); axes[2].set_title('State Switches')
    axes[3].plot(seam_fractions); axes[3].set_title('Seam Fraction')
    axes[4].plot(signed_branch_means); axes[4].set_title('Signed Branch Mean')
    axes[5].plot(p_rho3_norms, label='P_ρ₃'); axes[5].plot(p_rho3p_norms, label="P_ρ₃'"); 
    axes[5].plot(p_rho5_norms, label='P_ρ₅'); axes[5].legend(); axes[5].set_title('Projection Norms')
    
    unique, counts = np.unique(observer_path, return_counts=True)
    axes[6].bar(range(len(unique)), counts)
    axes[6].set_title('Observer Visits')
    
    plt.suptitle('EIM Tri-Lobe Collider — W.43 Audit', fontsize=16)
    plt.tight_layout()
    plt.show()
