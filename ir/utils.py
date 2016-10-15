#
#                                                                            */
#                               utils.py                                     */
#                                                                            */
#                         Espaces Imaginaires sound project                  */
#                                                                            */
# -------------------------------------------------------------------------- */

import os, sys
from datetime import date

import numpy as np

ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def cartesian(arrays,  out=None):
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
        cartesian(arrays[1:],  out=out[0:m, 1:])
        for j in xrange(1,  arrays[0].size):
            out[j*m:(j+1)*m, 1:] = out[0:m, 1:]
    return out

def set_folders(space):
    """ """

    results_path = os.path.join(ESPACES_PROJECT,'data','results',date.today().isoformat())

    folders = {}

    folders['green_fn_im'] = os.path.join(results_path,space,'green_fn','images')
    folders['green_fn_au'] = os.path.join(results_path,space,'green_fn','audio')
    folders['ev'] = os.path.join(results_path,space,'eigenvalues')

    for folder in folders.values():
        if not os.path.exists(folder):
            os.makedirs(folder)

    return folders

def get_paths(space,j_max,F,duration,c,nu):
    """ """
    folders = set_folders(space)
    name  = '%s_j_max_%i_freq_prop_%s_c_%1.1f_nu_%1.5f_dur_%1.1f' % (space,j_max,F,c,nu,duration)
    au_path = os.path.join(folders['green_fn_au'],name+'.wav')
    ev_path = os.path.join(folders['ev'],name+'.tsv')
    im_path = os.path.join(folders['green_fn_im'],name+'.png')
    return au_path, ev_path, im_path

