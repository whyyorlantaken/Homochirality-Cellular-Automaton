"""
 Cell state | Number of zeros | Number of ones | Number of twos
[     0              2                 5               1        ]
[     1              3                 4               1        ]
[                            ...                                ]
[     2              1                 6               1        ]
"""

import numpy as np

def getMooreCounts(array, boundaries = 'periodic'):
    """
    Compute counts of each state in the Moore neighborhood for each cell in the input 2D array.

    Parameters
    ----------
    array : 2D numpy array
        Input grid where each cell contains an integer state.
    boundaries : str, optional
        Type of boundary conditions to apply. Currently supports 'periodic' (default).

    Returns
    -------
    numpy.ndarray
        A 2D array of shape (N, n_states + 1) where N is the total number of cells in the grid and n_states is the maximum state value in the input array. The first column contains the original cell states, and the subsequent columns contain the counts of each state in the Moore neighborhood.
    """
    n_states = np.max(array) + 1

    N            = array.size
    result       = np.zeros((N, n_states + 1), dtype=int)
    result[:, 0] = array.ravel()

    if boundaries == 'periodic':

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue

                shifted = np.roll(np.roll(array, dx, axis=0), dy, axis=1)
                
                for s in range(n_states):
                    result[:, s + 1] += (shifted == s).ravel()

    return result 



