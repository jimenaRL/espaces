#
#                                                                            */
#                         espaces.py                                         */
#                                                                            */
#                Espaces Imaginaires sound project                           */
#                                                                            */
# -------------------------------------------------------------------------- */

# All units in International System of Units (SI)

import os

import numpy as np

from utils import set_paths, open_osx
from signals import Signal

from eigenvalues import one_torus
from green_fn import compute_green_fn
from convolutions import convolve_signals

# add to python path
ESPACES_PROJECT = os.environ['ESPACES_PROJECT']

def espaces(torus_j_max,L,duration,path_es):

    ## set physical parameters
    sound_speed   = 3.4e2
    viscosity     = 1.7e-5

    # set saving paths
    gf_im_path, gf_au_path = set_paths('green_fn',torus_j_max,L,duration)
    cv_im_path, cv_au_path = set_paths('cv',torus_j_max,L,duration)
    es_im_path, es_au_path = set_paths('es',torus_j_max,L,duration)

    # read and save audio for emitted sound
    sig_es = Signal(path_es,mono=True)
    sampling_rate = sig_es.fs

    # compute 1-torus eigen-values
    print "\tcomputing 1-torus eigen-values..."
    eigen_vals = one_torus(sound_speed,L,torus_j_max)

    # compute and save green function
    print "\tcomputing green function..."
    green_fn_0 = compute_green_fn(sound_speed, viscosity, eigen_vals, duration, sampling_rate)
    sig_gf = Signal(green_fn_0,fs=sampling_rate,mono=True,normalize=True)

    # convolve emitted sound with the green function and save it
    print "\tperforming convolution..."
    sig_cv = convolve_signals(sig_gf,sig_es,mode='full',kind='ola')

    # save audio and image
    sig_es.write(es_au_path)
    sig_es.save_image(es_im_path, title='emitted sound')

    sig_gf.write(gf_au_path)
    sig_gf.save_image(gf_im_path, title='green_fn_0')

    sig_cv.write(cv_au_path)
    sig_cv.save_image(cv_im_path, title='reverberated sound')

    # look at results
    open_osx(cv_au_path,cv_im_path,gf_au_path,gf_im_path,es_au_path,es_im_path)

if __name__:

    # set emited sound
    path_es = os.path.join(ESPACES_PROJECT,'data','examples','speech.wav')

    # ## settings 
    # # NOTE : the physical bound for the 1-torus eigen-values is
    # #              int(np.square(sound_speed/viscosity))
    # #        but this leads to a memory allocation error.
    torus_j_max   = 10
    torus_lengths = [100] # np.linspace(1e-2,1e4,10) # [1e-2,1e-1,1e-0,1e1,1e2,1e3,1e4]
    duration      = 1.0

    for L in torus_lengths: 
        print "\tlength : %1.2f" % L
        espaces(torus_j_max,L,duration,path_es)
