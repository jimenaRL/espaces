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

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def list2str(lst):
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

def set_folders():
    """ """

    results_path = os.path.join(ESPACES_PROJECT,'data','results',date.today().isoformat())

    folders = {}

    folders['green_fn_im'] = os.path.join(results_path,'green_fn','images')
    folders['green_fn_au'] = os.path.join(results_path,'green_fn','audio')

    folders['cv_im'] = os.path.join(results_path,'conv_result','images')
    folders['cv_au'] = os.path.join(results_path,'conv_result','audio')

    folders['es_im'] = os.path.join(results_path,'emitted_sound','images')
    folders['es_au'] = os.path.join(results_path,'emitted_sound','audio')

    for key in folders:
        if not os.path.exists(folders[key]):
            os.makedirs(folders[key])

    return folders

def set_paths(type,j_max=None,L=None,duration=None):
    """ """

    L = list2str(L)

    if type=='green_fn':
        name  = 'green_function_from_eigen_vals_j_max_%s_torus_length_%s_%1.1f_sec' % (j_max,L,duration)
        im_folder = set_folders()['green_fn_im']
        au_folder = set_folders()['green_fn_au']
    elif type=='cv':
        name = 'conv_j_max_%s_torus_length_%s_%1.1f_sec' % (j_max,L,duration)
        im_folder = set_folders()['cv_im']
        au_folder = set_folders()['cv_au']
    elif type=='es':
        name = 'emitted_sound'
        im_folder = set_folders()['es_im']
        au_folder = set_folders()['es_au']
    return os.path.join(im_folder,name+'.png'), os.path.join(au_folder,name+'.wav')