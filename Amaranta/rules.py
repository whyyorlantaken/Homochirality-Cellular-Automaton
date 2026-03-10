import numpy as np

###########################
# Deterministic Rules
###########################

def autocatalysis(neighborhood):
    """
    Reads a neighborhood array with the following structure:

    Cell state | Number of zeros | Number of ones | Number of twos
    [     0              2                 5               1        ]
    [     1              3                 4               1        ]
    [                            ...                                ]
    [     2              1                 6               1        ]

    Shape: N x 4, where N is the total number of cells in the grid.

    The function turns the achiral cells (state 0) into chiral cells (state 1 or 2)
    if the number of chiral neighbors (state 1 and state 2) is greater than the number
    of achiral neighbors (state 0). If the number of achiral neighbors is equal to the
    number of chiral neighbors, the cell state remains unchanged.

    It returns an array of new states for each cell in the grid.
    """
    new_states = []

    for state, number_of_zeros, number_of_ones, number_of_twos in neighborhood:
        if state == 0 and number_of_zeros < (number_of_ones + number_of_twos):
            if number_of_ones > number_of_twos:
                new_states.append(1)
            elif number_of_twos > number_of_ones:
                new_states.append(2)
            else:
                new_states.append(state)
        else:
            new_states.append(state)

    return np.array(new_states)

def mutualInhibition(neighborhood):
    """
    Reads a neighborhood array with the following structure:

    Cell state | Number of zeros | Number of ones | Number of twos
    [     0              2                 5               1        ]
    [     1              3                 4               1        ]
    [                            ...                                ]
    [     2              1                 6               1        ]

    Shape: N x 4, where N is the total number of cells in the grid.

    The funcion turns the chiral cells (state 1 or 2) into achiral cells (state 0)
    if the neighborhood contains a majority of cells with the opposite chirality.
    If the number of cells with the opposite chirality is equal to the number of cells
    with the same chirality, the cell state remains unchanged.

    It returns an array of new states for each cell in the grid.
    """
    new_states = []

    for state, number_of_zeros, number_of_ones, number_of_twos in neighborhood:
        if state == 1 and (number_of_zeros + number_of_ones) < number_of_twos:
            new_states.append(0)
        elif state == 2 and (number_of_zeros + number_of_twos) < number_of_ones:
            new_states.append(0)
        else:
            new_states.append(state)

    return np.array(new_states)

########################
# Stochastic Rules
########################

def spontaneusNeutrality(epsilon, p_neutral, neighborhood, dist_type='uniform'):
    """
    Reads a neighborhood array with the following structure:

    Cell state | Number of zeros | Number of ones | Number of twos
    [     0              2                 5               1        ]
    [     1              3                 4               1        ]
    [                            ...                                ]
    [     2              1                 6               1        ]

    Shape: N x 4, where N is the total number of cells in the grid.

    The function turns the chiral cells (state 1 or 2) into achiral cells (state 0)
    with a probability p_neutral, regardless of the neighborhood composition.
    p_neutral is modulared by the parameter epsilon, which represents the strength
    of the stochastic effect.

    It returns an array of new states for each cell in the grid.
    """
    new_states = []
    prob = epsilon * p_neutral

    for state, number_of_zeros, number_of_ones, number_of_twos in neighborhood:
        if state in [1, 2]:

            if dist_type == 'uniform':
                rand = np.random.rand()

            elif dist_type == 'normal':
                rand = np.random.normal(0, 1) 

            elif dist_type == 'lognormal':
                rand = np.random.lognormal(0, 1)

            if rand < prob:
                new_states.append(0)
            else:
                new_states.append(state)
        else:
            new_states.append(state)

    return np.array(new_states)

def spontaneousChirality(epsilon, p_chiral, neighborhood, dist_type='uniform'):
    """
    Reads a neighborhood array with the following structure:

    Cell state | Number of zeros | Number of ones | Number of twos
    [     0              2                 5               1        ]
    [     1              3                 4               1        ]
    [                            ...                                ]
    [     2              1                 6               1        ]

    Shape: N x 4, where N is the total number of cells in the grid.

    The function turns the achiral cells (state 0) into chiral cells (state 1 or 2)
    with a probability p_chiral, regardless of the neighborhood composition.
    p_chiral is modulared by the parameter epsilon, which represents the strength
    of the stochastic effect.

    It returns an array of new states for each cell in the grid.
    """
    new_states = []
    prob = epsilon * p_chiral

    for state, number_of_zeros, number_of_ones, number_of_twos in neighborhood:
        if state == 0:

            if dist_type == 'uniform':
                rand = np.random.rand()

            elif dist_type == 'normal':
                rand = np.random.normal(0, 1) 

            elif dist_type == 'lognormal':
                rand = np.random.lognormal(0, 1)

            if rand < prob:
                new_states.append(1 if np.random.rand() < 0.5 else 2)  # 50% chance to become 1 or 2
            else:
                new_states.append(state)
        else:
            new_states.append(state)

    return np.array(new_states)

def diffusion(epsilon, p_copy, neighborhood, dist_type='uniform'):
    """
    Reads a neighborhood array with the following structure:

    Cell state | Number of zeros | Number of ones | Number of twos
    [     0              2                 5               1        ]
    [     1              3                 4               1        ]
    [                            ...                                ]
    [     2              1                 6               1        ]

    Shape: N x 4, where N is the total number of cells in the grid.

    The function allows a cell to copy one of its neighbors' states with a
    probability p_copy, regardless of the neighborhood composition.
    p_copy is modulared by the parameter epsilon, which represents the strength
    of the stochastic effect.

    It returns an array of new states for each cell in the grid.
    """
    new_states = []
    prob = epsilon * p_copy

    for state, number_of_zeros, number_of_ones, number_of_twos in neighborhood:

        if dist_type == 'uniform':
            rand = np.random.rand()

        elif dist_type == 'normal':
            rand = np.random.normal(0, 1)

        elif dist_type == 'lognormal':
            rand = np.random.lognormal(0, 1)

        if rand < prob:
            neighbors_states = [0]*number_of_zeros + [1]*number_of_ones + [2]*number_of_twos
            new_states.append(np.random.choice(neighbors_states))  # also uses uniform distribution but can be changed
        else:
            new_states.append(state)

    return np.array(new_states)