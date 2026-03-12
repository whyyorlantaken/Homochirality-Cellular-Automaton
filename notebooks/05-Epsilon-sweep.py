import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_sweep_data(sweep_dir):
    """
    Load simulation sweep data from a directory of epsilon experiments.
    
    Parameters:
    -----------
    sweep_dir : str
        Path to the sweep directory containing eps_* folders
        
    Returns:
    --------
    dict
        Dictionary containing:
        - 'epsilons': array of epsilon values
        - 'mean_0', 'mean_A', 'mean_B': mean values for each cell type
        - 'max_0', 'max_A', 'max_B': max values for each cell type
        - 'last_0', 'last_A', 'last_B': final values for each cell type
        - 'records': dict of DataFrames indexed by epsilon
    """
    # Load all results indexed by epsilon value
    records = {}
    for folder in os.listdir(sweep_dir):
        if not folder.startswith('eps_'):
            continue
        path = os.path.join(sweep_dir, folder, 'evolution-achiral_majority_128.csv')
        if not os.path.isfile(path):
            continue
        eps = float(folder.replace('eps_', ''))
        records[eps] = pd.read_csv(path)
    
    epsilons = np.array(sorted(records.keys()))
    mean_0   = np.array([records[e]['Achiral'].mean()    for e in epsilons])
    mean_A   = np.array([records[e]['Chiral A'].mean()   for e in epsilons])
    mean_B   = np.array([records[e]['Chiral B'].mean()   for e in epsilons])
    max_0    = np.array([records[e]['Achiral'].max()     for e in epsilons])
    max_A    = np.array([records[e]['Chiral A'].max()    for e in epsilons])
    max_B    = np.array([records[e]['Chiral B'].max()    for e in epsilons])
    last_0   = np.array([records[e]['Achiral'].iloc[-1]  for e in epsilons])
    last_A   = np.array([records[e]['Chiral A'].iloc[-1] for e in epsilons])
    last_B   = np.array([records[e]['Chiral B'].iloc[-1] for e in epsilons])
    
    print(f"Loaded {len(epsilons)} epsilon values from {sweep_dir}")
    
    return {
        'epsilons': epsilons,
        'mean_0': mean_0, 'mean_A': mean_A, 'mean_B': mean_B,
        'max_0': max_0, 'max_A': max_A, 'max_B': max_B,
        'last_0': last_0, 'last_A': last_A, 'last_B': last_B,
        'records': records
    }

if __name__ == "__main__":

    # Load sweep data
    sweep_dir = 'experiments/sweep_achiral_majority_128_eps_0.0_to_1.0'
    data      = load_sweep_data(sweep_dir)
    
    fig, ax = plt.subplots(figsize=(4*1.3, 3*1.3), dpi=200)
    ax.plot(data['epsilons'], data['last_0'], label='Achiral',  color='#4e0f04', lw=4, marker='o')
    ax.plot(data['epsilons'], data['last_A'], label='Chiral A', color='#ea7ac6', lw=4, marker='o')
    ax.plot(data['epsilons'], data['last_B'], label='Chiral B', color='#658338', lw=4, marker='o')
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(color='gray', linestyle='--', lw=0.5, alpha=0.3)
    plt.savefig(os.path.join(sweep_dir, 'steady_state_128.png'))
    plt.show()