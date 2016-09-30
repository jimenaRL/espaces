#
#                                                                            */
#                         espaces.py                                         */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os
import sys
import time
import itertools

from joblib import Parallel, delayed

import numpy as np

import matplotlib.pyplot as plt

from utils import set_paths, open_osx
from signals import Signal

from eigenvalues import *
from green_fn import compute_green_fn, compute_green_fn_theano
from convolutions import convolve_signals


ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

PATH_ES = os.path.join(ESPACES_PROJECT,'data','examples','speech_small.wav')


def espaces(path_es=PATH_ES,F=[440],j_max=100,duration=1,kind='n_torus',c=3.4e2,nu=1.7e-5):

    # read and save audio for emitted sound
    sig_es = Signal(path_es,mono=True,normalize=True)
    sampling_rate = sig_es.fs

    start_t = time.time()

    if kind=='n_torus':
        eigen_vals =  n_torus(F,c,j_max)

    elif kind=='sphere_3':
        eigen_vals =  sphere_3(F,c,j_max)

    elif kind=='s2e1':
        eigen_vals =  s2e1(F,c,j_max)

    elif kind=='h2e1':
        eigen_vals =  h2e1(F,c,j_max)

    # print "eigen-values  took %1.2f seconds" % ((time.time()-start_t))

    # compute and save green function
    start_t = time.time()
    green_fn_0 = compute_green_fn(c, nu, eigen_vals, duration, sampling_rate)
    # print "NUMPY green_fn_0 took %1.3f seconds" % ((time.time() -start_t))
    sig_gf = Signal(green_fn_0,fs=sampling_rate,mono=True,normalize=True)


    # compute and save green function
    # start_t = time.time()
    # theano_green_fn_0 = compute_green_fn_theano(c, nu, eigen_vals, duration, sampling_rate)
    # print "THEANO green_fn_0  took %1.3f seconds" % ((time.time() -start_t))

    # convolve emitted sound with the green function and save it
    start_t = time.time()
    sig_cv = convolve_signals(sig_es,sig_gf,kind='ola')
    # print "convolution  took %1f milliseconds" % ((time.time() -start_t)*1e3)

    # save audio and image

    # set saving paths
    if not type(F)==list:
        F = [F]
    gf_im_path, gf_au_path = set_paths('green_fn',kind,j_max,F,duration,c,nu)
    cv_im_path, cv_au_path = set_paths('cv',kind,j_max,F,duration,c,nu)
    es_im_path, es_au_path = set_paths('es',kind,j_max,F,duration,c,nu)
    ev_im_path, _          = set_paths('ev',kind,j_max,F,duration,c,nu)

    # save eigen_values
    l = []
    for item in eigen_vals:
        l.extend( [item['value']]*item['multiplicity'] )
    with open(ev_im_path[:-3]+'dat','w') as f :
        f.writelines( ['%1.20f\n' % i for i in l])

    # if not os.path.exists(es_au_path):
    #     sig_es.write(es_au_path)
    # if not os.path.exists(es_im_path):
    #     sig_es.save_image(es_im_path, title='emitted sound')

    sig_gf.write(gf_au_path)
    # sig_gf.save_image(gf_im_path, title='green_fn_0')

    # sig_cv.write(cv_au_path)
    # sig_cv.save_image(cv_im_path, title='reverberated sound')

    # look at results
    # open_osx(cv_im_path,gf_im_path,ev_im_path)
    # sig_cv.play()
    # sig_gf.play()
    # os.system("osascript -e 'quit app \"Preview\"'")

    # plt.close('all')

# def compute_s2e1():

#     # s2e1
#     j_max = 100
#     duration = .0

#     c = 3.4e2
#     nu = 1.7e-5 * .5e3


#     kind = 's2e1'

#     f1 = np.linspace(0.1,5.,10)
#     f2 = np.linspace(5.,10.,10)

#     for F in itertools.product(f1,f2):
#         print 'kind %s \t F %s' % (kind,str(F))
#         espaces(PATH_ES,F,j_max,duration,kind,c,nu)

# def compute_h2e1():

#     # h2e1

#     c = 3.4e2
#     nu = 1.7e-5 * .5e3

#     j_max = 1000
#     duration = 1.0

#     f1 = np.linspace(10,100,10)
#     kind = 'h2e1'
#     for F in f1:
#         print '%s %s' % (kind,str(F))
#         espaces(PATH_ES,[F],j_max,duration,kind,c,nu)

### OK
# def compute_torus_3():

#     # ceci marche bien  OK 
#     c = 3.4e2
#     nu = 1.7e-5

#     j_max = 25
#     duration  = 2.0

#     kind = 'n_torus'

#     # F = [100,100,100]
#     # F = [50,50,50]
#     # F = [100,50,75]

#     espaces(PATH_ES,F,j_max,duration,kind,c,nu)


def compute_sphere_3():

    # 3-torus
    j_max = 100
    duration = 2.0

    c = 3.4e2
    nu = 1.7e-5 * .5e3

    F = 0.5
    kind = 'sphere_3'

    print 'kind %s \t F %s' % (kind,str(F))
    espaces(PATH_ES,F,j_max,duration,kind,c,nu)


if __name__:

    # compute_torus_3() OK

    compute_sphere_3()
    # compute_s2e1()
    # compute_h2e1()


