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

def spontaneusNeutrality(epsilon, p_neutral, neighborhood):
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
            rand = np.random.rand()  # uses uniform distribution (change for lognormal?)
            if rand < prob:
                new_states.append(0)
            else:
                new_states.append(state)
        else:
            new_states.append(state)

    return np.array(new_states)

def spontaneousChirality(epsilon, p_chiral, neighborhood):
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
            rand = np.random.rand()  # uses uniform distribution
            if rand < prob:
                new_states.append(1 if np.random.rand() < 0.5 else 2)  # 50% chance to become 1 or 2
            else:
                new_states.append(state)
        else:
            new_states.append(state)

    return np.array(new_states)

def diffusion(epsilon, p_copy, neighborhood):
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
        rand = np.random.rand()  # uses uniform distribution
        if rand < prob:
            neighbors_states = [0]*number_of_zeros + [1]*number_of_ones + [2]*number_of_twos
            new_states.append(np.random.choice(neighbors_states))  # also uses uniform distribution but can be changed
        else:
            new_states.append(state)

    return np.array(new_states)

# Original implementation ------------------------------------

# ###########################
# # Deterministic Rules
# ###########################

# def autocatalysis(neighborhood):
#     """
#     Reads a neighborhood array with the following structure:

#     Cell state | Number of zeros | Number of ones | Number of twos
#     [     0              2                 5               1        ]
#     [     1              3                 4               1        ]
#     [                            ...                                ]
#     [     2              1                 6               1        ]

#     Shape: N x 4, where N is the total number of cells in the grid.

#     The function turns the achiral cells (state 0) into chiral cells (state 1 or 2)
#     if the number of chiral neighbors (state 1 and state 2) is greater than the number
#     of achiral neighbors (state 0). If the number of achiral neighbors is equal to the
#     number of chiral neighbors, the cell state remains unchanged.

#     It returns an array of new states for each cell in the grid.
#     """
#     # initialize new state
#     new_states = []

#     # iterate for each row 
#     for state in neighborhood:
#         state = neighborhood[state][0]
#         number_of_zeros = neighborhood[state][1]
#         number_of_ones = neighborhood[state][2]
#         number_of_twos = neighborhood[state][3]

#         if state==0 and number_of_zeros<number_of_ones+number_of_twos:
#             if number_of_ones>number_of_twos:
#                 new_states.append(1)
#             elif number_of_twos>number_of_ones:
#                 new_states.append(2)
#         else:
#             new_states.append(0)

#     #turn list into array
#     new_states = np.array(new_states)

#     return new_states
    
# def mutualInhibition(neighborhood):
#     """
#     Reads a neighborhood array with the following structure:

#     Cell state | Number of zeros | Number of ones | Number of twos
#     [     0              2                 5               1        ]
#     [     1              3                 4               1        ]
#     [                            ...                                ]
#     [     2              1                 6               1        ]

#     Shape: N x 4, where N is the total number of cells in the grid.

#     The funcion turns the chiral cells (state 1 or 2) into achiral cells (state 0)
#     if the neighborhood contains a majority of cells with the opposite chirality.
#     If the number of cells with the opposite chirality is equal to the number of cells
#     with the same chirality, the cell state remains unchanged.

#     It returns an array of new states for each cell in the grid.
#     """
#     # initialize new state
#     new_states = []

#     # iterate for each row 
#     for state in neighborhood:
#         state = neighborhood[state][0]
#         number_of_zeros = neighborhood[state][1]
#         number_of_ones = neighborhood[state][2]
#         number_of_twos = neighborhood[state][3]

#         if state==1 and (number_of_zeros+number_of_ones)<number_of_twos:
#             new_states.append(0)
#         if state==2 and (number_of_zeros+number_of_twos)<number_of_ones:
#             new_states.append(0)
#         else:
#             new_states.append(state)

#     #turn list into array
#     new_states = np.array(new_states)

#     return new_states

# ########################
# # Stochastic Rules
# ########################

# def spontaneusNeutrality(epsilon, p_neutral, neighborhood):
#     """
#     Reads a neighborhood array with the following structure:

#     Cell state | Number of zeros | Number of ones | Number of twos
#     [     0              2                 5               1        ]
#     [     1              3                 4               1        ]
#     [                            ...                                ]
#     [     2              1                 6               1        ]

#     Shape: N x 4, where N is the total number of cells in the grid.

#     The function turns the chiral cells (state 1 or 2) into achiral cells (state 0)
#     with a probability p_neutral, regardless of the neighborhood composition.
#     p_neutral is modulared by the parameter epsilon, which represents the strength
#     of the stochastic effect.

#     It returns an array of new states for each cell in the grid.
#     """
#     # initialize new state
#     new_states = []

#     # Compute probability of state change
#     prob = epsilon * p_neutral

#     # iterate for each row 
#     for state in neighborhood:
#         state = neighborhood[state][0]
#         number_of_zeros = neighborhood[state][1]
#         number_of_ones = neighborhood[state][2]
#         number_of_twos = neighborhood[state][3]

#         if state in [1, 2]:
#             # Generate a random number between 0 and 1
#             rand = np.random.rand() #uses uniform distribution (change for lognormal?)
#             # If the random number is less than the probability, change the state to 0
#             if rand < prob:
#                 new_states.append(0)
#         else:
#             new_states.append(state)

#     # turn list into array
#     new_states = np.array(new_states)

#     return new_states

# def spontaneousChirality(epsilon, p_chiral, neighborhood):
#     """
#     Reads a neighborhood array with the following structure:

#     Cell state | Number of zeros | Number of ones | Number of twos
#     [     0              2                 5               1        ]
#     [     1              3                 4               1        ]
#     [                            ...                                ]
#     [     2              1                 6               1        ]

#     Shape: N x 4, where N is the total number of cells in the grid.

#     The function turns the achiral cells (state 0) into chiral cells (state 1 or 2)
#     with a probability p_chiral, regardless of the neighborhood composition.
#     p_chiral is modulared by the parameter epsilon, which represents the strength
#     of the stochastic effect.

#     It returns an array of new states for each cell in the grid.
#     """
#     # initialize new state
#     new_states = []

#     # Compute probability of state change
#     prob = epsilon * p_chiral

#     # iterate for each row 
#     for state in neighborhood:
#         state = neighborhood[state][0]
#         number_of_zeros = neighborhood[state][1]
#         number_of_ones = neighborhood[state][2]
#         number_of_twos = neighborhood[state][3]

#         if state==0:
#             # Generate a random number between 0 and 1
#             rand = np.random.rand() #uses uniform distribution
#             # If the random number is less than the probability, change the state to 1 or 2
#             if rand < prob:
#                 if np.random.rand() < 0.5: #50% chance to become 1 or 2
#                     new_states.append(1)
#                 else:
#                     new_states.append(2)
#         else:
#             new_states.append(state)

#     # turn list into array
#     new_states = np.array(new_states)
#     return new_states

# def diffusion(epsilon, p_copy, neighborhood):
#     """
#     Reads a neighborhood array with the following structure:

#     Cell state | Number of zeros | Number of ones | Number of twos
#     [     0              2                 5               1        ]
#     [     1              3                 4               1        ]
#     [                            ...                                ]
#     [     2              1                 6               1        ]

#     Shape: N x 4, where N is the total number of cells in the grid.

#     The function allows a cell to copy one of its neighbors' states with a
#     probability p_copy, regardless of the neighborhood composition.
#     p_copy is modulared by the parameter epsilon, which represents the strength
#     of the stochastic effect.

#     It returns an array of new states for each cell in the grid.
#     """
#     # initialize new state
#     new_states = []

#     # Compute probability of state change
#     prob = epsilon * p_copy

#     # iterate for each row 
#     for state in neighborhood: 
#         state = neighborhood[state][0]
#         number_of_zeros = neighborhood[state][1]
#         number_of_ones = neighborhood[state][2]
#         number_of_twos = neighborhood[state][3]

#         # Generate a random number between 0 and 1
#         rand = np.random.rand() #uses uniform distribution
#         # If the random number is less than the probability, copy a neighbor's state
#         if rand < prob:
#             neighbors_states = [0]*number_of_zeros + [1]*number_of_ones + [2]*number_of_twos
#             new_state = np.random.choice(neighbors_states) #also uses uniform distribution but can be changed
#             new_states.append(new_state)
#         else:
#             new_states.append(state)

#     # turn list into array
#     new_states = np.array(new_states)
#     return new_states