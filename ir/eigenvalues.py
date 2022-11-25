#
#                                                                            */
#                        eigenvalues.py                                      */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os
import numpy as np
from ee_utils import cartesian, ESPACES_PROJECT

# from joblib import Memory
# memory = Memory(
#     cachedir=os.path.join(ESPACES_PROJECT, "data", "joblib_cache"),
#     verbose=0)


def _space_product(ea_eigen_vals, eb_eigen_vals):
    """ Returns a list containing the eigen-values and their multiplicities
        of -Delta (negative Laplacien) in the E_A X E_B manifold.

        ex_eigen_vals: [list of dict] eigen-values
                        and their multiplicities of a manifold ex
    """

    ea_ev_factor = [v['value'] for v in ea_eigen_vals]
    eb_ev_factor = [v['value'] for v in eb_eigen_vals]

    ea_m_factor = [v['multiplicity'] for v in ea_eigen_vals]
    eb_m_factor = [v['multiplicity'] for v in eb_eigen_vals]

    ev_cartesian_prod = cartesian([ea_ev_factor, eb_ev_factor])
    m_cartesian_prod = cartesian([ea_m_factor, ea_m_factor])

    values = [
        np.sum(ev_cartesian_prod[k])
        for k in range(len(ev_cartesian_prod))
    ]
    multiplicities = [
        np.prod(m_cartesian_prod[k])
        for k in range(len(m_cartesian_prod))
    ]

    eigen_vals = [{'value': values[k], 'multiplicity': multiplicities[k]}
                  for k in range(len(values))]

    return eigen_vals


def s2e1(F=[0.1, 0.1], c=3.4e2, j_max=1, **unusedkwargs):
    """ Returns a list containing eigen-values of -Delta (negative Laplacien)
    in the S^2 X E^1 manifold.
        c: [float] sound velocity
        F: [c/r, c/l] where r is the 2-sphere radious
           and l the length of the 1-torus
        j_max: [int] set index of eigen-values to compute as
               {-j_max, ..., j_max} in each direction
    """
    s2_eigen_vals = s2(F=[F[0]], c=c, j_max=int(np.sqrt(j_max)))
    e1_eigen_vals = n_torus(F=[F[1]], c=c, j_max=int(np.sqrt(j_max)))

    return _space_product(s2_eigen_vals, e1_eigen_vals)


def h2e1(F=[0.1], c=3.4e2, j_max=1, kind=0, **unusedkwargs):
    """ Returns a list containing eigen-values of -Delta (negative Laplacien)
    in the H^2 X E^1 manifold.
        c: [float] sound velocity
        F: [list] list of length 1 containing c/l,
               where l is the length of the 1-torus
        j_max: [int] set index of eigen-values to compute as
               {-j_max, ..., j_max} in each direction
    """

    def hyperbolic(j_max=1, kind=0):
        """
        From 'An Algorithm for the Computation of Eigenvalues,
        Spectral Zeta Functions,
        and Zeta determinants on hyperbolic surfaces'
        by A. Strohmaier and Ville Uski, arXiv:1110.2150
        http://homepages.lboro.ac.uk/~maas3/publications/eigdata/datafile.html
        """

        kind_index = {
            0: 'eig-maxsymm-24.txt',
            1: 'eig-maxsymm-48.txt',
            2: 'eig-octagon.txt',
            3: 'eig-pol-1-0-500.dat'
        }

        path = os.path.join(
            ESPACES_PROJECT,
            'espaces/ir/data/eigenvalues',
            kind_index[kind])
        with open(path, 'r') as f:
            ll = [float(ii[:-1]) for ii in f.readlines()]

        eigen_vals = [{'value': ll[k], 'multiplicity': 1}
                      for k in range(0, j_max)]

        return eigen_vals

    assert len(F) == 1

    h2_eigen_vals = hyperbolic(j_max=int(np.sqrt(j_max)))
    e1_eigen_vals = n_torus(F=F, c=c, j_max=int(np.sqrt(j_max)))

    return _space_product(h2_eigen_vals, e1_eigen_vals)


def n_torus(F=[0.1], c=3.4e2, j_max=1, **unusedkwargs):
    """ Returns a list containing eigen-values of -Delta (negative Laplacien)
    in the n-torus manifold.
        c    : [float] sound velocity
        F    : [list] list of length n containing c/l1, c/l2, ...;
               where l1, l2, ... are the n-torus lengths
        j_max: [int] set index of eigen-values to compute
               as {-j_max, ..., j_max} in each direction
    """
    n = len(F)
    k_list = [
        [np.square(2 * np.pi * j * F[index] / c) for j in range(1, j_max + 1)]
        for index in range(n)
    ]
    cartesian_prod = cartesian(k_list)
    values = [np.sum(cartesian_prod[k]) for k in range(len(cartesian_prod))]
    # remove repetitive values
    values = set(values)
    # and count for multiplicities
    eigen_vals = [{'value': v, 'multiplicity': 2**(n - 1)} for v in values]

    return eigen_vals


def e3(F=[0.1, 0.1, 0.1], c=3.4e2, j_max=1, **unusedkwargs):
    assert len(F) == 3
    return n_torus(F, c, j_max)


def e1(F=[0.1], c=3.4e2, j_max=1, **unusedkwargs):
    assert len(F) == 1
    return n_torus(F, c, j_max)


def s2(F=[0.1], c=3.4e2, j_max=1):
    """ Returns a list containing eigen-values of -Delta (negative Laplacien)
        in the 2-sphere manifold.
        c    : [float] sound velocity
        F    : [list] list of length 1 containing c/l,
               where l is the 3-sphere radious
        j_max: [int] number de eigenvalue
    """
    eigen_vals = [{'value': (2 * np.pi * F[0] / c)**2 * k * (k + 1),
                   'multiplicity': k + 2} for k in range(1, j_max + 1)]

    return eigen_vals


def s3(F=[0.1], c=3.4e2, j_max=1, **unusedkwargs):
    """ Returns a list containing eigen-values of -Delta (negative Laplacien)
        in the 3-sphere manifold.
        c    : [float] sound velocity
        F    : [list] list of length 1 containing c/r,
               where r is the 3-sphere radious
        j_max: [int] number de eigenvalue
    """
    eigen_vals = [{
        'value': (2 * np.pi * F[0] / c) ** 2 * k * (k + 2),
        'multiplicity': (k + 1)**2
    } for k in range(1, j_max + 1)]

    return eigen_vals


def _check_params(params):

    default_params = {'c': 3.4e2, 'j_max': 1}

    for key in ['space', 'F']:
        if key not in params:
            raise ValueError(
                f'Missing key {key} in eigenvalues params: {params}')

    if params['space'] not in globals():
        raise ValueError(f"Not implemented space: {params['space']}")

    allowed_shapes = {'s2e1': 2, 'h2e1': 1, 'e3': 3, 's3': 1, 'e1': 1}
    if not len(params['F']) == allowed_shapes[params['space']]:
        raise ValueError(
            f'Wrong shape key {key} in eigenvalues params: {params}')

    params.update({
        k: v if k not in params else params[k]
        for k, v in default_params.items()
    })

    return params


# @memory.cache
def get_eigenvalues(ev_params):
    ev_params = _check_params(ev_params)
    eigenvalues_ = globals()[ev_params['space']](**ev_params)
    return eigenvalues_, ev_params
