import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime
import os

def export_simulation_to_excel(results, filename=None):
    """
    Export Tri-Lobe EIM simulation results to Excel (your preferred format)
    Compatible with your EIM Semantic Projection Dictionary workbooks.
    """
    if filename is None:
        filename = f"EIM_Collider_Run_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # Main diagnostics sheet
        diag_df = pd.DataFrame({
            'Step': range(len(results['mean_weights'])),
            'Mean_Edge_Weight': results['mean_weights'],
            'Global_Saturation': results['global_sats'],
            'State_Switches': results['state_switches'],
            'Seam_Fraction': results['seam_fractions'],
            'Signed_Branch_Mean': results['signed_branch_means'],
            'P_rho3_Norm': results['p_rho3_norms'],
            'P_rho3p_Norm': results['p_rho3p_norms'],
            'P_rho5_Norm': results['p_rho5_norms']
        })
        diag_df.to_excel(writer, sheet_name='Diagnostics', index=False)
        
        # Summary sheet
        summary = {
            'Total_OBS_Commits': [results['seam_commits']],
            'Commit_Rate_%': [results['seam_commits'] / len(results['mean_weights']) * 100],
            'Final_Seam_Fraction': [results['final_seam_fraction']],
            'Final_Signed_Branch_Mean': [results['final_signed_branch_mean']],
            'Unique_Nodes_Visited': [len(set(results['observer_path']))],
            'Num_Cells': [results.get('num_cells', 5)],
            'Kappa': [results.get('kappa', 143.9)],
            'Eta': [results.get('eta', 0.05)],
            'Run_Date': [datetime.now().strftime('%Y-%m-%d %H:%M')]
        }
        pd.DataFrame(summary).to_excel(writer, sheet_name='Summary', index=False)
        
        # Observer path
        pd.DataFrame({'Observer_Path': results['observer_path']}).to_excel(
            writer, sheet_name='Observer_Path', index=False)
    
    print(f"✅ Results exported to {filename}")
    return filename


def save_graph_state(G, filename="eim_graph_state.gpickle"):
    """Save graph state for resuming simulations"""
    nx.write_gpickle(G, filename)
    print(f"Graph saved to {filename}")


def load_graph_state(filename="eim_graph_state.gpickle"):
    """Load previously saved graph"""
    if os.path.exists(filename):
        return nx.read_gpickle(filename)
    else:
        print("No saved graph found.")
        return None


def connect_to_semantic_dictionary(results, workbook_path=None):
    """
    Placeholder for linking simulation outputs to your main EIM Semantic Projection Dictionary.
    Can be expanded to push scalars (seam fraction, branch mean, commit rate) into specific sheets.
    """
    print("🔗 Semantic Dictionary Connector Ready")
    print(f"Key metrics for Codex / Dashboard:")
    print(f"  • Final Seam Fraction: {results['final_seam_fraction']:.4f}")
    print(f"  • Signed Branch Mean: {results['final_signed_branch_mean']:.4f}")
    print(f"  • OBS Commit Rate: {results['seam_commits']/len(results['mean_weights'])*100:.1f}%")
    # Future: pandas to_excel append to specific sheets in your v10+ workbook
    return results


# Convenience wrapper for full run + export
def run_and_export(max_steps=400, gw_step=None, **kwargs):
    from .simulation import run_tri_lobe_eim_simulation
    
    G, commits, seam_frac, branch_mean, path = run_tri_lobe_eim_simulation(
        max_steps=max_steps, gw_step=gw_step, show_plots=False, **kwargs
    )
    
    results = {
        'mean_weights': [],  # Populate from simulation (we'll enhance simulation.py later if needed)
        'global_sats': [],
        'state_switches': [],
        'seam_fractions': [],
        'signed_branch_means': [],
        'p_rho3_norms': [],
        'p_rho3p_norms': [],
        'p_rho5_norms': [],
        'observer_path': path,
        'seam_commits': commits,
        'final_seam_fraction': seam_frac,
        'final_signed_branch_mean': branch_mean,
        'num_cells': kwargs.get('num_cells', 5),
        'kappa': kwargs.get('kappa', 143.9),
        'eta': kwargs.get('eta', 0.05)
    }
    
    export_simulation_to_excel(results)
    connect_to_semantic_dictionary(results)
    return G, results
