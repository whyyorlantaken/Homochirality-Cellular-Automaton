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
        else:
            self.array = array

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
            images = np.zeros((self.total_steps, *self.array.shape), dtype=int)

        # Save initial state counts
        unique, counts = np.unique(self.array, return_counts=True)
        count_dict = dict(zip(unique, counts))
        list_0.append(count_dict.get(0, 0))
        list_1.append(count_dict.get(1, 0))
        list_2.append(count_dict.get(2, 0))
        
        # Time evolution loop
        for i in range(self.total_steps):
            
            if self.save_images:
                images[i] = self.array

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

        # Save evolution
        if self.save_evolution:

            name = f"{self.chaos_mode}-{self.epsilon}_dist-{self.dist_type}"

            if self.chaos_mode == 'pulse':
                name = f"{self.chaos_mode}-{self.pulse_magnitude}_dist-{self.dist_type}"

            # Folder
            os.makedirs(f"data/time-evolution/{name}", exist_ok=True)

            df = pd.DataFrame({'Achiral': list_0, 'Chiral A': list_1, 'Chiral B': list_2})
            df.to_csv(f"data/time-evolution/{name}/evolution.csv", index = False)

        # Save images
        if self.save_images:

            name = f"{self.chaos_mode}-{self.epsilon}_dist-{self.dist_type}"

            if self.chaos_mode == 'pulse':
                name = f"{self.chaos_mode}-{self.pulse_magnitude}_dist-{self.dist_type}"

            np.save(f"data/time-evolution/{name}/images.npy", images)

        return list_0, list_1, list_2
