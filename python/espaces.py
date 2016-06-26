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

import numpy as np

from utils import set_paths, open_osx
from signals import Signal

from eigenvalues import n_torus, picard
from green_fn import compute_green_fn
from convolutions import convolve_signals

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def espaces(path_es,j_max=100,L=[1],duration=1):


    # set physical parameters
    c = 3.4e2
    nu = 1.7e-5

    # read and save audio for emitted sound
    sig_es = Signal(path_es,mono=True,normalize=True)
    sampling_rate = sig_es.fs

    start_t = time.time()
    eigen_params = { 'kind' :'n_torus', 'params' : {} }

    # eigen_vals,sym =  n_torus(L,j_max)
    eigen_vals,sym =  picard()

    print "eigen-values  took %1.2f seconds" % ((time.time()-start_t))

    # compute and save green function
    start_t = time.time()
    green_fn_0 = compute_green_fn(c, nu, eigen_vals, duration, sampling_rate, sym)
    print "green_fn_0  took %1.3f seconds" % ((time.time() -start_t))
    sig_gf = Signal(green_fn_0,fs=sampling_rate,mono=True,normalize=True)

    import matplotlib.pyplot as plt
    plt.plot(sig_gf.data,'-'); plt.show()

    # convolve emitted sound with the green function and save it
    start_t = time.time()
    sig_cv = convolve_signals(sig_es,sig_gf,kind='ola')
    print "convolution  took %1f milliseconds" % ((time.time() -start_t)*1e3)

    # save audio and image

    # set saving paths
    gf_im_path, gf_au_path = set_paths('green_fn',j_max,L,duration)
    cv_im_path, cv_au_path = set_paths('cv',j_max,L,duration)
    es_im_path, es_au_path = set_paths('es',j_max,L,duration)

    if not os.path.exists(es_au_path):
        sig_es.write(es_au_path)
    if not os.path.exists(es_im_path):
        sig_es.save_image(es_im_path, title='emitted sound')

    sig_gf.write(gf_au_path)
    sig_gf.save_image(gf_im_path, title='green_fn_0',)

    sig_cv.write(cv_au_path)
    sig_cv.save_image(cv_im_path, title='reverberated sound')

    # look at results
    open_osx(cv_im_path,gf_im_path)
    sig_gf.play()
    sig_cv.play()
    os.system("osascript -e 'quit app \"Preview\"'")

if __name__:

    path_es = os.path.join(ESPACES_PROJECT,'data','examples','speech_small.wav')

    j_max = 20
    L = [40,20,30]
    duration  = 1.0

    espaces(path_es,j_max,L,duration)

