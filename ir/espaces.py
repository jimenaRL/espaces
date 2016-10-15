#
#                                                                            */
#                         espaces.py                                         */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os, sys, time
import itertools, copy

# from joblib import Parallel, delayed

import numpy as np

from utils import set_paths, open_osx
from ir import get_ir


ESPACES_PROJECT = os.environ['ESPACES_PROJECT']


def espaces(ir_params):

    # compute ir and eigenvalues
    ir_signal, eigen_vals = get_ir(ir_params)

    # to do rigth
    ir_params_ = copy.deepcopy(ir_params)
    path_args = ir_params_['ev_params']
    path_args.update({ 'duration' : ir_params_['duration'],
                       'nu'       : ir_params_['nu'] })


    # save eigenvalues
    ev_im_path, _  = set_paths('ev',**path_args)
    l = [item['value']*item['multiplicity'] for item in eigen_vals]
    with open(ev_im_path[:-3]+'dat','w') as f:
        f.writelines( ['%1.20f\n' % i for i in l])

    # save ir
    ir_im_path, ir_au_path = set_paths('green_fn',**path_args)
    ir_signal.write(ir_au_path)
    ir_signal.save_image(ir_im_path, title='green_fn_0')


def compute_s2e1():

    ir_params = {  'ev_params'      : {'space':'s2e1', 'c':3.4e2, 'j_max':100},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e3,
                   'sampling_rate'  : 8000,
                }

    f1 = np.linspace(0.1,5.,10)
    f2 = np.linspace(5.,10.,10)

    for F in itertools.product(f1,f2):
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = F
        espaces(ir_params)

def compute_h2e1():

    ir_params = {  'ev_params'      : {'space':'h2e1', 'c':3.4e2, 'j_max':1000},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e3,
                   'sampling_rate'  : 8000,
                }

    f1 = np.linspace(10,100,10)
    for F in f1:
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = [F]
        espaces(ir_params)

def compute_e3():

    ir_params = {  'ev_params'      : {'space':'e3', 'c':3.4e2, 'j_max':25},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5,
                   'sampling_rate'  : 8000,
                }

    space = 'n_torus'

    for F in ( [100,100,100], [50,50,50], [100,50,75]):
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = F
        espaces(ir_params)
 

    espaces(PATH_ES,F,j_max,duration,space,c,nu)


def compute_s3():

    ir_params = {  'ev_params'      : {'space':'s3', 'c':3.4e2, 'j_max':200},
                   'duration'       : 15.0,
                   'nu'             : 1.7e-5 * .5e3,
                   'sampling_rate'  : 8000,
                }

    f1 = np.linspace(0.5,0.5,1)
    for F in f1:
        print "\n--------%s--------\n" % ir_params
        ir_params['ev_params']['F'] = [F]
        espaces(ir_params)


if __name__:

    compute_e3()
    compute_s3()
    compute_s2e1()
    compute_h2e1()


