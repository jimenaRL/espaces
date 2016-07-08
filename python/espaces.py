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

from eigenvalues import n_torus, picard, sphere_3
from green_fn import compute_green_fn, compute_green_fn_theano
from convolutions import convolve_signals

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def espaces(path_es='',F=[440],j_max=100,duration=1,kind='n_torus',c=3.4e2,nu=1.7e-5):

    # read and save audio for emitted sound
    sig_es = Signal(path_es,mono=True,normalize=True)
    sampling_rate = sig_es.fs

    start_t = time.time()

    if kind=='n_torus':
        eigen_vals =  n_torus(F,c,j_max)

    if kind=='sphere_3':
        eigen_vals =  sphere_3(F,c,j_max)

    print "eigen-values  took %1.2f seconds" % ((time.time()-start_t))

    # compute and save green function
    start_t = time.time()
    green_fn_0 = compute_green_fn(c, nu, eigen_vals, duration, sampling_rate)
    print "NUMPY green_fn_0 took %1.3f seconds" % ((time.time() -start_t))
    sig_gf = Signal(green_fn_0,fs=sampling_rate,mono=True,normalize=True)


    # compute and save green function
    start_t = time.time()
    theano_green_fn_0 = compute_green_fn_theano(c, nu, eigen_vals, duration, sampling_rate)
    print "THEANO green_fn_0  took %1.3f seconds" % ((time.time() -start_t))

    # convolve emitted sound with the green function and save it
    start_t = time.time()
    sig_cv = convolve_signals(sig_es,sig_gf,kind='ola')
    print "convolution  took %1f milliseconds" % ((time.time() -start_t)*1e3)

    # save audio and image

    # set saving paths
    if not type(F)==list:
        F = [F]
    gf_im_path, gf_au_path = set_paths('green_fn',kind,j_max,F,duration)
    cv_im_path, cv_au_path = set_paths('cv',kind,j_max,F,duration)
    es_im_path, es_au_path = set_paths('es',kind,j_max,F,duration)
    ev_im_path, _          = set_paths('ev',kind,j_max,F,duration)

    _evs = np.array([i['value'] for i in eigen_vals])
    _evs.sort()
    plt.plot(_evs,'*-')
    plt.savefig(ev_im_path)

    if not os.path.exists(es_au_path):
        sig_es.write(es_au_path)
    if not os.path.exists(es_im_path):
        sig_es.save_image(es_im_path, title='emitted sound')

    sig_gf.write(gf_au_path)
    sig_gf.save_image(gf_im_path, title='green_fn_0',)

    sig_cv.write(cv_au_path)
    sig_cv.save_image(cv_im_path, title='reverberated sound')

    # look at results
    # open_osx(cv_im_path,gf_im_path,ev_im_path)
    # sig_gf.play()
    # sig_cv.play()
    # os.system("osascript -e 'quit app \"Preview\"'")

if __name__:

    path_es = os.path.join(ESPACES_PROJECT,'data','examples','speech_small.wav')

    # set physical parameters
    c = 3.4e2
    nu = 1.7e-5


    # n-torus
    j_max = 15
    duration  = 1.0

    kind = 'n_torus'

    F = [1.,5.,15.]
    espaces(path_es,F,j_max,duration,kind,c,nu)


    # f1 = np.linspace(0.1,5.,50)
    # f2 = np.linspace(5.,10.,50)
    # f3 = np.linspace(15.,100.,50)


    # for F in itertools.product(f1,f2,f3):
    #     print '%s %s' % (kind,str(F))
    #     espaces(path_es,F,j_max,duration,kind,c,nu)

    # sphere_3
    # j_max = 1000
    # duration  = 25.0
    # f1 = np.linspace(0.01,5,100)
    # kind = 'sphere_3'
    # for F in f1: 
    #     print '%s %s' % (kind,str(F))
    #     espaces(path_es,F,j_max,duration,kind,c,nu)


