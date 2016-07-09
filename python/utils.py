#
#                                                                            */
#                               utils.py                                     */
#                                                                            */
#                         Espaces Imaginaires sound project                  */
#                                                                            */
# -------------------------------------------------------------------------- */

import os
import sys
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

def list2str(lst):
    lst = [lst] if type(lst)==int else lst
    lst_str = ''
    for l in range(len(lst)-2): lst_str += (str(lst[l])+'_')
    lst_str += str(lst[len(lst)-1])
    return lst_str

def open_osx(*args):
    """ """
    if sys.platform=='darwin':
        for arg in args:
            os.system("open %s" % arg)
    else:
        raise StandardError("open_osx only implemente for mac osx")

def set_folders(kind):
    """ """

    results_path = os.path.join(ESPACES_PROJECT,'data','results',date.today().isoformat())

    folders = {}

    folders['green_fn_im'] = os.path.join(results_path,'green_fn',kind,'images')
    folders['green_fn_au'] = os.path.join(results_path,'green_fn',kind,'audio')

    folders['cv_im'] = os.path.join(results_path,'conv_result',kind,'images')
    folders['cv_au'] = os.path.join(results_path,'conv_result',kind,'audio')

    folders['ev_im'] = os.path.join(results_path,'eigenvalues',kind)
    folders['ev_au'] = os.path.join(results_path,'eigenvalues',kind)

    folders['es_im'] = os.path.join(results_path,'emitted_sound','images')
    folders['es_au'] = os.path.join(results_path,'emitted_sound','audio')


    for key in folders:
        if not os.path.exists(folders[key]):
            os.makedirs(folders[key])

    return folders

def set_paths(type,kind,j_max,F,duration,c,nu):
    """ """

    F = list2str(F)

    if type=='ev':
        name  = 'eigen_vals_%s_j_max_%s_freq_prop_%s_c_%s_nu_%s_sec_%1.1f' % (kind,j_max,F,c,nu,duration)
        im_folder = set_folders(kind)['ev_im']
        au_folder = set_folders(kind)['ev_au']
    if type=='green_fn':
        name  = 'green_fn_%s_j_max_%s_freq_prop_%s_c_%s_nu_%s_sec_%1.1f' % (kind,j_max,F,c,nu,duration)
        im_folder = set_folders(kind)['green_fn_im']
        au_folder = set_folders(kind)['green_fn_au']
    elif type=='cv':
        name = 'conv_%s_j_max_%s_freq_prop_%s_c_%s_nu_%s_sec_%1.1f' % (kind,j_max,F,c,nu,duration)
        im_folder = set_folders(kind)['cv_im']
        au_folder = set_folders(kind)['cv_au']
    elif type=='es':
        name = 'emitted_sound'
        im_folder = set_folders(kind)['es_im']
        au_folder = set_folders(kind)['es_au']
    return os.path.join(im_folder,name+'.png'), os.path.join(au_folder,name+'.wav')