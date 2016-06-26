#
#                                                                            */
#                        eigenvalues.py                                      */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

import numpy as np
import itertools

def _cartesian(arrays,  out=None):
    """
    Generate a cartesian product of input arrays.
    Parameters
    ----------
    arrays : list of array-like
        1-D arrays to form the cartesian product of.
    out : ndarray
        Array to place the cartesian product in.
    Returns
    -------
    out : ndarray
        2-D array of shape (M,  len(arrays)) containing cartesian products
        formed of input arrays.
    """

    arrays = [np.asarray(x) for x in arrays]
    dtype = arrays[0].dtype

    n = np.prod([x.size for x in arrays])
    if out is None:
        out = np.zeros([n,  len(arrays)],  dtype=dtype)

    m = n / arrays[0].size
    out[:, 0] = np.repeat(arrays[0],  m)
    if arrays[1:]:
        _cartesian(arrays[1:],  out=out[0:m, 1:])
        for j in xrange(1,  arrays[0].size):
            out[j*m:(j+1)*m, 1:] = out[0:m, 1:]
    return out

def n_torus(L=[1], j_max=1):
    """ Returns the eigen-values of the n-torus in a list. 

        c     : [float] sound velocity
        L     : [float] list of n-torus lengths
        j_max : [int] set index of eigen-values to compute as {-j_max, ..., j_max} in each direction
    """

    n = len(L)
    k_list = [ [np.square(2*np.pi*j/L[index]) for j in range(0, j_max)] for index in range(n) ]
    eigen_vals = _cartesian(k_list)
    sym = True

    return eigen_vals, sym

def picard(c=340, L=[1], j_max=1):
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
