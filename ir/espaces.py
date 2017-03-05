#
#                                                                            */
#                         espaces.py                                         */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os, sys, csv, time
import itertools, copy

# from joblib import Parallel, delayed

import numpy as np

from ee_utils import get_paths, cartesian
from impulse_reponse import get_ir

class EspaceClient(object):

    def __init__(self):
        pass

    def handle_request(self,ir_params):
        saved_audio_path = espaces(ir_params)
        return {'saved_audio_path':saved_audio_path}


def espaces(ir_params):

    # set save paths results
    path_kwargs = copy.deepcopy(ir_params['ev_params'])
    path_kwargs.update({'duration' : ir_params['duration'],
                        'nu'       : ir_params['nu'] })
    paths  = get_paths(**path_kwargs)

    au_path = paths.get('audio')

    if not os.path.exists(au_path):

        # compute ir and eigenvalues
        ir_signal, eigen_vals = get_ir(ir_params)
        # save ir audio
        ir_signal.write(au_path)
        print "Audio file saved at %s." % au_path

        # save eigenvalues
        if 'evs' in paths:
            with open(paths['evs'],'w') as f:
                writer = csv.writer(f,delimiter='\t')
                writer.writerows([ (item['value'],item['multiplicity']) for item in eigen_vals])

        # save ir image
        if 'image' in paths:
            ir_signal.save_image(paths['image'], title='impulse response')

    else:
        print "Audio file found at %s." % au_path

    return au_path



