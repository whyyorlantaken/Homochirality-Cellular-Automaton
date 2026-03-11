<img src="project image/logo_header.png" alt="Logo" width="600">

### A digital twin of prebiotic chiral symmetry breaking using a spatial cellular automaton.

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Made with ❤️ in Ecuador](https://img.shields.io/badge/Made%20with%20❤️%20in-Ecuador-purple)]()

## Problem
Homochirality is the preferred handedness of molecules in living systems. This project explores the conditions under which homochirality robustly emerges, persists, or fails when varying environmental complexity, represented by a chaos parameter ε.

## Approach
The digital twin represents a chemically active surface using a spatial cellular automaton (CA). Achiral, left-, and right-handed molecules are discrete states that interact locally through rules simulating autocatalysis, mutual inhibition, diffusion, and stochastic fluctuations.

## Directory structure

```
Amaranta/
│
├── Amaranta/              # Source package
│   ├── __init__.py
│   ├── analytics.py       # Metrics and analysis functions
│   ├── counts.py          # Moore neighborhood counts
│   ├── rules.py           # Logic for all CA rules
│   └── simulation.py      # ChiralTwin: time-loop and ε scaling
│
├── data/
│   ├── initial-conditions/  # Initial grid states (.npy)
│   └── time-evolution/      # Simulation outputs (.csv, .gif, .png)
│
├── experiments/           # Epsilon Sweep scripts and results
│
├── notebooks/             # Jupyter exploration notebooks
│   ├── 01-Neighbor-count.ipynb
│   ├── 02-Evolution-testing.ipynb
│   ├── 03-ChiralTwin.ipynb
│   ├── 04-Save-evolution.ipynb
│   ├── 05-Epsilon-sweep.ipynb
│   ├── 06-Definitive-ICs.ipynb
│   └── 07-Fixing-parameters.ipynb
│
├── results/               # Final plots and animations
├── sketchs/               # Design sketches
├── project image/         # Logo and header images
│
├── main.py                # Entry point to run experiments
├── config.yaml            # Configuration file example
└── README.md
```

## How to Run

```python
python main.py config.yaml -ic initial_conditions
```
