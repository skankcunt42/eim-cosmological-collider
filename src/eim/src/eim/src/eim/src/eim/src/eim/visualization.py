import matplotlib.pyplot as plt
import numpy as np

def plot_diagnostics(mean_weights, global_sats, state_switches, 
                    seam_fractions, signed_branch_means,
                    p_rho3_norms, p_rho3p_norms, p_rho5_norms,
                    observer_path, seam_commits, max_steps):
    """Full diagnostic dashboard for Tri-Lobe EIM simulation"""
    fig, axes = plt.subplots(4, 3, figsize=(20, 16))
    axes = axes.flatten()
    
    axes[0].plot(mean_weights)
    axes[0].set_title('Mean Edge Weight Evolution')
    axes[0].set_xlabel('Step')
    
    axes[1].plot(global_sats)
    axes[1].set_title('Global Saturation')
    axes[1].set_xlabel('Step')
    
    axes[2].plot(state_switches)
    axes[2].set_title('Evaporation State Switches')
    axes[2].set_xlabel('Step')
    
    axes[3].plot(seam_fractions)
    axes[3].set_title('Seam Fraction (Memory/Total)')
    axes[3].set_xlabel('Step')
    axes[3].set_ylim(0, 1)
    
    axes[4].plot(signed_branch_means)
    axes[4].set_title('Signed Branch Mean (ρ₃ − ρ₃′)')
    axes[4].set_xlabel('Step')
    axes[4].axhline(0, color='gray', linestyle='--')
    
    axes[5].plot(p_rho3_norms, label='P_ρ₃ (Memory)')
    axes[5].plot(p_rho3p_norms, label="P_ρ₃' (Conjugate)")
    axes[5].plot(p_rho5_norms, label='P_ρ₅ (Interaction)')
    axes[5].set_title('Spectral Projection Norms')
    axes[5].legend()
    axes[5].set_xlabel('Step')
    
    # Observer visits
    unique, counts = np.unique(observer_path, return_counts=True)
    axes[6].bar(range(len(unique)), counts)
    axes[6].set_title(f'Observer Node Visit Distribution\n({len(unique)} unique nodes)')
    axes[6].set_xlabel('Node Index (sorted)')
    
    axes[7].text(0.5, 0.5, f'Total OBS Commits: {seam_commits}\n'
                          f'Commit Rate: {seam_commits/max_steps*100:.1f}%\n'
                          f'Final Seam Fraction: {seam_fractions[-1]:.3f}',
                 ha='center', va='center', fontsize=12, transform=axes[7].transAxes)
    axes[7].axis('off')
    
    plt.suptitle('Tri-Lobe EIM Cosmological Collider — W.43 Audit', fontsize=16)
    plt.tight_layout()
    plt.show()
