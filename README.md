<img src="project image/logo_header.png" alt="Logo" width="800">

<div align="center">

### A digital twin of prebiotic chiral symmetry breaking
### using a spatial cellular automata.

</div>

<div align="center">

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Made with ❤️ in Ecuador](https://img.shields.io/badge/Made%20with%20❤️%20in-Ecuador-purple)]()

</div>

## Problem
Homochirality is the preferred handedness of molecules in living systems. This project explores the conditions under which homochirality robustly emerges, persists, or fails when varying *environmental complexity*, represented by a chaos parameter ε.

## Approach
The digital twin represents a chemically active surface using a spatial cellular automaton (CA). Achiral, left-, and right-handed molecules are discrete states (0, 1, 2) that interact locally through rules simulating autocatalysis, mutual inhibition, diffusion, and stochastic fluctuations.

## Directory structure

```
Amaranta/
│
├── Amaranta/                # Source package
│   ├── __init__.py
│   ├── counts.py            # Moore neighborhood counts
│   ├── rules.py             # Logic for all CA rules
│   └── simulation.py        # ChiralTwin: Main simulation class
│
├── data/
│   ├── initial-conditions/  # Initial grid states (.npy)
│   └── time-evolution/      # Simulation outputs (.csv, .gif, .png)
│
├── experiments/             # Epsilon sweep scripts and results
│
├── notebooks/             
│
├── results/                 # Final plots and animations
├── project image/           # Logo and header images
│
├── main.py                  # Entry point to run experiments
├── config.yaml              # Configuration file example
└── README.md
```

## How to Run

Clone the repository and navigate to the project directory:

```bash
git clone https://github.com/whyyorlantaken/Amaranta.git
cd Amaranta
```

Install dependencies:

```bash
pip install -r requirements.txt
```
Run the simulation with a configuration file and specify the initial conditions:

```python
python main.py config.yaml -ic initial_conditions
```
