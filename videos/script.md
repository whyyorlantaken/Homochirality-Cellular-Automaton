# Video Script

## Hook

In the origins of life, one mystery keeps coming back: living systems pick one molecular handedness, known as **homochirality**.

And that single bias might be the difference between chemistry that stays random… and chemistry that becomes life.

## Problem

In this project we a ask sharp question: when does homochirality robustly emerge and persist and when does it fail?

## Method

To test that, we built **Amaranta**: a digital twin of a chemically active surface, using a spatial cellular automaton. Each grid cell is a discrete state:

- `0` = achiral
- `1` = left-handed
- `2` = right-handed

Local interactions simulate autocatalysis, mutual inhibition, diffusion, and noise. We vary environmental complexity using a chaos parameter, **ε**, to see if stable chirality appears as the environment becomes more unpredictable.

HERE! -----------------------------

Our workflow starts with:

1. **Loading the initial conditions** — we run scenarios to represent different starting worlds.
2. **Reading parameters**, including:
    - Simulation controls
    - Probabilities of the stochastic processes
    - The chaos mode
3. We built a `ChiralTwin` class to evolve the system step by step.
4. Each step applies rules that blend determinism and chance, influenced by the cell's neighborhood:
    - **Autocatalysis** gives the most common local chirality to an achiral cell.
    - **Mutual inhibition** cancels out opposite chirality locally.
    - **Spontaneous neutrality** removes chirality randomly via `p_neutral`.
    - **Spontaneous chirality** assigns chirality randomly via `p_chiral`.
    - **Diffusion** duplicates chirality randomly via `p_copy`.

    These last three stochastic rules are modulated by the chaos parameter **ε**.

## Results & Limitations

Our main results are:

1. **Stochasticity is necessary** for the emergence of chirality *(pulso_128)*.
2. **Homochirality emerges** when there is significant diffusion *(constant_064)*.
3. However, in larger spatial grids (higher resolution), chiral species still dominate but **homochirality is no longer achieved** *(constant_512, case 1)*.
4. We expected that small symmetry breaking would always amplify over time (as the literature suggests), but we encountered cases where a slightly more abundant achiral species **ended up less abundant** by the end of the simulation *(constant_512, case 2)*.
5. Lastly, our **epsilon sweep results were inconclusive** due to a pipeline issue — see the repository for details.

> 📂 Check our repo to see the full results!
