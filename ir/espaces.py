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

    # compute ir and eigenvalues
    ir_signal, eigen_vals = get_ir(ir_params)

    # save results
    path_kwargs = copy.deepcopy(ir_params['ev_params'])
    path_kwargs.update({'duration' : ir_params['duration'],
                        'nu'       : ir_params['nu'] })

    au_path, ev_path, im_path  = get_paths(**path_kwargs)

    # save eigenvalues
    with open(ev_path,'w') as f:
        writer = csv.writer(f,delimiter='\t')
        writer.writerows([ (item['value'],item['multiplicity']) for item in eigen_vals])

    # save ir
    ir_signal.write(au_path)
    ir_signal.save_image(im_path, title='impulse response')

    print "audio saved at %s" % au_path
    return au_path

def compute_s2e1():

    ir_params = {  'ev_params'      : {'space':'s2e1', 'c':3.4e2, 'j_max':1000},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e3,
                   'sampling_rate'  : 8000,
                }

    f = [0.001,0.01,0.1,1,10,100,1000,10000]
    for F in cartesian([f,f]):
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = F
        espaces(ir_params)

def compute_h2e1():

    ir_params = {  'ev_params'      : {'space':'h2e1', 'c':3.4e2, 'j_max':1000},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e3,
                   'sampling_rate'  : 8000,
                }

    f = [0.001,0.01,0.1,1,10,100,1000,10000]
    for F in f:
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = [F]
        espaces(ir_params)

def compute_e3():

    ir_params = {  'ev_params'      : {'space':'e3', 'c':3.4e2, 'j_max':15},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5,
                   'sampling_rate'  : 8000,
                }

    space = 'n_torus'

    f = [0.001,0.01,0.1,1,10,100]

    # for F in ( [100,100,100], [50,50,50], [100,50,75]):
    for F in cartesian([f,f,f]):
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = F
        espaces(ir_params)

def compute_s3():

    ir_params = {  'ev_params'      : {'space':'s3', 'c':3.4e2, 'j_max':200},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e4,
                   'sampling_rate'  : 8000,
                }

    f1 = [0.001,0.01,0.1,1,10,100]
    for F in f1:
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = [F]
        espaces(ir_params)

# if __name__:

#     compute_s3()
#     compute_h2e1()
#     compute_s2e1()
#     compute_e3()


