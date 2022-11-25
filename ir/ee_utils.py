#
#                                                                            */
#                               utils.py                                     */
#                                                                            */
#                         Espaces Imaginaires sound project                  */
#                                                                            */
# -------------------------------------------------------------------------- */

import os
from datetime import date

import numpy as np

ESPACES_PROJECT = os.path.realpath(os.path.join(os.path.abspath(__file__),
                                                os.pardir,
                                                os.pardir,
                                                os.pardir))

print("ESPACES_PROJECT = %s" % ESPACES_PROJECT)


def cartesian(arrays, out=None):
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
        out = np.zeros([n, len(arrays)], dtype=dtype)

    m = n // arrays[0].size
    out[:, 0] = np.repeat(arrays[0], m)
    if arrays[1:]:
        cartesian(arrays[1:], out=out[0:m, 1:])
        for j in range(1, arrays[0].size):
            out[j * m:(j + 1) * m, 1:] = out[0:m, 1:]
    return out


def set_folders(space, simple_paths=False):

    folders = {}

    if simple_paths:
        results_path = os.path.join(ESPACES_PROJECT, 'data')
        folders['audio'] = os.path.join(results_path, space)

    else:
        results_path = os.path.join(ESPACES_PROJECT, 'data', 'dates',
                                    date.today().isoformat())
        folders['evs'] = os.path.join(results_path, space, 'eigenvalues')
        folders['image'] = os.path.join(
            results_path, space, 'green_fn', 'images')
        folders['audio'] = os.path.join(
            results_path, space, 'green_fn', 'audio')

    for folder in folders.values():
        if not os.path.exists(folder):
            os.makedirs(folder)

    return folders


def get_paths(**kwargs):
    """ """

    kwargs['F'] = '_'.join([str(f) for f in kwargs.get('F', [])])
    name = '_'.join([f"{k}_{v}" for k, v in kwargs.items()])
    folders = set_folders(kwargs.get('space', 'unknown'))

    paths = {}

    paths['audio'] = os.path.join(folders['audio'], name + '.wav')

    if 'evs' in folders:
        paths['evs'] = os.path.join(folders['evs'], name + '.tsv')
    if 'image' in folders:
        paths['image'] = os.path.join(folders['image'], name + '.png')

    return paths
