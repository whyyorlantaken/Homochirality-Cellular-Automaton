# Homochirality Cellular Automaton

A digital twin of prebiotic chiral symmetry breaking using a spatial cellular automaton.

## Problem
Homochirality is the preferred handedness of molecules in living systems. This project explores the conditions under which homochirality robustly emerges, persists, or fails when varying environmental complexity, represented by a chaos parameter ε.

## Proposed approach
The digital twin represents a chemically active surface using a spatial cellular automaton (CA). Achiral, left-, and right-handed molecules are discrete states that interact locally through rules simulating autocatalysis, mutual inhibition, diffusion, and stochastic fluctuations.

## Directory structure

```
Homochirality-Cellular-Automaton/
│
├── data/                  # Saved initial states (.npy) and evolution (.csv)
├── experiments/           # All configuration.yaml files for scenarios
│
├── src/   
│   ├── __init__.py
│   │
│   ├── spatial-domain.py  # Grid state, Moore, boundaries
│   ├── rules.py           # Logic for all rules
│   ├── simulation.py      # DigitalTwin: the time-loop and ε scaling
│   │
│   ├── plotting.py        
│   └── analytics.py
│
├── results/               # Final plots, animations
│  
├── main.py                # Entry point to run experiments
├── config.yaml            # Configuration file example
└── README.md           
```

## Run

```python
python main.py config.yaml
```

## Example `main.py`

```python
import argparse
import yaml
from src.simulation import DigitalTwin

def main():

    # Configuration file
    parser = argparse.ArgumentParser(
      description="Run homochirality cellular automaton digital twin with specified configuration"
      )
    parser.add_argument("config", 
	    help="Path to the .yaml configuration file"
	    )
    args = parser.parse_args()

    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)

    twin = DigitalTwin(config)
    twin.run()

if __name__ == "__main__":
    main()
```

## Example `config.yaml`

```yaml
simulation:
  grid_size: [128, 128]
  total_steps: 1000
  boundary_condition: "periodic"

probabilities:
  p_neutral: 0.05      
  p_chiral: 0.02
  p_copy: 0.1

chaos:
  epsilon: 1.0         
  seed: 42             
  mode: "constant"

  pulse:
    start_step: 400
    end_step: 500
    magnitude: 5.0 

  linear_increase:
    start_step: 400
    end_step: 500
    max_epsilon: 5.0
```
