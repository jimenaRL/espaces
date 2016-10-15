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

def open_osx(*args):
    """ """
    if sys.platform=='darwin':
        for arg in args:
            os.system("open %s" % arg)
    else:
        raise StandardError("open_osx only implemente for mac osx")

def set_folders(space):
    """ """

    results_path = os.path.join(ESPACES_PROJECT,'data','results',date.today().isoformat())

    folders = {}

    folders['green_fn_im'] = os.path.join(results_path,space,'green_fn','images')
    folders['green_fn_au'] = os.path.join(results_path,space,'green_fn','audio')

    folders['cv_im'] = os.path.join(results_path,space,'conv_result','images')
    folders['cv_au'] = os.path.join(results_path,space,'conv_result','audio')

    folders['ev_im'] = os.path.join(results_path,space,'eigenvalues')
    folders['ev_au'] = os.path.join(results_path,space,'eigenvalues')

    folders['es_im'] = os.path.join(results_path,'emitted_sound','images')
    folders['es_au'] = os.path.join(results_path,'emitted_sound','audio')


    for key in folders:
        if not os.path.exists(folders[key]):
            os.makedirs(folders[key])

    return folders

def set_paths(type,space,j_max,F,duration,c,nu):
    """ """

    if type=='ev':
        name  = 'eigen_vals_%s_j_max_%s_freq_prop_%s_c_%s_nu_%s_sec_%1.1f' % (space,j_max,F,c,nu,duration)
        im_folder = set_folders(space)['ev_im']
        au_folder = set_folders(space)['ev_au']
    if type=='green_fn':
        name  = 'green_fn_%s_j_max_%s_freq_prop_%s_c_%s_nu_%s_sec_%1.1f' % (space,j_max,F,c,nu,duration)
        im_folder = set_folders(space)['green_fn_im']
        au_folder = set_folders(space)['green_fn_au']
    elif type=='cv':
        name = 'conv_%s_j_max_%s_freq_prop_%s_c_%s_nu_%s_sec_%1.1f' % (space,j_max,F,c,nu,duration)
        im_folder = set_folders(space)['cv_im']
        au_folder = set_folders(space)['cv_au']
    elif type=='es':
        name = 'emitted_sound'
        im_folder = set_folders(space)['es_im']
        au_folder = set_folders(space)['es_au']
    return os.path.join(im_folder,name+'.png'), os.path.join(au_folder,name+'.wav')