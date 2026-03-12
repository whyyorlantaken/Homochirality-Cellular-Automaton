# Video Script

## Hook

[Mariannly]

In the origins of life, one mystery keeps coming back: living systems pick one molecular handedness, known as **homochirality**.

[Yorlan]

And that might be the difference between chemistry that stays random… and chemistry that becomes life.

## Problem

[Yorlan]

In this project we ask: when does homochirality emerge and persist and when does it fail?

## Method

[Mariannly]

To test that, we built **Amaranta**: a digital twin of a chemically active surface, using cellular automata. Each grid cell is a discrete state:

- `0` = achiral
- `1` = left-handed
- `2` = right-handed

[Mariannly]

Our workflow starts with:

1. **Loading the initial conditions** — we run scenarios to represent different starting worlds.
2. Then we set **the parameters**, including:
    - Simulation controls
    - Probabilities of stochastic processes
    - and the chaos mode.

[Yorlan]

3. Then, our class `ChiralTwin` evolves the system.
4. Each step applies rules that blend determinism and chance, influenced by the cell's neighborhood:

    - In **autocatalysis**, an achiral cell adopts the dominant chirality
    - While **mutual inhibition** cancels out opposite chirality locally.
    - In **spontaneous neutrality**, a chiral cell loses its handedness at random
    - While in **spontaneous chirality**, an achiral cell randomly gains one.
    - And in **diffusion** any cell copies a random neighbor's state.

    We modulate the stochastic processes using a chaos parameter, **ε**, to see if stable chirality appears as the environment becomes more unpredictable.

## Results & Limitations

[Mariannly]

Our main results are:

1. That, without any randomness, the system remains achiral, as here where we turn stochastic rules on for a period of time. 

2. Next, we varied the intensity of the chaos parameter and found that homochirality emerges more robustly in the high regime. Also that the chiral type dominance oscillates over epsilon.

3. For instance, this is the full time evolution of a high-ε simulation, where homochirality emerges.

[Yorlan]

4. However, we didn't find the same results in higher resolutions as seen here where neither of them dominate.

5. Lastly, we expected that differences in the initial conditions would keep growing over time, but this was not always the case, especially in high-res simulations. We suspect that spatial distributions play a key role here.

[Mariannly]

> 📂 Check our repo out! Thank you!
