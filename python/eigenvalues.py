#
#                                                                            */
#                        eigenvalues.py                                      */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

import numpy as np
import itertools

from utils import cartesian


def n_torus(F=[440], c=3.4e2, j_max=1):
    """ Returns a list containing eigen-values of the Laplacien in the N-TORUS manifold. 
        F     : [c/l1, c/l2, ...] where l1, l2, ... are the n-torus lengths
        j_max : [int] set index of eigen-values to compute as {-j_max, ..., j_max} in each direction
    """

    n = len(F)
    k_list = [ [np.square(2*np.pi*j*F[index]/c) for j in range(1, j_max+1)] for index in range(n) ]
    cartesian_prod = cartesian(k_list)
    values = [np.sum(cartesian_prod[k]) for k in range(len(cartesian_prod))]

    eigen_vals = [ {'value' : values[k], 'multiplicity' : 2**(n-1) }
                  for k in range(len(values))
                  ]

    return eigen_vals

def sphere_3(F=440, c=3.4e2,j_max=1):
    """ Returns a list containing eigen-values of the Laplacien in the 3_sphere manifold. 
        c     : [float] sound velocity
        F     : c/l where l is the 3-sphere radious
        j_max : [int] number de eigenvalue
    """
    eigen_vals =  [{'value'        : 2*np.pi*(k)*(k+2)*F/c,
                    'multiplicity' : int((k+1)*(k+2)*(k+3)/6)
                    }
                    for k in range(1,j_max+1)
                 ]

    return eigen_vals

def picard(c=3.4e2, L=[1], j_max=1):
    """ from http://arxiv.org/pdf/math-ph/0305048v2.pdf """

    l = [8.55525104,  6.62211934,
    11.10856737, 10.18079978,
    12.86991062, 12.11527484, 12.11527484,
    14.07966049, 12.87936900,
    15.34827764, 14.14833073,
    15.89184204, 14.95244267, 14.95244267,
    17.33640443, 16.20759420,
    17.45131992, 17.45131992, 16.99496892, 16.99496892,
    17.77664065, 17.86305643, 17.86305643,
    19.06739052, 18.24391070,
    19.22290266, 18.83298996,
    19.41119126, 19.43054310, 19.43054310,
    20.00754583, 20.30030720, 20.30030720,
    20.70798880, 20.70798880, 20.60686743,
    20.81526852, 21.37966055, 21.37966055,
    21.42887079, 21.44245892,
    22.12230276, 21.83248972, 21.83248972,
    22.63055256, 22.58475297, 22.58475297,
    22.96230105, 22.96230105, 22.85429195,
    23.49617692, 23.49768305, 23.49768305,
    23.52784503, 23.84275866,
    23.88978413, 23.88978413, 23.89515755, 23.89515755,
    24.34601664, 24.42133829, 24.42133829,
    24.57501426, 25.03278076, 25.03278076,
    24.70045917, 25.42905483,
    25.47067539, 25.77588591, 25.77588591,
    25.50724616, 26.03903968,
    25.72392169, 25.72392]

    eigen_vals =  np.array(l).reshape(len(l),1)
    sym = False

    return eigen_vals, sym
