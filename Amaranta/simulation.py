# config = {

#     'simulation': {
#         'total_steps': 250,
#         'boundary_condition': 'periodic',
#         'save_evolution': True
#         'save_images': True 
#     },
#     'probs': {
#         'dist_type': 'uniform',
#         'seed': 42,
#         'p_neutral': 0.1,
#         'p_chiral': 0.1,
#         'p_copy': 0.8
#     },
#     'chaos': {
#         'mode': 'constant',

#         'constant': {
#             'epsilon': 0.1
#         },

#         'pulse': {
#             'start_step': 30,
#             'end_step': 60,
#             'magnitude': 0.5
#         },

#         'linear': {
#             'start_epsilon': 0.0,
#             'end_epsilon': 1.0
#         }
#     }
# }

import numpy as np
import pandas as pd
import os
import time
import warnings
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.animation import FuncAnimation, PillowWriter

from .counts import getMooreCounts
from .rules import *

class ChiralTwin:
    """
    A digital twin for simulating homochirality using a 2D cellular automaton approach.
    All states are represented as integers: 0 for achiral, 1 for left-handed, and 2 for right-handed.

    Parameters
    ----------
    array_file : str
        Path to the file containing the initial state of the grid in .npy format.
    config : dict
        A dictionary containing all necessary parameters for the simulation.
    """

    def __init__(self, array, config):

        # Load iitial state
        if isinstance(array, str):
            self.array  = np.load(array)
            self.icname = array.split("/")[-1].split(".")[0]
        else:
            self.array = array
            self.icname = "custom-array"

        # Read parameters from config
        self.config = config

        self.total_steps        = config['simulation']['total_steps']
        self.boundary_condition = config['simulation']['boundary_condition']
        self.save_evolution     = config['simulation']['save_evolution']
        self.save_images        = config['simulation']['save_images']

        self.dist_type = config['probs']['dist_type']
        self.seed      = config['probs']['seed']
        np.random.seed(self.seed)

        self.p_neutral = config['probs']['p_neutral']
        self.p_chiral  = config['probs']['p_chiral']
        self.p_copy    = config['probs']['p_copy']

        self.chaos_mode = config['chaos']['mode']

        # Set epsilon
        if self.chaos_mode == 'constant':
            self.epsilon = config['chaos']['constant']['epsilon']

        # For now, we'll stick to constant mode.
        if self.chaos_mode == 'pulse':
            self.pulse_start     = config['chaos']['pulse']['start_step']
            self.pulse_end       = config['chaos']['pulse']['end_step']
            self.pulse_magnitude = config['chaos']['pulse']['magnitude']

        if self.chaos_mode == 'linear':
            self.lin_start_epsilon = config['chaos']['linear']['start_epsilon']
            self.lin_end_epsilon   = config['chaos']['linear']['end_epsilon']

        # Print params
        print(f"    ===========================================================================")
        print(f"    PARAMETERS")
        print()
        print(f"       General")
        print(f"         > Initial condition:  {self.icname}.npy")
        print(f"         > Boundary condition: {self.boundary_condition}")
        print(f"         > Total steps:        {self.total_steps}")
        print(f"         > Save evolution:     {self.save_evolution}")
        print(f"         > Save images:        {self.save_images}")
        print()
        print(f"       Chaos")
        print(f"         > Mode:               {self.chaos_mode}")
        print(f"         > Magnitude:          {self.epsilon}")
        print()
        print(f"       Probabilities")
        print(f"         > Distribution type:  {self.dist_type}")
        print(f"         > Seed:               {self.seed}")
        print(f"         > P(neutral):         {self.p_neutral:.2f}")
        print(f"         > P(chiral):          {self.p_chiral:.2f}")
        print(f"         > P(copy):            {self.p_copy:.2f}")
        print(f"    ===========================================================================")

    def timeEvolution(self):
        """
        Simulates the time evolution of the system based on the defined rules and parameters.

        Returns:
        list_0 : A list containing the count of achiral states (0) at each time step.
        list_1 : A list containing the count of left-handed chiral states (1) at each time step.
        list_2 : A list containing the count of right-handed chiral states (2) at each time step
        """
        #Initialize
        list_0 = []        
        list_1 = []
        list_2 = []

        # initialize 3d array to save images (time, x, y)
        if self.save_images:
            data = np.zeros((self.total_steps, *self.array.shape), dtype=int)

        # Save initial state counts
        unique, counts = np.unique(self.array, return_counts=True)
        count_dict = dict(zip(unique, counts))
        list_0.append(count_dict.get(0, 0))
        list_1.append(count_dict.get(1, 0))
        list_2.append(count_dict.get(2, 0))

        # Info
        print(f"    EVOLUTION")
        print()
        print(f"       Progress")

        start_time = time.time()
        
        # Time evolution loop
        for i in range(self.total_steps):
            
            if self.save_images:
                data[i] = self.array

            # Modes logic is done here.
            if self.chaos_mode == 'pulse':
                if self.pulse_start <= i < self.pulse_end:
                    self.epsilon = self.pulse_magnitude
                else:
                    self.epsilon = 0

            elif self.chaos_mode == 'linear':
                self.epsilon = np.interp(i, [0, self.total_steps], [self.lin_start_epsilon, self.lin_end_epsilon])

            # Moore counts + each rule in order, chaining output into the next step.
            neighborhood = getMooreCounts(self.array, boundaries = self.boundary_condition)
            array        = autocatalysis(neighborhood).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = mutualInhibition(neighborhood).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = spontaneusNeutrality(self.epsilon, self.p_neutral, neighborhood, self.dist_type).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = spontaneousChirality(self.epsilon, self.p_chiral, neighborhood, self.dist_type).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = diffusion(self.epsilon, self.p_copy, neighborhood, self.dist_type).reshape(self.array.shape)

            self.array   = array

            unique, counts = np.unique(array, return_counts=True)
            count_dict = dict(zip(unique, counts))
            list_0.append(count_dict.get(0, 0))
            list_1.append(count_dict.get(1, 0))
            list_2.append(count_dict.get(2, 0))

            # Progess each 20% of the evolution
            if self.total_steps >= 5 and (i + 1) % (self.total_steps // 5) == 0:
                print(f"         - {i + 1}/{self.total_steps}")

        end_time = time.time()
        elapsed_time = end_time - start_time

        print(f"         > Success!")
        print()
        print(f"       Performance")
        print(f"         > Total time:         {elapsed_time:.2f}s")
        print(f"         > Time per step:      {elapsed_time / self.total_steps:.4f}s")
        print(f"    ===========================================================================")
        
        # Save evolution
        if self.save_evolution:

            name = f"{self.chaos_mode}-{self.epsilon}_dist-{self.dist_type}"

            if self.chaos_mode == 'pulse':
                name = f"{self.chaos_mode}-{self.pulse_magnitude}_dist-{self.dist_type}"

            # Folder
            os.makedirs(f"data/time-evolution/{name}", exist_ok=True)

            df = pd.DataFrame({'Achiral': list_0, 'Chiral A': list_1, 'Chiral B': list_2})
            df.to_csv(f"data/time-evolution/{name}/evolution-{self.icname}.csv", index = False)

            #gif of time evolution
            fig, ax = plt.subplots(figsize=(4*1.3, 3*1.3), dpi=200)

            line, = ax.plot([], [], label='Achiral', color='#4e0f04', lw=4)
            line_chiral_a, = ax.plot([], [], label='Chiral A', color='#ea7ac6', lw=4)
            line_chiral_b, = ax.plot([], [], label='Chiral B', color='#658338', lw=4)

            ax.set_xlim(0, len(df) - 1)
            ax.set_ylim(0, df['Achiral'].max())
            #ax.set_xlabel('Time')
            #ax.set_ylabel('Cell Number')
            #ax.set_title("t = 0")
            ax.legend(fontsize=12, loc='upper right')
            ax.grid(color='gray', linestyle='--', lw=0.5, alpha=0.3)

            def update(t):
                x = np.arange(t + 1)
                y = df['Achiral'].iloc[:t + 1]
                y_chiral_a = df['Chiral A'].iloc[:t + 1]
                y_chiral_b = df['Chiral B'].iloc[:t + 1]
                line.set_data(x, y)
                line_chiral_a.set_data(x, y_chiral_a)
                line_chiral_b.set_data(x, y_chiral_b)
                #ax.set_title(f"t = {t}")
                return [line, line_chiral_a, line_chiral_b]

            ani = FuncAnimation(fig, update, frames=df['Achiral'].shape[0], interval=120, blit=True)

            # Save last frame as png
            update(len(df) - 1)
            plt.savefig(f"data/time-evolution/{name}/time_evolution-{self.icname}.png", dpi=200)
            
            # Save GIF
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ani.save(f"data/time-evolution/{name}/time_evolution-{self.icname}.gif", writer=PillowWriter(fps=8))
            plt.close(fig)

            print(f"       Time evolution")
            print(f"          > Data: evolution-{self.icname}.csv")
            print(f"          > GIF:  time_evolution-{self.icname}.gif")

        # Save images
        if self.save_images:

            name = f"{self.chaos_mode}-{self.epsilon}_dist-{self.dist_type}"

            if self.chaos_mode == 'pulse':
                name = f"{self.chaos_mode}-{self.pulse_magnitude}_dist-{self.dist_type}"

            # Class colors: 0,1,2
            cmap = ListedColormap(["white", "#ea7ac6", "#658338"])
            norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], cmap.N)

            fig, ax = plt.subplots(figsize=(4, 4))
            im = ax.imshow(data[0], cmap=cmap, norm=norm, interpolation="nearest")
            ax.set_axis_off()

            def update(t):
                im.set_data(data[t])
                #ax.set_title(f"t = {t}")
                return [im]

            ani = FuncAnimation(fig, update, frames=data.shape[0], interval=120, blit=True)

            # Save last frame as png
            im.set_data(data[-1])
            plt.savefig(f"data/time-evolution/{name}/spatial-{self.icname}.png", dpi=200)
            
            # Save GIF
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                ani.save(f"data/time-evolution/{name}/spatial-{self.icname}.gif")

            print()
            print(f"       Spatial evolution")
            print(f"          > PNG:  spatial-{self.icname}.png")
            print(f"          > GIF:  spatial-{self.icname}.gif")
            print(f"    ===========================================================================")
        print()
        print(f"                              Simulation completed.")
        print()
        print(f"    ===========================================================================")

            # print(f"Spatial GIF saved!")

        return list_0, list_1, list_2
