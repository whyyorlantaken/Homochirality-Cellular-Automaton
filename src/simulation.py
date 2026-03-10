# initialize
    # read array with initial conditions from data or user imput
    # read parameters (read config)
    #initialize somthing to save states population (total de zeros, unos y dos) and images (in array) (for visualization)

#LOOP
    # use getMooreCounts
    # update epsilon and probs (?)
    # update states (time evolution) (applying rules: deterministic and then stochastic or the other way around?)
    # save states population and images (arrays) (for visualization)

import numpy as np

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

        if isinstance(array, str):
            self.array  = np.load(array)
        else:
            self.array = array

        self.config = config

        self.total_steps        = config['simulation']['total_steps']
        self.boundary_condition = config['simulation']['boundary_condition']

        self.p_neutral = config['probs']['p_neutral']
        self.p_chiral  = config['probs']['p_chiral']
        self.p_copy    = config['probs']['p_copy']

        self.chaos_mode = config['chaos']['mode']

        if self.chaos_mode == 'constant':
            self.epsilon = config['chaos']['constant']['epsilon']

        # For now, we'll stick to constant mode.
        if self.chaos_mode == 'pulse':
            self.pulse_start     = config['chaos']['pulse']['start_step']
            self.pulse_end       = config['chaos']['pulse']['end_step']
            self.pulse_magnitude = config['chaos']['pulse']['magnitude']

        if self.chaos_mode == 'linear_increase':
            self.lin_start_epsilon = config['chaos']['linear_increase']['start_epsilon']
            self.lin_end_epsilon   = config['chaos']['linear_increase']['end_epsilon']

        self.seed    = config['chaos']['seed']
        # np.random.seed(self.seed)

    def timeEvolution(self):

        list_0 = []        
        list_1 = []
        list_2 = []

        unique, counts = np.unique(self.array, return_counts=True)
        count_dict = dict(zip(unique, counts))
        list_0.append(count_dict.get(0, 0))
        list_1.append(count_dict.get(1, 0))
        list_2.append(count_dict.get(2, 0))
        
        for i in range(self.total_steps):

            # Modes logic is done here.
            if self.chaos_mode == 'pulse':
                if self.pulse_start <= i < self.pulse_end:
                    self.epsilon = self.pulse_magnitude
                else:
                    self.epsilon = 0

            elif self.chaos_mode == 'linear_increase':
                self.epsilon = np.interp(i, [0, self.total_steps], [self.lin_start_epsilon, self.lin_end_epsilon])

            # Moore counts + each rule in order, chaining output into the next step.
            neighborhood = getMooreCounts(self.array, boundaries = self.boundary_condition)
            array        = autocatalysis(neighborhood).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = mutualInhibition(neighborhood).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = spontaneusNeutrality(self.epsilon, self.p_neutral, neighborhood).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = spontaneousChirality(self.epsilon, self.p_chiral, neighborhood).reshape(self.array.shape)

            neighborhood = getMooreCounts(array, boundaries = self.boundary_condition)
            array        = diffusion(self.epsilon, self.p_copy, neighborhood).reshape(self.array.shape)

            self.array   = array

            unique, counts = np.unique(array, return_counts=True)
            count_dict = dict(zip(unique, counts))
            list_0.append(count_dict.get(0, 0))
            list_1.append(count_dict.get(1, 0))
            list_2.append(count_dict.get(2, 0))

        return list_0, list_1, list_2
