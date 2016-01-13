#
#                                                                            */
#                        eigenvalues.py                                      */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

import numpy as np
import itertools

def one_torus(c,L,j_max):
    """ Returns the eigen-values of a 1-torus in a list. 

        c     : [float] sound velocity
        L     : [float] length of the torus
        j_max : [int] set index of eigen-values to compute as {-j_max,...,j_max}
    """
    return [ np.square(2*np.pi*j/L) for j in range(-j_max,j_max+1) ]

def two_torus(c=340,L=[1,2],j_max=[1,1]):
    """ Returns the eigen-values of the n-torus in a list. 

        c     : [float] sound velocity
        L     : [float] list of 2-torus lengths (must be of size 2)
        j_max : [list of int] set list of index of eigen-values to compute as {-j_k_max,...,j_k_max} in each direction
        n     : torus dimension
    """
    if not len(L)==2:
        raise ValueError("Size of L must be 2, found %i" % len(L))
    else:
        L = np.array(L,dtype='f8')
    if not len(j_max)==2:
        raise ValueError("Size of j_max must be 2, found %i" % len(j_max))
    else:
        j_max = np.array(j_max,dtype='i8')
    temp = np.array([[ (j1/L[1]+j0/L[0]) for j1 in range(-j_max[1],j_max[1]+1) ] for j0 in range(-j_max[0],j_max[0]+1) ])
    return np.square(2*np.pi*temp).flatten()
           
def n_torus(c=340,L=[1,2],j_max=1,n=2):
    """ Returns the eigen-values of the n-torus in a list. 

        c     : [float] sound velocity
        L     : [float] list of n-torus lengths (must be of size n)
        j_max : [int] set index of eigen-values to compute as {-j_max,...,j_max} in each direction
        n     : torus dimension
    """

    if not (type(n)==int and n>0):
        raise ValueError("n must be a positive integer, found %s" % str(n))
    if not len(L)==n:
        raise ValueError("Size of L must be %i, found %i" % (n,len(L)))
    else:
        L = np.array(L,dtype='f8')
    if not len(j_max)==n:
        raise ValueError("Size of j_max must be %i, found %i" % (n,len(j_max)))
    else:
        j_max = np.int64(j_max)
    if n==1:
        return one_torus(c,L,j_max)
    elif n==2:
        return two_torus(c,L,j_max)
    else:
        k_list =  [ [2*np.pi*i/L[index] for i in range(-j_max[index],j_max[index]+1)] for index in range(n) ]
        cartesian_prod = itertools.product(*k_list)
        return np.array([l for l in cartesian_prod]).flatten()

def get_eigenvalues(identifier, kwargs=None): 
    """ TO DO """