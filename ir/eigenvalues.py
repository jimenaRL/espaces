#
#                                                                            */
#                        eigenvalues.py                                      */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

import os

import numpy as np
import itertools

from utils import cartesian, ESPACES_PROJECT


def espace_product(eA_eigen_vals,eB_eigen_vals):
    """ Returns a list containing eigen-values and their multiciplies of the Laplacien in the E_A X E_B manifold. """


    eA_ev_factor = [ v['value'] for v in eA_eigen_vals]
    eB_ev_factor = [ v['value'] for v in eB_eigen_vals]

    eA_m_factor = [ v['multiplicity'] for v in eA_eigen_vals]
    eB_m_factor = [ v['multiplicity'] for v in eB_eigen_vals]

    ev_cartesian_prod = cartesian([eA_ev_factor,eB_ev_factor])
    m_cartesian_prod = cartesian([eA_m_factor,eA_m_factor])

    values         = [np.sum(ev_cartesian_prod[k]) for k in range(len(ev_cartesian_prod))]
    multiplicities = [np.prod(m_cartesian_prod[k]) for k in range(len(m_cartesian_prod))]


    eigen_vals = [ {'value' : values[k], 
                    'multiplicity' : multiplicities[k] }
                     for k in range(len(values))
                  ]

    return eigen_vals



def s2e1(F=[0.1,0.1], c=3.4e2, j_max=1):
    """ Returns a list containing eigen-values of the Laplacien in the S^2 X E^1 manifold. 
        F     : [c/r, c/l] where where r is the 2-sphere radious and l the length of the 1-torus
        j_max : [int] set index of eigen-values to compute as {-j_max, ..., j_max} in each direction
    """

    assert(len(F)==2)
    s2_eigen_vals = sphere_2(F=F[0], c=c,j_max=int(np.sqrt(j_max)))
    e1_eigen_vals = n_torus(F=[F[1]], c=c, j_max=int(np.sqrt(j_max)))


    return espace_product(s2_eigen_vals,e1_eigen_vals)


def h2e1(F=[0.1], c=3.4e2, j_max=1):
    """ Returns a list containing eigen-values of the Laplacien in the H^2 X E^1 manifold. 
        F     : [c/l] where where l is the length of the 1-torus
        j_max : [int] set index of eigen-values to compute as {-j_max, ..., j_max} in each direction
    """

    assert(len(F)==1)
    h2_eigen_vals = hyperbolic(j_max=int(np.sqrt(j_max)))
    e1_eigen_vals = n_torus(F=F, c=c, j_max=int(np.sqrt(j_max)))

    return espace_product(h2_eigen_vals,e1_eigen_vals)


def hyperbolic(j_max=1):
    """ from http://homepages.lboro.ac.uk/~maas3/publications/eigdata/datafile.html """

    name = 'eig-maxsymm-24.txt'
    # name = 'eig-maxsymm-48.txt'
    # name = 'eig-octagon.txt'
    # name = 'eig-pol-1-0-500.dat'

    path = os.path.join(ESPACES_PROJECT,'dev','eigenvalues',name)
    with open(path,'r') as f: 
        l = [float(i[:-1]) for i in f.readlines()]

    eigen_vals =  [{'value'        : l[k],
                    'multiplicity' : 1
                    }
                    for k in range(0,j_max)
                 ]

    return eigen_vals


def n_torus(F=[0.1], c=3.4e2, j_max=1):
    """ Returns a list containing eigen-values of the Laplacien in the n-torus manifold. 
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

def sphere_3(F=0.1, c=3.4e2,j_max=1):
    """ Returns a list containing eigen-values of the Laplacien in the 3-sphere manifold. 
        c     : [float] sound velocity
        F     : c/r where r is the 3-sphere radious
        j_max : [int] number de eigenvalue
    """
    eigen_vals =  [{'value'        : 2*np.pi*(k)*(k+2)*F/c,
                    'multiplicity' : int((k+1)*(k+2)*(k+3)/6)
                    }
                    for k in range(1,j_max+1)
                 ]

    return eigen_vals

def sphere_2(F=0.1, c=3.4e2,j_max=1):
    """ Returns a list containing eigen-values of the Laplacien in the 2-sphere manifold. 
        c     : [float] sound velocity
        F     : c/l where l is the 3-sphere radious
        j_max : [int] number de eigenvalue
    """
    eigen_vals =  [{'value'        : 2*np.pi*(k)*(k+1)*F/c,
                    'multiplicity' : int((k+1)*(k+2)/2)
                    }
                    for k in range(1,j_max+1)
                 ]

    return eigen_vals