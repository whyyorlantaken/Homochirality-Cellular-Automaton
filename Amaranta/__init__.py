"""
Amaranta — Homochirality Cellular Automaton
===========================================
A simulation package for studying the emergence of homochirality via a 2D
cellular automaton.

Modules
-------
counts      : Moore-neighborhood state counting.
rules       : Deterministic and stochastic transition rules.
simulation  : ChiralTwin digital-twin class that orchestrates time evolution.
plotting    : Visualisation utilities.
analytics   : Clustering analysis (in progress).
"""

from .counts import getMooreCounts

# Deterministic
from .rules import autocatalysis, mutualInhibition

# Stochastic
from .rules import spontaneusNeutrality, spontaneousChirality, diffusion

from .simulation import ChiralTwin

# Plotting (stubs — imported so they are accessible via the package)
# from .plotting import (
#     chiralPopulationPlot,
#     chaosParameterPlot,
#     phaseSpacePlot,
#     spatialPlot,
#     spatialgif,
# )

# __all__ = [
#     # counts
#     "getMooreCounts",
#     # rules — deterministic
#     "autocatalysis",
#     "mutualInhibition",
#     # rules — stochastic
#     "spontaneusNeutrality",
#     "spontaneousChirality",
#     "diffusion",
#     # simulation
#     "ChiralTwin",
#     # plotting
#     "chiralPopulationPlot",
#     "chaosParameterPlot",
#     "phaseSpacePlot",
#     "spatialPlot",
#     "spatialgif",
# ]
