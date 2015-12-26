#
#                                                                            */
#                        eigenvalues.py                                      */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

import numpy as np

def one_torus(c,L,j_max):
    """ Returns the eigen-values of a 1-torus in a list. 

        c     : [float] sound velocity
        L     : [float] length of the torus
        j_max : [int] set index of eigen-values to compute as {-j_max,...,j_max}
    """
    return [ np.square(2*np.pi*j/L) for j in range(-j_max,j_max+1) ]


def get_eigenvalues(identifier, kwargs=None): 
    """ TO DO """